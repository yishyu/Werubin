function closeAlbumModal(){
    $("#album-modal").modal('hide');
}

function openAlbumModal() {
    $("#album-modal").modal('show');
}
$("#publishAlbumButton").unbind().click(async function () {
    /*
        The album button is not "submit" button; this function does the 
        necessary actions instead
    */
    let albumName = $("#albumName").val()
    let response = await $.ajax({
        url: "/travels/api/post/add-album/",
        type: 'POST',
        data:{
            'albumName': albumName
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        }
    })
    if (response.message) { // error message
        $("#albumModalErrors").removeClass()
        $("#albumModalErrors").addClass("alert alert-danger")
        $("#albumModalErrors").html(response.message)
    } else { // success message
        $("#albumModalErrors").removeClass()
        $("#albumModalErrors").addClass("alert alert-success")
        $("#albumModalErrors").html("Album added.")
    }
})