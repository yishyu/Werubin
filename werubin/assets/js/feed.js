var LIMIT = 5
var OFFSET = 0
function feed(feed_type){
    /*
        Depending on the picked feed: ForYou Explore Followers
        The feed is regenerated dynamically by this function
    */
    $(".feed").removeClass('blue-text').addClass('yellow-text')
    $(`#${feed_type}`).removeClass('yellow-text').addClass('blue-text')
    $("#posts").empty()
    OFFSET = 0 // first load with offset 0 because we are changing feed
    paginatedFeed({feed_type: feed_type, offset: OFFSET, limit: LIMIT});
    OFFSET += LIMIT
}

function getFeedType(){
    /**
     * Displays the right feed when the page is loaded
     */
    var hash = $(location).attr('hash');
    if (hash === ""){
        history.pushState(null,null, '#ForYou');
        return "ForYou"
    }
    else
        return hash.slice(1)
}

$( document ).ready(function(){
    /*
        Loads the field corresponding to the anchor
    */
    // first feed load
    const feed_type = getFeedType()
    feed(feed_type)

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
                let current_feed_type = this.getFeedType()
                paginatedFeed({feed_type: current_feed_type, offset: OFFSET, limit: LIMIT});
                OFFSET += LIMIT
            }
        }

     });

    // event on feed buttons
    $(".feed").unbind().click(function(e) {
        feed($(this).attr("id"))
        history.pushState(null,null,`#${$(this).attr("id")}`);
        e.preventDefault();
    });

});