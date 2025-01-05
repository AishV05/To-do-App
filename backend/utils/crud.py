from routers.models import Task
from .db import tasks_collection
from bson import ObjectId
from bson.errors import InvalidId
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_task(task: Task):
    task_data = task.dict()
    tasks_collection.insert_one(task_data)
    return task

async def get_all_task():
    tasks = await tasks_collection.find().to_list(None)
    for task in tasks:
        task['_id'] = str(task['_id']) 
    return tasks


async def update_task(task_id: str, update_data: dict):
    try:
        object_id = ObjectId(task_id)  
    except InvalidId:
        logging.warning(f"Invalid task ID format: {task_id}")
        return None

    og_task = await tasks_collection.find_one({"_id": object_id})  

    if not og_task:
        logging.warning(f"Task with ID {task_id} not found")
        return None

    changes = []
    for key, value in update_data.items():
        if key in og_task and og_task[key] != value:
            changes.append((key, og_task[key], value))
            og_task[key] = value

    if not changes:
        logging.info(f"No changes to apply for task ID {task_id}")
        return og_task

    result = await tasks_collection.update_one(
        {"_id": object_id},  # Update by ObjectId
        {"$set": update_data}
    )

    if result.modified_count == 0:
        logging.error(f"Failed to update task with ID {task_id}")
        return None

    updated_task = await tasks_collection.find_one({"_id": object_id})
    return updated_task


async def delete_task(task_id: str):
    try:
        object_id = ObjectId(task_id)  # Convert task_id to ObjectId
    except InvalidId:
        logging.warning(f"Invalid task ID format: {task_id}")
        return False

    result = await tasks_collection.delete_one({"_id": object_id})  # Query by ObjectId
    return result.deleted_count > 0