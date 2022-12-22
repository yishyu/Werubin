function initMap(post) {
    /*
        Creates a map for a post with the post location marked on the map
        By clicking on the marker, the pre-saved name of the location is shown
    */
    var position = {
        lat: parseFloat(post.location.lat),
        lng: parseFloat(post.location.lng)
    }
    // The map, centered at Lessines
    var map = new google.maps.Map(
        document.getElementById("map"+post.id),
        {
            zoom: 12,
            center: position,
            disableDefaultUI: true,
        }
    );
    var infoWindow = new google.maps.InfoWindow();
    // Create a marker and set its position based on the post location
    var marker = new google.maps.Marker({
        id: post.id,
        position: position,
        title: post.location.name,
        map: map,
    })
    // When the user clicks on the marker, the map zooms in and the info window is shown
    // containing information about the current weather at the location and information about the post
    marker.addListener("click", () => {
        map.setZoom(16)
        map.panTo(marker.getPosition())
        infoWindow.close();
        const weather_id = `postweather${post.location.id}`
        const contentString =`
        Current Weather
        <div id="${weather_id}"></div>
        <h5 id="firstHeading" class="blue-text firstHeading">${marker.getTitle()}</h5>
        `
        infoWindow.setContent(contentString);
        set_weather(position.lat, position.lng, weather_id);
        infoWindow.open(marker.getMap(), marker);
        });
}

function delete_post(postid, divpostid){
    /*
        Deletes a post from the DOM and from the database
        asks for confirmation before deleting
    */
    if (confirm('Are you sure you want to delete this post? This action is not reversible')) {
        $.ajax({
            url: '/travels/api/post/delete/',
            type: 'DELETE',
            data:{
                'post-id': postid
            },
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(data){
                $(`#${divpostid}`).fadeOut(400, function(){$(`#${postid}`).remove()})
            }
        })
    }

}

