var flip = document.getElementById("comment_form_show"),
    form = document.getElementById("new_comment_form");

flip.onclick = function () {
    if (form) {
        form.hidden = false;
        flip.hidden = true;
    }
};