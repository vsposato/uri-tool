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
$serverport = $ENV{'SERVER_PORT'};
$utHome = $Bin;
dotEnvBash("$utHome/uritool");

$bdn = "URITOOL_BASEDIR_$serverport";
$baseDir = $ENV{$bdn};
$dirbase = $ENV{$bdn}."/uritool";


autoflush STDOUT 1;
$input = <STDIN>;
chomp($input);
%inData = ins2kvp($input);
$ruser = $inData{'ruser'};
$inbasket = $dirbase . "/inbasket";
$inbasket .= "/$ruser" if $ruser ne '';
$wip = "$dirbase/wip";
$wip .= "/$ruser" if  $ruser ne '';
$retract = "$dirbase/retract";
$retract .= "/$ruser" if  $ruser ne '';

$filebase = $inData{'filebase'};
$indexbase = $inData{'indexbase'};
$idx = $indexbase;
$indexbase = $indexbase+1;
#$indexbase = ($indexbase > 4)?0:$indexbase+1;
$auxbase = $inData{'auxbase'};
$log = $ENV{'URITOOL_LOG_DIR'};
open LOG, ">>$log/uritool.log";
autoflush LOG 1;
print LOG "+++++++++++++++++++ dispose.cgi\n";
$nothing=1;
foreach $k ( keys %inData){
    print LOG "$k=$inData{$k}\n";
    if($nothing && $k !~ /^(Retract|Clear|Exclude|Check)/){
	$nothing=0;
    }
}
$fragment = "Content-Type: text/html\n";
$fragment .= "Expires: Tue, 01 Jan 1981 01:00:00 GMT\n\n";
foreach $k ( keys %inData){
    if($k =~ /^CheckAll(.*?)/){
	$grp = $1;
	$op = "chkall";
	last;
    } elsif($k =~ /^Clear(.*?)/){
	$grp = $1;
	$op = "clear";
	last;
    } elsif($k =~ /^Exclude(.*?)/){
	$grp = $1;
	$op = "exclude";
	last;
    } elsif($k =~ /^Retract(.*?)/){
	$grp = $1;
	$op = "retract";
	last;
    } elsif($k =~ /^Undo(.*?)/){
	$grp = $1;
	$op = "undo";
	last;
    } else {
	$grp = $1;
	$op = "noop";
    }
}

if($op eq "chkall"){
    doChkAll($grp);
} elsif($op eq "clear"){
    doClear($grp);
} elsif($op eq "exclude"){
    doExclude($grp);
} elsif($op eq "retract"){
    doRetract($grp);
} elsif($op eq "undo"){
    doUndo($grp);
} else {
    doNoop($grp);
}


sub doChkAll {
    my($g)=@_;

}

sub doClear {
    my($g)=@_;

}


sub doExclude {
    my($g)=@_;
    opResponse("green");
}


sub doRetract {
    my($g)=@_;
    recordRetracts();
    opResponse("grey");
}

