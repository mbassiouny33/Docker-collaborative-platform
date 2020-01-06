

var myObj = JSON.parse(myJSONfile);

console.log(myObj);

function returnUsername(){
    //return myObj.username;
	return "";
}
function returnWordpressURL(){
    return myObj.wordpress;
}
function returnNextcloudURL(){
    return myObj.nextcloud;
}
function returnRocketchatURL(){
    return myObj.rocketchat;
}
function returnKeycloakURL(){
    return myObj.admin;
}

//Username
var usernameDiv = document.getElementById("welcomeUsername");
usernameDiv.innerHTML = returnUsername();
var usernameDiv2 = document.getElementById("welcomeUsername2");
usernameDiv2.innerHTML = returnUsername();

//Wordpress Link
var wordpressLink = document.getElementById("link-wordpress");
wordpressLink.href = returnWordpressURL();
var wordpressLink2 = document.getElementById("link-wordpress2");
wordpressLink2.href = returnWordpressURL();

//Nextcloud Link
var nextcloudLink = document.getElementById("link-nextcloud");
nextcloudLink.href = returnNextcloudURL();
var nextcloudLink2 = document.getElementById("link-nextcloud2");
nextcloudLink2.href = returnNextcloudURL();

//Rocketchat Link
var rocketchatLink = document.getElementById("link-rocketchat");
rocketchatLink.href = returnRocketchatURL();
var rocketchatLink2 = document.getElementById("link-rocketchat2");
rocketchatLink2.href = returnRocketchatURL();

//Keycloak Link
var keycloakLink = document.getElementById("link-keycloak");
keycloakLink.href = returnKeycloakURL();
var keycloakLink2 = document.getElementById("link-keycloak2");
keycloakLink2.href = returnKeycloakURL();