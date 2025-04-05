async function sendMessage() {
    let inputField = document.getElementById("user-input");
    let chatBox = document.getElementById("chat-box");
    let loading = document.getElementById("loading");
    let greetUser = document.getElementById("greet-user");
    let userMessage = inputField.value.trim();

    if (!userMessage) return;
    greetUser.classList.add("hidden");

    // Add user's message
    let userBubble = document.createElement("div");
    userBubble.className = "message user self-end";
    userBubble.textContent = userMessage;
    chatBox.appendChild(userBubble);

    inputField.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Show loading
    loading.classList.remove("hidden");

    try {
        let response = await fetch("/models/chat/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: userMessage })
        });

        let data = await response.json();

        // Hide loading
        loading.classList.add("hidden");

        // Show bot response
        let botBubble = document.createElement("div");
        botBubble.className = "message bot self-start";
        botBubble.textContent = data.response;
        chatBox.appendChild(botBubble);
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        loading.classList.add("hidden");
        let errorBubble = document.createElement("div");
        errorBubble.className = "message bot self-start text-red-500";
        errorBubble.textContent = "Something went wrong. Please try again.";
        chatBox.appendChild(errorBubble);
    }
}
