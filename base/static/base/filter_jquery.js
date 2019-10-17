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
        post_data = { csrfmiddlewaretoken: token, }
        build_housing = $('#build_housing'),
        par = $('#par');
        type = $('#type');

        if ($("#str").val() != '') {
            new_str = $form.find( "input[name='obj_str']" ).val();
            post_data['obj_str'] = new_str;
        };
        if ($("#build").val() != '') {
            new_build = $form.find( "input[name='obj_build']" ).val();
            post_data['obj_build'] = new_build;
        };
        if (build_housing.is("input")) {
            if (build_housing.val() != '') {
                new_buildhousing = $form.find( "input[name='obj_buildhousing']" ).val();
                post_data['obj_buildhousing'] = new_buildhousing;
            };
        };
        if (par.is("input")) {
            if (par.val()!='') {
                new_par = $form.find( "input[name='obj_par']" ).val();
                post_data['obj_par'] = new_par;
            };
        };
        if (type.val()!='') {
            new_type = $form.find( "input[name='obj_type']" ).val();
            post_data['obj_type'] = new_type;
        };
        if ($("#ticket_content").val() != '') {
            new_content = $form.find( "textarea[name='ticket_content']" ).val();
            post_data['ticket_content'] = new_content;
        };
        if ($("#ticket_date").val() != '') {
            new_date = $form.find( "input[name='ticket_date']" ).val();
            post_data['ticket'] = new_date;
        };

        var posting = $.post( url, post_data );

        posting.done(function( data ) {
            var content = $( data ).find( "#new_ticket_form" );
            $( "#new_ticket_form" ).empty();
            content.appendTo( "#new_ticket_form" );
        });
    }, 

    field_clear: function (input_name) {

        if ($("#type").is("input")) {
            $("#type").prop("disabled",true);
            $("#type").val('');
        };

        if (input_name == "build" || input_name == "str" || input_name == "build_housing" || input_name == "par") {
            if ($("#par").val()!='') {
                $("#par").prop("placeholder",$("#par").val());
                $("#par").val('');
            } else {
                $("#par").prop("placeholder","Парадная");
            };
        };

        if (input_name == "build" || input_name == "str" || input_name == "build_housing") {
            if ($("#build_housing").val()!='') {
                $("#build_housing").prop("placeholder",$("#build_housing").val());
                $("#build_housing").val('');
            } else {
                $("#build_housing").prop("placeholder","Корпус");
            };

            if ($("#par").is("input")) {
                $("#par").prop("placeholder","Парадная");
                $("#par").prop("disabled",true);
                $("#par").val('');
            };
        };

        if (input_name == "build" || input_name == "str") {
            if ($("#build").val()!='') {
                $("#build").prop("placeholder",$("#build").val());
                $("#build").val('');
            } else {
                $("#build").prop("placeholder","Дом");
            };

            if ($("#build_housing").is("input")) {
                $("#build_housing").prop("placeholder","Корпус");
                $("#build_housing").prop("disabled",true);
                $("#build_housing").val('');
            };
            if ($("#par").is("input")) {
                $("#par").prop("placeholder","Парадная");
                $("#par").prop("disabled",true);
                $("#par").val('');
            };
        };

        if (input_name == "str") {
            if ($("#str").val()!='') {
                $("#str").prop("placeholder",$("#str").val());
                $("#str").val('');
            } else {
                $("#str").prop("placeholder","Улица");
            };

            $("#build").prop("placeholder","Дом");
            $("#build").prop("disabled",true);
            $("#build").val('');
        };
    }
};

$( document ).ajaxStop(function() {
    Form.init();

///CHANGE
    $("#str").change(function() {
        Form.field_change();
    });
    $("#build").change(function() {
        Form.field_change();
    });
    $("#build_housing").change(function() { 
        Form.field_change();
    });
    $("#par").change(function() { 
        Form.field_change();
    });
///CLICK
    $("#str").on('click', function() {
        Form.field_clear("str");
    });
    $("#build").on('click', function() {
        Form.field_clear("build");
    });
    $("#build_housing").on('click', function() {
        Form.field_clear("build_housing");
    });
    $("#par").on('click', function() {
        Form.field_clear("par");
    });
});

///CHANGE
$("#str").change(function() {
    Form.field_change();
});
$("#build").change(function() {
    Form.field_change();
});
$("#build_housing").change(function() { 
    Form.field_change();
});
$("#par").change(function() { 
    Form.field_change();
});
///CLICK
$("#str").on('click', function() {
    Form.field_clear("str");
});
$("#build").on('click', function() {
    Form.field_clear("build");
});
$("#build_housing").on('click', function() {
    Form.field_clear("build_housing");
});
$("#par").on('click', function() {
    Form.field_clear("par");
});

$(window).on('load',function() {

    Form.init();

    $("#date_checker").on('change', function() {
        if (date_checker.checked == false) {
            ticket_date.disabled=true;
        } else {
            ticket_date.disabled=false;
        };
    });

    $("#fur").on('click', function () {
        if (fur_block) {
            fur_block.hidden = !fur_block.hidden;
        };
    });
});
