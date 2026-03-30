import logging

class ContextManager:
    """
    Maintains the 'Short Term Memory'. Critical for agents to know what 
    previous agents discovered.
    """
    def __init__(self, window_size=4000):
        self.context_window = window_size
        self.history = []
        self.cumulative_context = ""

    def add_to_context(self, agent_name, task, result):
        entry = f"\nAgent: {agent_name}\nTask: {task}\nResult: {result}\n"
        self.history.append({
            "agent": agent_name,
            "task": task,
            "result": result
        })
        self.cumulative_context += entry
        logging.info(f"Context updated with result from {agent_name}")

    def get_context(self):
        # In a real system, we'd truncate based on tokens, 
        # but for simplicity, we'll return the whole string here.
        return self.cumulative_context

    def clear(self):
        self.history = []
        self.cumulative_context = ""
