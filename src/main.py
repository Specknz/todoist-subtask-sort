from todoist_api_python.api import TodoistAPI

api = TodoistAPI("YOUR_API_TOKEN")

task = api.get_task("6X4Vw2Hfmg73Q2XR")
print(f"Task: {task.content}")

comments_iter = api.get_comments(task_id=task.id)
for comments in comments_iter:
    for comment in comments:
        print(f"Comment: {comment.content}")