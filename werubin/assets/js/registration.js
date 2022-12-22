function comparePasswords() {
    /**
     * compares the 2 passwords for the 2 input fields
     */
    if ($("#password").val() != $("#confirmPassword").val()) {
        $("#confirmPassword")[0].setCustomValidity("Passwords must match")
    } else {
        $("#confirmPassword")[0].setCustomValidity("")
    }
}

function userNameKeyPressed() {
    /**
     * check if the username is available each time a keyup event is fired
     */
    var un = $("#validationCustomUsername").val()
    let url = "/users/api/user_exists/"

    $.ajax({
        url: url,
        type: 'PUT',
        data: {
            "username": un
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        // username IS found => not ok
        success: function (data) {
            if (data["user_exists"]) {
                $("#validationCustomUsername")[0].setCustomValidity("Username already taken")
            } else {
                $("#validationCustomUsername")[0].setCustomValidity("")
            }
        }
    })
}

function emailKeyPressed() {
    /**
     * check if the email is available each time a keyup event is fired
     */
    var un = $("#validationCustomEmail").val()
    let url = "/users/api/email_exists/"

    $.ajax({
        url: url,
        type: 'PUT',
        data: {
            "email": un
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        // username IS found => not ok
        success: function (data) {
            if (data["email_exists"]) {
                $("#validationCustomEmail")[0].setCustomValidity("Email already taken")
                $("#emailAlreadyTaken").html("Email is already taken")
            } else {
                $("#validationCustomEmail")[0].setCustomValidity("")
                $("#emailAlreadyTaken").html("")
            }
        }
    })
}

