<?xml version="1.0"?>
<xsl:stylesheet version='2.0'
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:vfx='http://vivoweb.org/ext/functions'
        xmlns:xs='http://www.w3.org/2001/XMLSchema'
        exclude-result-prefixes='xs vfx xsl'
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
<xsl:param name='grp' required='yes'/>
<xsl:param name='state' required='yes'/>

<xsl:output method='xml'  indent='yes' normalization-form='NFC'/>
<!-- designed and coded by Joseph R. Mc Enerney jrm424@cornell.edu -->
<xsl:template match='/'>
<JournalGroups>
<xsl:for-each select='//group'>
<xsl:choose>
<xsl:when test='$grp = position()'>

<xsl:element name='group'>
<xsl:attribute name='done' select='$state'/>
<xsl:attribute name='count' select='./@count'/>
<xsl:attribute name='skl' select='./@skl'/>

<xsl:for-each select='./journal'>
<xsl:copy-of select='.'/>
</xsl:for-each>

</xsl:element>

</xsl:when>
<xsl:otherwise>
<xsl:copy-of select='.'/>
</xsl:otherwise>
</xsl:choose>
</xsl:for-each>

</JournalGroups>
<xsl:value-of select='"&#x0a;"'/>
</xsl:template>

</xsl:stylesheet>
