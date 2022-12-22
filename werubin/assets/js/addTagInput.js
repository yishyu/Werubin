var currentTagFieldId = 1
function reset_tags(){
    /*
        Remove all tag fields in the modal form
    */
    for (currentTagFieldId; currentTagFieldId > 0; currentTagFieldId--){
        $(`#postTag${currentTagFieldId}Row`).remove()
    }
    currentTagFieldId = 1
}

function addNewTagField() {
    /*
        Add a new tag field to the modal form
    */
    let tagFieldId = "postTag" + currentTagFieldId
    currentTagFieldId += 1

    let postTagHTML = `
        <div id="${tagFieldId}Row" class="row mt-1">
            <div class="form-group col-9">
                <input class="tagInput center form-control" id="${tagFieldId}" type="text" name="${tagFieldId}" placeholder="Enter a tag...">
            </div>
            <div id="deleteTag" class="center ml-1 col-1 btn btn-outline-danger" onclick="deleteTagField({tagRow: '${tagFieldId}Row'})">
                x
            </div>
        </div>
    `

    $("#tagInputs").append(postTagHTML)
    return tagFieldId

}

function deleteTagField({tagRow}) {
    /*
        Delete a tag field from the modal form
    */
    $(`#${tagRow}`).remove()
}
