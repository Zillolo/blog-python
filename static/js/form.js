function showDeleteAlert(url) {
    var ret = confirm("Do you really want to delete this post?");
    if(ret == true) {
        window.location = url;
    }
}

function validatePostForm(action) {
    var errorString = "";

    var title = document.forms["postForm"]["title"].value;
    if(title == null || title == "") {
        errorString += "The title field may not be empty.\n";
    }

    var author = document.forms["postForm"]["author"].value;
    if(author == null || author == "") {
        errorString += "The author field may not be empty.\n";
    }

    var content = document.forms["postForm"]["content"].value;
    if(content == null || content == "") {
        errorString += "The content field may not be empty.\n";
    }

    if(errorString != "") {
        alert(errorString);
        return false;
    } else {
        return true;
    }
}
