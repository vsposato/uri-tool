/*
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


*/


function setSource(){
    
    var src = document.getElementById('hpc').value.split(':');
    var s = src[0];

    if(src[1] != '') s += ':' + src[1];
    if(src[2] != '') s += '/' + src[2];
    document.getElementById('source').innerHTML = s;

}


// designed and coded by Joseph R. Mc Enerney jrm424@cornell.edu
function clearGrp(g,cnt,ilk){
    for(var n=1;n<=cnt;n++){
        var rb ="G"+g+"P"+n;
        var e = document.getElementById("LB"+rb);
        e.checked = false;
	e=document.getElementById("U"+rb);
        e.checked = false;
        if(ilk == 'J'){
	    e=document.getElementById("A"+rb);
	    e.checked = false;
	    e=document.getElementById("I"+rb);
	    e.checked = false;
	    e=document.getElementById("E"+rb);
	    e.checked = false;
	}
    }
    clrTxtPeep(g,ilk);
}

function chkItem(g,n,ilk){
    var rb ="G"+g+"P"+n;
    var e = document.getElementById("LB"+rb);
    e.checked = true;
    e=document.getElementById("U"+rb);
    e.checked = true;
    var sp = document.getElementById("GLB"+g+"P"+n);
    var s = sp.innerHTML;
    document.getElementById("Label"+g).value = s;
    if(ilk == 'J'){
	e=document.getElementById("A"+rb);
	e.checked = true;
	e=document.getElementById("I"+rb);
	e.checked = true;
	e=document.getElementById("E"+rb);
	e.checked = true;
	sp = document.getElementById("GA"+g+"P"+n);
	s = sp.innerHTML;
	document.getElementById("Abbrev"+g).value = s;

	sp = document.getElementById("GI"+g+"P"+n);
	s = sp.innerHTML;
	document.getElementById("ISSN"+g).value = s;

	sp = document.getElementById("GE"+g+"P"+n);
	s = sp.innerHTML;
	document.getElementById("EISSN"+g).value = s;
    }
}

function clrTxtPeep(g,ilk) {
    document.getElementById("Label"+g).value = '';
    if(ilk == 'J'){
	document.getElementById("Abbrev"+g).value = '';
	document.getElementById("ISSN"+g).value = '';
	document.getElementById("EISSN"+g).value = '';
    }
}


function undoOJ(g,ilk){
    var x;
    if(ilk == 'Org'){
        x='o';
    } else {
        x='j';
    }
    var url = "/cgi-bin/dd"+x+"Undo.cgi?";
    url += "grp="+g;
    url += "&token="+document.getElementById("token").value;
    var ee =document.getElementById("Group"+g);
    ee.style.display='inline';
    ee.innerHTML = " Working";
    loadXMLDoc(url);

}

