function closeLikeShareModal(){
    $("#likes-shares-modal").modal('hide');
}

function openLikeShareModal({ modalType, id, username }) {
    let modalTitle;
    let url = "/users/api/get/";

    switch (modalType) {
        case "shared":
            modalTitle = "Shared by"
            url += "?type=shared&id=" + id
            break;
        case "liked":
            modalTitle = "Liked by"
            url += "?model=post&type=liked&id=" + id
            break;
        case "comment-liked":
            modalTitle = "Liked by"
            url += "?model=comment&type=liked&id=" + id
            break;
        case "following":
            modalTitle = "Users following " + username
            url += "?type=following&id=" + id
            break;
        case "followers":
            modalTitle = "Users " + username + " follows"
            url += "?type=followers&id=" + id
            break;
        default:
            console.log("woops")
            break;
    }

    $.get({
          url: url
        , success: function(data) {
            toggleLikeShareModal({
                defaultProfilePictureUrl: defaultProfilePictureUrl,
                modalTitle: modalTitle,
                modalType: modalType,
                data: data
            })
        }
    })
}

function toggleLikeShareModal({ modalTitle, data }){
    let output = ""
    let url = "/users/api/current_user"
    $.getJSON({
        url: url,
        success: function(data){
            return data
        }
    }).then(
        current_user => {
            for (user of data) {
                let picture = user.profile_picture ? user.profile_picture : defaultProfilePictureUrl
                let follow_text = current_user.followers.includes(user.id) ? "Unfollow" : "Follow"
                let userID = "likes-shares-modal-user-button-" + user.username
                let follow_button = current_user.id != user.id ? `<button id="${userID}" class="followButton btn btn-outline-warning" onClick="onFollowClick('${user.id}', '${userID}')"> ${follow_text}</button>`: ''

                output += `
                    <div class="row justify-content-around mb-2">
                        <div class="col-2">
                            <img src=${picture} height=50px width=50px class="rounded-image">
                        </div>
                        <div class="col-6 center">
                            <span>${user.username}</span>
                        </div>
                        <div class="col-2 center">
                            ${follow_button}
                        </div>
                    </div>
                `
            }
            if (data.length == 0) { output = `<p class="center">Nobody yet!</p>`}

            $("#likes-shares-modal-title").html(modalTitle)
            $("#likes-shares-modal-body").html(output)
            $("#likes-shares-modal").modal('show');
        }
    )
}

function onFollowClick(userId, userObjId) {
    let userObj= $(`#${userObjId}`)
    let url = "/users/api/follow_user/"
    $.ajax({
        url: url,
        type: 'PUT',
        data:{
            "user-id": userId
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data){
            if (data["follow-status"] == 1){
                userObj.html("Unfollow")
            } else {
                userObj.html("Follow")
            }
        }
    })
}