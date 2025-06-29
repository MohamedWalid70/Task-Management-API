from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from sqlmodel import SQLModel, Field as SQLField


class TaskStatus(str, Enum):
    """Task status enumeration"""
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class TaskPriority(str, Enum):
    """Task priority enumeration"""
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class SortField(str, Enum):
    """Sort field enumeration"""
    id = "id"
    title = "title"  # type: ignore
    status = "status"
    priority = "priority"
    created_at = "created_at"
    updated_at = "updated_at"
    due_date = "due_date"
    assigned_to = "assigned_to"


class SortOrder(str, Enum):
    """Sort order enumeration"""
    asc = "asc"
    desc = "desc"


class Task(SQLModel, table=True):
    """Task database model"""
    id: Optional[int] = SQLField(default=None, primary_key=True)
    title: str = SQLField(max_length=200, nullable=False)
    description: Optional[str] = SQLField(max_length=1000, nullable=True)
    status: TaskStatus = SQLField(default=TaskStatus.pending, nullable=False)
    priority: TaskPriority = SQLField(default=TaskPriority.medium, nullable=False)
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = SQLField(default=None, nullable=True)
    due_date: Optional[datetime] = SQLField(default=None, nullable=True)
    assigned_to: Optional[str] = SQLField(max_length=100, nullable=True)


class TaskCreate(BaseModel):
    """Model for creating a new task"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.pending, description="Task status")
    priority: TaskPriority = Field(default=TaskPriority.medium, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Task deadline")
    assigned_to: Optional[str] = Field(None, max_length=100, description="Assignee name")

    @validator('title')
    def validate_title(cls, v):
        """Validate and sanitize title"""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()

    @validator('due_date')
    def validate_due_date(cls, v):
        """Validate due date is in the future"""
        if v:
            now = datetime.now(timezone.utc)
            # Make v timezone-aware if it's naive
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)
            if v <= now:
                raise ValueError('Due date must be in the future')
        return v


class TaskUpdate(BaseModel):
    """Model for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")
    priority: Optional[TaskPriority] = Field(None, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Task deadline")
    assigned_to: Optional[str] = Field(None, max_length=100, description="Assignee name")

    @validator('title')
    def validate_title(cls, v):
        """Validate and sanitize title"""
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Title cannot be empty or whitespace only')
            return v.strip()
        return v

    @validator('due_date')
    def validate_due_date(cls, v):
        """Validate due date is in the future"""
        if v:
            now = datetime.now(timezone.utc)
            # Make v timezone-aware if it's naive
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)
            if v <= now:
                raise ValueError('Due date must be in the future')
        return v


class TaskResponse(BaseModel):
    """Model for task API responses"""
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: Optional[datetime]
    due_date: Optional[datetime]
    assigned_to: Optional[str]

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Model for paginated task list responses"""
    tasks: list[TaskResponse]
    total: int
    skip: int
    limit: int
    has_more: bool


class TaskFilters(BaseModel):
    """Model for advanced task filtering"""
    status: Optional[TaskStatus] = Field(None, description="Filter by task status")
    priority: Optional[TaskPriority] = Field(None, description="Filter by task priority")
    assigned_to: Optional[str] = Field(None, description="Filter by assignee")
    search: Optional[str] = Field(None, description="Search in title and description")
    due_date_from: Optional[datetime] = Field(None, description="Filter tasks due from this date")
    due_date_to: Optional[datetime] = Field(None, description="Filter tasks due until this date")
    created_from: Optional[datetime] = Field(None, description="Filter tasks created from this date")
    created_to: Optional[datetime] = Field(None, description="Filter tasks created until this date")


class TaskSort(BaseModel):
    """Model for task sorting"""
    field: SortField = Field(default=SortField.created_at, description="Field to sort by")
    order: SortOrder = Field(default=SortOrder.desc, description="Sort order")


class BulkTaskUpdate(BaseModel):
    """Model for bulk task updates"""
    task_ids: List[int] = Field(..., description="List of task IDs to update")
    updates: TaskUpdate = Field(..., description="Updates to apply to all tasks")

    @validator('task_ids')
    def validate_task_ids(cls, v):
        """Validate task IDs list length"""
        if len(v) < 1:
            raise ValueError('At least one task ID is required')
        if len(v) > 100:
            raise ValueError('Maximum 100 task IDs allowed')
        return v


class BulkTaskDelete(BaseModel):
    """Model for bulk task deletion"""
    task_ids: List[int] = Field(..., description="List of task IDs to delete")

    @validator('task_ids')
    def validate_task_ids(cls, v):
        """Validate task IDs list length"""
        if len(v) < 1:
            raise ValueError('At least one task ID is required')
        if len(v) > 100:
            raise ValueError('Maximum 100 task IDs allowed')
        return v


class HealthResponse(BaseModel):
    """Model for health check response"""
    status: str
    timestamp: datetime
    version: str = "1.0.0"


class APIInfo(BaseModel):
    """Model for API information response"""
    name: str
    version: str
    description: str
    endpoints: dict[str, str] 