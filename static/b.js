import { Server } from "socket.io";

const websocket = 1;
var username = document.getElementsByClassName('guest')[0].innerHTML;
const io = new Server({maxHttpBufferSize: 1e8});
var socket = io;

socket.on('disconnect', function() {
    console.log('Disconnecting');
});
socket.on('connect', function() {
    console.log('Connecting');
    socket.emit('get-active-users');
});
// Receive messages from the server
socket.on('serverSent', function(message) {
    //console.log('Message received:', message);
    addMessageToChat(message);
});

socket.on('update-active-users', function (activeUserList) {
    var userList = document.getElementById("active-user-list");
    userList.innerHTML = '';
    for (var user in activeUserList) {
        var totalTime = activeUserList[user];
        var time;
        const minuteMark = 60;
        if (totalTime >= minuteMark) {
            var minutes = Math.floor(totalTime / minuteMark); // this finds the amount of minutes
            var seconds = totalTime % minuteMark; // this finds the amount of seconds
            time = minutes + ' minutes ' + seconds + ' seconds';
        } else {
            time = totalTime + ' seconds';
        }
        var listItem = document.createElement('li');
        listItem.textContent = user + ': ' + time;
        userList.appendChild(listItem);
    }
});

// Function to handle logout
function logout() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            // Redirect the user to the homepage after logout
            console.log("Logged OUT successfully");
            window.location.href = "/";
        }
    }
    request.open("POST", "/logout");
    request.send();
}

// Function to handle register
function register() {
    const username = document.getElementById("reg-form-username").value;
    const password = document.getElementById("reg-form-pass").value;
    const password2 = document.getElementById("reg-form-pass2").value;
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            // Handle successful registration response if needed
            console.log("Registered successfully");
            window.location.href = "/";
        }
    }
    let formData = [String(username), String(password), String(password2)];
    request.open("POST", "/register");
    request.send(JSON.stringify(formData));
//    request.send(formData);
}

// Function to handle logout
function logout() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            // Redirect the user to the homepage after logout
            console.log("Logged OUT successfully");
            window.location.href = "/";
        }
    }
    request.open("POST", "/logout");
    request.send();
}

// Function to handle register
function register() {
    const username = document.getElementById("reg-form-username").value;
    const password = document.getElementById("reg-form-pass").value;
    const password2 = document.getElementById("reg-form-pass2").value;
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            // Handle successful registration response if needed
            console.log("Registered successfully");
            window.location.href = "/";
        }
    }
    let formData = [String(username), String(password), String(password2)];
    request.open("POST", "/register");
    request.send(JSON.stringify(formData));
//    request.send(formData);
}

// Function to handle login
function login() {
    const username = document.getElementById("login-form-username").value;
    const password = document.getElementById("login-form-pass").value;
    //const formData = new FormData(document.getElementById("login-form"));
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            // Handle successful login response if needed
            console.log("Logged in successfully");
            window.location.href = "/";
        }
    }
    let formData = [String(username), String(password)];
    request.open("POST", "/login");
    request.send(JSON.stringify(formData));
    //request.send(formData);
}

    document.getElementById("register-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission
        register(); // Call register function
    });

    document.getElementById("login-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission
        login(); // Call login function
    });

    document.getElementById("logout-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission
        logout(); // Call logout function
    });

    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//CHAT MESSAGES
// Function to handle sending chat messages (both text and image)
function sendChat() {
    const chatTextBox = document.getElementById("chat-text-box");
    const message = chatTextBox.value;
    chatTextBox.value = "";
    // Retrieve XSRF token
    const xsrf = document.getElementById("xsrf-token").value;
    // Get the uploaded image file
    const imageFile = document.getElementById("image-upload").files[0];
    if (!imageFile) {
        console.log("Must upload an image with any message");
    }
    else {
        document.getElementById("image-upload").value = "";
        if (username != "Guest") {
            if (websocket == 1) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    const imageData = event.target.result.split(',')[1]; // [0] = data:image/png;base64, [1] = actual base 64 encoded image
                    socket.emit('clientSent', {'message': message, 'image': imageData});
                };
                reader.readAsDataURL(imageFile);
            }
            else {
                // Create a FormData object to send text and image together
                const formData = new FormData();
                formData.append('message', message); // Append text message
                formData.append('image', imageFile); // Append image file
                // Create a new XMLHttpRequest object
                const request = new XMLHttpRequest();
                request.onreadystatechange = function () {
                    if (this.readyState === 4) {
                        if (this.status === 200) {
                            console.log(this.response);
                            window.location.href = "/";
                            // Display the uploaded image and text message
                            //displayChatMessage(message, URL.createObjectURL(imageFile));
                        } else if (this.status === 403) {
                            console.error("403 Forbidden: Submission rejected");
                        }
                    }
                }

                request.open("POST", "/chat-messages");
                request.setRequestHeader("X-XSRF-Token", xsrf);
                console.log(formData);
                request.send(formData);
            }
        //    request.send(JSON.stringify(formData));

            chatTextBox.focus();
        }
    }
}

// Add event listener to the "Send" button
document.getElementById("chat-button").addEventListener("click", function(event) {
    sendChat(); // Call the sendChat() function when the button is clicked
});

