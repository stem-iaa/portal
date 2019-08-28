var original_edit_button_text;

var quill;

$(document).ready(function () {
    original_edit_button_text = $("#edit_button").text();

    quill = new Quill('#content', {
        theme: 'snow'
    });
    quill.enable(false);
    $(".ql-toolbar").hide();
});

var editing = false;
var editables = {};

$("#edit_button").on("click", function () {
    console.log("click");
    if (editing) {
        var editable_content = {};
        for (var id in editables) {
            editable_content[id] = $("#" + id + " textarea").val();
        }

        editable_content["portfolio"] = $(".ql-editor").html();

        $.ajax({
            url: "/profile/" + profile_user + "/update",
            type: "post",
            dataType: "json",
            data: editable_content,
            success: function (data) {
                if (!data.error) {
                    location.reload();
                }
            }
        });
    } else {
        $(".editable").each(function () {
            editables[this.id] = this;
            let current_html = $(this).html();
            $(this).html("<textarea style='width: 100%;'>" + current_html + "</textarea>");
            let textarea = $("#" + this.id + " textarea")[0];
            textarea.style.height = textarea.scrollHeight + 5 + "px";
        });

        quill.enable(true);
        $(".ql-toolbar").show();

        editing = true;
        $("#edit_button").text("Save");
    }
});

$("#upload-picture-button").on("click", function () {
    $("#upload-picture-input").click();
});

$("#upload-picture-input").on("change", function () {
    if ($("#upload-picture-input").get(0).files.length != 0) {
        $("#upload-picture-form").submit();
    }
});


