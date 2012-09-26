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
$input = $ENV{'QUERY_STRING'};
$wuser = $ENV{'REMOTE_USER'};

$vacct = 'vivouritool@gmail.com';
$utHome = $Bin;
dotEnvBash("$utHome/.uritool");
$spEnv = $ENV{'VIVO_ACCT_ENV_PATH'};
dotEnvBash("$spEnv/.sp");
$vacct = $ENV{'VIVO_ACCT_ID'};



$bdn = "URITOOL_BASEDIR_$serverport";
$baseDir = $ENV{$bdn};

$bxd = "URITOOL_XSLT_DIR_$serverport";
$xslt = $ENV{$bxd};

$wip = "$baseDir/uritool/wip";

$bbd = "URITOOL_BIN_DIR_$serverport";
$binDir = $ENV{$bbd};

$ENV{'PATH'} = "$binDir:$ENV{'PATH'}";

autoflush STDOUT 1;
open LOG, ">>$baseDir/logs/uritool.log";
autoflush LOG 1;
print LOG "+++++++++++++++++++ openObj.cgi\n";

$fragment = "Content-Type: text/html\n";
$fragment .= "Expires: Tue, 01 Jan 1981 01:00:00 GMT\n\n";
print $fragment;	


print LOG "$input\n";
chomp($input);
%inData = ins2kvp($input);
foreach $k ( keys %inData){
    print LOG "$k=$inData{$k}\n";
}

$hpc = $inData{'hpc'};
@hpc = split /\:/, $inData{'hpc'};
$host = $hpc[0] if $hpc[0] ne '';
$port = $hpc[1] if $hpc[1] ne '';
$ctxt = $hpc[2] if $hpc[2] ne '';
if($host eq ''){
    $host='vivo.cornell.edu';
}
if($port eq ''){
    $port= '8080';
}

$hpcp  = " -h $host " if $host ne '';
$hpcp .= " -p $port " if $port ne '';
$hpcp .= " -c $ctxt " if $ctxt ne '';
print LOG $hpcp . "\n";

#$uno = nextUno();

$saxon = $ENV{'saxon'};
$inbasket = "$baseDir/uritool/inbasket";
lookup($inData{'uri'});



sub lookup{
    my($u)= @_;
    $fb = $inData{'filebase'};
    $rb = $inData{'rootbase'};
    $fb =~ s/-[0-9A-F]{6}$//;
    $usr = $inData{'ruser'};
    my $cmd = "discover -b $baseDir -u $wuser -n $vacct ";
    $cmd .= " $hpcp -O $inbasket/$usr/$fb-AUX.xml $u ";
    print LOG "$cmd\n";
    qx($cmd);

    $cmd = "/bin/rm -f $inbasket/$usr/$fb-AUX*.html";
    print LOG "$cmd\n";
    qx($cmd);

    $cmd ="$saxon $inbasket/$usr/$fb-AUX.xml $xslt/Sum2Html.xsl";
    $cmd .=" filebase=$fb-AUX ruser=$usr ";
    $cmd .=" rootbase=$rb auxbase=true wuser=$wuser hpc=$hpc ";
    $cmd .=" | tee $inbasket/$usr/$fb-AUX.html";
    print LOG "$cmd\n";
    my @res = qx($cmd);
    print join ("", @res);

    $cmd = "cp $inbasket/$usr/$fb-AUX.html ";
    $cmd .= " $wip/$usr/$fb-AUX.html ";
    print LOG "$cmd\n";
    my @res = qx($cmd);

    $cmd = "getrip $inbasket/$usr/$fb-AUX.html > $inbasket/$usr/$fb-AUX.tmap";
    print LOG "$cmd\n";
    qx($cmd);
}
