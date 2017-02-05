
var base_url = window.location.href;

// Gets the value from the dropdown box with the provided id
function get_dropdown(id) {
    box = document.getElementById(id);
    return box[box.selectedIndex].text
}

function add_sub(sub, subs_list) {
    var content = document.createTextNode(subs[i][0]);
    subs_list.appendChild(content);
    var br = document.createElement("br");
    subs_list.appendChild(br);
}

subsRequest = new XMLHttpRequest();
subsRequest.onreadystatechange = function(){
    subs_list = document.getElementById("list");
    if (subsRequest.readyState === XMLHttpRequest.DONE && subsRequest.status === 200) {
        subs_list.innerHTML = "";    // Clear the existing list

        var subs = JSON.parse(subsRequest.responseText);
        // add the new list
        for(i=0; i < subs.length; i++) {
            add_sub(subs[i], subs_list)
        }
    }
}

// main block
window.onload = function() {
    document.getElementById("submit").onclick = function() {
        var tag = get_dropdown("tags");
        var city = get_dropdown("cities");

        //make AJAX request
        request = base_url + "get_data/" + city + '/' + tag;
        subsRequest.open('GET', request, true);
        subsRequest.send(null);
    }
}
