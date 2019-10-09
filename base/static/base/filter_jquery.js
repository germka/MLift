var Form = {

    init: function() {
        var
        str = $('#str'),
        build = $('#build'),
        build_housing = $('#build_housing'),
        par = $('#par'),
        type = $('#type'),
        date_checker = $('#date_checker'),
        ticket_date = $('#ticket_date'),
        ticket_content = $('#ticket_content'),
        fur = $('#fur'),
        fur_block = $('#fur_block');

    if ( str.val() != '') {
        build.prop("disabled",false); 
    } else {
        build.prop("disabled",true);
    };

    if (build_housing.is("input")) {
        if (build.val() != '') {
            build_housing.prop("disabled",false);
        } else {
            build_housing.prop("disabled",true);
            if (type.is("input")) {
                type.prop("disabled",true);
            };
        };
        if (build_housing.val() == '') {
            if (type.is("input")) {
                type.prop("disabled",true);
            };
        };
    };

    if (build_housing.is("input") && par.is("input")) {
        if (build_housing.val() != '') {
            par.prop("disabled",false);
        } else {
            par.prop("disabled",true);
        };
    };

    if (par.is("input")) {
        if (type.is("input")) {
            if (par.val() != '') {
                type.prop("disabled",false);
            } else {
                type.prop("disabled",true);
            };
        };
        if (build.val() == '') {
            if (!build_housing.is("input")) {
                par.prop("disabled",true);
            };
        };
    };

    if (date_checker.prop("checked") == false) {
        ticket_date.prop("disabled",true);
    };
    if (fur_block.is("input")) {
        fur_block.prop("hidden",true);
    };
},

    field_change: function() {
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
        $( "#new_ticket_form" ).empty();
        content.appendTo( "#new_ticket_form" );
    });
    }
}

$( document ).ajaxStop(function() {
    Form.init();
  });

$( "#str" ).change(function() { 
    Form.field_change(); 
});
$( "#str" ).on("click", function() { 
    var
        str = $('#str'),
        build = $('#build'),
        build_housing = $('#build_housing'),
        par = $('#par'),
        type = $('#type');

    if (str.val()!='') {
        str.prop("placeholder",str.val());
    } else {
        str.prop("placeholder","Улица");
        build.prop("placeholder","Дом");
        if (build_housing.is("input")) {
            build_housing.prop("placeholder","Корпус");
        };
        if (par.is("input")) {
            par.prop("placeholder","Парадная")
        };
    };
    str.val('');
    build.val('');
    build.prop("disabled",true);
    if (build_housing.is("input")) {
        build_housing.val(''); 
        build_housing.prop("disabled","true");
    };
    if (par.is("input")) {
        par.val('');
        par.prop("disabled",true);
    };
    if (type.is("input")) {
        type.val('');
        type.prop("disabled",true);
    };

});

$( "#build" ).change(function() { 
    Form.field_change();
});

$( "#build_housing" ).change(function() { 
    Form.field_change();
});

$( "#par" ).change(function() { 
    Form.field_change();
});

window.onload=function() {

//disabling all forms except obj_str

Form.init();

//functions
//str 
//str.onchange = function() {
//    build.disabled=false;
//    new_ticket_form.submit();
//};
/*str.onclick = function() {
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
};*/

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