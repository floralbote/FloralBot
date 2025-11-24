document.addEventListener("DOMContentLoaded", () => {

const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

async function sendMessageToBackend(message) {
    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    return data.response;
}

function appendMessage(content, sender) {
    const bubble = document.createElement("div");
    bubble.classList.add(
        "max-w-[80%]", "py-2", "px-4", "rounded-xl", "text-sm", "shadow"
    );

    if (sender === "user") {
        bubble.classList.add(
            "bg-green-600", "text-white", "self-end", "ml-auto"
        );
    } else {
        bubble.classList.add(
            "bg-white/90", "text-green-800", "border", "border-gray-200"
        );
    }

    bubble.textContent = content;
    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    input.value = "";

    const loadingMsg = document.createElement("div");
    loadingMsg.className = "text-green-700 text-sm italic";
    loadingMsg.textContent = "Digitando...";
    chatBox.appendChild(loadingMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    const botReply = await sendMessageToBackend(message);

    loadingMsg.remove();
    appendMessage(botReply, "bot");
});

});



