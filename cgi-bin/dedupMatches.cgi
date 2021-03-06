#!/usr/bin/perl
# Copyright (c) 2012, Cornell University
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#     * Neither the name of Cornell University nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 

use FindBin qw($Bin);
use lib $Bin;
use FileHandle;

use common;

use POSIX qw( strftime );

$g_T0 = time();
$g_TMS = strftime("\%M\%S", localtime($g_T0) );

# get env vars 
#
$serverport = $ENV{'SERVER_PORT'};
$ruser = $ENV{'REMOTE_USER'};
$input = $ENV{'QUERY_STRING'};
$utHome = $Bin;
dotEnvBash("$utHome/uritool");
$spEnv = $ENV{'VIVO_ACCT_ENV_PATH'};
$vacct = $ENV{'VIVO_ACCT_ID'};


# set up directory paths
#
$bdn = "URITOOL_BASEDIR_$serverport";
$baseDir = $ENV{$bdn};
$dirbase = $ENV{$bdn}."/uritool";
$saxon = $ENV{'saxon'};
$inbasket = $dirbase . "/inbasket";
$inbasket .= "/$ruser" if $ruser ne '';

$bxd = "URITOOL_XSLT_DIR_$serverport";
$xslt = $ENV{$bxd};

$wip = "$dirbase/wip";
$wip .= "/$ruser" if  $ruser ne '';
$retract ="$dirbase/retract";
$retract .= "/$ruser" if  $ruser ne '';
$assert = "$dirbase/assert";
$assert .= "/$ruser" if  $ruser ne '';

# http preamble string
#
$outhdr = "Content-Type: text/html\n";
$outhdr .= "Expires: Tue, 01 Jan 1981 01:00:00 GMT\n\n";

# set up logging
#
autoflush STDOUT 1;
$log = $ENV{'URITOOL_LOG_DIR'};
open LOG, ">>$log/uritool.log";
autoflush LOG 1;

print LOG "\n+++++++++++++++++++ dedupMatches.cgi\n";
print LOG "\$bdn = $bdn \n";
print LOG "\$baseDir = $baseDir \n";
print LOG "\$dirbase = $dirbase \n";
print LOG "\$inbasket = $inbasket \n";
print LOG "\$input = $input \n";
print LOG "\$retract = $retract \n";
print LOG "\$assert = $assert \n";
print LOG "\$wip = $wip \n";

# log and parse query string
chomp($input);
print LOG $input . "\n";
%inData = ins2kvp($input);
$token = $inData{"token"};
$ilk = '';
if($token =~ /-TKDDO/){
    $ilk = "Org";
} else {
    $ilk = "Journal";
}

# this flat file should contain a mapping of
# ids to value. this file is constructed when
# the group xml is uploaded.
#
$file = $inbasket . '/' . $token . ".txt";
$grp = $inData{"grp"};
$gsize = $inData{"grpsize"};
$chosenUri = $inData{"uri"};

@hpc = split /\:/, $inData{'hpc'};
$host = $hpc[0] if $hpc[0] ne '';
$port = $hpc[1] if $hpc[1] ne '';
$ctxt = $hpc[2] if $hpc[2] ne '';
# TODO Need to add an environment variable that gets the default host & port if one is not passed from the GUI
if ($host eq '' || $port eq '') {
	print LOG "Host: " . $host . " Port: " . $port . " is blank! \n";
	exit 1;
}
$hpcp  = " -h $host " if $host ne '';
$hpcp .= " -p $port " if $port ne '';
$hpcp .= " -c $ctxt " if $ctxt ne '';
print LOG $hpcp . "\n";
$HPC = "$host:$port:$ctxt";

# this is the list of 'kept' group members
#
@Included = split /\|/, $inData{"inc"};

sub isIncluded {
    my($u) = @_;
    my $xx = 0;
    for(my $k=0;$k<scalar(@Included);$k++){
	if($Included[$k] == $u){
	    $xx = 1;
	    break;
	}
    }
    return $xx;
}

# log stuff
#
print LOG "scalar(\@Included) = ".scalar(@Included)."\n";
print LOG "\$inc = $inData{'inc'}\n";
print LOG "\$token = $token\n";
print LOG "\$file = $file \n";
print LOG "\$grp = $grp \n";
print LOG "\$gsize = $gsize \n";
print LOG "\$chosenUri = $chosenUri \n";

# clear previous ntriples for group
print LOG "/bin/rm -f $retract/$token-*.$grp.*.nt\n";
qx(/bin/rm -f $retract/$token-*.$grp.*.nt);
print LOG "/bin/rm -f $assert/$token-*.$grp.*.nt\n";
qx(/bin/rm -f $assert/$token-*.$grp.*.nt);
qx(/bin/rm -f $assert/$token-AllAsserts.nt $retract/$token-AllRetracts.nt);
# read in mapping file and populate hashes
#
open INF, $file;
while(<INF>){
    my($id,$v) = split(/\|/);
    my $g,$p;
    $id =~ /^([AIEUL][B]*)G(\d+)P(\d+)$/;
    $t = $1;
    $g = $2;
    $p = $3;
    next if $g != $grp;
    $HbyT{$t}{$p} = $v;
    $H{$id} = $v;
    if($t eq 'U' && $id ne $chosenUri && isIncluded($p)){
	$UnchosenUris{$p} = $v;
	push @Unchosen, $p;
    }
}

