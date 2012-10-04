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
use ulist;
use CGI;
use POSIX qw( strftime );
$g_T0 = time();

$dmy = strftime("%d%b%y%p", localtime($g_T0) );

$UNO = '1';
$wuser = $ENV{'REMOTE_USER'};
$serverport = $ENV{'SERVER_PORT'};

$utHome = $Bin;

dotEnvBash("$utHome/.uritool");
$spEnv = $ENV{'VIVO_ACCT_ENV_PATH'};
$vacct = $ENV{'VIVO_ACCT_ID'};

$bdn = "URITOOL_BASEDIR_$serverport";
$baseDir = $ENV{$bdn};

$bxd = "URITOOL_XSLT_DIR_$serverport";
$xslt = $ENV{$bxd};
$ENV{'URITOOL_XSLT'} = $xslt;

$bbd = "URITOOL_BIN_DIR_$serverport";
$binDir = $ENV{$bbd};

$ENV{'PATH'} = "$binDir:$ENV{'PATH'}";
 
$log = $ENV{'URITOOL_LOG_DIR'};
open LOG, ">>$log/uritool.log";
autoflush LOG 1;
print LOG "+++++++++++++++++++ lp.cgi\n";
print LOG $ENV{'PATH'} . "\n";
$saxon = $ENV{'saxon'};

# directory paths
$inbasket = "$baseDir/uritool/inbasket";
$wip = "$baseDir/uritool/wip";
$retract = "$baseDir/uritool/retract";
$assert = "$baseDir/uritool/assert";
$upldir = "$baseDir/uritool/tmp";

$stdns = $ENV{'URITOOL_STD_NS'} if $ENV{'URITOOL_STD_NS'} ne '';

$g_cgi = new CGI; 

print LOG "wuser=$wuser\n";
print LOG "SERVER_PORT=$serverport\n";

# param setup
$g_usr = $g_cgi->param('usr');
$g_usr = trim($g_usr);
$g_uri = trim($g_cgi->param('uri'));
$g_token = trim($g_cgi->param('token'));
$g_tok = $g_token;
$g_token .= "-TK";
$g_op = $g_cgi->param('op');
$path = $g_cgi->param("uris");
$g_rc = trim($g_cgi->param('rc'));
$gpath = $g_cgi->param("gfile");
$criteria = trim($g_cgi->param("criteria"));
$rcomb = $g_cgi->param("rmerge");
$acomb = $g_cgi->param("amerge");

$jgpath = $g_cgi->param("jgfile");
$jcriteria = trim($g_cgi->param("jcriteria"));
$jrcomb = $g_cgi->param("jrmerge");
$jacomb = $g_cgi->param("jamerge");

$ogpath = $g_cgi->param("ogfile");
$ocriteria = trim($g_cgi->param("ocriteria"));
$orcomb = $g_cgi->param("ormerge");
$oacomb = $g_cgi->param("oamerge");

$host = trim($g_cgi->param("host"));
$port = trim($g_cgi->param("port"));
$ctxt = trim($g_cgi->param("ctxt"));

# TODO Need to add an environment variable that gets the default host & port if one is not passed from the GUI
if ($host eq '' || $port eq '') {
	print LOG "Host: " . $host . " Port: " . $port . " is blank! \n";
	exit 1;
}

$hpc = $host . ($port ne '' ?":$port":"") . ($ctxt ne '' ?"/$ctxt":'');
print LOG "H:P/C $hpc\n";
$HPC = "$host:$port:$ctxt";

$hpcp  = " -h $host " if $host ne '';
$hpcp .= " -p $port " if $port ne '';
$hpcp .= " -c $ctxt " if $ctxt ne '';
print LOG $hpcp . "\n";

# get the ball rolling...
$fragment = "Content-Type: text/html\n";
$fragment .= "Expires: Tue, 01 Jan 1981 01:00:00 GMT\n\n";
print $fragment;

if( $g_usr eq ''){
    $outError = "Missing Netid.";
    onError();
    exit 0;
}
foreach my $usr (@UserList){
    chomp($usr);
    if($usr eq $g_usr){
        $flag = 1;
        last;
    }
}
if(!defined($flag)){
    $outError = "Unknown Netid: $g_usr.";
    onError();
    exit 0;
}

