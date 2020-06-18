var Form = {

    init: function() {
        var
        manage_comp = $('#managecomp')
        str = $('#str'),
        build = $('#build'),
        build_housing = $('#build_housing'),
        par = $('#par'),
        type = $('#type'),
        date_checker = $('#date_checker'),
        date_start_checker = $('#date_start_checker'),
        date_end_checker = $('#date_end_checker'),
        status_start_checker = $('#status_start_checker'),
        status_end_checker = $('#status_end_checker'),
        ticket_date = $('#ticket_date'),
        ticket_content = $('#ticket_content'),
        fur = $('#fur'),
        fur_block = $('#fur_block');

        if (str.val() != '') {
            build.prop("disabled",false); 
        } else {
            build.prop("disabled",true);
        };

        if (build.is("input")) {
            if (type.is("input")) {
                if (build.val() != '') {
                    type.prop("disabled",false);
                } else {
                    type.prop("disabled",true);
                    type.val('');
                };
            };
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
        if (date_start_checker.prop("checked") == false) {
            $("#ticket_date_start").prop("disabled",true);
        };
        if (date_end_checker.prop("checked") == false) {
            $("#ticket_date_end").prop("disabled",true);
        };
        if (status_start_checker.prop("checked") == false) {
            $("#status_date_start").prop("disabled",true);
        };
        if (status_end_checker.prop("checked") == false) {
            $("#status_date_end").prop("disabled",true);
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
        par = $('#par'),
        type = $('#type'),
        ticket_type = $('#tickettype'),
        manage_comp = $('#managecomp'),
        date_start_checker = $('#date_start_checker'),
        date_end_checker = $('#date_end_checker'),
        ticket_date_start = $('#ticket_date_start'),
        ticket_date_end = $('#ticket_date_end'),
        sender = $('#ticket_sender'),
        decline = $('#declineact');

        if (manage_comp.is("input")) {
            if (manage_comp.val() != '') {
                post_data['manage_comp'] = manage_comp.val();
            };
        };
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
        if (date_start_checker.prop("checked")) {
            if (ticket_date_start.is("input")) {
                if (ticket_date_start.val()!='') {
                    new_date_start = $form.find( "input[name='ticket_date_start']" ).val();
                    post_data['ticket_date_start'] = new_date_start;
                };
            };
        };
        if (date_end_checker.prop("checked")) {
            if (ticket_date_end.is("input")) {
                if (ticket_date_end.val()!='') {
                    new_date_end = $form.find( "input[name='ticket_date_end']" ).val();
                    post_data['ticket_date_end'] = new_date_end;
                };
            };
        };
        if (type.val()!='') {
            new_type = $form.find( "input[name='obj_type']" ).val();
            post_data['obj_type'] = new_type;
        };
        if ($("#ticket_content").prop('placeholder') != "Текст заявки") {
            new_content_placeholder = $form.find( "textarea[name='ticket_content']" ).prop('placeholder');
            post_data['ticket_content_placeholder'] = new_content_placeholder;
        };
        if ($("#ticket_content").val() != '') {
            new_content = $form.find( "textarea[name='ticket_content']" ).val();
            post_data['ticket_content'] = new_content;
        };
        if ($("#ticket_date").val() != '') {
            new_date = $form.find( "input[name='ticket_date']" ).val();
            post_data['ticket'] = new_date;
        };
        if (ticket_type.val() != '') {
            new_ticket_type = $form.find( "input[name='ticket_type']" ).val();
            post_data['ticket_type'] = new_ticket_type;
        };
        if (sender.val() != '') {
            new_sender = $form.find( "input[name='ticket_sender']" ).val();
            post_data['ticket_sender'] = new_sender;
        };
        if (decline.prop("checked")) {
            post_data['declineact'] = "on";
        };

        post_data['sender'] = "jQuery";

        var posting = $.post( url, post_data );

        posting.done(function( data ) {
            var content = $( data ).find( "#new_ticket_form" );
            $( "#new_ticket_form" ).empty().append( content );
        });
    }, 

    field_clear: function (input_name) {

        if ($("#type").is("input")) {
            $("#type").prop("disabled",true);
            $("#type").val('');
        };

        if (input_name == "comp") {
            if ($("#managecomp").val != '') {
                $("#managecomp").prop("placeholder",$("#managecomp").val());
                $("#managecomp").val('');
            } else {
                $("#managecomp").prop("placeholder","Владелец");
            };
        };

        if (input_name == "area") {
            if ($("#area_list").val != '') {
                $("#area_list").prop("placeholder",$("#area_list").val());
                $("#area_list").val('');
            } else {
                $("#area_list").prop("placeholder","Район");
            };
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
    $("#managecomp").change(function() {
        Form.field_clear("str");
        Form.field_change();
    });
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
    $("#date_checker").on('change', function() {
        if ($("#date_checker").prop("checked")) {
            $("#ticket_date").prop("disabled",false);
        } else {
            $("#ticket_date").prop("disabled",true);
        };
    });
    $("#date_start_checker").on('change', function() {
        if ($("#date_start_checker").prop("checked")) {
            $("#ticket_date_start").prop("disabled",false);
            $("#ticket_date_start").val( $("#date_now").val() );
        } else {
            $("#ticket_date_start").prop("disabled",true);
        };
    });
    $("#date_end_checker").on('change', function() {
        if ($("#date_end_checker").prop("checked")) {
            $("#ticket_date_end").prop("disabled",false);
        } else {
            $("#ticket_date_end").prop("disabled",true);
        };
    });

///CLICK
    $("#managecomp").on('click', function() {
        Form.field_clear("comp");
    })
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
    $("#ticket_content").on('click', function() {
        if ($("#ticket_content").val() == '') {
            if ($("#ticket_content").prop('placeholder') != "Текст заявки") {
                $("#ticket_content").val( $("#ticket_content").prop('placeholder') );
            };
        };
    });

});

$(window).on('load',function() {

    Form.init();

///CHANGE
    $("#managecomp").change(function() {
        Form.field_clear("str");
        Form.field_change();
    });
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
    $("#date_checker").on('change', function() {
        if ($("#date_checker").prop("checked")) {
            $("#ticket_date").prop("disabled",false);
        } else {
            $("#ticket_date").prop("disabled",true);
        };
    });
    $("#date_start_checker").on('change', function() {
        if ($("#date_start_checker").prop("checked")) {
            $("#ticket_date_start").prop("disabled",false);
            old_date = $("#ticket_date_start").val();
            $("#ticket_date_start").val( $("#date_now").val() );
        } else {
            $("#ticket_date_start").prop("disabled",true);
            $("#ticket_date_start").val(old_date);
        };
    });
    $("#date_end_checker").on('change', function() {
        if ($("#date_end_checker").prop("checked")) {
            $("#ticket_date_end").prop("disabled",false);
        } else {
            $("#ticket_date_end").prop("disabled",true);
        };
    });
    $("#status_start_checker").on('change', function() {
        if ($("#status_start_checker").prop("checked")) {
            $("#status_date_start").prop("disabled",false);
        } else {
            $("#status_date_start").prop("disabled",true);
        };
    });
    $("#status_end_checker").on('change', function() {
        if ($("#status_end_checker").prop("checked")) {
            $("#status_date_end").prop("disabled",false);
        } else {
            $("#status_date_end").prop("disabled",true);
        };
    });

///CLICK
    $("#managecomp").on('click', function() {
        Form.field_clear("comp");
    })
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
    $("#ticket_content").on('click', function() {
        if ($("#ticket_content").val() == '') {
            if ($("#ticket_content").prop('placeholder') != "Текст заявки") {
                $("#ticket_content").val( $("#ticket_content").prop('placeholder') );
            };
        };
    });
    $('#area_list').on('click', function() {
        Form.field_clear("area");
    });
});