$curi = $H{$chosenUri};
chomp $curi;
$name = $vacct;

$flag = 'LV';
# gather all nt from kb2 for grp uris - this is retract stuff
for(my $u=1; $u <= $gsize; $u++){
    my $xx = isIncluded($u);
    print LOG "$u  $xx\n";
    next if $xx == 0;
    my $outf = '';
    my $uri = $HbyT{'U'}{$u};
    chomp $uri;   

    print LOG "$uri vs $curi $u ".(defined($UnchosenUris{$u})?'D':'U') . "\n";

    next if ($uri eq $curi) &&  defined($UnchosenUris{$u});
    if(defined($UnchosenUris{$u})){
	$outf = "$wip/$token-R.$grp.$u.nt";
    } else {
	$outf = "$wip/$token-C.$grp.$u.nt";
    }

    print LOG "$uri $outf\n";

    my $const = spc($uri);
    my $of = "$wip/$token-spcon.$grp.$u.rq";
    qx(echo '$const' > $of);
    my $cmd;
    $cmd = "sparqltool ";
    $cmd .= " -c $ctxt " if $ctxt ne '';
    $cmd .= " -C N-Triple";
    $cmd .= " -h $host";
    $cmd .= " -p $port" if $port ne '';
    $cmd .= " -n $name";
    $cmd .= " -P env";
    $cmd .= " -o $outf";
    $cmd .= " -i $of";
    $cmd .= " -u $ruser";
    print LOG "$cmd\n";
    $r = doit($cmd,$flag);
    exit 1 if $r;
    if(defined($UnchosenUris{$u})){
	# copy to retract dir
	qx(cp $outf $retract);
	
	# make a copy of unchosen results for modification
	# and assertion
	
	my $f = "$wip/$token-M.$grp.$u.nt";
	print LOG "\nsed -e 's=$uri=$curi=' $outf > $f\n";

	# replace unchosen uris with chosen uri - this is part of assert
	qx(sed -e 's=$uri=$curi=' $outf > $f);
    } else {
	$chosenIdx = $u;
    }
}

# strip from assert copies any triple with title,abbreviation,
# issn, eissn or label. also, make aka triples as needed
#

foreach my $u (@Unchosen){
    my $f = "$wip/$token-M.$grp.$u.nt";
    next if -z $f || ! -e $f;
    my $ff = "$wip/$token-A.$grp.$u-$chosenIdx.nt";
    open INNT, $f;
    open OUTNT, ">$ff";
    autoflush OUTNT 1;
    while(<INNT>){
	if(/http:\/\/www.w3.org\/2000\/01\/rdf-schema\#label/){
	    my $trip = $_;
	    $_ = "#" . $_;
	    print OUTNT $_;
	    $trip =~ s/http:\/\/www.w3.org\/2000\/01\/rdf-schema\#label/http:\/\/vivoweb.org\/ontology\/aka\#label/;
	    print OUTNT $trip;
	} elsif(/http:\/\/vivoweb.org\/ontology\/core\#title/){
	    my $trip = $_;
	    $_ = "#" . $_;
	    print OUTNT $_;
	    $trip =~ s/http:\/\/vivoweb.org\/ontology\/core\#title/http:\/\/vivoweb.org\/ontology\/aka\#title/;
	    print OUTNT $trip;
	} elsif($ilk eq 'Journal' && /http:\/\/vivoweb.org\/ontology\/core\#abbreviation/){
	    my $trip = $_;
	    $_ = "#" . $_;
	    print OUTNT $_;
	    $trip =~ s/http:\/\/vivoweb.org\/ontology\/core\#abbreviation/http:\/\/vivoweb.org\/ontology\/aka\#abbreviation/;
	    print OUTNT $trip;
	}  elsif($ilk eq 'Journal' && /http:\/\/purl\/ontology\/bibo\/issn/){
	    my $trip = $_;
	    $_ = "#" . $_;
	    print OUTNT $_;
	    $trip =~ s/http:\/\/purl\/ontology\/bibo\/issn/http:\/\/vivoweb.org\/ontology\/aka\#issn/;
	    print OUTNT $trip;
	} elsif($ilk eq 'Journal' && /http:\/\/purl\/ontology\/bibo\/eissn/){
	    my $trip = $_;
	    $_ = "#" . $_;
	    print OUTNT $_;
	    $trip =~ s/http:\/\/purl\/ontology\/bibo\/eissn/http:\/\/vivoweb.org\/ontology\/aka\#eissn/;
	    print OUTNT $trip;
	} else {
	    print OUTNT $_;
	}
    }
    close INNT;
    close OUTNT;
    # copy to assert dir
    qx(cp $ff $assert);
}

