function getCurrentIndex(imageArray){
    /*
    Returns the index of the current image in the imageArray
    This is used to know which image to show when the user clicks on the next/prev buttons
    */
    const currentimage = $('#modal-img').attr('src')
    var current_index = 0
    for (var i=0; i<imageArray.length; i++){
        if(imageArray[i].image == currentimage){
            current_index = i
        }
    }
    return current_index
}

function switchImages(imageArray, go_next){
    /**
     * Displays the next or previous image depending on the go_next boolean
     */
    let current_index = getCurrentIndex(imageArray)
    if (go_next){
        current_index += 1
        if (current_index >= imageArray.length)
            current_index = 0
    }
    else{
        current_index -= 1
        if (current_index < 0)
            current_index = imageArray.length - 1
    }
    $('#modal-img').attr('src', imageArray[current_index].image);
}

function openImages({albumId, postId, title, imageArray, imageurl, postIds}){
    /**
     * opens the image modal and sets all the bindings to the buttons
     */
    $("#image-modal-title").html(title)
    $("#image-modal").modal("show");
    $("#prev-img").unbind().click(function(e){switchImages(imageArray, false)})
    $("#next-img").unbind().click(function(e){switchImages(imageArray, true)})

    if (!albumId) { // no albumid means it's the post image viewer
        $("#delete-image-button").unbind().click(function(e){deleteImageFromPost({imageArray, postId})})
    } else { // albumid means it's the album image viewer
        $("#delete-image-button").unbind().click(function(e){removePostFromAlbum({albumId, imageArray, postIds})})
    }

    // keyboard navigation for the image modal
    $(`#image-modal`).keyup(function(event) {
        if (event.keyCode === 37) {  //left arrow
            $(`#prev-img`).click();
        } else if(event.keyCode === 39){
            $(`#next-img`).click();
        }
    });

    $(`#image-modal-body`).html(
        `<img id="modal-img" width=100% src=${imageurl}>`
    )
}

function remove_post_from_album({albumId, imageArray, postIds}) {
    /*
        Removes the post from the album
        by sending a PUT request to the server
    */
    let current_index = getCurrentIndex(imageArray)

    if (imageArray[current_index] == noAlbumPictureUrl) {
        return
    }

    let postId = postIds[current_index]

    $.ajax({
        url: "/travels/api/post/remove-post-from-album/",
        type: 'PUT',
        data:{
            'postId': postId,
            'albumId': albumId
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function () {
            closeModal('image-modal')
        }
    })
}

function deleteImageFromPost({ imageArray, postId }) {
    /**
     * function called when the delete button is pressed on the imageModal showing a post
     */

    //image array from post image viewer has pic id but not the album one
    let current_index = getCurrentIndex(imageArray)

    $.ajax({
        url: "/travels/api/post/remove-image-from-post/",
        type: 'PUT',
        data:{
            'postId': postId,
            'imageId': imageArray[current_index].id
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function () {
            closeModal('image-modal')
            $(`#postimg${imageArray[current_index].id}`).remove()
            imageArray.splice(current_index, 1);
        }
    })
}