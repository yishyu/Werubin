//{% load static %}

function closeAddToAlbumModal(){
    $("#add-to-album-modal").modal('hide');
    $("#add-to-album-modal-body").html(`<div id="addToAlbumRow" class="row"></div>`);
}

async function openAddToAlbumModal({ postId }) {
    $('#add-to-album-modal').modal({backdrop: 'static', keyboard: false})
    $("#add-to-album-modal").modal('show');

    var albumsArray = await $.ajax({
        url: '/travels/api/post/get-albums/',
        type: 'GET',
        data:{
            'user-id': userId
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        }
    })

    let albumHtml = `<div class="col-4 p-1">{% include "album.html" %}</div>`
    let i = 0;
    for (; i < albumsArray.length; i++) {
        let pic = (albumsArray[i].posts.length == 0 || albumsArray[i].posts[0].images.length == 0) ? noAlbumPictureUrl : albumsArray[i].posts[0].images[0].image
        let rowId = "addToAlbumRow_" + postId
        let newRowId = rowId + "_" + Math.floor(i/3)
        if (i % 3 == 0) {
            $(`#${rowId}`).attr("id", newRowId)
            $("#add-to-album-modal-body").append(`</div><div id="${rowId}" class="row">`)
        }
        let containerId = "albumContainer_"+ postId + "_" + i
        $(`#${rowId}`).append(albumHtml)
        $(`#${rowId} #albumContainer`).attr("id", containerId)
        $(`#${containerId} img`).attr("src", pic)
        $(`#${containerId}`).removeAttr('onclick')
        
        $(`#${containerId} .top-left`).html(albumsArray[i].name)
        
        if (albumsArray[i].posts.filter((x) => x.id == postId).length > 0) {
            $(`#${containerId} img`).addClass("selected")
            $(`#${containerId} .check-mark`).show()
        }
        
        let albumId = albumsArray[i].id

        $(`#${containerId}`).unbind().click(async () => {
            if ($(`#${containerId} img`).hasClass("selected")) {
                if (! await $.ajax({
                    url: "/travels/api/post/remove-post-from-album/",
                    type: 'PUT',
                    data:{
                        'postId': postId,
                        'albumId': albumId
                    },
                    headers: {
                        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                    }
                })) {
                    $(`#${containerId} img`).removeClass("selected")
                    $(`#${containerId} .check-mark`).hide()
                }
            } else {
                if (! await $.ajax({
                    url: "/travels/api/post/add-post-to-album/",
                    type: 'PUT',
                    data:{
                        'postId': postId,
                        'albumId': albumId
                    },
                    headers: {
                        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                    }
                })) {
                    $(`#${containerId} img`).addClass("selected")
                    $(`#${containerId} .check-mark`).show()
                }
            }
        })
    }
    $(`#albumContainer_${postId}`).attr("id", "albumContainer_"+ postId + "_" + (i + 1))

    // if length = 0
}
