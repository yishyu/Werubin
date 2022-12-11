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
