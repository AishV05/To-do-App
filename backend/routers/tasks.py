from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from bson import ObjectId
from bson.errors import InvalidId
from utils.db import tasks_collection
from utils.auth import get_current_user
from .models import Task, CustomJSONEncoder, statusUpdate, descriptionUpdate, titleUpdate
import logging
import json
from utils.crud import create_task, get_all_task, update_task, delete_task
from fastapi.encoders import jsonable_encoder

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/tasks")
async def create_task_endpoint(task: Task, current_user: dict = Depends(get_current_user)):
    logger.info(f"User '{current_user}' is creating a task with data: {task}")
    task_data = await create_task(task)
    if not task_data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Task creation failed")
    return task_data

@router.get("/tasks", response_model=List[Task])
async def get_all_tasks_endpoint(current_user: dict = Depends(get_current_user)):
    
    task_data = await get_all_task()
    if task_data is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return json.loads(json.dumps(task_data, cls=CustomJSONEncoder))

@router.put("/tasks/{task_id}/status", response_model=Task)
async def update_status(task_id: str, update: statusUpdate, user: dict = Depends(get_current_user)):
    updated_task = await update_task(task_id, update.dict(exclude_unset=True))
    
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or update failed")
    
    logger.info(f"status: {updated_task['status']}")
    return updated_task

@router.put("/tasks/{task_id}/title", response_model=Task)
async def update_title(task_id: str, update: titleUpdate, user: dict = Depends(get_current_user)):
    updated_task = await update_task(task_id, update.dict(exclude_unset=True))
    
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or update failed")
    
    logger.info(f"title: {updated_task['title']}")
    return updated_task
@router.put("/tasks/{task_id}/description", response_model=Task)
async def update_description(task_id: str, update: descriptionUpdate, user: dict = Depends(get_current_user)):
    updated_task = await update_task(task_id, update.dict(exclude_unset=True))
    
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or update failed")
    
    logger.info(f"description: {updated_task}")
    return updated_task


@router.delete("/tasks/{task_id}")
async def delete_task_endpoint(task_id: str, user: dict = Depends(get_current_user)):
    logger.info(f"User '{user}' is attempting to delete task with ID: {task_id}")

    deleted = await delete_task(task_id)
    if not deleted:
        logger.warning(f"Task with ID {task_id} not found or deletion failed")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or deletion failed"
        )
    
    logger.info(f"Task with ID {task_id} successfully deleted")
    return {"message": "Task deleted successfully"}


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task_by_id(task_id: str, user: dict = Depends(get_current_user)):
    """
    Fetch a task by its ID.
    """
    logger.info(f"User '{user}' is requesting task with ID: {task_id}")
    
    try:
        # Convert task_id to ObjectId
        object_id = ObjectId(task_id)
    except InvalidId:
        logger.warning(f"Invalid task ID format: {task_id}")
        raise HTTPException(
            status_code=400, detail="Invalid task ID format"
        )
    
    # Fetch the task from the database
    task = await tasks_collection.find_one({"_id": object_id})
    
    if not task:
        logger.warning(f"Task with ID {task_id} not found")
        raise HTTPException(
            status_code=404, detail="Task not found"
        )
    
    # Convert ObjectId to string for JSON serialization
    task["_id"] = str(task["_id"])
    logger.info(f"Task with ID {task_id} successfully retrieved: {task}")
    return task