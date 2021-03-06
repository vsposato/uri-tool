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
<xsl:param name='ind' required='yes'/>
<xsl:param name='insp' required='yes'/>
<xsl:param name='outsp' required='yes'/>

<xsl:output method='xml' indent='yes' normalization-form='NFC'/>
<xsl:strip-space elements="*"/>

<xsl:variable name='ins' 
  select="document($insp)/inPredicates"/>
<!-- designed and coded by Joseph R. Mc Enerney jrm424@cornell.edu -->
<xsl:variable name='outs' 
  select="document($outsp)/outPredicates"/>

<xsl:template match='/'>
<xsl:element name='Summary' inherit-namespaces='no'>
<xsl:element name='topic' inherit-namespaces='no'>
<xsl:value-of select='$ind'/>
</xsl:element>
<xsl:copy-of select="$ins"/>

<xsl:copy-of select="$outs"/>
</xsl:element>
<xsl:value-of select='"&#xA;"'/>
</xsl:template>

</xsl:stylesheet>
