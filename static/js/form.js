function showDeleteAlert(url) {
    var ret = confirm("Do you really want to delete this post?");
    if(ret == true) {
        window.location = url;
    }
}
