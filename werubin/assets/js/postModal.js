function closePostModal(){
    $("#post-modal").modal('hide');
}

function openPostModal() {
    $("#post-modal").modal('show');
}

function closeModal(id){
    $(`#${id}`).modal('hide')
}