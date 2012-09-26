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
function pop(x){
	//alert(x);
	ele = document.getElementById(x);
	x = x+'\-';
	
	
	var regx = new RegExp(x);
	var inputs = document.getElementsByTagName("input");
	//alert("ninputs "+inputs.length);
	for(n=0;n<inputs.length;n++){
	    var objId = inputs[n].name;
	    //alert( objId);
	    var ms = objId.match(regx);
	    if(ms != null){
		if(!ele.checked)
                    inputs[n].checked=false;
                else
                    inputs[n].checked=true;
            }
	    //alert(inputs[n].name);
        }
	//alert(inputs[n].name);
}

function popKb2(x){
	ele = document.getElementById(x);
	x = x+'\-';	
	var regx = new RegExp(x);
	var inputs = document.getElementsByTagName("input");

	for(n=0;n<inputs.length;n++){
	    var objId = inputs[n].name;
	    if(inputs[n].title == 'kb-2'){
	        var ms = objId.match(regx);
	        if(ms != null){
		    if(!ele.checked)
                        inputs[n].checked=false;
                    else
                        inputs[n].checked=true;
                }
            }

        }
}

function fixLangAndDatatypes(){
	var rgx = /_\|_/;
	var pres = document.getElementsByTagName("pre");
	for(n=0;n<pres.length;n++){
	    if(pres[n].innerHTML.match(rgx)){
		//alert(pres[n].innerHTML);
		var d = pres[n].innerHTML;
		//var a = d.split('_|_');
		//var rx = /^(.*?)_\|_.*?$/;
                var rx = /^(.*?)_\|_/;
	        d = d.replace(rx,'$1');
		//alert(d);
		pres[n].innerHTML = d;
            }
	    
        }

}
function clear(){
	var inputs = document.getElementsByTagName("input");
	for(n=0;n<inputs.length;n++){
	   if( inputs[n].type == 'checkbox' && inputs[n].disabled == false)
		inputs[n].checked=false;
        }
}

function setAll(){
	var inputs = document.getElementsByTagName("input");
	for(n=0;n<inputs.length;n++){
	   if( inputs[n].type == 'checkbox' && inputs[n].disabled == false)
		inputs[n].checked=true;
        }
}

function setGroup(x){
	ele  = document.getElementById(x);
	if(ele != null){
		ele.checked=true;
		pop(x);
        }
}
function clrGroup(x){
	ele  = document.getElementById(x);
	if(ele != null){
		ele.checked=false;
		pop(x);
        }
}
function setKb2InGroup(x){
	ele  = document.getElementById(x);
	if(ele != null){
		ele.checked=true;
		popKb2(x);
        }
}
function clrKb2InGroup(x){
	ele  = document.getElementById(x);
	if(ele != null){
		ele.checked=false;
		popKb2(x);
        }
}
function openObj(o){
	var id = o.id;
	var idO = id.replace("open","O");
	var type = id.replace("open","P");
	//alert(type)
	if(document.getElementById(type).innerHTML == "rdf:type"){
	    var r = confirm("You chose a type. Probably large Result Set");
	    if(r == false) 
               return;
        }
	var td = document.getElementById(idO);
	var childs = td.getElementsByTagName("a");
	var uri = childs[0].href;
//	alert(uri);
	var args = "uri="+encodeURI(uri);
	args += "&rootbase="+document.getElementById('rootbase').value;
	args += "&filebase="+document.getElementById('filebase').value;
	args += "&indexbase="+document.getElementById('indexbase').value;
        args += "&ruser="+document.getElementById('ruser').value;
        args += "&hpc="+document.getElementById('hpc').value;
//      alert(args);
	window.open("/cgi-bin/openObj.cgi?"+args,"objex");

}
function openSubj(o){
	var id = o.id;
	var idS = id.replace("open","S");
	var type = id.replace("open","P");
	//alert(type)
	if(document.getElementById(type).innerHTML == "rdf:type"){
	    var r = confirm("You chose a type. Probably large Result Set");
	    if(r == false) 
                return;
        }
	var td = document.getElementById(idS);
	var childs = td.getElementsByTagName("a");
	var uri = childs[0].href;
//	alert(uri);
	var args = "uri="+encodeURI(uri);
	args += "&rootbase="+document.getElementById('rootbase').value;
	args += "&filebase="+document.getElementById('filebase').value;
	args += "&indexbase="+document.getElementById('indexbase').value;
        args += "&ruser="+document.getElementById('ruser').value;
	 args += "&hpc="+document.getElementById('hpc').value;
//      alert(args);
	window.open("/cgi-bin/openObj.cgi?"+args,"objex");

}
