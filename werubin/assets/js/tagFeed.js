var LIMIT = 5
var OFFSET = 0

function tag_posts(tag){
    $("#posts").empty()
    paginated_feed({feed_type: "SingleTag", offset: OFFSET, limit: LIMIT, parameters:`&tag=${tag}`});
    OFFSET += LIMIT
}

$( document ).ready(function(){
    tag_posts(tag)
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
                paginated_feed({feed_type: "SingleTag", offset: OFFSET, limit: LIMIT, parameters:`&tag=${tag}`});
                OFFSET += LIMIT
            }
        }

        });
});