sub doUndo {
    my($g)=@_;
    my $rb = $inData{'rootbase'};
    my $suffix = $inData{'filebase'};
    $suffix =~ s/^$rb(.*?)$/$1/;
    my $sfx = $suffix;
    $sfx =~ s/-\d+$//;
    print LOG "\$inData{'rootbase'} = $inData{'rootbase'}\n";
    print LOG "\$inData{'filebase'} = $inData{'filebase'}\n";
    print LOG "\$suffix = $suffix\n";
    my $aux = "";
    $aux = "-AUX" if $inData{'filebase'} =~ /-AUX/;
    # a bit clumsy but it works
    if(($idx == 0 && $inData{'rootbase'} eq $inData{'filebase'}) ||
       ($idx == 1 && $inData{'rootbase'}. $suffix eq $inData{'filebase'})){
	print $fragment;
        print LOG "First Case\n";
	my $retr = "$retract/$rb-retract.txt";
	print LOG "$retr\n";
	my $prev = "$retract/$rb$aux-retract-$idx.txt";
	print LOG "$prev\n";
	my $tmpf = "$wip/ax$rb-retract.txt";
	print LOG "$tmpf\n";
	open PREV, $prev;
	my @Prev = <PREV>;
	close PREV;
	open RETR, $retr;
	my @Retr = <RETR>;
	close RETR;
	open TMPL, ">$tmpf";
	foreach my $tripR (@Retr){
	    my $flag = 0;
	    foreach my $tripP (@Prev){
		if($tripR eq $tripP){
		    $flag = 1;
		    last;
		}
	    }
	    print TMPL $tripR if $flag == 0;
	}
	close TMPL;
	print LOG "mv $retr $retr.sv\n";
	qx(mv $retr $retr.sv);

	print LOG "mv $tmpf $retr\n";
	qx(mv $tmpf $retr);
	
	my $inf = "$wip/$rb$sfx.html";
	print LOG "\$inf = $inf\n";
	open INF, $inf;
	while(<INF>){
	    print;
	}
	if($suffix ne ""){
	    print LOG "/bin/rm -f $wip/$inData{'rootbase'}$suffix.html\n";
	    qx(/bin/rm -f $wip/$inData{'rootbase'}$suffix.html);
	}
	print LOG "/bin/rm -f $retract/$rb$aux-retract-*\n";
	qx(/bin/rm -f $retract/$rb$aux-retract-*);
	return;
    }
    print LOG "Other Cases\n";
    my $ind = $idx-1;	
    print LOG "\$ind = $ind\n";
    
    my $html = "$wip/$inData{'rootbase'}$sfx-$ind.html";
    $html = "$wip/$inData{'rootbase'}$sfx.html" if $ind <= 0;
    print LOG "$html\n";
    my $retr = "$retract/$rb-retract.txt";
    print LOG "$retr\n";
    my $tmpf = "$wip/ax$rb-retract.txt";
    print LOG "$tmpf\n";
    my $prev = "$retract/$rb$aux-retract-$idx.txt";
    print LOG "$prev\n";
    open PREV, $prev;
    my @Prev = <PREV>;
    close PREV;
    open RETR, $retr;
    my @Retr = <RETR>;
    close RETR;
    open TMPL, ">$tmpf";
    foreach my $tripR (@Retr){
	my $flag = 0;
	foreach my $tripP (@Prev){
	    if($tripR eq $tripP){
		$flag = 1;
		last;
	    }
	}
	print TMPL $tripR if $flag == 0;
    }
    close TMPL;
    print LOG "mv $retr $retr.sv\n";
    qx(mv $retr $retr.sv);
    print LOG "mv $tmpf $retr\n";
    qx(mv $tmpf $retr);

    print $fragment;
    open INF, $html;
    while(<INF>){
	print;
    }
    print LOG "/bin/rm -f $wip/$inData{'rootbase'}$aux-$idx.html\n";
    qx(/bin/rm -f $wip/$inData{'rootbase'}$aux-$idx.html);
    print LOG "/bin/rm -f $retract/$rb$aux-retract-$idx.txt\n";
    qx(/bin/rm -f $retract/$rb$aux-retract-$idx.txt);
    return;
}


sub doNoop {
    my($g)=@_;
    responseInData("green");
}
sub responseInData{
    
    print $fragment;
    print <<"RESP";
<html>
<body> request k-v pairs:<BR/>
RESP
    foreach $k ( keys %inData){
	print "$k->$inData{$k}<BR/>\n";
    }
    print <<"RESP2";
</body>
</html>
RESP2
}

