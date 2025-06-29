# Task Management API

A comprehensive RESTful API for managing tasks built with FastAPI, Pydantic, and SQLModel. This API demonstrates best practices in API design, data validation, database operations, and clean code architecture.

## Features

- **Full CRUD Operations**: Create, Read, Update, Delete tasks
- **Data Validation**: Comprehensive input validation using Pydantic
- **Database Integration**: SQLModel/SQLAlchemy with SQLite
- **Filtering & Pagination**: Filter tasks by status/priority with pagination support
- **RESTful Design**: Proper HTTP methods and status codes
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Error Handling**: Proper error responses with meaningful messages

## Technical Stack

- **FastAPI** - Modern web framework for building APIs
- **Pydantic** - Data validation and serialization
- **SQLModel** - ORM for database operations (built on SQLAlchemy)
- **SQLite** - Database (for simplicity)
- **Python 3.9+** - Programming language

## Project Structure

```
task-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application setup
│   ├── models.py        # Pydantic models and database schema
│   ├── database.py      # Database configuration
│   ├── crud.py          # Database operations
│   └── routes.py        # API endpoints
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation & Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project**
   ```bash
   # If you have the project files, navigate to the project directory
   cd task-management-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

   Or alternatively:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the API**
   - API Base URL: `http://localhost:8000/api/v1`
   - Interactive Documentation: `http://localhost:8000/docs`
   - Alternative Documentation: `http://localhost:8000/redoc`

## Database Schema

### Task Model

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique task identifier |
| title | String | Required, Max 200 chars | Task title |
| description | String | Optional, Max 1000 chars | Task description |
| status | Enum | Required, Default: "pending" | Task status |
| priority | Enum | Required, Default: "medium" | Task priority |
| created_at | DateTime | Auto-generated | Creation timestamp |
| updated_at | DateTime | Optional | Last update timestamp |
| due_date | DateTime | Optional | Task deadline |
| assigned_to | String | Optional, Max 100 chars | Assignee name |

### Enums

**TaskStatus:**
- `pending`
- `in_progress`
- `completed`
- `cancelled`

**TaskPriority:**
- `low`
- `medium`
- `high`
- `urgent`

## API Endpoints

### 1. API Information
- **GET** `/api/v1/` - Get API information and available endpoints

### 2. Health Check
- **GET** `/api/v1/health` - Check API health status

### 3. Task Management

#### Create Task
- **POST** `/api/v1/tasks` - Create a new task
  - **Status Code**: 201 (Created)
  - **Request Body**: TaskCreate model
  - **Response**: TaskResponse model

#### List Tasks
- **GET** `/api/v1/tasks` - List all tasks with optional filtering and pagination
  - **Query Parameters**:
    - `skip` (int, default: 0): Number of tasks to skip
    - `limit` (int, default: 100, max: 1000): Maximum number of tasks to return
    - `status` (TaskStatus, optional): Filter by task status
    - `priority` (TaskPriority, optional): Filter by task priority
  - **Response**: TaskListResponse model with pagination info

#### Get Task
- **GET** `/api/v1/tasks/{task_id}` - Get a specific task by ID
  - **Status Code**: 200 (OK) or 404 (Not Found)
  - **Response**: TaskResponse model

#### Update Task
- **PUT** `/api/v1/tasks/{task_id}` - Update an existing task
  - **Status Code**: 200 (OK) or 404 (Not Found)
  - **Request Body**: TaskUpdate model (all fields optional)
  - **Response**: TaskResponse model

#### Delete Task
- **DELETE** `/api/v1/tasks/{task_id}` - Delete a task
  - **Status Code**: 204 (No Content) or 404 (Not Found)

### 4. Filtering Endpoints

#### Tasks by Status
- **GET** `/api/v1/tasks/status/{status}` - Get tasks filtered by status
  - **Query Parameters**: `skip`, `limit` (same as list tasks)
  - **Response**: TaskListResponse model

#### Tasks by Priority
- **GET** `/api/v1/tasks/priority/{priority}` - Get tasks filtered by priority
  - **Query Parameters**: `skip`, `limit` (same as list tasks)
  - **Response**: TaskListResponse model

