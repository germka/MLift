window.onload=function() {

str = document.getElementById('str')
build = document.getElementById('build')
build_housing = document.getElementById('build_housing')
par = document.getElementById('par')
type = document.getElementById('type')
date_checker = document.getElementById('date_checker')
ticket_date = document.getElementById('ticket_date')
ticket_content = document.getElementById('ticket_content')
fur = document.getElementById('fur')
fur_block = document.getElementById('fur_block')

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
            if (type) {
                type.disabled=true;
            };
        };
        if (build_housing.value == '') {
            if (type) {
                type.disabled=true;
            };
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
        if (type) {
            if (par.value != '') {
                type.disabled=false;
            } else {
                type.disabled=true;
            };
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
    if (fur_block) {
        fur_block.hidden = true;
    };
};
form_init();

//functions
/*str.onchange = */function field_change() {
    var $form = $( "#new_ticket_form" ),
    url = $form.attr( "action" ),
    token = $form.find( "input[name='csrfmiddlewaretoken']" ).val(),
    post_data = { csrfmiddlewaretoken: token, };

    if (str.value != '') {
        new_str = $form.find( "input[name='obj_str']" ).val();
        post_data['obj_str'] = new_str;
    };
    if (build.value != '') {
        build = $form.find( "input[name='obj_build']" ).val();
        post_data['obj_build'] = new_build;
    };
    if (build_housing) {
        if (build_housing.value != '') {
            new_buildhousing = $form.find( "input[name='obj_buildhousing']" ).val();
            post_data['obj_buildhousing'] = new_buildhousing;
        };
    };
    if (par) {
        if (par.value != '') {
            new_par = $form.find( "input[name='obj_par']" ).val();
            post_data['obj_par'] = new_par;
        };
    };
    if (type.value != '') {
        new_type = $form.find( "input[name='obj_type']" ).val();
        post_data['obj_type'] = new_type;
    };
    if (ticket_content.value != '') {
        new_content = $form.find( "input[name='ticket_content_']" ).val();
        post_data['ticket_content'] = new_content;
    };
    if (ticket_date.value != '') {
        new_date = $form.find( "input[name='ticket_date']" ).val();
        post_data['ticket'] = new_date;
    };

    var posting = $.post( url, post_data );

    posting.done(function( data ) {
        var content = $( data ).find( "#new_ticket_form" );
        
        $( "#new_ticket_form" ).empty().append( content );
    });
};

//str
str.onchange = function() {
    build.disabled=false;
    new_ticket_form.submit();
};
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
    if (type) {
        type.value = '';
        type.disabled=true;
    };
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
    if (type) {
        type.value = '';
        type.disabled=true;
    };
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
        if (type) {
            type.value = '';
            type.disabled=true;
        };
    };
};

//par
if (par) {
    par.onchange = function() {
        if (type) {
            type.disabled=false;
        };
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
        if (type) {
            type.value = '';
            type.disabled=true;
        };
    };
};

if (type) {
    type.onclick = function() {
        if (type.value) {
            type.placeholder=type.value;
        } else {
            type.placeholder="Тип лифта"
        };
        type.value = '';
    };
};

date_checker.onchange = function() {
    if (date_checker.checked == false) {
        ticket_date.disabled=true;
    } else {
        ticket_date.disabled=false;
    };
};

fur.onclick = function () {
    if (fur_block) {
        fur_block.hidden = !fur_block.hidden;
    };
};

};