if( $g_token eq '' || $g_token eq '*'){
    $outError = "Missing token or token='*'.";
    onError();
    exit 0;
}

$inbasket .= "/$g_usr" if $g_usr ne '';
$wip .= "/$g_usr" if $g_usr ne '';
$retract .= "/$g_usr" if $g_usr ne '';
$assert .= "/$g_usr" if $g_usr ne '';


if($g_op eq 'lookup'){
    clearFiles();
    if($path ne ''){
	$path =~ s/.*[\/\\](.*)/$1/;
	
	$handle = $g_cgi->upload("uris");
	$upld = "$g_token_$g_usr\_$UNO.txt";
	
	open UPLOADFILE, ">$upldir/$upld";
	binmode UPLOADFILE;
	
	while ( <$handle> ){
	    print UPLOADFILE;
	}
	close UPLOADFILE;
	
	lookupMany("$upldir/$upld",$g_token,$g_token);
    } else {
	lookupOne($g_uri,$g_token,$g_token);
    }
} elsif($g_op eq 'restart') {
    findMostRecentWork();
} elsif($g_op eq 'dispGrp') {
    $g_token .= "DDP";
    clearFiles();
    if($gpath ne ''){
	$gpath =~ s/.*[\/\\](.*)/$1/;
	
	my $handle = $g_cgi->upload("gfile");
	my $upld = "$g_token_$g_usr\_$UNO.xml";
	
	open UPLOADFILE, ">$upldir/$upld";
	binmode UPLOADFILE;
	
	while ( <$handle> ){
	    print UPLOADFILE;
	}
	close UPLOADFILE;
	processAndDisplay("$upldir/$upld",$g_token);
    }
} elsif($g_op eq 'dispJGrp') {
    $g_token .= "DDJ";
    clearFiles();
    if($jgpath ne ''){
        $jgpath =~ s/.*[\/\\](.*)/$1/;

        my $handle = $g_cgi->upload("jgfile");
        my $upld = "$g_token_$g_usr\_$UNO.xml";

        open UPLOADFILE, ">$upldir/$upld";
        binmode UPLOADFILE;

        while ( <$handle> ){
            print UPLOADFILE;
        }
        close UPLOADFILE;
        processAndDisplayM("$upldir/$upld",$g_token,"journal");
    }
} elsif($g_op eq 'dispOGrp') {
print LOG "dispOGrp\n";
    $g_token .= "DDO";
    clearFiles();
    if($ogpath ne ''){
        $ogpath =~ s/.*[\/\\](.*)/$1/;

        my $handle = $g_cgi->upload("ogfile");
        my $upld = "$g_token_$g_usr\_$UNO.xml";

        open UPLOADFILE, ">$upldir/$upld";
        binmode UPLOADFILE;

        while ( <$handle> ){
            print UPLOADFILE;
        }
        close UPLOADFILE;
        processAndDisplayM("$upldir/$upld",$g_token,"org");
    }

} elsif($g_op eq 'restartGrp') {
    $g_token .= "DDP";
    my $cmd .= "$saxon $inbasket/$g_token.xml $xslt/GroupsToHtml.xsl";
    $cmd .= " token=$g_token ruser=$g_usr  wuser=$wuser hpc=$HPC" ;

    $cmd .= " | tee $inbasket/$g_token.html";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    print join ("", @res);
} elsif($g_op eq 'restartJGrp') {
    $g_token .= "DDJ";
    my $cmd .= "$saxon $inbasket/$g_token.xml $xslt/MatchJournalGroupsToHtml.xsl";
    $cmd .= " token=$g_token ruser=$g_usr wuser=$wuser ilk=journal hpc=$HPC " ;

    $cmd .= " | tee $inbasket/$g_token.html";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    print join ("", @res);
}  elsif($g_op eq 'restartOGrp') {
    $g_token .= "DDO";
    my $cmd .= "$saxon $inbasket/$g_token.xml $xslt/MatchOrgGroupsToHtml.xsl";
    $cmd .= " token=$g_token ruser=$g_usr  wuser=$wuser ilk=org hpc=$HPC " ;

    $cmd .= " | tee $inbasket/$g_token.html";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    print join ("", @res);
}

