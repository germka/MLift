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

    /*document.onmouseover = function() {
        block.style.transform = "translate(0, -100%)";
        block_div.style.transform = "translate(0, -100%)";
    };
    filters.onmouseover = function() {
        block.style.transform = "translate(0, 0%)";
        block_div.style.transform = "translate(0, 0%)";
    };
    filters_menu.onmouseover = function() {
        block.style.transform = "translate(0, 0%)";
        block_div.style.transform = "translate(0, 0%)";
    };
    filters.list.onmouseleave = function() {
        block.style.transform = "translate(0, -100%)";
        block_div.style.transform = "translate(0, -100%)";
    }*/

    var //Close ticket button position
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
