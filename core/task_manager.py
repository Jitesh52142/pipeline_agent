import logging

class TaskManager:
    """
    State machine that holds the JSON array of tasks, 
    tracks status (pending/done), and stores results.
    """
    def __init__(self):
        self.tasks = []

    def load_tasks(self, tasks):
        """
        Input: [ {id: 1, status: "pending", agent: "researcher"}, ... ]
        """
        self.tasks = []
        for i, task in enumerate(tasks):
            task_id = f"task_{i+1}"
            self.tasks.append({
                "id": task_id,
                "task": task["task"],
                "agent": task["agent"],
                "status": "pending",
                "result": None
            })
        logging.info(f"TaskManager: Tasks loaded: {self.tasks}")

    def find_pending_task(self):
        for task in self.tasks:
            if task["status"] == "pending":
                return task
        return None

    def mark_complete(self, task_id, result):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["result"] = result
                logging.info(f"TaskManager: Task {task_id} marked as completed")

    def all_tasks_completed(self):
        return all(task["status"] == "completed" for task in self.tasks)

    def get_results(self):
        return [task["result"] for task in self.tasks]