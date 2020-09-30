window.onload = function () {
    var
    main = document.getElementById("main"),
    marker = document.getElementById("marker"),
    filters = document.getElementById("str_filter"),
    block = document.getElementById("filters"),
    filters_menu = document.getElementById("filters_menu"),
    translate = [];
    //alignment for menu decorator
    if (main && marker) {
        var offset = 0;
        marker.style.left = ((main.firstElementChild.offsetWidth - marker.offsetWidth) / 2) + "px";
        for (var i = 0; i < (main.childElementCount - 1); i++) {
            offset = main.children[i].offsetLeft - ((marker.offsetWidth - main.children[i].offsetWidth) / 2);
            if (i == 0) {
                var start_offset = offset;
                document.styleSheets[(document.styleSheets.length-1)].insertRule("#marker { left:" + offset.toString() + "px !important; }", document.styleSheets[(document.styleSheets.length-1)].cssRules.length);
                translate[i] = "#main li:nth-child(" + (i+1).toString()  + "):hover ~ #marker { transform: translate( 0, 0); }";
            } else {
                translate[i] = "#main li:nth-child(" + (i+1).toString()  + "):hover ~ #marker { transform: translate( " + (offset - start_offset).toString() + "px, 0); }";
            }
            document.styleSheets[(document.styleSheets.length-1)].insertRule(translate[i], document.styleSheets[(document.styleSheets.length-1)].cssRules.length);
        };

    }

    if (filters) { //Filer menu visiblity
        block_div = block.children.item(HTMLDivElement);
        filters.onclick = function() {
            block.style.visibility = "visible"
        };
        filters.onchange = function() {
            document.location.href = "http://base.masterlift.pro/tickets/str/" + filters.value;
        };
    };

};

//Comments block hide/show
var flip = document.getElementById("comment_form_show"),
form = document.getElementById("new_comment_form");

if (flip) {
    flip.onclick = function () {
        if (form) {
            form.hidden = false;
            flip.hidden = true;
        };
    };
};
