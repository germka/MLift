$(window).on('load', function() {
    links = $('.reason_group_link');
    links.each(function(index) {
        $(this).on('click', function() {
            list_item = $('#reason_list_'+(index+1));
            list_item.prop('hidden', !list_item.prop('hidden'));
        });
    });
});