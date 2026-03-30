import logging

class TaskScheduler:
    """
    Logic engine that decides what runs next. 
    Simple systems use linear lists; complex ones use DAGs.
    """
    def __init__(self, task_manager):
        self.task_manager = task_manager

    def next_task(self):
        """
        Logic engine that decides what runs next.
        """
        next_task = self.task_manager.find_pending_task()
        if next_task:
            logging.info(f"TaskScheduler: Selected next task {next_task['id']}")
            return next_task
        else:
            logging.info("TaskScheduler: All tasks completed.")
            return None