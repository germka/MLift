var flip = document.getElementById("comment_form_show"),
    form = document.getElementById("new_comment_form");

flip.onclick = function () {
    if (form) {
        form.hidden = false;
        flip.hidden = true;
    }
};

window.onload = function () {
    var
    button = document.getElementById("ticket_close_button"),
    table = document.getElementById("index_table"),
    content_row = document.getElementById("ticket_content_row"),
    content_info = document.getElementById("ticket_content_info");

    if (content_row && content_info) {
        content_row.style.minHeight = (content_info.offsetHeight + 8).toString() + 'px';
    };
    if (button && table) {
        button.style.top = (table.offsetHeight - 148 - 160).toString() + 'px';
    };
}