function merge(g,ilk){
    //alert("Merge "+g + "  " + "UG"+g);
    var e = document.getElementById("Gsize"+g);
    var sz = e.value;
    var f = rbTest("UG"+g, sz);
    if(f == -1){
	alert('Choose a URI.');
	return;
    }
    var F = f;
    var uri = document.getElementById("UG"+g+"P"+f).value;

    var inc = incCollect(g,sz);

    var lst = inc.split('|');
    var flag = 0;
    for(var n=0;n<lst.length;n++){
	if(lst[n] == f){
	    flag = 1;
	    break;
	}
    }
    if(flag == 0){
	alert("The chosen URI must be 'included'.");
	return;
    }
    if(lst.length < 2){
	alert("At least two URIs must be 'included'.");
	return;
    }
    
    var clabel = '';
    var label = trim(document.getElementById("Label"+g).value);
    document.getElementById("Label"+g).value = label;
    var lb = '';
    if(label == '') {
	f = rbTest("LBG"+g, sz);
	if(f != -1 && label == ''){
	    label = document.getElementById("GLB"+g+"P"+f).innerHTML;
	    lb = document.getElementById("LBG"+g+"P"+f).value;
	} else {
	    label = document.getElementById("GLB"+g+"P"+F).innerHTML;
	    lb = document.getElementById("LBG"+g+"P"+F).value;
	}
    } else {
	clabel = document.getElementById("GLB"+g+"P"+F).innerHTML;
    }
    var cabbr = '';
    var abbr = '';
    var abrc = '';
    var cissn = '';
    var issn = '';
    var isnc = '';    
    var ceissn = '';
    var eissn = '';
    var eisnc = '';

    if(ilk == 'J'){
	abbr = trim(document.getElementById("Abbrev"+g).value);
	document.getElementById("Abbrev"+g).value = abbr;
	if(abbr == ''){
	    f = rbTest("AG"+g, sz);
	    if(f != -1 && abbr == ''){
		abbr = document.getElementById("GA"+g+"P"+f).innerHTML;
		abrc = document.getElementById("AG"+g+"P"+f).value;
	    } else {
		abbr = document.getElementById("GA"+g+"P"+F).innerHTML;
		abrc = document.getElementById("AG"+g+"P"+F).value;
	    }
	} else {
	    cabbr = document.getElementById("GA"+g+"P"+F).innerHTML;
	}

	issn = trim(document.getElementById("ISSN"+g).value);
	document.getElementById("ISSN"+g).value = issn;
	if(issn == ''){
	    f = rbTest("IG"+g, sz);
	    if(f != -1 && issn == ''){
		issn = document.getElementById("GI"+g+"P"+f).innerHTML;
		isnc = document.getElementById("IG"+g+"P"+f).value;
	    } else {
		issn = document.getElementById("GI"+g+"P"+F).innerHTML;
		isnc = document.getElementById("IG"+g+"P"+F).value;
	    }
	} else {
	    cissn = document.getElementById("GI"+g+"P"+F).innerHTML;
	}
	eissn = trim(document.getElementById("EISSN"+g).value);
	document.getElementById("EISSN"+g).value = eissn;
	if(eissn == ''){
	    f = rbTest("IG"+g, sz);
	    if(f != -1 && eissn == ''){
		eissn = document.getElementById("GE"+g+"P"+f).innerHTML;
		eisnc = document.getElementById("EG"+g+"P"+f).value;
	    } else {
		eissn = document.getElementById("GE"+g+"P"+F).innerHTML;
		eisnc = document.getElementById("EG"+g+"P"+F).value;
	    }
	} else {
	    ceissn = document.getElementById("GE"+g+"P"+F).innerHTML;
	}
    }
    var hpc = trim(document.getElementById("hpc").value);
    var url = "/cgi-bin/dedupMatches.cgi?";
    url += "grp="+g;
    url += "&grpsize="+sz;
    url += "&uri="+encodeURI(uri);
    url += "&label="+encodeURIComponent(trim(label));
    url += "&lb="+encodeURIComponent(trim(lb));
    url += "&clabel="+encodeURIComponent(trim(clabel));	
    if(ilk == 'J'){
	url += "&abbr="+encodeURIComponent(trim(abbr));
	url += "&abrc="+encodeURIComponent(trim(abrc));
	url += "&cabbr="+encodeURIComponent(trim(cabbr));
	
	url += "&issn="+encodeURIComponent(trim(issn));
	url += "&isnc="+encodeURIComponent(trim(isnc));
	url += "&cissn="+encodeURIComponent(trim(cissn));	
    }
    url += "&hpc="+encodeURIComponent(trim(hpc));
    url += "&token="+document.getElementById("token").value;
    url += "&inc="+inc;
    //alert(url);
    var ee =document.getElementById("Group"+g);
    ee.style.display='inline';
    ee.innerHTML = " Working";
    loadXMLDoc(url);
}
function rbTest(g,sz){
    var f = -1;
    for(var n=1;n<=sz;n++){
	var e=document.getElementById(g+"P"+n);
	//alert(g+"P"+n);
	if(e.checked){
	    f = n;
	    break;
	}
    }
    //alert(f);
    return f;
}

function incCollect(g,sz){
    var list = '';
    for(var n=1;n<=sz;n++){
	var e=document.getElementById("XG"+g+"P"+n);
	//alert(g+"P"+n);
	if(e.checked){
	    if(list != '')
		list += '|';
	    list += n;
	}
    }
    //alert(f);
    return list;
}


function map(g,s,p,ilk){
    var e = document.getElementById(s);
    if(p == 'LB'){
	document.getElementById("Label"+g).value=e.innerHTML;
	return;
    }
    if(ilk == 'J'){
	if(p == 'A'){
	    document.getElementById("Abbrev"+g).value=e.innerHTML;
	    return;
	}
	
	if(p == 'I'){
	    document.getElementById("ISSN"+g).value=e.innerHTML;
	    return;
	}
	if(p == 'E'){
	    document.getElementById("EISSN"+g).value=e.innerHTML;
	    return;
	}
    }
    return;
    
}


function trim(str) { 
    if(str == null)
	return "";
    str = str.replace(/^\s+/, ''); 
    str = str.replace(/\s+$/, '');
    return str;
}

function loadXMLDoc(url)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
	    xmlhttp=new XMLHttpRequest();
	}
    else
	{// code for IE6, IE5
	    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
    xmlhttp.onreadystatechange=function()
	{
	    if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
		    //alert('Done '+xmlhttp.responseText);
		    var parts = xmlhttp.responseText.split('|');
		    //alert("Group"+parts[0]);
		    if(!parts[0].match(/^>>>/)){
			var e =document.getElementById("Group"+parts[0]);
			if(parts[1] == "Undo")
			    e.style.display='none';
			else
			    e.style.display='inline';
			e.innerHTML = " Done";
		    } else {
			alert("FAULT: " + parts[0]);
		    }
		    //alert(parts[1]);
		}
	}
    xmlhttp.open("GET",url,true);
    xmlhttp.send();
}
