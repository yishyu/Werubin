var currentTagFieldId = 1
function addNewTagField() {
    let tagFieldId = "postTag" + currentTagFieldId
    currentTagFieldId += 1

    $("#addTag").remove()

    let postTagHTML = `
        <div class="row">
            <div class="form-group col-10">
                <input class="tagInput center form-control" id="${tagFieldId}" type="text" name="${tagFieldId}" placeholder="Enter a tag...">
            </div>
            <div id="addTag" class="center col-1 btn btn-outline-warning" onclick="addNewTagField()">
                +
            </div>
        </div>
    `

    $("#tagInputs").append(postTagHTML)

}

// https://stackoverflow.com/questions/46260312/how-to-submit-a-list-of-items-in-an-html-form

$(document).ready(function() {
    // on user clicks submit button, this code will be executed first
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
