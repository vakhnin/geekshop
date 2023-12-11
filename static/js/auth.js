$(document).ready(function () {
    "use strict";

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $("#login-modal, #registration-modal").on('hide.bs.modal', function () {
       $(".error-div").text("");
    });

    $("#login-modal, #registration-modal").on('shown.bs.modal', function () {
       $(".error-div").text("");
    });

    $('#login').on('click', () => {
    $.ajax(
        {
            method: "POST",
            headers: {"X-CSRFToken": csrftoken},
            mode: "same-origin",
            url: "/auth/login/",
            data: {
                username: $("#username").val(),
                password:  $("#password").val()
                },
            success: (data) => {
                if ( data.error ) {
                    $(".error-div").text(data.error);
                } else {
                    const searchString = new URLSearchParams(window.location.search);
                    const redirect_to = searchString.get('redirect_to');
                    if ( redirect_to ) {
                        window.location.replace(redirect_to);
                    }

                    $("#navbar").html(data.content);
                    $("#login-modal").modal('hide');
                }
            },
        });
    });

    $('#registration').on('click', () => {
    $.ajax(
        {
            method: "POST",
            headers: {"X-CSRFToken": csrftoken},
            mode: "same-origin",
            url: "/auth/register/",
            data: {
                first_name: $("#first_name").val(),
                last_name: $("#last_name").val(),
                username: $("#username-reg").val(),
                email: $("#email").val(),
                password1:  $("#password1").val(),
                password2:  $("#password2").val()
                },
            success: (data) => {
                if ( data.error ) {
                    $(".error-div").text(data.error);
                } else {
                    const searchString = new URLSearchParams(window.location.search);
                    const redirect_to = searchString.get('redirect_to');
                    if ( redirect_to ) {
                        window.location.replace(redirect_to);
                    }

                    $("#navbar").html(data.content);
                    $("#registration-modal").modal('hide');
                }
            },
        });
    });
});
