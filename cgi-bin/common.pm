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



%OntoMap = (
 "far:" => "http://vitro.mannlib.cornell.edu/ns/reporting#",
 "acti:" => "http://vivoweb.org/ontology/activity-insight#",
 "bibo:" => "http://purl.org/ontology/bibo/",
 "cce:" => "http://vivoweb.org/ontology/cornell-cooperative-extension#",
 "hr:" => "http://vivo.cornell.edu/ns/hr/0.9/hr.owl#",
 "dcterms:" => "http://purl.org/dc/terms/",
 "dcelem:" => "http://purl.org/dc/elements/1.1/",
 "event:" => "http://purl.org/NET/c4dm/event.owl#",
 "foaf:" => "http://xmlns.com/foaf/0.1/",
 "ospcu:" => "http://vivoweb.org/ontology/cu-vivo-osp#",
 "rdfs:" => "http://www.w3.org/2000/01/rdf-schema#",
 "rdf:" => "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
 "vivo:" => "http://vivoweb.org/ontology/core#",
 "vivoc:" => "http://vivo.library.cornell.edu/ns/0.1#",
 "vitro-public:" => "http://vitro.mannlib.cornell.edu/ns/vitro/public#",
 "owl:" => "http://www.w3.org/2002/07/owl#",
 "vitro:" => "http://vitro.mannlib.cornell.edu/ns/vitro/0.7#",
 "geo:" => "http://aims.fao.org/aos/geopolitical.owl#",
 "xsd:" => "http://www.w3.org/2001/XMLSchema#",
 "pubmed:" => "http://vitro.mannlib.cornell.edu/ns/pubmed#"

);

# designed and coded by Joseph R. Mc Enerney jrm424@cornell.edu

# remove leading an trailing white space
sub trim {
    my($a) = @_;
    $a =~ s/^\s*(\S+)\s*$/$1/;
    $a =~ s/^\s*(\S.*\S)\s*$/$1/;
    $a =~ s/(\s*)//;
    return $a;
}

#encode control characters
sub encode_ctrls {
    my($x)=@_;
    if((ord($x)<32) || (ord($x)>127)) {
	return sprintf('%%%2.2X',ord($x));
    } else {
	return $x;
    }
}
# URL encoder
sub urlencode {
    my($x)=@_;
    $x =~ s/([%+&=<>\[\]\\^`{}|~:?;])/sprintf('%%%2.2X',ord($1))/ge;
    $x =~ s/(.|[\n])/encode_ctrls($1)/ge;
    $x =~ s/ /+/g;
    return $x;
}

# make a URL encoded string from
# a hash
sub weave {
    my($ref)=@_;
    my $x = '';
    my $z;
    foreach $k (keys(%$ref)) {
	next if $k =~ /^HI/;
	$x .= "&" unless !$x;
	$x .= urlencode($k) . "=" . urlencode($ref->{$k});
    }
    return $x;
}

# make a hash from a URL encoded string
sub ins2kvp {
    my($in)=@_;
    my(@fields,$one,%data,$n,$v);

    @fields = split("&",$in);
	
    foreach $one ( @fields ) {
	($n , $v) = split( "=", $one);
	$n =~ s/\+/ /g;
	$n =~ s/%(..)/pack("c",hex($1))/ge;
	$v =~ s/\+/ /g;
	$v =~ s/%(..)/pack("c",hex($1))/ge;
	if($data{$n} ne "") {
	    $data{$n} .= "|";
	}
	$data{$n} .= trim($v);

    }

    return %data;
}
sub nextUno {
    my($file) = @_;
    my($res,$n,$m,$ctr);
    if(!defined($file)){
        $file = "./.Uno";
    }
    #print LOGIT "Uno: $file\n";
    sysopen(CTR,$file, O_RDWR | O_CREAT);
    autoflush CTR 1;
    flock(CTR, LOCK_EX);
    $ctr = <CTR> || "000000";
    seek (CTR,0,0);
    $n = $m = hex( $ctr );
    $n++;
    #print LOGIT "Uno: $n\n";
    $n = 0 if($n >= 0xFFFFFF);
    printf CTR "%06lX\n",$n;
    close CTR;
    return sprintf("%06lX",$m);
}
sub dotEnvBash {
    my($envpath) = @_;
    my @env = qx(/bin/bash  -c ". $envpath;env");
    foreach my $ev (@env){
        my($evn,$evv) = split /=/,$ev;
        chomp $evv;

	$ENV{$evn} = $evv;

    }
}
1;

