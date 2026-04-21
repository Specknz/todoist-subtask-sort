import os
import datetime
from dataclasses import dataclass
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task

load_dotenv()

@dataclass
class TaskOrder:
    id: str
    due_date: datetime.date | None

API = TodoistAPI(os.environ["TODOIST_API_TOKEN"])
TASK_ID = os.environ["TASK_ID"]


def main():
    """Fetches subtasks for the configured parent task, sorts them by due date
    ascending (tasks with no due date first), and updates their order in Todoist."""

    logbook_tasks = API.get_tasks(parent_id=TASK_ID)

    taskOrders: list[TaskOrder] = []

    for tasks in logbook_tasks:
        for task in tasks:
            taskOrder = TaskOrder(id=task.id, due_date=task.due.date if task.due else None)
            taskOrders.append(taskOrder)
                
    taskOrders.sort(key=lambda x: x.due_date if x.due_date is not None else datetime.date.min)
        
    new_order = 1
    for taskOrder in taskOrders:
        API.update_task(task_id=taskOrder.id, order=new_order)
        new_order += 1
        
        
if __name__ == "__main__":
    main()