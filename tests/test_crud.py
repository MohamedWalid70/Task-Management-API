import pytest
from datetime import datetime, timezone, timedelta
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from app.models import Task, TaskStatus, TaskPriority, SortField, SortOrder
from app.crud import TaskCRUD


@pytest.fixture
def session():
    """Create a test database session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create tables
    from app.models import Task
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session


@pytest.fixture
def sample_tasks(session):
    """Create sample tasks for testing"""
    tasks_data = [
        {
            "title": "Complete API Documentation",
            "description": "Write comprehensive documentation",
            "status": TaskStatus.pending,
            "priority": TaskPriority.high,
            "assigned_to": "John Doe",
            "due_date": datetime.now(timezone.utc) + timedelta(days=5)
        },
        {
            "title": "Implement User Authentication",
            "description": "Add JWT-based authentication",
            "status": TaskStatus.in_progress,
            "priority": TaskPriority.medium,
            "assigned_to": "Jane Smith",
            "due_date": datetime.now(timezone.utc) + timedelta(days=3)
        },
        {
            "title": "Add Unit Tests",
            "description": "Write comprehensive unit tests",
            "status": TaskStatus.completed,
            "priority": TaskPriority.low,
            "assigned_to": "Bob Wilson"
        },
        {
            "title": "Database Optimization",
            "description": "Optimize database queries and indexes",
            "status": TaskStatus.pending,
            "priority": TaskPriority.urgent,
            "assigned_to": "Alice Johnson",
            "due_date": datetime.now(timezone.utc) + timedelta(days=1)
        }
    ]
    
    tasks = []
    for task_data in tasks_data:
        task = TaskCRUD.create_task(session, task_data)
        tasks.append(task)
    
    return tasks


class TestTaskCRUD:
    """Test CRUD operations for tasks"""
    
    def test_create_task(self, session):
        """Test creating a new task"""
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": TaskStatus.pending,
            "priority": TaskPriority.medium
        }
        
        task = TaskCRUD.create_task(session, task_data)
        
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.status == TaskStatus.pending
        assert task.priority == TaskPriority.medium
        assert task.created_at is not None
    
    def test_get_task(self, session, sample_tasks):
        """Test getting a task by ID"""
        task_id = sample_tasks[0].id
        task = TaskCRUD.get_task(session, task_id)
        
        assert task is not None
        assert task.id == task_id
        assert task.title == "Complete API Documentation"
    
    def test_get_task_not_found(self, session):
        """Test getting a non-existent task"""
        task = TaskCRUD.get_task(session, 999)
        assert task is None
    
    def test_get_tasks_basic(self, session, sample_tasks):
        """Test getting all tasks with basic pagination"""
        tasks, total = TaskCRUD.get_tasks(session, skip=0, limit=10)
        
        assert len(tasks) == 4
        assert total == 4
        assert all(isinstance(task, Task) for task in tasks)
    
    def test_get_tasks_with_status_filter(self, session, sample_tasks):
        """Test filtering tasks by status"""
        tasks, total = TaskCRUD.get_tasks(session, status=TaskStatus.pending)
        
        assert total == 2
        assert all(task.status == TaskStatus.pending for task in tasks)
    
    def test_get_tasks_with_priority_filter(self, session, sample_tasks):
        """Test filtering tasks by priority"""
        tasks, total = TaskCRUD.get_tasks(session, priority=TaskPriority.high)
        
        assert total == 1
        assert tasks[0].priority == TaskPriority.high
    
    def test_get_tasks_with_assigned_to_filter(self, session, sample_tasks):
        """Test filtering tasks by assignee"""
        tasks, total = TaskCRUD.get_tasks(session, assigned_to="John Doe")
        
        assert total == 1
        assert tasks[0].assigned_to == "John Doe"
    
    def test_get_tasks_with_search(self, session, sample_tasks):
        """Test searching tasks by title and description"""
        tasks, total = TaskCRUD.get_tasks(session, search="documentation")
        
        assert total == 1
        assert "documentation" in tasks[0].title.lower() or "documentation" in (tasks[0].description or "").lower()
    
    def test_get_tasks_with_date_filters(self, session, sample_tasks):
        """Test filtering tasks by date ranges"""
        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
        tasks, total = TaskCRUD.get_tasks(session, due_date_from=tomorrow)
        
        assert total >= 1
        assert all(task.due_date >= tomorrow for task in tasks if task.due_date)
    
    def test_get_tasks_with_sorting(self, session, sample_tasks):
        """Test sorting tasks"""
        # Sort by title ascending
        tasks, total = TaskCRUD.get_tasks(
            session, 
            sort_field=SortField.title, 
            sort_order=SortOrder.asc
        )
        
        assert len(tasks) == 4
        # Check if titles are sorted alphabetically
        titles = [task.title for task in tasks]
        assert titles == sorted(titles)
    
    def test_get_tasks_with_pagination(self, session, sample_tasks):
        """Test pagination"""
        tasks, total = TaskCRUD.get_tasks(session, skip=1, limit=2)
        
        assert len(tasks) == 2
        assert total == 4
    
    def test_update_task(self, session, sample_tasks):
        """Test updating a task"""
        task_id = sample_tasks[0].id
        update_data = {
            "status": TaskStatus.completed,
            "description": "Updated description"
        }
        
        updated_task = TaskCRUD.update_task(session, task_id, update_data)
        
        assert updated_task is not None
        assert updated_task.status == TaskStatus.completed
        assert updated_task.description == "Updated description"
        assert updated_task.updated_at is not None
    
    def test_update_task_not_found(self, session):
        """Test updating a non-existent task"""
        result = TaskCRUD.update_task(session, 999, {"status": TaskStatus.completed})
        assert result is None
    
    def test_delete_task(self, session, sample_tasks):
        """Test deleting a task"""
        task_id = sample_tasks[0].id
        success = TaskCRUD.delete_task(session, task_id)
        
        assert success is True
        
        # Verify task is deleted
        deleted_task = TaskCRUD.get_task(session, task_id)
        assert deleted_task is None
    
    def test_delete_task_not_found(self, session):
        """Test deleting a non-existent task"""
        success = TaskCRUD.delete_task(session, 999)
        assert success is False
    
    def test_bulk_update_tasks(self, session, sample_tasks):
        """Test bulk updating tasks"""
        task_ids = [sample_tasks[0].id, sample_tasks[1].id]
        update_data = {"status": TaskStatus.completed}
        
        updated_count, total_count = TaskCRUD.bulk_update_tasks(session, task_ids, update_data)
        
        assert updated_count == 2
        assert total_count == 2
        
        # Verify tasks are updated
        for task_id in task_ids:
            task = TaskCRUD.get_task(session, task_id)
            assert task is not None
            assert task.status == TaskStatus.completed
    
    def test_bulk_delete_tasks(self, session, sample_tasks):
        """Test bulk deleting tasks"""
        task_ids = [sample_tasks[0].id, sample_tasks[1].id]
        
        deleted_count, total_count = TaskCRUD.bulk_delete_tasks(session, task_ids)
        
        assert deleted_count == 2
        assert total_count == 2
        
        # Verify tasks are deleted
        for task_id in task_ids:
            task = TaskCRUD.get_task(session, task_id)
            assert task is None
    
    def test_search_tasks(self, session, sample_tasks):
        """Test searching tasks"""
        tasks, total = TaskCRUD.search_tasks(session, "authentication")
        
        assert total == 1
        assert "authentication" in tasks[0].title.lower() or "authentication" in (tasks[0].description or "").lower()
    
    def test_get_tasks_by_status(self, session, sample_tasks):
        """Test getting tasks by status"""
        tasks, total = TaskCRUD.get_tasks_by_status(session, TaskStatus.pending)
        
        assert total == 2
        assert all(task.status == TaskStatus.pending for task in tasks)
    
    def test_get_tasks_by_priority(self, session, sample_tasks):
        """Test getting tasks by priority"""
        tasks, total = TaskCRUD.get_tasks_by_priority(session, TaskPriority.urgent)
        
        assert total == 1
        assert tasks[0].priority == TaskPriority.urgent 