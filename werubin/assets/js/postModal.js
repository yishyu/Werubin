function closePostModal(){
    closeModal("post-modal")
}

function openPostModal() {
    $("#postForm").attr("method", "POST")
    $("#postForm").attr("action", "/travels/api/post/add/")
    $("#post-modal-title").html("Post your trip !")
    $("#post-id").val("")
    openModal("post-modal")
}

function openModal(id){
    $(`#${id}`).modal('show')
}

function closeModal(id){
    $(`#${id}`).modal('hide')
}

function openUpdateModal(post){
    // Prefill Modal

    // Post-id
    $("#post-id").val(post.id)

    // Title
    $("#post-modal-title").html("Edit Your Trip !")

    // Location
    if (post.location.lat != ""){
        $("#lat").val(post.location.lat)
        $("#lng").val(post.location.lng)
        $("#googleAutocomplete").val(post.location.name)
    }else{
        $("#lat").val("")
        $("#lng").val("")
        $("#googleAutocomplete").val("")
    }
    // Content
    $("#postContent").val(post.content)
    // Tags
    $("#postTag0").val(post.tags[0].name)
    for (var i=1; i < post.tags.length; i++){
        var tagId = addNewTagField()
        $(`#${tagId}`).val(post.tags[i].name)
    }
    // Api
    $("#postForm").attr("method", "PUT")
    $("#postForm").attr("action", "/travels/api/post/update/")

    // open Modal
    openModal("post-modal")


}

$('#post-modal').on('hidden.bs.modal', function () {
    $("#locate-me").prop('disabled', false);
    $("#postModalErrors").empty()
    $(".form-control").val("")
    reset_tags()
});

$("#postForm").unbind().submit(function(e) {

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
        success: function(post)
        {
            if (typeof data.get('post-id') !== 'undefined'){
                $(`#${data.get('post-id')}postDiv`).remove()
            }
            closePostModal();
            add_post(post, false);

        },
        error: function (xhr, ajaxOptions, thrownError) {
            let text = ''
            for (var missing_key of xhr.responseJSON["Missing Keys"]){
                text += `${missing_key} <br>`
            }
            if (text != '')
                text = "Missing Information: " + text

            for (var other_problems of xhr.responseJSON["Others"]){
                text += `${other_problems} <br>`
            }
            $("#postModalErrors").html(text)

          }
    });

});