// Function to display chat message (text and image)
function displayImage(imageUrl) {
    let image;
    if (imageUrl) {
        image = document.createElement("img");
        image.src = imageUrl;
        image.alt = "Uploaded Image";
        image.className = "formatted-image";
        image.width = 300; // Set the desired width
        image.height = 200; // Set the desired height

    }
    return image
}

function createImageUrlFromBase64(base64String) {
    const binaryString = atob(base64String);
    const byteArray = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
        byteArray[i] = binaryString.charCodeAt(i);
    }
    const blob = new Blob([byteArray], { type: 'image/jpeg' }); // Adjust the type if needed
    return URL.createObjectURL(blob);
}

function upvoteMessage(messageId) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
            window.location.href = "/";
        }
    }
    request.open("POST", "/upvote/" + messageId);
    request.send();
}

function downvoteMessage(messageId) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
            window.location.href = "/";
        }
    }
    request.open("POST", "/downvote/" + messageId);
    request.send();
}

function clearChat() {
    const chatMessages = document.getElementById("chat-messages-section-content");
    chatMessages.innerHTML = "";
}

function chatMessageHTML(messageJSON) {
    const username = messageJSON.username;
    const message = messageJSON.message;
    const messageId = messageJSON.id;
    const im = messageJSON.img;
    // console.log(im);
    const upv = messageJSON.upv
    const dwv = messageJSON.dwv
    /*const imagef = displayImage(URL.createObjectURL(im));*/
    const imageUrl = createImageUrlFromBase64(im);
    // console.log(imageUrl);
    const imageElement = displayImage(imageUrl);
    // console.log(imageElement);

//    let messageHTML = "<br><span id='message_" + messageId + "'><b>" + username + "</b>: " + message + "</span>";
    let messageHTML = "<br><span id='message_" + messageId + "'><b>" + username + "</b>: <br> Planet:<br>" + (imageElement ? imageElement.outerHTML : "") + "<br>Reasononing:<br>" + message + "</span>";
    messageHTML += "<br><button onclick='upvoteMessage(\"" + messageId + "\")'>Upvote</button> " + upv + " ";
    /*let messageHTML = "<br><button onclick='upvoteMessage(\"" + messageId + "\")'>Upvote</button> ";
    messageHTML += "<span id='message_" + messageId + "'><b>" + username + "</b>: " + message + "</span>";*/
/*
    messageHTML += "<span id='message_" + messageId + "'><b>" + username + "</b>: \nPlanet: \n" + imagef + "\nReason:\n" + message + "\n</span>";
*/
    messageHTML += " <button onclick='downvoteMessage(\"" + messageId + "\")'>Downvote</button> " + dwv + "<br>";
//    messageHTML += "<br><button onclick='downvoteMessage(\"" + messageId + "\")'>Downvote</button> \n";
    return messageHTML;
}

function addMessageToChat(messageJSON) {
    const chatMessages = document.getElementById("chat-messages-section-content");
    //chatMessages.innerHTML += "Here we go"
    chatMessages.innerHTML += chatMessageHTML(messageJSON);
//    chatMessages.scrollIntoView(false);
//    chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
    chatMessages.scrollTop = chatMessages.scrollHeight + 30;
}
function updateChat() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            clearChat();
            const messages = JSON.parse(this.response);
            for (const message of messages) {
                addMessageToChat(message);
            }
        }
    }
    request.open("GET", "/chat-messages");
    request.send();
}





/*function displayChatMessage(message, imageUrl) {
    const chatMessages = document.getElementById("chat-messages-section-content");
    // creates display line
    chatMessages.innerHTML += chatMessageHTML(messageJSON);

    const messageDiv = document.createElement("div");
    const messageText = document.createElement("p");
    messageText.textContent = message;
    *//*messageDiv.appendChild(messageText);*//*
    messageDiv.appendChild("Planet: \n");
    if (imageUrl) {
        const image = document.createElement("img");
        image.src = imageUrl;
        image.alt = "Uploaded Image";
        messageDiv.appendChild(image);
    }
    messageDiv.appendChild("\nReason: \n");
    messageDiv.appendChild(messageText);

    chatMessages.appendChild(messageDiv);

    // Scroll to the bottom of the chat messages
    chatMessages.scrollTop = chatMessages.scrollHeight;
}*/

function welcome() {
    document.getElementById("paragraph").innerHTML += "<br/>We aim to destroy the Justice League and take over the Galaxy. Here is some JavaScript Text. A show of Even more genius. Braniacs Project 1 😀";
    document.getElementById("paragraph").innerHTML += "<br/>Upload an image of a Planet and Enter text explaining why you think that planet's capture is feasible and useful to our cause";
    document.getElementById("paragraph").innerHTML += "<br/>The other Braniacs will Upvote or Downvote as they see fit.";


    document.getElementById("chat-messages").innerHTML += "Register and Sign in to post. Guest posts are NOT allowed and will return errors. You can only vote once per message. Vote wisely."
    updateChat();
    if (websocket == 0){
        setInterval(updateChat, 10000);
    }
}


