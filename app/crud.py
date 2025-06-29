from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Session, select, func, desc, asc, or_
from .models import Task, TaskStatus, TaskPriority, SortField, SortOrder


class TaskCRUD:
    """CRUD operations for Task model"""

    @staticmethod
    def create_task(session: Session, task_data: dict) -> Task:
        """Create a new task"""
        task = Task(**task_data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task(session: Session, task_id: int) -> Optional[Task]:
        """Get a task by ID"""
        statement = select(Task).where(Task.id == task_id)
        return session.exec(statement).first()

    @staticmethod
    def get_tasks(
        session: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        assigned_to: Optional[str] = None,
        search: Optional[str] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        sort_field: SortField = SortField.created_at,
        sort_order: SortOrder = SortOrder.desc
    ) -> tuple[List[Task], int]:
        """Get tasks with advanced filtering, sorting, and pagination"""
        statement = select(Task)
        
        # Apply filters
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if assigned_to:
            statement = statement.where(Task.assigned_to == assigned_to)
        if search:
            search_term = f"%{search}%"
            statement = statement.where(
                or_(
                    Task.title.ilike(search_term),  # type: ignore
                    Task.description.ilike(search_term)  # type: ignore
                )
            )
        if due_date_from:
            statement = statement.where(Task.due_date >= due_date_from)  # type: ignore
        if due_date_to:
            statement = statement.where(Task.due_date <= due_date_to)  # type: ignore
        if created_from:
            statement = statement.where(Task.created_at >= created_from)
        if created_to:
            statement = statement.where(Task.created_at <= created_to)
        
        # Get total count with same filters
        count_statement = select(func.count(Task.id))  # type: ignore
        if status:
            count_statement = count_statement.where(Task.status == status)
        if priority:
            count_statement = count_statement.where(Task.priority == priority)
        if assigned_to:
            count_statement = count_statement.where(Task.assigned_to == assigned_to)
        if search:
            search_term = f"%{search}%"
            count_statement = count_statement.where(
                or_(
                    Task.title.ilike(search_term),  # type: ignore
                    Task.description.ilike(search_term)  # type: ignore
                )
            )
        if due_date_from:
            count_statement = count_statement.where(Task.due_date >= due_date_from)  # type: ignore
        if due_date_to:
            count_statement = count_statement.where(Task.due_date <= due_date_to)  # type: ignore
        if created_from:
            count_statement = count_statement.where(Task.created_at >= created_from)
        if created_to:
            count_statement = count_statement.where(Task.created_at <= created_to)
        
        total = session.exec(count_statement).first() or 0
        
        # Apply sorting
        sort_column = getattr(Task, sort_field.value)  # type: ignore
        if sort_order == SortOrder.asc:
            statement = statement.order_by(asc(sort_column))
        else:
            statement = statement.order_by(desc(sort_column))
        
        # Apply pagination
        statement = statement.offset(skip).limit(limit)
        tasks = session.exec(statement).all()
        
        return list(tasks), total

    @staticmethod
    def update_task(session: Session, task_id: int, task_data: dict) -> Optional[Task]:
        """Update an existing task"""
        task = TaskCRUD.get_task(session, task_id)
        if not task:
            return None
        
        # Update fields
        for field, value in task_data.items():
            if value is not None:
                setattr(task, field, value)
        
        # Update the updated_at timestamp
        task.updated_at = datetime.now(timezone.utc)
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: int) -> bool:
        """Delete a task"""
        task = TaskCRUD.get_task(session, task_id)
        if not task:
            return False
        
        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def get_tasks_by_status(session: Session, status: TaskStatus, skip: int = 0, limit: int = 100) -> tuple[List[Task], int]:
        """Get tasks by status with pagination"""
        return TaskCRUD.get_tasks(session, skip, limit, status=status)

    @staticmethod
    def get_tasks_by_priority(session: Session, priority: TaskPriority, skip: int = 0, limit: int = 100) -> tuple[List[Task], int]:
        """Get tasks by priority with pagination"""
        return TaskCRUD.get_tasks(session, skip, limit, priority=priority)

    @staticmethod
    def bulk_update_tasks(session: Session, task_ids: List[int], updates: dict) -> tuple[int, int]:
        """Bulk update multiple tasks"""
        # Get tasks that exist
        statement = select(Task).where(Task.id.in_(task_ids))  # type: ignore
        tasks = session.exec(statement).all()
        
        if not tasks:
            return 0, 0
        
        updated_count = 0
        for task in tasks:
            # Update fields
            for field, value in updates.items():
                if value is not None:
                    setattr(task, field, value)
            
            # Update the updated_at timestamp
            task.updated_at = datetime.now(timezone.utc)
            session.add(task)
            updated_count += 1
        
        session.commit()
        return updated_count, len(task_ids)

    @staticmethod
    def bulk_delete_tasks(session: Session, task_ids: List[int]) -> tuple[int, int]:
        """Bulk delete multiple tasks"""
        # Get tasks that exist
        statement = select(Task).where(Task.id.in_(task_ids))  # type: ignore
        tasks = session.exec(statement).all()
        
        if not tasks:
            return 0, 0
        
        deleted_count = 0
        for task in tasks:
            session.delete(task)
            deleted_count += 1
        
        session.commit()
        return deleted_count, len(task_ids)

    @staticmethod
    def search_tasks(session: Session, search_term: str, skip: int = 0, limit: int = 100) -> tuple[List[Task], int]:
        """Search tasks by title and description"""
        return TaskCRUD.get_tasks(session, skip, limit, search=search_term) 