(() => {
  const MAX_LENGTH = 300;

  const chat = document.getElementById("chat");
  const form = document.getElementById("ask-form");
  const input = document.getElementById("question");
  const sendBtn = document.getElementById("send-btn");
  const counter = document.getElementById("char-count");
  const clearBtn = document.getElementById("clear-btn");
  const chips = document.querySelectorAll(".chip");

  let busy = false;

  function addCarIcon(container, className) {
    const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    icon.setAttribute("class", className);
    icon.setAttribute("viewBox", "0 0 24 24");
    icon.setAttribute("aria-hidden", "true");
    icon.setAttribute("focusable", "false");

    const use = document.createElementNS("http://www.w3.org/2000/svg", "use");
    use.setAttribute("href", "#icon-car-front");
    icon.appendChild(use);
    container.appendChild(icon);
  }

  function timeNow() {
    return new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
  }

  function scrollToBottom() {
    chat.scrollTop = chat.scrollHeight;
  }

  function updateState() {
    sendBtn.disabled = busy || input.value.trim() === "";
    chips.forEach((chip) => (chip.disabled = busy));
    counter.textContent = input.value.length + "/" + MAX_LENGTH;
    counter.classList.toggle("near-limit", input.value.length >= MAX_LENGTH - 30);
  }

  // type: "bot", "user" or "bot error". textContent keeps messages safe from XSS.
  function addMessage(text, type) {
    const row = document.createElement("div");
    row.classList.add("msg", ...type.split(" "));

    if (type.startsWith("bot")) {
      const avatar = document.createElement("span");
      avatar.className = "avatar";
      avatar.setAttribute("aria-hidden", "true");
      addCarIcon(avatar, "avatar-icon");
      row.appendChild(avatar);
    }

    const content = document.createElement("div");
    content.className = "content";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    const meta = document.createElement("div");
    meta.className = "meta";
    meta.textContent = timeNow();

    content.append(bubble, meta);
    row.appendChild(content);
    chat.appendChild(row);
    scrollToBottom();
    return row;
  }

  function showTyping() {
    const row = document.createElement("div");
    row.className = "msg bot typing";
    row.setAttribute("aria-label", "Assistant is typing");

    const avatar = document.createElement("span");
    avatar.className = "avatar";
    avatar.setAttribute("aria-hidden", "true");
    addCarIcon(avatar, "avatar-icon");

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    for (let i = 0; i < 3; i++) {
      const dot = document.createElement("span");
      dot.className = "dot";
      bubble.appendChild(dot);
    }

    row.append(avatar, bubble);
    chat.appendChild(row);
    scrollToBottom();
    return row;
  }

  function addRetry(row, question) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "retry-btn";
    button.textContent = "Try again";
    button.addEventListener("click", () => {
      row.remove();
      askQuestion(question, true);
    });
    row.querySelector(".content").appendChild(button);
  }

  function showWelcome() {
    addMessage(
      "Hello! I'm the workshop assistant. Ask me about prices, opening hours, repairs, or bookings, or pick a topic below.",
      "bot"
    );
  }

  async function askQuestion(question, isRetry = false) {
    if (busy) return;
    busy = true;
    if (!isRetry) addMessage(question, "user");
    updateState();
    const typing = showTyping();

    try {
      const response = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question }),
      });
      const data = await response.json();
      typing.remove();

      if (response.ok) {
        addMessage(data.answer, "bot");
      } else {
        addMessage(data.error || "Something went wrong. Please try again.", "bot error");
      }
    } catch (err) {
      typing.remove();
      const row = addMessage("Could not reach the server. Please check your connection.", "bot error");
      addRetry(row, question);
    } finally {
      busy = false;
      updateState();
      if (window.matchMedia("(hover: hover)").matches) input.focus();
    }
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const question = input.value.trim();
    if (!question || busy) return;
    input.value = "";
    updateState();
    askQuestion(question);
  });

  input.addEventListener("input", updateState);

  chips.forEach((chip) => {
    chip.addEventListener("click", () => askQuestion(chip.dataset.question));
  });

  clearBtn.addEventListener("click", () => {
    if (busy) return;
    chat.innerHTML = "";
    showWelcome();
    input.focus();
  });

  showWelcome();
  updateState();
  // Avoid popping the keyboard open on touch devices
  if (window.matchMedia("(hover: hover)").matches) input.focus();
})();