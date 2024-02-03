// onclic handle to list student to student profile
function callurl(username) {
    // Encode the username to ensure the URL is correctly formatted
    var encodedUsername = encodeURIComponent(username);
    // Construct the full URL using template literals and the encoded username
    window.location = `${encodedUsername}`;
}