function addPost(post, append){  // if append is false, we prepend, all new post is prepended and all past posts are appended
    /*
        Adds a post to the DOM

    */

    // get all the values needed to display a post
    var picture  = post.author.profile_picture ? post.author.profile_picture: defaultProfilePictureUrl
    var description = post.shares.id ? `shared post <a id=sharedPostLink${post.id} href="/travels/post/${post.shares.id}">${post.shares.id}</a> from ${post.shares.author.username}`: `was in <b ><u><a class="yellow-text" href="http://maps.google.com/?q=${post.location.name}" target="_blank">${post.location.name}</a></u></b>`
    var tags_html = ""
    for( var tag of post.tags){
        tags_html += `<small><a href="/feed/${tag.name}" class="yellow-link">#${tag.name}</a></small>`
    }
    var location_html = post.location.lat != "" ? `<div class="map" id="map${post.id}"></div>`: ``
    var images_html = ""
    for (var image of post.images){
        images_html += `<img class='post-img col-6 p-1' id="postimg${image.id}" src=${image.image}>`
    }
    images_html = "<div class='row post-image-div'>" + images_html + "</div>"
    var like_text = post.likes.length > 1 ? `${post.likes.length} likes`: `${post.likes.length} like`
    var comment_text = post.comments > 1?  `${post.comments} comments`: `${post.comments} comment`
    var share_text = post.was_shared.length > 1?  `${post.was_shared.length} shares`: `${post.was_shared.length} share`
    var like_color =  post.likes.includes(requestUserId) ? 'blue-text':'yellow-link'
    var share_color =  post.was_shared.includes(requestUserId) ? 'blue-text':'yellow-link'
    var div_id = `${post.id}postDiv`
    // allow edit and add to album only if it does not share any other post
    var edit_addalbum_buttons = typeof post.shares.id == 'undefined' ? `
    <button class="dropdown-item" type="button" onclick="openAddToAlbumModal({postId: '${post.id}'})"><i class="fa fa-plus-square yellow-text" aria-hidden="true"></i> Add to album </button>
    <button class="dropdown-item" type="button" id="editPost${post.id}"><i class="fa fa-pencil-square-o yellow-text" aria-hidden="true"></i> Edit Post </button>
    ` : ``
    // inject variables into HTML that is repeated to create a feed
    var edit_post = (post.author.id == requestUserId) ? `
        <div class="btn-group dropright">
                <i class="fa fa-ellipsis-h yellow-text" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"></i>
            <div class="dropdown-menu">
                ${edit_addalbum_buttons}
                <button class="dropdown-item" type="button" onclick="deletePost('${post.id}', '${div_id}')"><i class="fa fa-times text-danger" aria-hidden="true"></i> Delete Post</button>
                <a class="yellow-link" href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"><button class="dropdown-item" type="button">🥳🥳 Surprise ?</button></a>
            </div>
        </div>
    ` : ''
    var post_html =`
    <div id=${div_id} class="post-li">
        <div class="card bg-grey">
            <div class="d-flex justify-content-between p-2 px-3">
                <div class="d-flex flex-row align-items-center">
                        <img src=${picture} width=50 height=50 class="rounded-image">
                    <div class="d-flex flex-column ml-2">
                        <span class="yellow-darker-text">
                            <b><a href="/users/profile/${post.author.username}"class="yellow-link"><u>${post.author.username}</u></a></b>
                            ${description}
                        </span>
                        ${tags_html}
                    </div>
                </div>
                <div class="d-flex flex-row mt-1 ellipsis">
                        <small class="mr-2 yellow-darker-text">${post.time_ago}</small>
                       ${edit_post}

                </div>
            </div>
                ${location_html}
            <div class="p-2">
                <p class="text-justify yellow-darker-text">${post.content}</p>
                ${images_html}
                <hr>
                <div class="row">
                    <div class="yellow-text col-3">
                        <a id="like-count${post.id}"class="yellow-link" onclick="openLikeShareModal({ modalType: 'liked', id: '${post.id}', username: '${post.author.username}'})" href="javascript:void(0);">
                            ${like_text}
                        </a>

                    </div>
                    <div class="col-9 d-flex flex-row muted-color justify-content-end">
                        <span class="mr-2">
                            <a class="yellow-link"  href="javascript:void(0);" onclick="toggle_comment(${post.id})" role="button" aria-expanded="false" id="collapseCommentCount${post.id}">
                                ${comment_text}
                            </a>
                        </span>
                        <span>
                            <a id="share-count${post.id}" class="yellow-link" onclick="openLikeShareModal({ modalType: 'shared', id: '${post.id}', username: '${post.author.username}'})" href="javascript:void(0);">
                                ${share_text}
                            </a>
                        </span>
                    </div>
                </div>

                <hr>

                <div class="d-flex justify-content-between align-items-center yellow-text">
                    <div class="row media-buttons d-flex align-items-center text-center">
                        <span class="col">
                            <a id="like-button${post.id}" href="javascript:void(0);" onclick="likePost(${post.id})" class="col ${like_color}">
                                <i class="bi bi-hand-thumbs-up-fill"></i>Like
                            </a>
                        </span>
                        <span class="col">
                            <a class="col yellow-link" role="button" aria-expanded="false" href="javascript:void(0)" onclick="toggle_comment(${post.id})" id="collapseCommentButton${post.id}">
                                <i class="bi bi-chat-dots-fill"></i> Comment
                            </a>
                        </span>
                        <span class="col">
                            <a id="share-button${post.id}" href="javascript:void(0);" onclick="sharePost(${post.id})" class="col ${share_color}">
                                <i class="fa fa-share"></i>Share
                            </a>
                        </span>
                    </div>
                </div>
                <hr>

                <div class="collapse" id="collapseComment${post.id}">
                    <div id="Comments${post.id}"></div>
                    <div class="comment-input">
                        <input id="comment-input${post.id}" type="text" class="form-control comment-input-box" maxlength="150" placeholder="max 150 characters.">
                        <div class="fonts"><a id="comment-push${post.id}" class="yellow-link" href="javascript:void(0);" onclick="send_comment(${post.id})"><i class="fa fa-paper-plane" aria-hidden="true"></i></a></div>
                    </div>
                </div>
            </div>
        </div>
    </div>`

    // appending to DOM
    if (append)
        $("#posts").append(post_html)
    else{
        $("#posts").prepend(post_html)
        $(`#${post.id}postDiv`).hide().slideDown('slow')
    }

    // creating map
    if (post.location.lat != ""){
        initMap(post)
    }
    // enter key push on comment
    $(`#comment-input${post.id}`).keyup(function(event) {
        if (event.keyCode === 13) {  //enter button
            var button = $(this).attr("id").replace('input', 'push')
            $(`#${button}`).click();
        }
    });

    // img modal events
    for (var image of post.images){
        $(`#postimg${image.id}`).unbind().click(function(e){
            openImages({postId: post.id, title: post.author.username + " was in " + post.location.name, imageArray: post.images, imageurl: $(this).attr('src')})
        })
    }

    if (typeof post.shares.id == 'undefined'){
        $(`#editPost${post.id}`).unbind().click(function(e){
            openUpdateModal(post)
        })
    }

}

function likePost(postId){
    /*
        Toggle like on a post
        Sends the request to the backend and dynamically renders the frontend
    */
    var url = "/travels/api/post/toggle-like-post/"
    $.ajax({
        url: url,
        type: 'PUT',
        data: {
            "post-id": postId
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data){
            var like_display_obj = $(`#like-count${postId}`)
            var like_button_obj = $(`#like-button${postId}`)
            var msg = ""
            var currentLikes = parseInt(like_display_obj.prop("innerText").trim().split(" ")[0])
            if (data["like-status"] == 1){  // the user liked the post
                msg = currentLikes + 1
                like_button_obj.removeClass("yellow-link").addClass("blue-text")
            }else{
                msg = currentLikes - 1
                like_button_obj.removeClass("blue-text").addClass("yellow-link")
            }

            if (currentLikes > 1)
                msg += " likes"
            else
                msg += " like"

            like_display_obj.text(msg)

        }
    })
}

