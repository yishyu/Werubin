var ids = {
    'user': 1,
    'post': 1
}
function reset_tags(type){
    let currentTagFieldId = ids[type]
    for (currentTagFieldId; currentTagFieldId > 0; currentTagFieldId--){
        $(`#${type}Tag${currentTagFieldId}Row`).remove()
    }
    ids[type] = 1
}

function addNewTagField(type) {
    let currentTagFieldId = ids[type]
    let tagFieldId = `${type}Tag${currentTagFieldId}`
    ids[type] += 1

    let TagHTML = `
        <div id="${tagFieldId}Row" class="row mt-1">
            <div class="form-group col-9">
                <input class="tagInput center form-control" id="${tagFieldId}" type="text" name="${tagFieldId}" placeholder="Enter a tag...">
            </div>
            <div id="deleteTag" class="center ml-1 col-1 btn btn-outline-danger" onclick="deleteTagField({tagRow: '${tagFieldId}Row'})">
                x
            </div>
        </div>
    `

    $(`#${type}TagInputs`).append(TagHTML)
    return tagFieldId

}

function deleteTagField({tagRow}) {
    /*
        Delete a tag field from the modal form
    */
    $(`#${tagRow}`).remove()
}
