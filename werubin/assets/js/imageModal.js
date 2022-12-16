function getCurrentIndex(imageArray){
    const currentimage = $('#modal-img').attr('src')
    var current_index = 0
    for (var i=0; i<imageArray.length; i++){
        if(imageArray[i].image == currentimage){
            current_index = i
        }
    }
    return current_index
}

function switch_image(imageArray, go_next){
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

function open_images({albumId, postId, title, imageArray, imageurl, postIds}){
    $("#image-modal-title").html(title)
    $("#image-modal").modal("show");
    $("#prev-img").unbind().click(function(e){switch_image(imageArray, false)})
    $("#next-img").unbind().click(function(e){switch_image(imageArray, true)})
    
    if (!albumId) { // no albumid means it's the post image viewer
        $("#delete-image-button").unbind().click(function(e){delete_image_from_post({imageArray, postId})})
    } else { // albumid means it's the album image viewer
        $("#delete-image-button").unbind().click(function(e){remove_post_from_album({albumId, imageArray, postIds})})
    }

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

function delete_image_from_post({ imageArray, postId }) {
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
            $.getJSON({
                url: `/travels/api/post/get/${postId}`,
                success: function (data) {
                    images_html = ""
                    for (var image of data.images){
                        images_html += `<img class='post-img' id="postimg${image.id}" src=${image.image}>`
                    }
                    $(`#${postId}postDiv .post-image-div`).html(images_html)
                }})
            
        }
    })
}