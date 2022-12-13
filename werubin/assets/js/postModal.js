function closePostModal(){
    $("#post-modal").modal('hide');
}

function openPostModal() {
    $("#post-modal").modal('show');
}

function closeModal(id){
    $(`#${id}`).modal('hide')
}

$("#postForm").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var data = new FormData(this)
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        headers:
        {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data)
        {
            closePostModal();
            add_post(data, false);
        }
    });

});