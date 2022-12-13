function switch_image(imageArray, go_next){
    const currentimage = $('#modal-img').attr('src')
    var current_index = 0
    for (var i=0; i<imageArray.length; i++){
        if(imageArray[i].image == currentimage){
            current_index = i
        }
    }
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

function open_images({imageArray, imageurl}){
    $("#image-modal").modal("show");
    $("#prev-img").unbind().click(function(e){switch_image(imageArray, false)})
    $("#next-img").unbind().click(function(e){switch_image(imageArray, true)})

    $(`#image-modal`).keyup(function(event) {
        if (event.keyCode === 37) {  //left arrow
            $(`#prev-img`).click();
        }else if(event.keyCode === 39){
            $(`#next-img`).click();
        }
    });

    $(`#image-modal-body`).html(
        `<img id="modal-img" width=100% src=${imageurl}>`
    )
}