// onclic handle to list student to student profile
function callurl(username) {
    // Encode the username to ensure the URL is correctly formatted
    var encodedUsername = encodeURIComponent(username);
    // Construct the full URL using template literals and the encoded username
    window.location = `${encodedUsername}`;
}


// for loader
window.addEventListener('load', function() {
    var loadingElement = document.getElementsByClassName('loading')[0]; // Get the first element
    if (loadingElement) { // Check if the element exists
        loadingElement.style.display = 'none';
    }
});


function initialize() {
    console.log('event triggered');
    var downloadLink = document.getElementById('downloadLink');
    var currentUrl = window.location.href;
    var downloadParam = "download=true";

    if (downloadLink) { // Ensure downloadLink is not null
        if (currentUrl.includes('?')) {
            downloadLink.href = currentUrl + '&' + downloadParam;
        } else {
            downloadLink.href = currentUrl + '?' + downloadParam;
        }
    }
}

if (document.readyState === "loading") {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    // DOMContentLoaded has already fired
    initialize();
}