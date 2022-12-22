var currentTagFieldId = 1

function resetTags(){
    /*
        removes all tag fields
    */
    for (currentTagFieldId; currentTagFieldId > 0; currentTagFieldId--){
        $(`#postTag${currentTagFieldId}Row`).remove()
    }
    currentTagFieldId = 1
}

function addNewTagField() {
    /*
        adds a new tag input field
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
        removes a tag field
    */
    $(`#${tagRow}`).remove()
}

// https://stackoverflow.com/questions/46260312/how-to-submit-a-list-of-items-in-an-html-form

$(document).ready(function() {
    // when user clicks submit button, this code will be executed first
    $('postForm').submit(function() {
        // we'll take all values of the Two dropdown and put them in 1 string
        var all_values = '';
        for (let i = 0; i < currentTagFieldId; i++) {
            let tagFieldId = "postTag" + currentTagFieldId
            if(all_values !== '') {
                all_values += $(tagFieldId).val();
            } else {
                all_values += ',' + $(tagFieldId).val();
            }
        }
        $('#tags').val(all_values);
    });
});
