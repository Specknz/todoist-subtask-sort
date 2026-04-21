import os
import datetime
import logging
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI
from task_order import TaskOrder

load_dotenv()

API = TodoistAPI(os.environ["TODOIST_API_TOKEN"])
TASK_ID = os.environ["TASK_ID"]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Fetches subtasks for the configured parent task, sorts them by due date
    ascending (tasks with no due date first), and updates their order in Todoist."""

    logbook_tasks = API.get_tasks(parent_id=TASK_ID)

    taskOrders: list[TaskOrder] = []

    for tasks in logbook_tasks:
        for task in tasks:
            taskOrder = TaskOrder(
                id=task.id, 
                content=task.content,
                due_date=task.due.date if task.due else None, 
                current_order=task.order)
            taskOrders.append(taskOrder)
                
    taskOrders.sort(key=lambda x: x.due_date if x.due_date is not None else datetime.date.min)
    
    new_order = 0
    for taskOrder in taskOrders:
        new_order += 1
        
        if (taskOrder.current_order == new_order):
            continue
        
        logging.log(
            logging.INFO, 
            f"Updating order: ({taskOrder.id}, {taskOrder.content}) - {taskOrder.current_order} -> {new_order}")
        try:
            API.update_task(task_id=taskOrder.id, order=new_order)
        except Exception as ex:
            logging.log(logging.ERROR, f"Error updating task order: {ex}")
            break
        
        
if __name__ == "__main__":
    main()