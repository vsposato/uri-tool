<?xml version="1.0"?>
<xsl:stylesheet version='2.0'
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"

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
<xsl:param name='token'  required='yes'/>
<xsl:param name='ruser'  required='yes'/>
<xsl:param name='wuser'  required='no'/>
<xsl:param name='hpc' required='yes'/>

<xsl:variable name='NL' select='"&#xA;"'/>
<xsl:output method='html' indent='yes' normalization-form='NFC'/>
<xsl:strip-space elements="*"/>


<xsl:template match='/'>
<html>
<head>
<title>UriTool DeDup Journal Matches</title>
<script src='/js/deDupMatches.js'/>
</head>
<body style='font-family:Arial,Verdana;font-size:10px;background-color:#F5F5F5'>
<H1>UriTool DeDup Journals</H1> 
<H2>Accessing:- <span id='source' style='color: red;font-size: 18px;font-family: courier'></span></H2>

<form action="/cgi-bin/dedupJMatches.cgi"  method='post'>
<xsl:value-of select='$NL'/>
<xsl:element name='input'>
<xsl:attribute name='type' select='"hidden"'/>
<xsl:attribute name='name' select='"token"'/>
<xsl:attribute name='id' select='"token"'/>
<xsl:attribute name='value' select='$token'/>
</xsl:element>
<!-- designed and coded by Joseph R. Mc Enerney jrm424@cornell.edu -->
<xsl:value-of select='$NL'/>
<xsl:element name='input'>
<xsl:attribute name='type' select='"hidden"'/>
<xsl:attribute name='name' select='"ruser"'/>
<xsl:attribute name='id' select='"ruser"'/>
<xsl:attribute name='value' select='$ruser'/>
</xsl:element>
<xsl:value-of select='$NL'/>
<xsl:element name='input'>
<xsl:attribute name='type' select='"hidden"'/>
<xsl:attribute name='name' select='"hpc"'/>
<xsl:attribute name='id' select='"hpc"'/>
<xsl:attribute name='value' select='$hpc'/>
</xsl:element>
<xsl:value-of select='$NL'/>

<table border='0' cellpadding='2' cellspacing='2'>
<xsl:for-each select='//group'>
<xsl:variable name='grp' select='position()'/>
<xsl:variable name='count' select='@count'/>
<xsl:variable name='done' select='if(@done = "Yes")then "Yes" else "No"'/>
<xsl:variable name='dsp' select='if($done="Yes") then "inline" else "none"'/>
<xsl:variable name='word' select='if($done="Yes") then " Done" else ""'/>
<tr>
<th><xsl:value-of select='concat("Group ",$grp)'/>
<xsl:element name='span'>
<xsl:attribute name='id' select='concat("Group",$grp)'/>
<xsl:attribute name='style' select='concat("display:", $dsp, ";color: red;")'/>
<xsl:value-of select='$word'/>
</xsl:element>
<xsl:element name='input'>
<xsl:attribute name='type' select='"hidden"'/>
<xsl:attribute name='name' select='concat("Gsize",$grp)'/>
<xsl:attribute name='id' select='concat("Gsize",$grp)'/>
<xsl:attribute name='value' select='$count'/>
</xsl:element>

</th>

<th style='text-align:center;font-size:14px;'>Keep</th>


<th style='text-align:left;font-size:14px;'>URI / Label</th>
<th style='text-align:left;font-size:14px;'>Abbreviation</th>
<th style='text-align:center;font-size:14px;'>ISSN</th>
<th style='text-align:center;font-size:14px;'>EISSN</th>
<th style='text-align:left;font-size:14px;'>Hash</th>
</tr>


<xsl:for-each select='journal'>
<xsl:variable name='ping' select='position()'/>

<tr>
<td style='text-align:center;'>
<xsl:element name='input'>
<xsl:attribute name='type' select='"button"'/>
<xsl:attribute name='name' select='concat("G",$grp,"P",$ping)'/>
<xsl:attribute name='id' select='concat("G",$grp,"P",$ping)'/>
<xsl:attribute name='value' select='"Pick"'/>
<xsl:attribute name='onclick' select='concat("chkItem(",$grp,",",$ping,",&#x27;J&#x27;)")'/>
</xsl:element>
</td>

