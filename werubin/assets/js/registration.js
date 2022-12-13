// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            }, false)
        })
})()

function comparePasswords() {
    if ($("#password").val() != $("#confirmPassword").val()) {
        $("#confirmPassword")[0].setCustomValidity("Passwords must match")
    } else {
        $("#confirmPassword")[0].setCustomValidity("")
    }
}

function userNameKeyPressed() {
    var un = $("#validationCustomUsername").val()
    let url = "{% url 'users:api:user_exists' %}"

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
