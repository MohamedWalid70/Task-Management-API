# Quick Start Guide

Get the Task Management API up and running in minutes!

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

## Quick Setup

### Option 1: Automated Setup (Recommended)

```bash
# Run the automated setup script
python setup.py
```

This will:
- ✅ Check Python version compatibility
- ✅ Install all required dependencies
- ✅ Create the database and tables
- ✅ Provide next steps

### Option 2: Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the API
python main.py
```

## Start the API

```bash
python main.py
```

The API will start on `http://localhost:8000`

## Test the API

### Option 1: Interactive Documentation
1. Open your browser and go to: `http://localhost:8000/docs`
2. You'll see the Swagger UI with all endpoints
3. Click on any endpoint to test it directly

### Option 2: Automated Test Script
```bash
python test_api.py
```

This will run comprehensive tests on all endpoints.

### Option 3: Manual Testing with curl

```bash
# Get API information
curl http://localhost:8000/api/v1/

# Health check
curl http://localhost:8000/api/v1/health

# Create a task
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Task",
    "description": "This is a test task",
    "priority": "high"
  }'

# List all tasks
curl http://localhost:8000/api/v1/tasks
```

## API Endpoints

- **API Info**: `GET /api/v1/`
- **Health Check**: `GET /api/v1/health`
- **Create Task**: `POST /api/v1/tasks`
- **List Tasks**: `GET /api/v1/tasks`
- **Get Task**: `GET /api/v1/tasks/{id}`
- **Update Task**: `PUT /api/v1/tasks/{id}`
- **Delete Task**: `DELETE /api/v1/tasks/{id}`
- **Tasks by Status**: `GET /api/v1/tasks/status/{status}`
- **Tasks by Priority**: `GET /api/v1/tasks/priority/{priority}`

## Troubleshooting

### Port Already in Use
```bash
# Kill process using port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Kill process using port 8000 (Linux/Mac)
lsof -ti:8000 | xargs kill -9
```

### Database Issues
```bash
# Delete the database file and restart
rm task_management.db
python main.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. Explore the interactive documentation at `http://localhost:8000/docs`
2. Try creating, updating, and deleting tasks
3. Test filtering and pagination features
4. Check out the full README.md for detailed documentation

Happy coding! 🚀 