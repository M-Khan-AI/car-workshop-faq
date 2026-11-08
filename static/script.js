const form = document.getElementById("ask-form");
const input = document.getElementById("question");
const sendBtn = document.getElementById("send-btn");
const chat = document.getElementById("chat");

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = "message " + type;
  div.textContent = text; // textContent (not innerHTML) keeps it safe from XSS
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

async function askQuestion(question) {
  addMessage(question, "user");
  const loading = addMessage("Thinking...", "bot loading");
  sendBtn.disabled = true;

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question }),
    });
    const data = await response.json();
    loading.remove();

    if (response.ok) {
      addMessage(data.answer, "bot");
    } else {
      addMessage(data.error || "Something went wrong.", "bot error");
    }
  } catch (err) {
    loading.remove();
    addMessage("Could not reach the server. Please try again.", "bot error");
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (!question) return;
  input.value = "";
  askQuestion(question);
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => askQuestion(chip.textContent));
});