<td style='text-align:center;width: 50px;'>
<xsl:element name='input'>
<xsl:attribute name='type' select='"checkbox"'/>
<xsl:attribute name='name' select='concat("XG",$grp,"P",$ping)'/>
<xsl:attribute name='id' select='concat("XG",$grp,"P",$ping)'/>
<xsl:attribute name='value' select='"X"'/>
<xsl:attribute name='checked' select='"checked"'/>
</xsl:element>
</td>


<td>
<table>
<tr><td style='width: 500px;text-align:left;font-size:14px;'>
<xsl:element name='input'>
<xsl:attribute name='type' select='"radio"'/>
<xsl:attribute name='name' select='concat("UG",$grp)'/>
<xsl:attribute name='id' select='concat("UG",$grp,"P",$ping)'/>
<xsl:attribute name='value' select='concat("UG",$grp,"P",$ping)'/>
<xsl:attribute name='onclick' select='""'/>
</xsl:element>
<xsl:element name='a'>
<xsl:attribute name='href' select='uri'/>
<xsl:attribute name='target' select='"vivo"'/>
<xsl:value-of select='uri'/>
</xsl:element>
</td>
</tr>
<tr>
<td style='width: 500px;text-align:left;font-size:14px;'>
<xsl:variable name='lb' select='concat("&#x27;",label,"&#x27;",",&#x27;LB&#x27;")'/>
<xsl:variable name='lbe' select='concat("&#x27;GLB",$grp,"P",$ping,"&#x27;")'/>
<xsl:element name='input'>
<xsl:attribute name='type' select='"radio"'/>
<xsl:attribute name='name' select='concat("LBG",$grp)'/>
<xsl:attribute name='id' select='concat("LBG",$grp,"P",$ping)'/>
<xsl:attribute name='value' select='concat("LBG",$grp,"P",$ping)'/>
<xsl:attribute name='onclick' select='concat("map(",$grp,",",$lbe,",&#x27;LB&#x27;,&#x27;J&#x27;)")'/>
</xsl:element>
<xsl:element name='span'>
<xsl:attribute name='id' select='concat("GLB",$grp,"P",$ping)'/>
<xsl:value-of select='label'/>
</xsl:element>
</td>
</tr>
</table>
</td>

<td style='width: 75px;text-align:left;font-size:14px;'>
<xsl:variable name='abbr' select='concat("&#x27;", abbr, "&#x27;" , ",&#x27;N&#x27;")'/>
<xsl:variable name='abbre' select='concat("&#x27;GA",$grp,"P",$ping,"&#x27;")'/>
<xsl:element name='input'>
<xsl:attribute name='type' select='"radio"'/>
<xsl:attribute name='name' select='concat("AG",$grp)'/>
<xsl:attribute name='id' select='concat("AG",$grp,"P",$ping)'/>
<xsl:attribute name='value' select='concat("AG",$grp,"P",$ping)'/>
<xsl:attribute name='onclick' select='concat("map(",$grp,",",$abbre,",&#x27;A&#x27;,&#x27;J&#x27;)")'/>
</xsl:element>
<xsl:element name='span'>
<xsl:attribute name='id' select='concat("GA",$grp,"P",$ping)'/>
<xsl:value-of select='abbr'/>
</xsl:element>
</td>

<td style='width: 75px;text-align:left;font-size:14px;'>
<xsl:variable name='issn' select='concat("&#x27;", issn, "&#x27;" , ",&#x27;N&#x27;")'/>
<xsl:variable name='issne' select='concat("&#x27;GI",$grp,"P",$ping,"&#x27;")'/>
<xsl:element name='input'>
<xsl:attribute name='type' select='"radio"'/>
<xsl:attribute name='name' select='concat("IG",$grp)'/>
<xsl:attribute name='id' select='concat("IG",$grp,"P",$ping)'/>
<xsl:attribute name='value' select='concat("IG",$grp,"P",$ping)'/>
<xsl:attribute name='onclick' select='concat("map(",$grp,",",$issne,",&#x27;I&#x27;,&#x27;J&#x27;)")'/>
</xsl:element>
<xsl:element name='span'>
<xsl:attribute name='id' select='concat("GI",$grp,"P",$ping)'/>
<xsl:value-of select='issn'/>
</xsl:element>
</td>