## Data Validation

### Input Validation Rules

1. **Title Validation**:
   - Cannot be empty or whitespace only
   - Must be trimmed of leading/trailing spaces
   - Maximum 200 characters

2. **Due Date Validation**:
   - Must be in the future (if provided)

3. **Description**:
   - Maximum 1000 characters
   - Optional field

4. **Assigned To**:
   - Maximum 100 characters
   - Optional field

### HTTP Status Codes

- **200** - Successful retrieval/update
- **201** - Successful creation
- **204** - Successful deletion (no content)
- **400** - Bad request (validation errors, etc.)
- **404** - Resource not found
- **422** - Validation errors (Pydantic)
- **500** - Internal server error

## Example API Calls

### 1. Create a New Task

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete API Documentation",
    "description": "Write comprehensive documentation for the task management API",
    "priority": "high",
    "due_date": "2024-01-15T18:00:00Z",
    "assigned_to": "John Doe"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete API Documentation",
  "description": "Write comprehensive documentation for the task management API",
  "status": "pending",
  "priority": "high",
  "created_at": "2024-01-10T10:30:00Z",
  "updated_at": null,
  "due_date": "2024-01-15T18:00:00Z",
  "assigned_to": "John Doe"
}
```

### 2. List All Tasks

```bash
curl -X GET "http://localhost:8000/api/v1/tasks?skip=0&limit=10"
```

### 3. Get Tasks by Status

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/status/pending?limit=5"
```

### 4. Update a Task

```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "description": "Updated description with more details"
  }'
```

### 5. Delete a Task

```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1"
```

## Testing the API

### Using the Interactive Documentation

1. Start the application: `python main.py`
2. Open your browser and go to: `http://localhost:8000/docs`
3. You'll see the interactive Swagger UI with all endpoints
4. Click on any endpoint to expand it and test it directly

### Using curl (Command Line)

All the example API calls above can be run using curl from the command line.

### Using Python requests

```python
import requests

# Base URL
base_url = "http://localhost:8000/api/v1"

# Create a task
response = requests.post(f"{base_url}/tasks", json={
    "title": "Test Task",
    "description": "This is a test task",
    "priority": "medium"
})

# Get all tasks
response = requests.get(f"{base_url}/tasks")

# Get tasks by status
response = requests.get(f"{base_url}/tasks/status/pending")
```

## Error Handling

The API provides comprehensive error handling with meaningful error messages:

### Validation Error Example
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Title cannot be empty or whitespace only",
      "type": "value_error"
    }
  ]
}
```

### Not Found Error Example
```json
{
  "detail": "Task not found"
}
```

## Design Decisions & Assumptions

1. **Database**: SQLite is used for simplicity and ease of setup. For production, consider PostgreSQL or MySQL.

2. **Pagination**: Implemented using skip/limit pattern for simplicity. For large datasets, consider cursor-based pagination.

3. **Validation**: Comprehensive validation using Pydantic with custom validators for business logic.

4. **Error Handling**: Proper HTTP status codes and meaningful error messages.

5. **CORS**: Configured to allow all origins for development. Configure appropriately for production.

6. **Timestamps**: Using UTC timestamps for consistency across timezones.

7. **Soft Deletes**: Not implemented for simplicity. Consider adding soft delete functionality for production use.

## Future Enhancements

1. **Authentication & Authorization**: Add JWT-based authentication
2. **User Management**: Add user registration and management
3. **Task Categories**: Add task categorization functionality
4. **File Attachments**: Add support for file uploads
5. **Task Comments**: Add commenting system
6. **Email Notifications**: Add email notifications for task updates
7. **Task Dependencies**: Add support for task dependencies
8. **Advanced Filtering**: Add date range filtering, search functionality
9. **Bulk Operations**: Add bulk create, update, delete operations
10. **Rate Limiting**: Add API rate limiting for production use

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `main.py` or kill the process using the port
2. **Database errors**: Delete the `task_management.db` file and restart the application
3. **Import errors**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Logs

The application logs are displayed in the console. For production, consider using a proper logging framework.

## License

This project is for educational purposes and demonstrates best practices in API development. # Task-Management-API
