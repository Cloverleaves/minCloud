/* Todo: restructuring */

/* Rename files and folders */
$(".item-input").change(function() {
    data = {
        path: $("#currentdir").val(),
        target: $(this).data("target"),
        name: $(this).val()
    }
    $.ajax({
        type: "POST",
        url: "/rename",
        data: data,
        success: function(data) {
            //todo: popups/notifications?
            //window.location.reload();
        }
    });
});

$('body').on('click', '.action-remove', function() {
    if (confirm("Do you really want to delete this file?")) {
        data = {
            path: $("#currentdir").val(),
            target: $(this).data("target")
        }
        $.ajax({
            type: "POST",
            url: "/delete",
            data: data,
            context: $(this),
            success: function(data) {
                console.log(this);
                $(this).closest(".file").fadeOut();
            }
        });
    }
});

// Auto upload on file select
$('body').on('change', '#upload-input', function() {
    $("#file-upload").submit();
});

$('body').on('focus', '#mkdir-input', function() {
    $("#mkdir-submit").fadeIn();
});

$('body').on('blur', '#mkdir-input', function() {
    $("#mkdir-submit").fadeOut();
});