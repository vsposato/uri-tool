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
<xsl:param name='filebase'  required='yes'/>
<xsl:param name='rootbase'  required='yes'/>
<xsl:param name='auxbase'  required='no'/>
<xsl:param name='ruser'  required='yes'/>
<xsl:param name='wuser'  required='no'/>
<xsl:param name='urinum'  required='no' select='"1"'/>
<xsl:param name='hpc' required='yes'/>


<xsl:variable name='NL' select='"&#xA;"'/>
<xsl:variable name='rb' select='substring-before($rootbase,"-TK")'/>

<!-- designed and coded by Joseph R. Mc Enerney jrm424@cornell.edu -->

<xsl:output method='html' indent='yes' normalization-form='NFC'/>
<xsl:strip-space elements="*"/>


<xsl:template match='/'>
<html>
<head>
<xsl:choose>
<xsl:when test='$auxbase = ""'>
<title>UriTool Main List</title>
</xsl:when>
<xsl:otherwise>
<title>UriTool Adjunct List</title>
</xsl:otherwise>
</xsl:choose>
<!-- meta http-equiv="Content-Type" content="text/html; charset=utf-8" -->
<xsl:element name='meta'>
<xsl:attribute name='http-equiv' select='"Content-Type"' />
<xsl:attribute name='content' select='"text/html; charset=utf-8"' />
</xsl:element>
<script src='/js/app.js'/>
<title>UriTool</title>
</head>
<body style='font-family:Arial,Verdana;font-size:10px;background-color:#F5F5F5'>
<xsl:comment><xsl:value-of select='concat("WUSER=",$wuser)'/></xsl:comment>

<xsl:comment> Current File Prefix:- <xsl:value-of select='$filebase'/> </xsl:comment>
<H1>UriTool </H1> 
<H2>Accessing:- <span id='source' style='color: red;font-size: 18px;font-family: courier'></span></H2>
<H2>Prefix Token:- <xsl:value-of select='$rb'/> </H2>
<H2>User <xsl:value-of select='concat("&#39;",$wuser,"&#39;")'/> 
working as <xsl:value-of select='concat("&#39;",$ruser,"&#39;")'/> </H2>
<H2>URI count:- <xsl:value-of select='$urinum'/> </H2>
<xsl:comment><xsl:value-of select='concat("FILEBASE:",$filebase)'/></xsl:comment>
<form action="/cgi-bin/dispose.cgi" method='post'>
<xsl:value-of select='$NL'/>
<xsl:element name='input'>
<xsl:attribute name='type' select='"hidden"'/>
<xsl:attribute name='name' select='"rootbase"'/>
<xsl:attribute name='id' select='"rootbase"'/>
<xsl:attribute name='value' select='$rootbase'/>
</xsl:element>
<xsl:value-of select='$NL'/>
<xsl:element name='input'>
<xsl:attribute name='type' select='"hidden"'/>
<xsl:attribute name='name' select='"filebase"'/>
<xsl:attribute name='id' select='"filebase"'/>
<xsl:attribute name='value' select='$filebase'/>
</xsl:element>
<xsl:value-of select='$NL'/>
<xsl:element name='input'>
<xsl:attribute name='type' select='"hidden"'/>
<xsl:attribute name='name' select='"indexbase"'/>
<xsl:attribute name='id' select='"indexbase"'/>
<xsl:attribute name='value' select='0'/>
</xsl:element>
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

<xsl:if test='$auxbase != ""'>
<xsl:element name='input'>
<xsl:attribute name='type' select='"hidden"'/>
<xsl:attribute name='name' select='"auxbase"'/>
<xsl:attribute name='id' select='"auxbase"'/>
<xsl:attribute name='value' select='$auxbase'/>
</xsl:element>
<xsl:value-of select='$NL'/>
<xsl:element name='input'>
<xsl:attribute name='type' select='"hidden"'/>
<xsl:attribute name='name' select='"rollback"'/>
<xsl:attribute name='id' select='"rollback"'/>
<xsl:attribute name='value' select='"No"'/>
</xsl:element>

