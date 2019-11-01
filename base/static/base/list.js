$(window).on('load', function() {
    links = $('.reason_group_link');
    links.each(function(index) {
        $(this).on('click', function() {
            reason = $('#reason_list_'+(index+1))
            reason.prop('hidden', !reason.prop('hidden'))
        })
    })
})