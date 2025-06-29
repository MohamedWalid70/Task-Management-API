from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from .database import get_session
from .models import (
    Task, TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    TaskStatus, TaskPriority, HealthResponse, APIInfo, TaskFilters,
    TaskSort, BulkTaskUpdate, BulkTaskDelete, SortField, SortOrder
)
from .crud import TaskCRUD

router = APIRouter()


@router.get("/", response_model=APIInfo, tags=["API Information"])
async def get_api_info():
    """Get API information and available endpoints"""
    return APIInfo(
        name="Task Management API",
        version="1.0.0",
        description="A comprehensive RESTful API for managing tasks with full CRUD operations, filtering, and pagination",
        endpoints={
            "GET /": "API information",
            "GET /health": "Health check",
            "POST /tasks": "Create a new task",
            "GET /tasks": "List all tasks with advanced filtering and pagination",
            "GET /tasks/{task_id}": "Get a specific task",
            "PUT /tasks/{task_id}": "Update a task",
            "DELETE /tasks/{task_id}": "Delete a task",
            "GET /tasks/status/{status}": "Get tasks by status",
            "GET /tasks/priority/{priority}": "Get tasks by priority",
            "GET /tasks/search": "Search tasks by title/description",
            "POST /tasks/bulk-update": "Bulk update multiple tasks",
            "POST /tasks/bulk-delete": "Bulk delete multiple tasks"
        }
    )


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health status"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow()
    )


@router.post("/tasks", response_model=TaskResponse, status_code=201, tags=["Tasks"])
async def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session)
):
    """Create a new task"""
    try:
        task_data = task.dict()
        created_task = TaskCRUD.create_task(session, task_data)
        return TaskResponse.from_orm(created_task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create task: {str(e)}")


@router.get("/tasks", response_model=TaskListResponse, tags=["Tasks"])
async def get_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by task priority"),
    assigned_to: Optional[str] = Query(None, description="Filter by assignee"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    due_date_from: Optional[datetime] = Query(None, description="Filter tasks due from this date"),
    due_date_to: Optional[datetime] = Query(None, description="Filter tasks due until this date"),
    created_from: Optional[datetime] = Query(None, description="Filter tasks created from this date"),
    created_to: Optional[datetime] = Query(None, description="Filter tasks created until this date"),
    sort_field: SortField = Query(SortField.created_at, description="Field to sort by"),
    sort_order: SortOrder = Query(SortOrder.desc, description="Sort order"),
    session: Session = Depends(get_session)
):
    """Get all tasks with advanced filtering, sorting, and pagination"""
    try:
        tasks, total = TaskCRUD.get_tasks(
            session, 
            skip=skip, 
            limit=limit, 
            status=status, 
            priority=priority,
            assigned_to=assigned_to,
            search=search,
            due_date_from=due_date_from,
            due_date_to=due_date_to,
            created_from=created_from,
            created_to=created_to,
            sort_field=sort_field,
            sort_order=sort_order
        )
        
        task_responses = [TaskResponse.from_orm(task) for task in tasks]
        
        return TaskListResponse(
            tasks=task_responses,
            total=total,
            skip=skip,
            limit=limit,
            has_more=(skip + limit) < total
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve tasks: {str(e)}")


@router.get("/tasks/search", response_model=TaskListResponse, tags=["Tasks"])
async def search_tasks(
    q: str = Query(..., description="Search term for title and description"),
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    session: Session = Depends(get_session)
):
    """Search tasks by title and description"""
    try:
        tasks, total = TaskCRUD.search_tasks(session, q, skip=skip, limit=limit)
        
        task_responses = [TaskResponse.from_orm(task) for task in tasks]
        
        return TaskListResponse(
            tasks=task_responses,
            total=total,
            skip=skip,
            limit=limit,
            has_more=(skip + limit) < total
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to search tasks: {str(e)}")


@router.get("/tasks/status/{status}", response_model=TaskListResponse, tags=["Tasks"])
async def get_tasks_by_status(
    status: TaskStatus,
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    session: Session = Depends(get_session)
):
    """Get tasks filtered by status"""
    try:
        tasks, total = TaskCRUD.get_tasks_by_status(session, status, skip=skip, limit=limit)
        
        task_responses = [TaskResponse.from_orm(task) for task in tasks]
        
        return TaskListResponse(
            tasks=task_responses,
            total=total,
            skip=skip,
            limit=limit,
            has_more=(skip + limit) < total
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve tasks by status: {str(e)}")


@router.get("/tasks/priority/{priority}", response_model=TaskListResponse, tags=["Tasks"])
async def get_tasks_by_priority(
    priority: TaskPriority,
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    session: Session = Depends(get_session)
):
    """Get tasks filtered by priority"""
    try:
        tasks, total = TaskCRUD.get_tasks_by_priority(session, priority, skip=skip, limit=limit)
        
        task_responses = [TaskResponse.from_orm(task) for task in tasks]
        
        return TaskListResponse(
            tasks=task_responses,
            total=total,
            skip=skip,
            limit=limit,
            has_more=(skip + limit) < total
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve tasks by priority: {str(e)}")


@router.post("/tasks/bulk-update", tags=["Tasks"])
async def bulk_update_tasks(
    bulk_update: BulkTaskUpdate,
    session: Session = Depends(get_session)
):
    """Bulk update multiple tasks"""
    try:
        updated_count, total_count = TaskCRUD.bulk_update_tasks(
            session, 
            bulk_update.task_ids, 
            bulk_update.updates.dict(exclude_none=True)
        )
        
        return {
            "message": f"Successfully updated {updated_count} out of {total_count} tasks",
            "updated_count": updated_count,
            "total_count": total_count
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to bulk update tasks: {str(e)}")


@router.post("/tasks/bulk-delete", tags=["Tasks"])
async def bulk_delete_tasks(
    bulk_delete: BulkTaskDelete,
    session: Session = Depends(get_session)
):
    """Bulk delete multiple tasks"""
    try:
        deleted_count, total_count = TaskCRUD.bulk_delete_tasks(session, bulk_delete.task_ids)
        
        return {
            "message": f"Successfully deleted {deleted_count} out of {total_count} tasks",
            "deleted_count": deleted_count,
            "total_count": total_count
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to bulk delete tasks: {str(e)}")


@router.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def get_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific task by ID"""
    task = TaskCRUD.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskResponse.from_orm(task)


@router.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    """Update an existing task"""
    # Remove None values from the update data
    update_data = {k: v for k, v in task_update.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    try:
        updated_task = TaskCRUD.update_task(session, task_id, update_data)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return TaskResponse.from_orm(updated_task)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update task: {str(e)}")


@router.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
async def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    """Delete a task"""
    success = TaskCRUD.delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found") 