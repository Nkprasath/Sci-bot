// Variable to store the latest question
var latestQuestion = "";
// function to clear yes and no buttons
function clearTeachOptions() {
    var teachOptions = document.querySelector(".teach-options");
    if (teachOptions) {
        teachOptions.remove();
    }
}
// function to open about.html page
function openPage() {
    window.location.href = "about.html";
}

// Add an event listener for the submit event
document.getElementById("chat-form").addEventListener("submit", function(event) {
    event.preventDefault();
    // Get user input
    var userMessage = document.getElementById("user-input").value;
    // Check if the user message is empty
    if (userMessage === "") {
        event.preventDefault(); // Prevent form submission
        return; // Exit the function
    }
    // keep track of latest question
    latestQuestion = userMessage
    // console.log(latestQuestion)
    var chatBox = document.getElementById("chat-box"); // Get the chat box element
    clearTeachOptions() // clear yes or no buttons if already displayed

    // Create a new element for the user's message
    var userMessageElement = document.createElement("div");
    userMessageElement.classList.add("message", "user-message");
    userMessageElement.textContent = userMessage;
    chatBox.appendChild(userMessageElement);

    // Create XMLHttpRequest object to send the user message to the backend for processing
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/process");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onload = function() {
        // executes only if response received
        if (xhr.status === 200) {
            var responseData = JSON.parse(xhr.responseText);
            var botMessage = responseData.response;
            var teach = responseData.teach;

            var botMessageElement = document.createElement("div");
            botMessageElement.classList.add("message", "bot-message");
            botMessageElement.textContent = botMessage;
            chatBox.appendChild(botMessageElement);
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom of the chat box

            // if teach flag is true, display yes no buttons and execute teach function accordingly
            if (teach) {
                var teachOptions = document.createElement("div");
                teachOptions.classList.add("teach-options");
                teachOptions.innerHTML = '<button onclick="teachBot(\'yes\')">Yes</button><button onclick="teachBot(\'no\')">No</button>';
                chatBox.appendChild(teachOptions);
            }
        }
    };
    xhr.send("user_input=" + encodeURIComponent(userMessage)); // Send the user message to backend
    document.getElementById("user-input").value = ""; // clear the input field for next question
});

// saves question and answer if clicked on yes, exit if no
function teachBot(choice) {
    var chatBox = document.getElementById("chat-box");
    var userResponse = document.getElementById("user-input").value.trim();
    // console.log(userResponse)

    // Remove the teach options
    clearTeachOptions()

    if (choice === 'no') {
        // Print "It's ok" message if the user chooses "No"
        var okMessage = document.createElement("div");
        okMessage.classList.add("message", "bot-message");
        okMessage.textContent = "It's ok!";
        chatBox.appendChild(okMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    } else if (choice === 'yes') {
        // Check if the user has entered a message, if no prompt to enter message
        if (userResponse === "") {
            var promptMessage = document.createElement("div");
            promptMessage.classList.add("message", "bot-message");
            promptMessage.textContent = "Please type something before pressing Yes.";
            chatBox.appendChild(promptMessage);
            chatBox.scrollTop = chatBox.scrollHeight;

            // Display the Yes/No buttons again
            var teachOptions = document.createElement("div");
            teachOptions.classList.add("teach-options");
            teachOptions.innerHTML = '<button onclick="teachBot(\'yes\')">Yes</button><button onclick="teachBot(\'no\')">No</button>';
            chatBox.appendChild(teachOptions);
        } else {
            // Send both the latest question and user's answer to the backend
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/teach");
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var responseData = JSON.parse(xhr.responseText);
                    var botMessage = responseData.response;

                    var botMessageElement = document.createElement("div");
                    botMessageElement.classList.add("message", "bot-message");
                    botMessageElement.textContent = botMessage;
                    chatBox.appendChild(botMessageElement);
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            };
            // Send the latest question and user's answer to the backend
            var data = "user_input=" + encodeURIComponent(latestQuestion) + "&answer=" + encodeURIComponent(userResponse);
            xhr.send(data);

            // Remove the Yes/No buttons
            clearTeachOptions()
        }
    }

    // Clear the user input field
    document.getElementById("user-input").value = "";
}
