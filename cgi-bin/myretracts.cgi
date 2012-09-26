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
autoflush STDOUT 1;

$input = $ENV{'QUERY_STRING'};
chomp($input);
$user = $ENV{'REMOTE_USER'};
$serverport = $ENV{'SERVER_PORT'};
$utHome = $Bin;
dotEnvBash("$utHome/.uritool");
#dotEnvBash("/home/ingest/.uritool");
$bdn = "URITOOL_BASEDIR_$serverport";

$baseDir = $ENV{$bdn};
$dirbase = $ENV{$bdn}."/uritool";

open LOG, ">>$baseDir/logs/uritool.log";
autoflush LOG 1;
print LOG "+++++++++++++++++++ myretracts\n";
print LOG "QUERY_STRING = $input\n";
print LOG "SERVER_PORT = $serverport\n";
print LOG "REMOTE_USER = $user\n";
print LOG "dirbase $dirbase\n";
print LOG "baseDir $baseDir\n";

$ENV{'PATH'} .= ":" . "$Bin";
print LOG "PATH $ENV{'PATH'}\n";
print LOG qx(which rdfcat);
%inData = ins2kvp($input);
$ruser = $inData{'ruser'};
$token = $inData{'token'};
$retracts = "$dirbase/retract/$ruser";
print LOG "retracts $retracts\n";

@txts = qx(ls -1 $retracts/$token-TK-retract.txt);
foreach my $f (@txts){
    chomp $f;

    my @parts = split /\//, $f;
    my $ff = $parts[$#parts];
    $ff =~ s/\.txt/\.nt/;
    $parts[$#parts] = $ff;
    $ff = join "/", @parts;
    print LOG "rdfcat -out N-TRIPLE -t $f > $ff\n";
    @res = qx(rdfcat -out N-TRIPLE -t $f > $ff 2>&1);
    print LOG join('',@res);
}
    
#qx(rdfcat -out N-TRIPLE -t $retracts/$token-TK-retract.txt > $retracts/$token-TK-retract.nt);
@matches = qx(ls -1 $retracts/$token-TK-retract.nt);
@list=();
push @list,'<table border="0" cellpadding="4" cellspacing="4" style="font-size:14px;"'."\n";
push @list,"<tr><th>Retract Files</th><th>Size</th><th>Date</th></tr>\n";
foreach my $f (@matches){
    chomp $f;
    next if -z $f;
    my $df = $f;
    $df =~ s=$retracts/==;
    my $fp = $f;
    $fp =~ s=$dirbase==;
    $fp = "/uritool".$fp;
    my @fs = stat($f);
    my $s = $fs[7];
    my $dt = $fs[9];
    my $o = $fs[4];
    my $line = "<tr><td><a target='trips' href='$fp'>$df</a></td><td>$s</td>";
    $line .= "<td>" .strftime("\%Y:\%m:\%d", localtime($dt)) . "</td>";
    $line .= "</tr>\n";
    push @list, $line;
}
print "Content-Type: text/html\nExpires: Tue, 01 Jan 1981 01:00:00 GMT\n\n";
print "<html>\n<head><title>UriTool Retract List</title></head>\n";
print "<body style='font-family:Arial,Verdana;font-size:14px;background-color:#F5F5F5'>\n";
print "<H1>Uri Tool</H1>\n";
print "<H2>Retract Files for '$ruser' matching '$token' as a prefix</H2>\n";
push @list,"</table>\n";

foreach my $line (@list){
    print $line; 
}

#print "dirbase $dirbase<br/>\n";
#print "baseDir $baseDir<br/>\n";
print "</body>\n";

# remove <token>-TK-retract-\d+.* from retract/<ruser>
# move <token>-TK-max.html to <token>-TK.html in wip
# sed modify the filebase, indexbase etc in html
# remove <token>-TK-\d+.* from wip