</xsl:if>
<table border='0' cellpadding='4' cellspacing='4'>
<xsl:for-each select='//Summary' >
<xsl:variable name='cbn' select='concat("U-",position())'/>
<xsl:variable name='pop'>
<xsl:text>pop("</xsl:text><xsl:value-of select='$cbn'/><xsl:text>")</xsl:text>
</xsl:variable>
<xsl:variable name='setG'>
<xsl:text>setGroup("</xsl:text><xsl:value-of select='$cbn'/><xsl:text>")</xsl:text>
</xsl:variable>
<xsl:variable name='clrG'>
<xsl:text>clrGroup("</xsl:text><xsl:value-of select='$cbn'/>
<xsl:text>")</xsl:text>
</xsl:variable>
<xsl:variable name='setGK'>
<xsl:text>setKb2InGroup("</xsl:text><xsl:value-of select='$cbn'/><xsl:text>")</xsl:text>
</xsl:variable>
<xsl:variable name='clrGK'>
<xsl:text>clrKb2InGroup("</xsl:text><xsl:value-of select='$cbn'/>
<xsl:text>")</xsl:text>
</xsl:variable>
<tr><td style='text-align:left;'>
<table border='0' cellpadding='4' cellspacing='0'>
<tr><td style='border:1px solid black;'>
<xsl:element name='input'>
<xsl:attribute name='type' select='"checkbox"'/>
<xsl:attribute name='name' select='$cbn'/>
<xsl:attribute name='id' select='$cbn'/>
<xsl:attribute name='value' select='"on"'/>
<xsl:attribute name='onclick' select='$pop'/>
</xsl:element>

</td><td style='border:1px solid black;text-align:center;'>
URI <xsl:value-of select='position()'/></td>
<td style='text-align:center;border:1px solid black;'>
<xsl:element name='a'>
<xsl:attribute name='href' select='topic'/>
<xsl:attribute name='target' select='"vivo"'/>
<xsl:value-of select='topic'/>
</xsl:element>
</td>
<td style='text-align:center;border:1px solid black;'>
<xsl:element name='a'>
<xsl:attribute name='href' select='concat("#",topic,"-ctrl")'/>
<xsl:attribute name='style' select='"text-decoration: none;color: blue;"'/>
Controls
</xsl:element>
</td>
</tr>
</table>
</td></tr>

<tr> <td colspan='3'>
&#160;
<xsl:if test='count(inPredicates/predicate)>0'>
<table border='0' cellpadding='4' cellspacing='4'>
<caption style='text-align: center'>URI as triple Object</caption>
<xsl:call-template name='obj'>
<xsl:with-param name='preds' select='inPredicates/predicate'/>
<xsl:with-param name='topic' select='topic'/>
<xsl:with-param name='topicstr' select='$cbn'/>

</xsl:call-template>
</table>
</xsl:if>
</td></tr>

<tr> <td colspan='3'>
&#160;
<xsl:if test='count(outPredicates/predicate)>0'>
<table border='0' cellpadding='4' cellspacing='4'>
<caption style='text-align: center'>URI as triple Subject</caption>
<xsl:call-template name='subj'>
<xsl:with-param name='preds' select='outPredicates/predicate'/>
<xsl:with-param name='topic' select='topic'/>
<xsl:with-param name='topicstr' select='$cbn'/>
</xsl:call-template>
</table>
</xsl:if>
</td></tr>
<tr> <td colspan='3' style='text-align: center'>
<xsl:element name='a'>
<xsl:attribute name='name' select='concat(topic,"-ctrl")'/>
</xsl:element>
<table border='0' cellpadding='4' cellspacing='4'>
<tr><td style='text-align: center'> Group Controls </td>
<td>
<table border='0' cellpadding='4' cellspacing='4'>
<tr>

<td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"button"'/>
<xsl:attribute name='name' select='concat("CheckAll",$cbn)'/>
<xsl:attribute name='value' select='"Check All in Group"'/>
<xsl:attribute name='onclick' select='$setG'/>
</xsl:element>
</td>

<td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"button"'/>
<xsl:attribute name='name' select='concat("Clear",$cbn)'/>
<xsl:attribute name='value' select='"Clear in Group"'/>
<xsl:attribute name='onclick' select='$clrG'/>
</xsl:element>
</td>

<td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"button"'/>
<xsl:attribute name='name' select='concat("CheckAllKb2s",$cbn)'/>
<xsl:attribute name='value' select='"Check All Kb2s in Group"'/>
<xsl:attribute name='onclick' select='$setGK'/>
</xsl:element>
</td>

<td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"button"'/>
<xsl:attribute name='name' select='concat("ClearAllKb2s",$cbn)'/>
<xsl:attribute name='value' select='"Clear Kb2s in Group"'/>
<xsl:attribute name='onclick' select='$clrGK'/>
</xsl:element>
</td>

</tr>
</table>
</td>
</tr>
<tr><td style='text-align: center'> Global Controls </td>
<td colspan='3'>
<table border='0' cellpadding='4' cellspacing='4'>
<tr><td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"submit"'/>
<xsl:attribute name='name' select='concat("Exclude",$cbn)'/>
<xsl:attribute name='value' select='"Exclude Checked"'/>
</xsl:element>
</td>
<td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"submit"'/>
<xsl:attribute name='name' select='concat("Retract",$cbn)'/>
<xsl:attribute name='value' select='"Save Checked for Retraction"'/>
</xsl:element>
</td>
<td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"submit"'/>
<xsl:attribute name='name' select='concat("Undo",$cbn)'/>
<xsl:attribute name='value' select='"Undo Last Save for Retraction"'/>
</xsl:element>
</td>

</tr>
</table>
</td>
</tr>


</table>
</td></tr>
<tr> <td colspan='3'><hr/> </td></tr>
<xsl:comment><xsl:value-of select='concat("__ENDTOPIC__",$cbn)'/></xsl:comment>
</xsl:for-each>

</table>
</form>
<script>
clear();
fixLangAndDatatypes();


setSource()

</script>
</body>
</html>
<xsl:value-of select='$NL'/>
</xsl:template>

<!-- ============================================= -->

<xsl:template name='obj'>
<xsl:param name='preds'/>
<xsl:param name='topic'/>
<xsl:param name='topicstr'/>
<xsl:for-each select='$preds'>

<xsl:variable name='p' select='puri'/>
<xsl:variable name='cbnip' select='concat($topicstr,"-ipo-",position())'/>

<xsl:for-each select='subject/suri'>

<xsl:variable name='cbnips' select='concat($cbnip,"-",position())'/>
<!-- <xsl:variable name='g' select='substring-after(../graph,"/vitro-")'/> -->
<xsl:variable name='g' select='../graph'/>
<xsl:variable name='flag' select='substring-after($g,"vitro-")'/>
<xsl:comment><xsl:value-of select='concat("START-",$cbnips)'/>

</xsl:comment>
<tr><td colspan='3' style='font-size:12px;'>
<xsl:value-of select='concat("Graph:- ",$g)'/></td></tr>
<tr><td>
<xsl:choose>
<xsl:when test='$auxbase=""'>
<xsl:element name='input'>
<xsl:attribute name='type' select='"button"'/>
<xsl:attribute name='name' select='concat($cbnips,"open")'/>
<xsl:attribute name='id' select='concat($cbnips,"open")'/>
<xsl:attribute name='value' select='"Open ?S"'/>
<xsl:attribute name='title' select='"Open Subject"'/>
<xsl:attribute name='onclick' select='"openSubj(this)"'/>
</xsl:element>
</xsl:when>
<xsl:otherwise>
&#160;
</xsl:otherwise>
</xsl:choose>

</td><td>?S</td>

<xsl:element name='td'>
<xsl:attribute name='id' select='concat($cbnips,"S")'/>


<xsl:element name='a'>

<xsl:attribute name='href' select='.'/>
<xsl:attribute name='target' select='"vivo"'/>
<xsl:value-of select='.'/>
</xsl:element>

</xsl:element></tr>
<tr><td><!-- &#160; -->
<xsl:element name='input'>
<xsl:attribute name='type' select='"checkbox"'/>
<xsl:attribute name='name' select='$cbnips'/>
<xsl:attribute name='id' select='$cbnips'/>
<xsl:attribute name='value' select='"on"'/>
<xsl:attribute name='title' select='$flag'/>

</xsl:element>
</td><td>?P</td>

<xsl:element name='td'>
<xsl:attribute name='id' select='concat($cbnips,"P")'/>


<xsl:value-of select='$p'/>
</xsl:element></tr>
<tr><td>&#160;</td><td>?O</td>

<xsl:element name='td'>
<xsl:attribute name='id' select='concat($cbnips,"O")'/>


<xsl:element name='a'>

<xsl:attribute name='href' select='$topic'/>
<xsl:attribute name='target' select='"vivo"'/>
<xsl:value-of select='$topic'/>
</xsl:element>

</xsl:element>
</tr>
<xsl:comment><xsl:value-of select='concat("END-",$cbnips)'/></xsl:comment>
<tr><td colspan='3'><hr width='200'/></td></tr>
</xsl:for-each>

</xsl:for-each>

</xsl:template>

<!-- ============================================= -->

<xsl:template name='subj'>
<xsl:param name='preds'/>
<xsl:param name='topic'/>
<xsl:param name='topicstr'/>
<xsl:for-each select='$preds'>

<xsl:variable name='p' select='puri'/>


<xsl:choose>
<xsl:when test='exists(datawraper)'>
<!-- Data Property case -->
<xsl:variable name='cbnip' select='concat($topicstr,"-opd-",position())'/>
<xsl:for-each select='datawraper'>

<xsl:variable name='cbnips' select='concat($cbnip,"-",position())'/>

<xsl:comment><xsl:value-of select='concat("START-",$cbnips)'/></xsl:comment>
<!-- <xsl:variable name='g' select='substring-after(graph,"/vitro-")'/> -->
<xsl:variable name='g' select='graph'/>
<xsl:variable name='flag' select='substring-after($g,"vitro-")'/>
<tr><td colspan='3' style='font-size:12px;'>
<xsl:value-of select='concat("Graph:- ",$g)'/></td></tr>
<tr><td>
&#160;
</td><td>?S</td>

<xsl:element name='td'>
<xsl:attribute name='id' select='concat($cbnips,"S")'/>

<xsl:element name='a'>

<xsl:attribute name='href' select='$topic'/>
<xsl:attribute name='target' select='"vivo"'/>
<xsl:value-of select='$topic'/>
</xsl:element>

</xsl:element>

</tr>
<tr><td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"checkbox"'/>
<xsl:attribute name='name' select='$cbnips'/>
<xsl:attribute name='id' select='$cbnips'/>
<xsl:attribute name='value' select='"on"'/>
<xsl:attribute name='title' select='$flag'/>
</xsl:element>


</td><td>?P</td>

<xsl:element name='td'>
<xsl:attribute name='id' select='concat($cbnips,"P")'/>
<xsl:value-of select='$p'/>
</xsl:element>

</tr>
<tr><td>&#160;</td><td>?O</td>
<xsl:element name='td'>
<xsl:attribute name='id' select='concat($cbnips,"O")'/>
<!-- <pre  style='width:600px;overflow:scroll'> -->
<xsl:choose>
<xsl:when test='string-length(datum)>60'>
<xsl:element name='pre'>
<xsl:attribute name='style' select='"width:600px;overflow:scroll"'/>

<xsl:value-of select='datum'/>
</xsl:element>
</xsl:when>
<xsl:otherwise>
<pre><xsl:value-of select='datum'/>
</pre>
</xsl:otherwise>
</xsl:choose>
</xsl:element>
</tr>
<xsl:comment><xsl:value-of select='concat("END-",$cbnips)'/></xsl:comment>
<tr><td colspan='3'><hr width='200'/></td></tr>
</xsl:for-each>
</xsl:when>

<xsl:otherwise>
<!-- Object Property Case -->
<xsl:variable name='cbnip' select='concat($topicstr,"-opo-",position())'/>
<xsl:for-each select='object/ouri'>
<xsl:variable name='cbnips' select='concat($cbnip,"-",position())'/>
<xsl:comment><xsl:value-of select='concat("START-",$cbnips)'/></xsl:comment>
<!-- <xsl:variable name='g' select='substring-after(../graph,"/vitro-")'/> -->
<xsl:variable name='g' select='../graph'/>
<xsl:variable name='flag' select='substring-after($g,"vitro-")'/>

<tr><td colspan='3' style='font-size:12px;'>
<xsl:value-of select='concat("Graph:- ",$g)'/></td></tr>
<tr><td>

&#160;
</td><td>?S</td>
<xsl:element name='td'>
<xsl:attribute name='id' select='concat($cbnips,"S")'/>

<xsl:element name='a'>

<xsl:attribute name='href' select='$topic'/>
<xsl:attribute name='target' select='"vivo"'/>
<xsl:value-of select='$topic'/>
</xsl:element>


</xsl:element>
</tr>
<tr><td>
<xsl:element name='input'>
<xsl:attribute name='type' select='"checkbox"'/>
<xsl:attribute name='name' select='$cbnips'/>
<xsl:attribute name='id' select='$cbnips'/>
<xsl:attribute name='value' select='"on"'/>
<xsl:attribute name='title' select='$flag'/>
</xsl:element>



</td><td>?P</td>
<xsl:element name='td'>
<xsl:attribute name='id' select='concat($cbnips,"P")'/>

<xsl:value-of select='$p'/>
</xsl:element>
</tr>
<tr><td>
<xsl:choose>
<xsl:when test='$auxbase=""'>
<xsl:element name='input'>
<xsl:attribute name='type' select='"button"'/>
<xsl:attribute name='name' select='concat($cbnips,"open")'/>
<xsl:attribute name='id' select='concat($cbnips,"open")'/>
<xsl:attribute name='value' select='"Open ?O"'/>
<xsl:attribute name='title' select='"Open Object"'/>
<xsl:attribute name='onclick' select='"openObj(this)"'/>
</xsl:element>
</xsl:when>
<xsl:otherwise>
&#160;
</xsl:otherwise>
</xsl:choose>

</td><td>?O</td>
<xsl:element name='td'>
<xsl:attribute name='id' select='concat($cbnips,"O")'/>

<xsl:element name='a'>
<xsl:attribute name='href' select='.'/>
<xsl:attribute name='target' select='"vivo"'/>
<xsl:value-of select='.'/>
</xsl:element>

</xsl:element></tr>
<xsl:comment><xsl:value-of select='concat("END-",$cbnips)'/></xsl:comment>
<tr><td colspan='3'><hr width='200'/></td></tr>
</xsl:for-each>
</xsl:otherwise>
</xsl:choose>

</xsl:for-each>
<xsl:value-of select='$NL'/>


</xsl:template>

</xsl:stylesheet>

