$(document).ready(function () {
    "use strict";

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $("#login-modal").on('hide.bs.modal', function () {
       $(".error-div").text("");
    });

    $('#login').on('click', () => {
    $.ajax(
        {
            method: "POST",
            headers: {"X-CSRFToken": csrftoken},
            mode: "same-origin",
            url: "auth/login/",
            data: {
                username: $("#username").val(),
                password:  $("#password").val()
                },
            success: (data) => {
                if ( data.error ) {
                    $(".error-div").text(data.error);
                } else {
                    $("#navbar").html(data.content);
                    $("#login-modal").modal('hide');
                }
            },
        });
    });
});
