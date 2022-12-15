//{% load static %}

function closeAddToAlbumModal(){
    $("#add-to-album-modal").modal('hide');
}

async function openAddToAlbumModal() {
    $("#add-to-album-modal").modal('show');

    let albumsArray = await $.ajax({
        url: '/travels/api/post/get-albums/',
        type: 'GET',
        data:{
            'user-id': userId
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        // success: function(data){
        //     console.log(data)
        //     //$(`#${divpostid}`).fadeOut(400, function(){$(`#${postid}`).remove()})
        // }
    })

    let albumHtml = `<div class="col-4 p-1">{% include "album.html" %}</div>`
    for (let i = 0; i < albumsArray.length; i++) {
        let pic = (albumsArray[i].posts.length == 0 || albumsArray[i].posts[0].images.length == 0) ? noAlbumPictureUrl : albumsArray[i].posts[0].images[0].image
        let newId = "albumRow" + Math.floor(i/3)
        if (i % 3 == 0) {
            $("#albumRow").attr("id", newId)
            $("#add-to-album-modal-body").append(`</div><div id="albumRow" class="row">`)
        }
        let containerId = "albumContainer" + i
        $("#albumRow").append(albumHtml)
        $("#albumContainer").attr("id", containerId)
        $(`#${containerId} img`).attr("src", pic)
        $(`#${containerId} div`).html(albumsArray[i].name)
        $(`#${containerId}`).prop('onclick',null).off('click')
        $(`#${containerId}`).click(function() {
            console.log("album appended")
        })
    }
    // if length = 0
}
