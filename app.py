from flask import Flask, request, jsonify, render_template
import logging
import os

# Core components
from agents.planner_agent import PlannerAgent
from core.task_manager import TaskManager
from core.task_scheduler import TaskScheduler
from core.agent_executor import AgentExecutor
from core.context_manager import ContextManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# -----------------------------
# Initialize System Components
# -----------------------------
# In a real system, these would be initialized per-session 
# if you need multi-user support.

planner = PlannerAgent()
task_manager = TaskManager()
context_manager = ContextManager()
executor = AgentExecutor(context_manager)
scheduler = TaskScheduler(task_manager)

# -----------------------------
# Home Route
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# Chat Route (Request Handler)
# -----------------------------

@app.route("/chat", methods=["POST"])
def chat():
    """
    Entry point for the API. Validates input and initializes the session memory.
    """
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' field"}), 400

        user_request = data["message"]
        logging.info(f"App: Received Request -> {user_request}")

        # Step 1: Planner Agent
        # The 'Brain' that decomposes high-level requests into atomic tasks.
        tasks = planner.plan(user_request)
        if not tasks:
            return jsonify({
                "status": "error",
                "message": "Planner failed to decompose request into tasks."
            }), 500

        # Step 2: Task Manager (State machine)
        # State machine that holds the JSON array of tasks, tracks status (pending/done).
        task_manager.load_tasks(tasks)

        # Step 3: Core Execution Loop
        # while tasks_remaining: 
        #   1. Get next task
        #   2. Execute agent
        #   3. Update context
        results = []

        while not task_manager.all_tasks_completed():
            # 3.1: Task Scheduler
            # Logic engine that decides what runs next.
            task = scheduler.next_task()
            if not task:
                break

            logging.info(f"App: Scheduling {task['id']} for {task['agent']}")

            # 3.2: Agent Executor (Thought-Action-Observation loop)
            # The runtime loop for a specific agent.
            result = executor.execute(task)

            # 3.3: Mark task complete and save result to memory
            task_manager.mark_complete(task["id"], result)

            # 3.4: Context Manager (Memory update)
            # Maintains the 'Short Term Memory'. Critical for agents to know previous discoveries.
            context_manager.add_to_context(task["agent"], task["task"], result)

            results.append({
                "task_id": task["id"],
                "task": task["task"],
                "agent": task["agent"],
                "result": result
            })

        # Step 4: Final Response
        return jsonify({
            "status": "success",
            "results": results,
            "final_context": context_manager.get_context()
        })

    except Exception as e:
        logging.error(f"App: Critical error in processing request: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# -----------------------------
# Run Server
# -----------------------------

if __name__ == "__main__":
    # Create required folders if they don't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')

    app.run(debug=True, port=5000)