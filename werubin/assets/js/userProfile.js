$("#profileButton").removeClass("yellow-text")
$("#profileButton").addClass("blue-text")

function initRoadMap(){
    /*
        Inits the road map by centering in in Center Europe
        with the min zoom level
    */
    var center = {
        lat: 50.378472,
        lng: 14.970598
    }
    // The map, centered at Lessines
    var map = new google.maps.Map(
        document.getElementById("roadMap"),
        {
            zoom: 1,
            center: center,
            disableDefaultUI: true,
        }
    );
    return map
}

function addToMap(map, post) {
    /*
        Creates a map for a post with the post location marked on the map
        By clicking on the marker, the pre-saved name of the location is shown
    */
    var position = {
        lat: parseFloat(post.location.lat),
        lng: parseFloat(post.location.lng)
    }
    var marker = new google.maps.Marker({
        id: post.id,
        position: position,
        title: post.location.name,
        map: map,
    })

    var infoWindow = new google.maps.InfoWindow();
    marker.addListener("click", () => {
        map.setZoom(5)
        map.panTo(marker.getPosition())
        infoWindow.close();
        var images_html = ""
        for (var image of post.images){
            images_html += `<img class="post-img" src=${image.image}>`
        }
        images_html += ""
        const weather_id = `weather${post.location.id}`
        const contentString =`
            <div class="container" id="content">
                <div class="row">
                    <div class="col-8">
                        Current Weather
                        <div id="${weather_id}"></div>
                    </div>
                    <div class="col-4">
                        posted ${post.time_ago}
                    </div>
                </div>
                <div class="row">
                    <h3 id="firstHeading" class="blue-text firstHeading">${marker.getTitle()}</h3>
                </div>

                <div id="bodyContent">
                    <p class="text-justify yellow-darker-text">${post.content}</p>
                    ${images_html}
                </div>
            </div>
            `
        infoWindow.setContent(contentString);
        set_weather(position.lat, position.lng, weather_id);
        infoWindow.open(marker.getMap(), marker);
        });
}

var LIMIT = 2
var OFFSET = 0

function user_posts(map){
    $("#posts").empty()
    paginated_feed({feed_type: "User", offset: OFFSET, limit: LIMIT, parameters:`&id=${userId}`});
    OFFSET += LIMIT
}

function setRoadMap(map){
    /*
        Sets the markers on the roadmap
        Use of a different function because user_posts will be paginated
        but on the roadmap we want all the locations
    */
    var url = `/users/api/road_map/?user-id=${userId}`
    $.getJSON({
        url:url,
        success: function(data){
            for (var post of data){
                addToMap(map, post)
            }
        }
    })
}

$( document ).ready(function(){
    var map = initRoadMap()
    user_posts()
    setRoadMap(map)
    // load next post at the bottom of the page
    var $win = $(window)
    $(window).scroll(function() {
        if($('.bottomPost').length > 0){
            var divTop = $('.bottomPost').first().offset().top,
            divHeight = $('.bottomPost').first().outerHeight(),
            wHeight = $(window).height(),
            windowScrTp = $(this).scrollTop();
            if (windowScrTp > (divTop+divHeight-wHeight-100)){
                $('.bottomPost').first().removeClass("bottomPost")
                paginated_feed({feed_type: "User", offset: OFFSET, limit: LIMIT,parameters:`&id=${userId}`});
                OFFSET += LIMIT
            }
        }

        });
});

$('#albumButton').unbind().click(function(){
    if ($('#caret-icon').hasClass("bi-caret-down")) {
        $('#caret-icon').removeClass("bi-caret-down").addClass("bi-caret-up")
    } else {
        $('#caret-icon').removeClass("bi-caret-up").addClass("bi-caret-down")
    }
});

async function albumModal({albumId, title, postids}) {
    var ids = postids.split(" ").filter((s) => s !== "")
    var images = []
    var postIds = []
    for (const id in ids) {
        let data = await $.getJSON({url: `/travels/api/post/get/${ids[id]}`})
        for (const img in data.images) {
            console.log(data.images)
            postIds.push(ids[id])
            images.push(data.images[img])
        }

    }
    if (images.length == 0) {
        open_images({title: title, imageArray: [noAlbumPictureUrl], imageurl: noAlbumPictureUrl})
    } else {
        open_images({albumId: albumId, title: title, imageArray: images, imageurl: images[0].image, postIds: postIds})
    }
}