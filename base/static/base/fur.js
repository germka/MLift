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
                $("#ticket_content").val(reason.text());
            });
        });
    });
});