<td style='width: 75px;text-align:left;font-size:14px;'>
<xsl:variable name='eissn' select='concat("&#x27;", eissn, "&#x27;" , ",&#x27;N&#x27;")'/>
<xsl:variable name='eissne' select='concat("&#x27;GE",$grp,"P",$ping,"&#x27;")'/>
<xsl:element name='input'>
<xsl:attribute name='type' select='"radio"'/>
<xsl:attribute name='name' select='concat("EG",$grp)'/>
<xsl:attribute name='id' select='concat("EG",$grp,"P",$ping)'/>
<xsl:attribute name='value' select='concat("EG",$grp,"P",$ping)'/>
<xsl:attribute name='onclick' select='concat("map(",$grp,",",$eissne,",&#x27;E&#x27;,&#x27;J&#x27;)")'/>
</xsl:element>
<xsl:element name='span'>
<xsl:attribute name='id' select='concat("GE",$grp,"P",$ping)'/>
<xsl:value-of select='eissn'/>
</xsl:element>
</td>


<td style='text-align:left;font-size:14px;'>
<xsl:element name='span'>
<xsl:attribute name='id' select='concat("GH",$grp,"P",$ping)'/>
<xsl:value-of select='../@skl'/>
</xsl:element>
</td>

</tr>
</xsl:for-each>

<tr>
<td colspan='2' style='text-align:center;'>
</td>

<td style='font-size:12px;'>
<xsl:element name='input'>
<xsl:attribute name='style' select='"font-size: 14px;"'/>
<xsl:attribute name='type' select='"text"'/>
<xsl:attribute name='name' select='concat("Label",$grp)'/>
<xsl:attribute name='id' select='concat("Label",$grp)'/>
<xsl:attribute name='value' select='""'/>
<xsl:attribute name='size' select='50'/>
</xsl:element>
</td>

<td style='font-size:12px;'>
<xsl:element name='input'>
<xsl:attribute name='style' select='"font-size: 14px;"'/>
<xsl:attribute name='type' select='"text"'/>
<xsl:attribute name='name' select='concat("Abbrev",$grp)'/>
<xsl:attribute name='id' select='concat("Abbrev",$grp)'/>
<xsl:attribute name='value' select='""'/>
<xsl:attribute name='size' select='8'/>
</xsl:element>

</td>

<td style='font-size:12px;'>
<xsl:element name='input'>
<xsl:attribute name='style' select='"font-size: 14px;"'/>
<xsl:attribute name='type' select='"text"'/>
<xsl:attribute name='name' select='concat("ISSN",$grp)'/>
<xsl:attribute name='id' select='concat("ISSN",$grp)'/>
<xsl:attribute name='value' select='""'/>
<xsl:attribute name='size' select='8'/>
</xsl:element>
</td>

<td style='font-size:12px;'>
<xsl:element name='input'>
<xsl:attribute name='style' select='"font-size: 14px;"'/>
<xsl:attribute name='type' select='"text"'/>
<xsl:attribute name='name' select='concat("EISSN",$grp)'/>
<xsl:attribute name='id' select='concat("EISSN",$grp)'/>
<xsl:attribute name='value' select='""'/>
<xsl:attribute name='size' select='8'/>
</xsl:element>
</td>


<td>
</td></tr>


<tr><td colspan='7'>
<table>
<tr><td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"button"'/>
<xsl:attribute name='name' select='concat("Clr",$grp)'/>
<xsl:attribute name='id' select='concat("Clr",$grp)'/>
<xsl:attribute name='value' select='"Clear Group"'/>
<xsl:attribute name='onclick' select='concat("clearGrp(",$grp,",",$count,",&#x27;J&#x27;)")'/>
</xsl:element>
</td><td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"button"'/>
<xsl:attribute name='name' select='concat("Mrg",$grp)'/>
<xsl:attribute name='id' select='concat("Mrg",$grp)'/>
<xsl:attribute name='value' select='"Merge"'/>
<xsl:attribute name='onclick' select='concat("merge(",$grp,",&#x27;J&#x27;)")'/>
</xsl:element>
</td>
<td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"button"'/>
<xsl:attribute name='name' select='concat("Undo",$grp)'/>
<xsl:attribute name='id' select='concat("Undo",$grp)'/>
<xsl:attribute name='value' select='"Undo"'/>
<xsl:attribute name='onclick' select='concat("undoOJ(",$grp,",&#x27;Journal&#x27;",")")'/>
</xsl:element>
</td>
</tr>
</table>
</td></tr>

<tr><td colspan='6'><hr width='100%'/></td></tr>

</xsl:for-each>

<script>

setSource()
</script>
</table>

</form>

</body>
</html>
<xsl:value-of select='$NL'/>
</xsl:template>

</xsl:stylesheet>
