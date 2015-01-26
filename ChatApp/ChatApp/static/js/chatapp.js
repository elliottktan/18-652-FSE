var req;
var numPosts;
var chatappcss = "/static/css/chatapp.css"

function sendRequest() {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "/chatapp/get_posts", true);
    req.send();
}

function handleResponse() {

    if (req.readyState != 4 || req.status != 200) {
        return;
    }
    var xmlData = req.responseXML;
    var posts = xmlData.getElementsByTagName("post");


    if (posts.length == numPosts) {
        return;
    }
    numPosts = posts.length;

    $(".chatapp-post").remove();
    list = document.getElementById("post-list");

    var xmlData = req.responseXML;
    var posts = xmlData.getElementsByTagName("post")
    
    for (var i=posts.length - 1; i>=0; i--) {

        var user = posts[i].getElementsByTagName("user")[0].textContent;
        var date = posts[i].getElementsByTagName("date")[0].textContent;
        var text = posts[i].getElementsByTagName("text")[0].textContent;

        var newPost = document.createElement("div");
        newPost.className = "chatapp-post";
        var newHeader = document.createElement("div");
        newHeader.className = "chatapp-header";

        var newUser = document.createElement("div");
        newUser.className = "chatapp-post-user";
        newUser.innerHTML = user;
        newHeader.appendChild(newUser);

        var newDate = document.createElement("div");
        newDate.className = "chatapp-post-date";
        newDate.setAttribute("align", "right");
        newDate.innerHTML = date;
        newHeader.appendChild(newDate);

        newPost.appendChild(newHeader);
        
        var newText = document.createElement("div");
        newText.className = "chatapp-post-text";
        newText.innerHTML = text;

        newPost.appendChild(newText);

        list.appendChild(newPost);
        
    }
}
window.setInterval(sendRequest, 500);
