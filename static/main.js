const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatContainer = document.getElementById("chat-container");

function addStatusMessage(text, type = "info") {
    const status = document.createElement("div");
    status.classList.add("status-update", type);
    status.innerText = text;
    chatContainer.appendChild(status);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return status;
}

function addAgentResult(agentId, task, result) {
    const wrapper = document.createElement("div");
    wrapper.classList.add("agent-card");

    const header = document.createElement("div");
    header.classList.add("agent-card-header");
    
    // Map icons/emojis to agents
    const icons = {
        "research_agent": "🔍",
        "analysis_agent": "📊",
        "writer_agent": "✍️"
    };
    const icon = icons[agentId] || "🤖";

    header.innerHTML = `<span class="agent-icon">${icon}</span> <span class="agent-name">${agentId.replace('_', ' ').toUpperCase()}</span>`;
    wrapper.appendChild(header);

    const taskText = document.createElement("div");
    taskText.classList.add("agent-task-desc");
    taskText.innerText = "Task: " + task;
    wrapper.appendChild(taskText);

    const resultBox = document.createElement("div");
    resultBox.classList.add("agent-result-box");
    resultBox.innerText = result;
    wrapper.appendChild(resultBox);

    chatContainer.appendChild(wrapper);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // User Message
    const userMsg = document.createElement("div");
    userMsg.classList.add("user-query");
    userMsg.innerHTML = `<h3>Plan for: ${text}</h3>`;
    chatContainer.appendChild(userMsg);

    userInput.value = "";
    userInput.disabled = true;
    sendBtn.disabled = true;

    // Step 1: Planning
    const planStatus = addStatusMessage("🧠 Orchestrating global plan...", "pending");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        planStatus.remove();

        if (data.status === "success") {
            addStatusMessage(`✅ Deployed ${data.results.length} agents successfully.`, "success");

            // Show individual agent cards
            data.results.forEach(res => {
                addAgentResult(res.agent, res.task, res.result);
            });

            addStatusMessage("🏁 Pipeline execution complete.", "success");
        } else {
            addStatusMessage("❌ System Failure: " + data.message, "error");
        }
    } catch (err) {
        addStatusMessage("❌ Connection Lost: " + err, "error");
    } finally {
        userInput.disabled = false;
        sendBtn.disabled = false;
    }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});