# gather label trips for chosen uri - this is retract stuff
$f = "$wip/$token-C.$grp.$chosenIdx.nt";
$ff = "$wip/$token-RC.$grp.$chosenIdx.nt";
open INNT, $f;
open OUTNT, ">$ff";
autoflush OUTNT 1;
while(<INNT>){
    if(/(http:\/\/www.w3.org\/2000\/01\/rdf-schema\#label|http:\/\/vivoweb.org\/ontology\/core\#title)/){
	print OUTNT $_;
    }
}
close INNT;
close OUTNT;
qx(cp $ff $retract);

# construct new label trips for chosen uri
$ff = "$wip/$token-AC.$grp.$chosenIdx.nt";
open OUTNT, ">$ff";
autoflush OUTNT 1;

$label = $inData{'label'};
$clabel = $inData{'clabel'};

$nt = "<$curi> <http:\/\/www.w3.org\/2000\/01\/rdf-schema\#label> \"$label\" .\n";
print OUTNT $nt if $label ne "";

$nt = "<$curi> <http:\/\/vivoweb.org/ontology/aka\#label> \"$clabel\" .\n";
print OUTNT $nt if $label ne "" && $clabel ne "" && $label ne $clabel;

$abbr = $inData{'abbr'};
$cabbr = $inData{'cabbr'};
$issn = $inData{'issn'};
$cissn = $inData{'cissn'};
$eissn = $inData{'eissn'};
$ceissn = $inData{'ceissn'};
if($ilk eq 'Journal'){
    $nt = "<$curi> <http:\/\/vivoweb.org\/ontology\/core\#abbreviation> \"$abbr\" . \n";
    print OUTNT $nt if $abbr ne "";
    $nt = "<$curi> <http:\/\/vivoweb.org/ontology/aka\#abbreviation> \"$cabbr\" .\n";
    print OUTNT $nt if $abbr ne "" && $cabbr ne "" && $abbr ne $cabbr;

    $nt = "<$curi> <http:\/\/purl\/ontology\/bibo\/issn> \"$issn\" . \n";
    print OUTNT $nt if $issn ne "";
    $nt = "<$curi> <http:\/\/vivoweb.org/ontology/aka\#issn> \"$cissn\" .\n";
    print OUTNT $nt if $issn ne "" && $cissn ne "" && $issn ne $cissn;

    $nt = "<$curi> <http:\/\/purl\/ontology\/bibo\/eissn> \"$eissn\" . \n";
    print OUTNT $nt if $eissn ne "";
    $nt = "<$curi> <http:\/\/vivoweb.org/ontology/aka\#eissn> \"$ceissn\" .\n";
    print OUTNT $nt if $eissn ne "" && $ceissn ne "" && $eissn ne $ceissn;

}
close OUTNT;
qx(cp $ff $assert);

# mark group as done
$cmd = "$saxon $inbasket/$token.xml $xslt/mark".$ilk."Group.xsl grp=$grp state=Yes";
$cmd .= " > $wip/$token.xml";
qx($cmd);
print LOG $cmd . "\n";
$cmd = "cp $wip/$token.xml $inbasket";
qx($cmd);

$g = $inData{'grp'};
print $outhdr. $g . '|Merge|' . $H{$inData{'uri'}} .'|'. join(", ",@Unchosen);

END {
    if($?){
	print $outhdr;
	print $ErrStr;
    }
}
sub spc {
    my($uri) = @_;
    $spCon = <<"INSOUTS";
construct {
     ?s ?p1 <$uri> .
     <$uri> ?p2 ?o
}
WHERE
{
   GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2> 
   {
       optional { ?s ?p1 <$uri> . }
       optional { <$uri> ?p2 ?o . }
   }
}
INSOUTS

    return $spCon;

}
$ErrStr = '';
$LogStr = '';
sub doit {
    my($cmd, $flag, $pw, $resp) = @_;
    $ErrStr .= "\n" if $ErrStr ne '';
    $LogStr .= "\n" if $LogStr ne '';
    #print "$cmd, $flag, $pw, $resp\n";
    my $t0 = time();
    $LogStr .= "$cmd\n" if $flag =~ /V/;
    $cmd =~ s/_PW_/$pw/ if $pw;
    my $pkg,$fn,$lno;
    ($pkg,$fn,$lno) = caller();
    my $callinfo = "Pkg=$pkg, File=$fn, Line=$lno";
    if($flag =~ /L/ && $resp){
	@$resp = qx($cmd);
	my $r = ($? >> 8);
	$ErrStr .= ">>>> ERROR !!! $callinfo\n" . join("", @$resp) if($r);
	my $dt = time() - $t0;
	$ErrStr .= "Elapsed time = $dt seconds.\n";
	return $r;
    } elsif($flag =~ /L/){
	my @res = qx($cmd);
	my $r = ($? >> 8);
	$ErrStr .=  ">>>> ERROR !!! $callinfo\n" . join("", @res) if($r);
	my $dt = time() - $t0;
	$ErrStr .= "Elapsed time = $dt seconds.\n";
	return $r;
    }
    my $dt = time() - $t0;
    $LogStr .= "Elapsed time = $dt seconds.\n";
    return 0;
}

