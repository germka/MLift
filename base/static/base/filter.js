window.onload=function() {

//disabling all forms except obj_str
document.getElementById('build').disabled=true;
document.getElementById('build_housing').disabled=true;
document.getElementById('par').disabled=true;
document.getElementById('type').disabled=true;

    document.getElementById('str').onchange = function() {
        document.getElementById('build').disabled=false;
}
    document.getElementById('build').onchange = function() {
        document.getElementById('build_housing').disabled=false;
}
    document.getElementById('build_housing').onchange = function() {
        document.getElementById('par').disabled=false;
}
    document.getElementById('par').onchange = function() {
        document.getElementById('type').disabled=false;
}

}
