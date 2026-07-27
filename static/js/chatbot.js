function toggleChat() {
    const box = document.getElementById("chatBox");

    if (box.style.display === "block") {
        box.style.display = "none";
    } else {
        box.style.display = "block";
    }
}

function escapeChatText(value) {
    const node = document.createElement("div");
    node.textContent = value;
    return node.innerHTML;
}

async function sendChat() {
    const input = document.getElementById("chatInput");
    const messages = document.getElementById("chatMessages");

    const text = input.value.trim();

    if (!text) return;

    // USER MESSAGE
    messages.innerHTML += `
        <div class="message user-message">
            <div class="bubble user-bubble">
                ${escapeChatText(text)}
            </div>
        </div>
    `;

    input.value = "";

    // AUTO SCROLL
    messages.scrollTop = messages.scrollHeight;

    // TYPING ANIMATION
    const typingId = "typing-" + Date.now();

    messages.innerHTML += `
        <div class="message bot-message" id="${typingId}">
            <div class="bubble bot-bubble typing">
                MindCare AI is typing...
            </div>
        </div>
    `;

    messages.scrollTop = messages.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: text
            })
        });

        const data = await response.json();

        // REMOVE TYPING
        document.getElementById(typingId).remove();

        // BOT RESPONSE
        messages.innerHTML += `
            <div class="message bot-message">
                <div class="bubble bot-bubble">
                    ${escapeChatText(data.reply)}
                </div>
            </div>
        `;

        messages.scrollTop = messages.scrollHeight;

    } catch (error) {

        document.getElementById(typingId).remove();

        messages.innerHTML += `
            <div class="message bot-message">
                <div class="bubble bot-bubble error-bubble">
                    Sorry, something went wrong.
                </div>
            </div>
        `;
    }
}

// ENTER KEY SUPPORT
document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("chatInput");

    if (input) {
        input.addEventListener("keypress", function(event) {

            if (event.key === "Enter") {
                event.preventDefault();
                sendChat();
            }

        });
    }

});
