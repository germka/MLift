$(window).on('load',function() {
    $("#fur").on('click', function () {
        if ($("#fur_block").is("div")) {
            $("#fur_block").prop("hidden", !$("#fur_block").prop("hidden"));
        };
    });

    $('.reason_list').each(function() {
        list = $(this);
        list.children().each(function() {
            $(this).on('click', function() {
                reason = $(this);
                if ($("#ticket_content").val().length <= 1) {
                    $("#ticket_content").empty();
                    $("#ticket_content").append(reason.text());
                } else {
                    $("#ticket_content").append(reason.text());
                };
            });
        });
    });
    $('#FUReason').change( function() {
        if ($("#ticket_content").val().length <= 1) {
            $("#ticket_content").empty();
            $("#ticket_content").append($('#FUReason').val());
        } else {
            $("#ticket_content").append($('#FUReason').val());
        };
    });
});