sub opResponse {
    my($color)=@_;
    my $r,$r1,$prefix,$inf,$rb;
    $inf = "$wip/$filebase.html";
    $prefix = $filebase;
    $rb = $inData{'rootbase'};
    if(! -e $inf){
	qx(cp $inbasket/$filebase.html $dirbase/wip);
    }
    print LOG "inf=$inf\n";

    $r = open HTML, $inf;
    
    $prefix =~ s/-\d+$//;
    print LOG "$wip/$prefix-$indexbase.html\n";
    $r1 = open HTML2, ">$wip/$prefix-$indexbase.html";
    autoflush HTML2 1;
    $fragment = "Content-Type: text/html\n";
    $fragment .= "Expires: Tue, 01 Jan 1981 01:00:00 GMT\n\n";
    print $fragment;
    my $cb = 0;
    my $cbrd = 0;
    my $cbed = 0;
    if(defined($r)){
	while(<HTML>){
	    my $line = $_;
	    if($line =~ /Current File Prefix/){
		$line =~ s/Current File Prefix:- .*?-->/Current File Prefix:- $prefix-$indexbase -->/;
	    }
	    foreach $k ( keys %inData){
		if($k =~ /^U-\d+-/){
		    if($line =~ /checkbox.*?id="$k.*?"/){
			$line =~ s/(id="$k.*?")/$1 disabled='true'/;
			$line =~ s/<td>/<td style='background-color:$color;'>/;
			last;
		    }
		}
	    }
	    if($line =~ /checkbox/){
		$cbrd++ if($line =~ /disabled='true'/ && $line =~ /grey/);
		$cbed++ if($line =~ /disabled='true'/ && $line =~ /green/);
		$cb++ if($line =~ /U-\d+-\w/);
	    }
	    my $nxt = $indexbase;
	    if($line =~ /name="indexbase"/){
		$line =~ s/value=".*?"/value="$indexbase"/;
	    }
	    if($line =~ /name="filebase"/){
		#$line =~ s/value=".*?"/value="$prefix\-$g_TMS"/;
		$line =~ s/value=".*?"/value="$prefix\-$indexbase"/;
	    }
	    if($nothing && $line =~ /<\/body>/){
		my $msg = "Nothing identified for retraction";
		print "<script>alert('$msg')</script>\n";
	    }
	    if($line =~ /<\/html>/){
		my $d = $cb - $cbrd - $cbed;
		my $msg = "Of $cb triples $cbrd have been marked\\n";
		$msg .= "for retraction and $cbed for exclusion;\\n";
		$msg .= "leaving $d to consider.";
		print "<script>alert('$msg')</script>\n";
	    }
	    print $line;
	    print HTML2 $line;
	}
	close HTML2;
    } else {
	if($auxbase ne ''){
	    print "Can't open $wip/$filebase.html";
	} else {
	    print "Can't open $wip/$filebase.html";
	}
    }
}

sub recordRetracts {
    my $prefix = $filebase;
    my $rb = $inData{'rootbase'};
    if($auxbase eq ''){
	$prefix = $rb;
    }
    $prefix =~ s/-\d+$//;
    my $aux = "";
    $aux = "-AUX" if $inData{'filebase'} =~ /-AUX/;
    open INF, "$inbasket/$prefix.tmap";
    
    print LOG "prefix=$prefix\n";
    print LOG "prefix.tmp = $inbasket/$prefix.tmap\n";
    my %Triples=();
    while(<INF>){
	my($key,$value) = split /==/, $_;
	$Triples{$key}=trim($value);
	print LOG "$key -> $value\n";
    }
    close INF;
    
    print LOG "nothing=$nothing\n";
    print LOG "$retract/$prefix-retract.txt\n";
    open RETRACT, ">>$retract/$rb-retract.txt";
    open RETRACT2, ">$retract/$rb$aux-retract-$indexbase.txt";
    foreach $k ( sort {nval($a) <=> nval($b) } ( keys %inData)){
	print LOG "$k -> $Triples{$k}\n";
	my $trip = prefix2namespace($Triples{$k});
	print LOG "$k -> $trip\n";
	chomp $trip;
	print RETRACT $trip . "\n" if $trip ne '';
	print RETRACT2 $trip . "\n" if $trip ne '';
    }
    close RETRACT;
    close RETRACT2;
}


sub nval {
    my($u)= @_;
    $u =~ /^U-(\d+)/;
    return $1;
}

sub prefix2namespace {
    my($u)=@_;
    $u =~ />\s<(.*?:)\w/;
    my $p = $1;
    my $ns = $OntoMap{$p};
    if($ns ne ''){
	$u =~ s|$p|$ns|;
    }
    return $u;
}