sub lookupOne{
    my($u,$fb,$rb)= @_;
    $u = fixNameSpace($u);
    #$fb =~ s/-[0-9A-F]{6}$//;
    my $cmd = "discover -b $baseDir -u $wuser -n $vacct";
    $cmd .= " $hpcp -O $inbasket/$fb.xml $u ";
    print LOG "$cmd\n";
    qx($cmd);
    $cmd ="$saxon $inbasket/$fb.xml $xslt/Sum2Html.xsl";
    $cmd .=" filebase=$fb rootbase=$rb ruser=$g_usr wuser=$wuser hpc=$HPC " ;
    $cmd .=" | tee $inbasket/$fb.html";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    print join ("", @res);
    $cmd = "cp $inbasket/$fb.html ";
    $cmd .= " $wip/$fb.html ";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    $cmd = "getrip $inbasket/$fb.html > $inbasket/$fb.tmap";
    print LOG "$cmd\n";
    qx($cmd);
}

sub lookupMany{
    my($path,$fb,$rb)= @_;
    # check size 
    if($path eq ''){
	$outError = "URI file not specified.";
        return;
    }
    my $fNumLines = qx(wc -l $path);
    ($fNumLines) = split(/\s/,$fNumLines);
    if($fNumLines == 0){
        $outError = "URI file empty.";
        return;
    }
    if($fNumLines >= 20){
	batchJob($fNumLines, $path);
	tellUser($fNumLines);
	return;
    }
    # deal with vcstd
    my $r = open INF, $path;
    if(!defined($r)){
	$outError = "Can't open $path";
	return;
    }
    $r = open OUT, ">/tmp/$rb$g_usr". "_uri.txt";
    if(!defined($r)){
        $outError = "Can't open /tmp/$rb$g_usr" . "_uri.txt";
        return;
    }
    autoflush OUT 1;
    while(<INF>){
    	my $u = fixNameSpace($_);
	print OUT "$u\n";
    }
    close INF;
    close OUT;
    my $cmd = "mv /tmp/$rb$g_usr"."_uri.txt $path";
    print LOG "$cmd\n";
    qx($cmd);

    # call dodiscover

    my $ctx = " -c $ctxt " if $ctxt ne '';
    $cmd = "dodiscover -v $hpcp -b $baseDir $ctx -u $wuser -n $vacct ";
    $cmd .= " -E $fNumLines -o $inbasket/$rb.xmls $path";
    print LOG "$cmd\n";
    qx($cmd);

    # call splitsum
    #chdir $inbasket;
    $cmd = "splitsum -A -m none -t $rb -x $inbasket/$rb.xmls";
    $cmd .= " > $inbasket/$rb.xml";
    print LOG "$cmd\n";
    qx($cmd);

    # call Sum2Html.xsl
    $cmd ="$saxon $inbasket/$rb.xml $xslt/Sum2Html.xsl";
    $cmd .=" filebase=$fb rootbase=$rb ruser=$g_usr  wuser=$wuser hpc=$HPC " ;
    $cmd .=" urinum=$fNumLines ";
    $cmd .=" | tee $inbasket/$rb.html";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    print join ("", @res);

    # call cp and getrip
    $cmd = "cp $inbasket/$rb.html ";
    $cmd .= " $wip/$rb.html ";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    # 
    $cmd = "getrip $inbasket/$rb.html > $inbasket/$rb.tmap";
    print LOG "$cmd\n";
    qx($cmd);

}

