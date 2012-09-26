<?xml version="1.0"?>
<xsl:stylesheet version='2.0'
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:sp="http://www.w3.org/2005/sparql-results#"
>
<!--
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

-->
<xsl:output method='xml' indent='yes' normalization-form='NFC'/>
<xsl:strip-space elements="*"/>

<xsl:template match='//sp:results'>

<!-- designed and coded by Joseph R. Mc Enerney jrm424@cornell.edu -->
<xsl:element name='outPredicates' inherit-namespaces='no'>
<xsl:variable name="x" > 
<xsl:for-each-group select='sp:result' 
group-by='./sp:binding[@name = "p"]/sp:uri'>

<xsl:element name='predicate' inherit-namespaces='no'>


<xsl:element name='puri' inherit-namespaces='no'>

<xsl:value-of select='current-grouping-key()'/>
</xsl:element>
<xsl:for-each select='current-group()'>

<xsl:variable name='grpele' select='.'/>

<xsl:choose>
<xsl:when test='sp:binding[@name = "O"]/sp:literal = "true"'>
<xsl:element name='object' inherit-namespaces='no'>

<xsl:element name='ouri' inherit-namespaces='no'>
<xsl:value-of select='$grpele/sp:binding[@name = "o"]/sp:uri'/>
</xsl:element>

<xsl:element name='type'  inherit-namespaces='no'>
<xsl:value-of select='$grpele/sp:binding[@name = "T"]/sp:uri'/>
</xsl:element>

<xsl:element name='graph'  inherit-namespaces='no'>
<xsl:value-of select='$grpele/sp:binding[@name = "g"]/sp:uri'/>
</xsl:element>



</xsl:element>
</xsl:when>
<xsl:otherwise>
<xsl:element name='datawraper' inherit-namespaces='no'>
<xsl:element name='datum' inherit-namespaces='no'>
<xsl:variable name='item' select='./sp:binding[@name = "o"]/sp:literal'/>
<xsl:variable name='lang' select='$item/@xml:lang'/>
<xsl:variable name='datatype' select='$item/@datatype'/>
<xsl:choose>
<xsl:when test='$lang != ""'>
<xsl:value-of select='concat($item,"_|_@",$lang)'/>
</xsl:when>
<xsl:when test='$datatype != ""'>
<xsl:value-of select='concat($item,"_|_^^&lt;",$datatype,"&gt;")'/>
</xsl:when>
<xsl:otherwise>
<xsl:value-of select='$item'/>
</xsl:otherwise>
</xsl:choose>
<!-- xsl:value-of select='./sp:binding[@name = "o"]/sp:literal'/ -->
</xsl:element>
<xsl:element name='graph'  inherit-namespaces='no'>
<xsl:value-of select='./sp:binding[@name = "g"]/sp:uri'/>
</xsl:element>
</xsl:element>

</xsl:otherwise>
</xsl:choose>
</xsl:for-each>

</xsl:element>
</xsl:for-each-group>
</xsl:variable>


<xsl:for-each select='$x/predicate'>
<xsl:copy>
<xsl:copy-of select='puri'/>


<xsl:for-each-group select='object' group-by='ouri'>
<xsl:element name='object' inherit-namespaces='no'>
<xsl:copy-of select='ouri'/>
<xsl:copy-of select='graph'/>
<xsl:element name='types' inherit-namespaces='no'>

<xsl:for-each select='current-group()'>
<xsl:sort select='type'/>
<xsl:copy-of select='type'/>

</xsl:for-each>
</xsl:element>
</xsl:element>
</xsl:for-each-group>


<xsl:for-each select='datawraper'>
<xsl:element name='datawraper' inherit-namespaces='no'>
<xsl:copy-of select='datum'/>
<xsl:copy-of select='graph'/>
</xsl:element>
</xsl:for-each>


</xsl:copy>
</xsl:for-each>

</xsl:element>

<xsl:value-of select='"&#xA;"'/>
</xsl:template>


</xsl:stylesheet>

