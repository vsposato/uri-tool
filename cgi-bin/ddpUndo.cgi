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
$ruser = $ENV{'REMOTE_USER'};
$input = $ENV{'QUERY_STRING'};
$utHome = $Bin;
dotEnvBash("$utHome/.uritool");

$bdn = "URITOOL_BASEDIR_$serverport";
$baseDir = $ENV{$bdn};
$dirbase = $ENV{$bdn}."/uritool";
$saxon = $ENV{'saxon'};
$bxd = "URITOOL_XSLT_DIR_$serverport";
$xslt = $ENV{$bxd};

$inbasket = $dirbase . "/inbasket";
$inbasket .= "/$ruser" if $ruser ne '';

$wip = "$dirbase/wip";
$wip .= "/$ruser" if  $ruser ne '';
$retract ="$dirbase/retract";
$retract .= "/$ruser" if  $ruser ne '';
$assert = "$dirbase/assert";
$assert .= "/$ruser" if  $ruser ne '';
$outhdr = "Content-Type: text/html\n";
$outhdr .= "Expires: Tue, 01 Jan 1981 01:00:00 GMT\n\n";

autoflush STDOUT 1;
$log = $ENV{'URITOOL_LOG_DIR'};
open LOG, ">>$log/uritool.log";
autoflush LOG 1;
print LOG "\n+++++++++++++++++++ dedup.cgi\n";
print LOG "\$bdn = $bdn \n";
print LOG "\$baseDir = $baseDir \n";
print LOG "\$dirbase = $dirbase \n";
print LOG "\$inbasket = $inbasket \n";
print LOG "\$input = $input \n";
print LOG "\$retract = $retract \n";
print LOG "\$assert = $assert \n";
print LOG "\$wip = $wip \n";
chomp($input);
%inData = ins2kvp($input);
$token = $inData{"token"};
$grp = $inData{"grp"};

print LOG "\$token = $token\n";

print LOG "\$grp = $grp \n";

qx(/bin/rm -f $assert/$token-*.$grp.*.nt $retract/$token-*.$grp.*.nt);
qx(/bin/rm -f $assert/$token-AllAsserts.nt $retract/$token-AllRetracts.nt);


# mark group as NOT done
$cmd = "$saxon $inbasket/$token.xml $xslt/markGroup.xsl grp=$grp state=No";
$cmd .= " > $wip/$token.xml";
qx($cmd);
print LOG $cmd . "\n";
$cmd = "cp $wip/$token.xml $inbasket";
qx($cmd);

$g = $inData{'grp'};
print $outhdr. $g . '|Undo';
