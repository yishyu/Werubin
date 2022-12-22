var LIMIT = 5
var OFFSET = 0

function tagPosts(tag){
    /**
     * displays a paginated feed of tagged posts
     */
    $("#posts").empty()
    paginatedFeed({feed_type: "SingleTag", offset: OFFSET, limit: LIMIT, parameters:`&tag=${tag}`});
    OFFSET += LIMIT
}

$( document ).ready(function(){
    /**
     * handles the load of next posts when scrolling to the bottom of the feed
     */
    tagPosts(tag)
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
                paginatedFeed({feed_type: "SingleTag", offset: OFFSET, limit: LIMIT, parameters:`&tag=${tag}`});
                OFFSET += LIMIT
            }
        }

        });
});