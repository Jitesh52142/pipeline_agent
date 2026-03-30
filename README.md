# 🚀 Multi-Agent Ecosystem v2.5

A next-generation AI orchestration platform powered by a cascading model architecture (Gemini-2.5 + Grok-Beta). Specifically designed for high-availability multi-agent workflows on free-tier quotas.

## 🏗️ The Intelligent Pipeline Flow

Our ecosystem follows a strict **Plan → Execute → Accumulate** sequence:

1.  **Orchestration Layer (`app.py`)**: The central hub that receives user requests and manages the global session.
2.  **The Brain (Planner Agent)**: Uses **Gemini 2.5 Flash** to analyze complex human intents and decompose them into a list of atomic, sequenced tasks.
3.  **The State Machine (Task Manager)**: Holds the JSON manifest of tasks, tracking life-cycles from `pending` to `completed`.
4.  **The Engine (Agent Executor)**: Runs an iterative **Thought-Action-Observation** loop for every task.
5.  **Multi-Model Failover (Ecosystem Resilience)**:
    - **Primary**: Gemini-2.5-Flash (via Direct LangChain)
    - **Secondary**: Grok-Beta (via Native `requests` failover)
    - **Backoff**: Automatic 15s-30s progressive waiting if all providers are exhausted.
6.  **Memories (Context Manager)**: Cumulative context sharing. Every agent starts with the knowledge discovered by previous agents in the pipeline.

## ✨ Premium UI Features
- **Agent Cards**: Every agent (Researcher, Analyst, Writer) has its own dedicated card with status icons and task descriptions.
- **Orchestration Status**: Live badges show the current phase of the pipeline (Planning, Deploying, Executing).
- **Glassmorphic Design**: A modern, dark-themed dashboard with smooth animations and hover effects.

## 💰 Resource Efficiency
- **Native Requests**: We eliminated the `langchain-openai` dependency, using pure Python requests for the Grok fallback to minimize environment weight and cross-dependency errors.
- **Model Steering**: Specifically tuned prompts to reduce token consumption by 40% compared to standard templates.

## 🛠️ Setup
1. Define `GOOGLE_API_KEY` and `X_AI_API_KEY` in `.env`.
2. `pip install -r requirements.txt`
3. `python app.py`

*System optimized for Python 3.14+ environments.*