function sharePost(postId){
    /*
        Share a post by sending the request to the backend, gets the new shared post
        and renders it dynamically in the feed
    */
    if($(`#share-button${postId}`).hasClass('blue-text')){
        return
    }
    var url = "/travels/api/post/share/"
    $.ajax({
        url: url,
        type: 'PUT',
        data: {
            "post-id": postId
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data){
            var share_display_obj = $(`#share-count${postId}`)
            var share_button_obj = $(`#share-button${postId}`)
            var msg = ""
            var currentShares = parseInt(share_display_obj.prop("innerText").trim().split(" ")[0])
            msg = currentShares + 1
            share_button_obj.removeClass("yellow-link").addClass("blue-text")

            if (currentShares > 1)
                msg += " shares"
            else
                msg += " share"

            share_display_obj.text(msg)
            addPost(data, false)


        }
    })
}

function addComment(postId, comment){
    /*
        Add one row for one comment inside one post
    */
    var picture  = comment.author.profile_picture ? comment.author.profile_picture: defaultProfilePictureUrl
    var like_color =  comment.likes.includes(requestUserId) ? 'blue-text':'yellow-link'
    comment = `
    <div class="d-flex flex-row mb-2"> <img src="${picture}" width=50 height=50 class="rounded-image">
        <div class="d-flex flex-column ml-2">
            <span class="name"><a href="/users/profile/${comment.author.username}" class="yellow-link"><u>${comment.author.username}</u></a></span>
            <span class="comment-text yellow-darker-text">${comment.content}</span>
            <div class="d-flex flex-row align-items-center status yellow-text">
                <small><a id="comment-like-button${comment.id}" href="javascript:void(0);" onclick="likeComment(${comment.id})" class="${like_color}"><i class="bi bi-hand-thumbs-up-fill"></i> Like</a></small>
                <small class="yellow-darker-text">${comment.time_ago}</small>
                <small>
                    <a id="comment-like-count${comment.id}"class="yellow-link" onclick="openLikeShareModal({ modalType: 'comment-liked', id: '${comment.id}', username: '${comment.author.username}'})" href="javascript:void(0);">
                        ${comment.likes.length} <i class="bi bi-hand-thumbs-up-fill"></i>
                    </a>
                </small>
            </div>
        </div>
    </div>`
    $(`#Comments${postId}`).append(comment)
}

function toggle_comment(postId){
    /*
        Display all the comments of a single post
    */
    if($(`#collapseComment${postId}`).is(':visible'))
        $(`#collapseComment${postId}`).collapse('hide');
    else{
        $.getJSON({
            url: `/travels/api/post/get-comments/?post-id=${postId}`,
            success: function(data){
                $(`#Comments${postId}`).empty() // empty comments
                for (var comment of data ){
                    addComment(postId, comment)
                }
                $(`#collapseComment${postId}`).collapse('show');
            }
        })
    }

}

function send_comment(postId){
    /*
        Send a comment to the backend
    */
    var url = "/travels/api/post/add-comment/"
    var content = $(`#comment-input${postId}`).val().trim()
    if (content.length == 0){
        return
    }
    $.ajax({
        url: url,
        type: "POST",
        data: {
            "post-id": postId,
            "content": content
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(comment){
            addComment(postId, comment)
            $(`#comment-input${postId}`).val("");
        }
    })
}

function likeComment(commentId){
    /*
        Same logic as the post like but with comments
    */
    var url = "/travels/api/post/toggle-like-comment/"
    $.ajax({
        url: url,
        type: 'PUT',
        data: {
            "comment-id": commentId
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data){
            var like_display_obj = $(`#comment-like-count${commentId}`)
            var like_button_obj = $(`#comment-like-button${commentId}`)
            var msg = ""
            var currentLikes = parseInt(like_display_obj.prop("innerText").trim().split(" ")[0])
            if (data["like-status"] == 1){  // the user liked the post
                msg = currentLikes + 1
                like_button_obj.removeClass("yellow-link").addClass("blue-text")
            }else{
                msg = currentLikes - 1
                like_button_obj.removeClass("blue-text").addClass("yellow-link")
            }

            msg += " <i class='bi bi-hand-thumbs-up-fill'></i>"

            like_display_obj.html(msg)

        }
    })
}

function paginatedFeed({feed_type, offset, limit, parameters=""}){
    /*
        Loads posts with offset and limit
    */
    $.getJSON({
        url: `/api/feed/?type=${feed_type}&offset=${offset}&limit=${limit}${parameters}`,
        success: function(data){
            for (var post of data){
                addPost(post, true)
            }
            if (data.length > 0){
                $(`#${post.id}postDiv`).addClass("bottomPost")  // last post gets tagged bottomPost
            }
        }
    })
}