sub processAndDisplay {
    my($src,$t)= @_;
    my $cmd = '';
    my $r = open INF, $src;
    if(!defined($r)){
	$outError = "Can't open $src";
	return;
    }
    close INF;
    qx(cp $src $inbasket/$t.xml);
    # transform .xml group file
    $cmd .= "$saxon $inbasket/$t.xml $xslt/GroupsToHtml.xsl";
    $cmd .= " token=$t ruser=$g_usr  wuser=$wuser hpc=$HPC " ;
    #$cmd .= " urinum=$fNumLines ";
    $cmd .= " | tee $inbasket/$t.html";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    print join ("", @res);

    # extract mapping file
    $cmd = "$saxon $inbasket/$t.xml $xslt/peepUriMap.xsl ";
    $cmd .= " > $inbasket/$t.txt ";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    print LOG join ("", @res);
}
sub processAndDisplayM {
    my($src,$t,$ilk)= @_;
    my $cmd = '';
    my $r = open INF, $src;
    if(!defined($r)){
        $outError = "Can't open $src";
        return;
    }
    close INF;
    qx(cp $src $inbasket/$t.xml);
    # transform .xml group file
    my $xsl = '';
    if($ilk eq 'journal'){
	$xsl = 'MatchJournalGroupsToHtml.xsl';
    } else {
        $xsl = 'MatchOrgGroupsToHtml.xsl';
    }
    $cmd .= "$saxon $inbasket/$t.xml $xslt/$xsl";
    $cmd .= " token=$t ruser=$g_usr  wuser=$wuser hpc=$HPC " ;
    #$cmd .= " urinum=$fNumLines ";
    $cmd .= " | tee $inbasket/$t.html";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    print join ("", @res);

    # extract mapping file
    if($ilk eq 'journal'){
	$xsl = 'journalUriMap.xsl';
    } else {
        $xsl = 'orgUriMap.xsl';
    }
    $cmd = "$saxon $inbasket/$t.xml $xslt/$xsl ";
    $cmd .= " > $inbasket/$t.txt ";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    print LOG join ("", @res);
}

sub fixNameSpace {
    my($u)=@_;
    chomp $u;
    if($u =~ /^vcstd:(.*)/){
	$u = $stdns . $1;
    } elsif($u !~ /^http:\/\//){
        $u = $stdns . $u;
    }
    return $u;
}		

sub onError {
    return if $outError eq '';
    print << "ERROR_PAGE";
<html>
<title>UriTool ERROR Page</title>
<body>
<p>ERROR: $outError</p>
</body>
</html
ERROR_PAGE
}

sub clearFiles{
    # remove files that have token for a prefix
    # from wip, inbasket and retract 
    my $t = $g_token . "-*";
    qx(/bin/rm -f $inbasket/$t $wip/$t $retract/$t $assert/$t);
}

sub findMostRecentWork {
    my $t = $g_tok . "-TK*.html";
    print LOG "$t\n";

    my $cmd = "ls -1t $wip/$t  | grep -v '\\-AUX' | grep -v '\\-TKD' ";
    print LOG $cmd . "\n";
    my @foi = qx($cmd);

    if(scalar(@foi)==0){
	$outError = "No such session for $g_tok.";
	onError();
	exit 0;
    }
    print LOG "$foi[0]";
    my $r = open INF, "$foi[0]";
    if(!defined($r)){
	$outError = "Can't open session for $g_tok.";
	onError();
	exit 0;

    }
    while(<INF>){
	print;
    }
    print LOG "$g_rc\n";
    if($g_rc eq 'Yes'){
        my $tt="$retract/$g_tok" . "-TK-*.* $retract/$g_tok-TK.*";
	print LOG $tt . "\n";
	qx(/bin/rm -f $tt);
    }
}

sub batchJob {
    my($cnt,$path) = @_;
    my $nohup = "nohup $baseDir/cgi-bin/batchLookup ";
    $nohup .= " $baseDir";
    $nohup .= " $g_usr";
    $nohup .= " $wuser";
    $nohup .= " $g_token";
    $nohup .= " $cnt";
    $nohup .= " $path";
    $nohup .= " $xslt";
    $nohup .= " $serverport";
    $nohup .= " $host";
    $nohup .= " $port";
    $nohup .= " $ctxt" if $ctxt ne '';
    $nohup .= " > $baseDir/logs/uritool.log 2>&1 & ";
    print LOG $nohup . "\n";
    my $r = system($nohup);
}

sub tellUser {
    my($cnt)=@_;
    my $tl = $cnt * 10;
    $tl = hms($tl) . " H:M:S ";
    print << "RESULT_PAGE";
<html>
<title>UriTool INFO Page</title>
<body>
<p>
Your upload file contains $cnt URIs. This could take more than
$tl.<br/> A batch job will be started to create the necessary files<br/>
and an email will be sent to inform you when the job is complete.
</p>
</body>
</html
RESULT_PAGE
}

sub hms {
    my($s) = @_;
    my $h = int($s/3600);
    my $r = $s - 3600*$h;
    my $m = int($r/60);
    my $s = $r - 60*$m;
    my $res;
    $res = sprintf("%02d:%02d:%02d", $h, $m, $s);
    return $res;
}
