window.onload=function() {

str = document.getElementById('str')
build = document.getElementById('build')
build_housing = document.getElementById('build_housing')
par = document.getElementById('par')
type = document.getElementById('type')
date_checker = document.getElementById('date_checker')
ticket_date = document.getElementById('ticket_date')

//disabling all forms except obj_str
function form_init() {
    if (str.value != '') {
        build.disabled=false; 
    } else {
        build.disabled=true;
    };

    if (build_housing) {
        if (build.value != '') {
            build_housing.disabled=false; 
        } else {
            build_housing.disabled=true;
            type.disabled=true;
        }
        if (build_housing.value == '') {
            type.disabled=true;
        };
    };

    if (build_housing && par) {
        if (build_housing.value != '') {
            par.disabled=false;
        } else {
            par.disabled=true;
        };
    };

    if (par) {
        if (par.value != '') {
            type.disabled=false;
        } else {
            type.disabled=true;
        };
        if (build.value == '') {
            if (!build_housing) {
                par.disabled = true;
            };
        };
    };

    if (date_checker.checked == false) {
        ticket_date.disabled=true;
    };
};
form_init();

//functions
function field_change() {
    var $form = $( "#new_ticket_form" ),
        str = $form.find( "input[name='obj_str']" ).val(),
        build = $form.find( "input[name='obj_build']" ).val(),
        build_housing = $form.find( "input[name='obj_buildhousing']" ).val(),
        par = $form.find( "input[name='obj_par']" ).val(),
        type = $form.find( "input[name='obj_type']" ).val(),
        content = $form.find( "input[name='ticket_content_']" ).val(),
        date = $form.find( "input[name='ticket_date']" ).val(),
        token = $form.find( "input[name='csrfmiddlewaretoken']" ).val(),
        url = $form.attr( "action" );
    var posting = $.post( url, { csrfmiddlewaretoken: token, obj_str: obj_str, ticket_content: "", } );

    posting.done(function( data ) {
        var content = $( data ).find( "#new_ticket_form" );
        $( "#new_ticket_form" ).empty().append( content );
    });
};

//str
str.onchange = function() {
    build.disabled=false;
    new_ticket_form.submit();
}
str.onclick = function() {
    if (str.value) {
        str.placeholder=str.value;
    } else {
        str.placeholder="Улица"
        build.placeholder="Дом"
        if (build_housing) {
            build_housing.placeholder="Корпус"
        };
        if (par) {
            par.placeholder="Парадная"
        };
    };
    str.value = '';
    build.value = '';
    build.disabled=true;
    if (build_housing) {
        build_housing.value = ''; 
        build_housing.disabled=true;
    };
    if (par) {
        par.value = '';
        par.disabled=true;
    };
    type.value = '';
    type.disabled=true;
};
//build
build.onchange = function() {
    if (build_housing) {
        build_housing.disabled=false;
    };
    new_ticket_form.submit();
};
build.onclick = function() {
    if (build.value) {
        build.placeholder=build.value;
    } else {
        build.placeholder="Дом"
        if (build_housing) {
            build_housing.placeholder="Корпус"
        };
        if (par) {
            par.placeholder="Парадная"
        };
    };
    build.value = '';
    if (build_housing) {
        build_housing.value = ''; 
        build_housing.disabled=true;
    };
    if (par) {
        par.value = '';
        par.disabled=true;
    };
    type.value = '';
    type.disabled=true;
}
//housing
if (build_housing) {
    build_housing.onchange = function() {
        if (par) {
            par.disabled=false;
        };
        new_ticket_form.submit();
    };
    build_housing.onclick = function() {
        if (build_housing.value) {
            build_housing.placeholder=build_housing.value;
        } else {
            build_housing.placeholder="Корпус"
            if (par) {
                par.placeholder="Парадная"
            };
        };
        build_housing.value = '';
        if (par) {
            par.value = '';
            par.disabled=true;
        };
        type.value = '';
        type.disabled=true;
    };
};

//par
if (par) {
    par.onchange = function() {
        type.disabled=false;
        new_ticket_form.submit();
    };
    par.onclick = function() {
        if (par.value) {
            par.placeholder=par.value;
        } else {
            par.placeholder="Парадная";
            if (build_housing) {
                build_housing.placeholder="Корпус"
            };
        };
        par.value = '';
        type.value = '';
        type.disabled=true;
    };
};

type.onclick = function() {
    if (type.value) {
        type.placeholder=type.value;
    } else {
        type.placeholder="Тип лифта"
    };
    type.value = '';
};


date_checker.onchange = function() {
    if (date_checker.checked == false) {
        ticket_date.disabled=true;
    } else {
        ticket_date.disabled=false;
    };
};

};