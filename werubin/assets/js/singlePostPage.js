function single_post(){
    /*
        only shows a single post based on the url
    */
    $.getJSON({
        url: $('#postidurl').val(),
        success: function(data){
            $("#posts").empty()
            addPost(data, true)
        }
    })
}