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
function clearGrp(g,cnt){
    for(var n=1;n<=cnt;n++){
        var rb ="G"+g+"P"+n;
        var e = document.getElementById("N"+rb);
        //alert("N"+rb);
        e.checked = false;
        e=document.getElementById("L"+rb);
        e.checked = false;
	e=document.getElementById("F"+rb);
        e.checked = false;
	e=document.getElementById("M"+rb);
        e.checked = false;
	e=document.getElementById("U"+rb);
        e.checked = false;
        e=document.getElementById("LB"+rb);
        e.checked = false;

    }
    clrTxtPeep(g);
}
function chkPeep(g,n){
    var rb ="G"+g+"P"+n;
    var e = document.getElementById("N"+rb);
    e.checked = true;
    e=document.getElementById("F"+rb);
    e.checked = true;
    e=document.getElementById("L"+rb);
    e.checked = true;
    e=document.getElementById("M"+rb);
    e.checked = true;
    e=document.getElementById("U"+rb);
    e.checked = true;
    e=document.getElementById("LB"+rb);
    e.checked = true;
    var sp = document.getElementById("GN"+g+"P"+n);
    var s = sp.innerHTML;
    map(g,s,"N");
    sp = document.getElementById("GL"+g+"P"+n);
    s = sp.innerHTML;
    map(g,s,"L");
    sp = document.getElementById("GF"+g+"P"+n);
    s = sp.innerHTML;
    map(g,s,"F");
    sp = document.getElementById("GM"+g+"P"+n);
    s = sp.innerHTML;
    map(g,s,"M");
    sp = document.getElementById("GLB"+g+"P"+n);
    s = sp.innerHTML;
    map(g,s,"LB");
}

function clrTxtPeep(g) {
    var e = document.getElementById("Netid"+g);
    e.value='';
    e = document.getElementById("Last"+g);
    e.value='';
    e = document.getElementById("First"+g);
    e.value='';
    e = document.getElementById("Middle"+g);
    e.value='';
    e = document.getElementById("Label"+g);
    e.value='';
}

function undoIt(g){
    var url = "/cgi-bin/ddpUndo.cgi?";
    url += "grp="+g;
    url += "&token="+document.getElementById("token").value;
    var ee =document.getElementById("Group"+g);
    ee.style.display='inline';
    ee.innerHTML = " Working";
    loadXMLDoc(url);

}
function merge(g){
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

    var netid = trim(document.getElementById("Netid"+g).value);
    document.getElementById("Netid"+g).value = netid;
    var nid = '';
    if(netid == '') {
	f = rbTest("NG"+g, sz);
	if(f != -1){
	    netid = document.getElementById("GN"+g+"P"+f).innerHTML;
	    nid =  document.getElementById("NG"+g+"P"+f).value
	} else {
	    netid = document.getElementById("GN"+g+"P"+F).innerHTML;
	    nid =  document.getElementById("NG"+g+"P"+F).value
	}
    }
    var lname = trim(document.getElementById("Last"+g).value);
    document.getElementById("Last"+g).value = lname;
    var ln = '';
    if(lname == '') {
	f = rbTest("LG"+g, sz);
	if(f != -1){	
	    lname = document.getElementById("GL"+g+"P"+f).innerHTML;
	    ln = document.getElementById("LG"+g+"P"+f).value
	} else {
	    lname = document.getElementById("GL"+g+"P"+F).innerHTML;
	    ln = document.getElementById("LG"+g+"P"+F).value
	}
    }

    var fname = trim(document.getElementById("First"+g).value);
    document.getElementById("First"+g).value = fname;
    var fn = '';
    if(fname == ''){
	f = rbTest("FG"+g, sz);
	if(f != -1 && fname == ''){
	    fname = document.getElementById("GF"+g+"P"+f).innerHTML;
	    fn = document.getElementById("FG"+g+"P"+f).value
	} else {
	    fname = document.getElementById("GF"+g+"P"+F).innerHTML;
	    fn = document.getElementById("FG"+g+"P"+F).value
	}
    }


    var mname = trim(document.getElementById("Middle"+g).value);
    document.getElementById("Middle"+g).value = mname;
    var mn = '';
    if(mname == '') {
	f = rbTest("MG"+g, sz);
	if(f != -1 && mname == ''){
	    mname = document.getElementById("GM"+g+"P"+f).innerHTML;
	    mn = document.getElementById("MG"+g+"P"+f).value;
	} else {
	    mname = document.getElementById("GM"+g+"P"+F).innerHTML;
	    mn = document.getElementById("MG"+g+"P"+F).value;
	}
    }

    var label = trim(document.getElementById("Label"+g).value);
    document.getElementById("Label"+g).value = label;
    var lb = '';
    if(label == '') {
	f = rbTest("LBG"+g, sz);
	if(f != -1 && label == ''){
	    label = document.getElementById("GLB"+g+"P"+f).innerHTML;
	    lb = document.getElementById("LBG"+g+"P"+f).value
	} else {
	    label = document.getElementById("GLB"+g+"P"+F).innerHTML;
	    lb = document.getElementById("LBG"+g+"P"+F).value
	}
    }

    var hpc = trim(document.getElementById("hpc").value);
    var url = "/cgi-bin/dedup.cgi?";
    url += "grp="+g;
    url += "&grpsize="+sz;
    url += "&uri="+encodeURI(uri);
    url += "&netid="+encodeURIComponent(trim(netid));
    url += "&nid="+encodeURIComponent(trim(nid));
    url += "&lname="+encodeURIComponent(trim(lname));
    url += "&ln="+encodeURIComponent(trim(ln));
    url += "&fname="+encodeURIComponent(trim(fname));
    url += "&fn="+encodeURIComponent(trim(fn));
    url += "&mname="+encodeURIComponent(trim(mname));
    url += "&mn="+encodeURIComponent(trim(mn));
    url += "&label="+encodeURIComponent(trim(label));
    url += "&lb="+encodeURIComponent(trim(lb));
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


function map(g,s,p){
    if(p == 'N'){
	document.getElementById("Netid"+g).value=s;
	return;
    }
    
    if(p == 'L'){
	document.getElementById("Last"+g).value=s;
	return;
    }

    if(p == 'F'){
	document.getElementById("First"+g).value=s;
	return;
    }

    if(p == 'M'){
	document.getElementById("Middle"+g).value=s;
	return;
    }

    if(p == 'LB'){
	document.getElementById("Label"+g).value=s;
	return;
    }
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
