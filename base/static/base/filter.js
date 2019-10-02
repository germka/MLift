window.onload=function() {
str = document.getElementById('str')
build = document.getElementById('build')
build_housing = document.getElementById('build_housing')
par = document.getElementById('par')
type = document.getElementById('type')

//disabling all forms except obj_str
if (str.value != '') {
    document.getElementById('build').disabled=false; 
} else {
    document.getElementById('build').disabled=true;
}

if (document.getElementById('build_housing')) {
    if (build.value != '') {
        document.getElementById('build_housing').disabled=false; 
    } else {
    document.getElementById('build_housing').disabled=true;
    }
}

if (document.getElementById('build_housing') && document.getElementById('par')) {
    if (build_housing.value != '') {
        document.getElementById('par').disabled=false;
    } else {
    document.getElementById('par').disabled=true;
    }
}

if (document.getElementById('par')) {
    if (par.value != '') {
        document.getElementById('type').disabled=false;
    } else {
    document.getElementById('type').disabled=true;
    }
}


document.getElementById('str').onchange = function() {
    document.getElementById('build').disabled=false;
    new_ticket_form.submit();
}
document.getElementById('build').onchange = function() {
    if (build_housing) {
        document.getElementById('build_housing').disabled=false;
    }
    new_ticket_form.submit();
}
if (build_housing) {
    document.getElementById('build_housing').onchange = function() {
        if (par) {
            document.getElementById('par').disabled=false;
        }
        new_ticket_form.submit();
    }
}
if (par)
    document.getElementById('par').onchange = function() {
        document.getElementById('type').disabled=false;
        new_ticket_form.submit();
    }
}
