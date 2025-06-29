#!/usr/bin/env python3
"""
Advanced Features Test Script for the Task Management API
This script demonstrates all the new bonus features implemented.
"""

import requests
import json
from datetime import datetime, timezone, timedelta

# API Configuration
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}


def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            print("Response:")
            print(json.dumps(response.json(), indent=2))
        except:
            print("Response:", response.text)
    print(f"{'='*60}")


def test_advanced_features():
    """Test all advanced features"""
    
    print("🚀 Testing Advanced Features of Task Management API")
    print("Make sure the API is running on http://localhost:8000")
    
    # Create test tasks for advanced testing
    print("\n1. Creating Test Tasks for Advanced Features...")
    
    tasks_data = [
        {
            "title": "Frontend Development",
            "description": "Build React components and implement responsive design",
            "priority": "high",
            "status": "in_progress",
            "assigned_to": "Alice Johnson",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=3)).isoformat() + "Z"
        },
        {
            "title": "Backend API Development",
            "description": "Implement RESTful API endpoints and database integration",
            "priority": "urgent",
            "status": "pending",
            "assigned_to": "Bob Smith",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat() + "Z"
        },
        {
            "title": "Database Schema Design",
            "description": "Design and implement database schema with proper relationships",
            "priority": "medium",
            "status": "completed",
            "assigned_to": "Carol Davis",
            "due_date": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat() + "Z"
        },
        {
            "title": "Testing and Quality Assurance",
            "description": "Write unit tests and perform integration testing",
            "priority": "low",
            "status": "pending",
            "assigned_to": "David Wilson",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=5)).isoformat() + "Z"
        },
        {
            "title": "Documentation and User Guide",
            "description": "Create comprehensive documentation and user guides",
            "priority": "medium",
            "status": "in_progress",
            "assigned_to": "Eve Brown",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat() + "Z"
        }
    ]
    
    created_tasks = []
    for i, task_data in enumerate(tasks_data):
        response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=HEADERS)
        print_response(response, f"Create Task {i+1}")
        if response.status_code == 201:
            created_tasks.append(response.json())
    
    if not created_tasks:
        print("❌ Failed to create test tasks. Cannot continue with advanced tests.")
        return
    
    task_ids = [task["id"] for task in created_tasks]
    
    # Test 2: Advanced Filtering
    print("\n2. Testing Advanced Filtering...")
    
    # Filter by status and priority
    response = requests.get(f"{BASE_URL}/tasks?status=pending&priority=urgent")
    print_response(response, "Filter by Status (pending) AND Priority (urgent)")
    
    # Filter by assignee
    response = requests.get(f"{BASE_URL}/tasks?assigned_to=Alice Johnson")
    print_response(response, "Filter by Assignee (Alice Johnson)")
    
    # Filter by date range
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat() + "Z"
    next_week = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat() + "Z"
    response = requests.get(f"{BASE_URL}/tasks?due_date_from={tomorrow}&due_date_to={next_week}")
    print_response(response, "Filter by Due Date Range (tomorrow to next week)")
    
    # Test 3: Advanced Sorting
    print("\n3. Testing Advanced Sorting...")
    
    # Sort by title ascending
    response = requests.get(f"{BASE_URL}/tasks?sort_field=title&sort_order=asc")
    print_response(response, "Sort by Title (Ascending)")
    
    # Sort by priority descending
    response = requests.get(f"{BASE_URL}/tasks?sort_field=priority&sort_order=desc")
    print_response(response, "Sort by Priority (Descending)")
    
    # Sort by due_date ascending
    response = requests.get(f"{BASE_URL}/tasks?sort_field=due_date&sort_order=asc")
    print_response(response, "Sort by Due Date (Ascending)")
    
    # Test 4: Text Search
    print("\n4. Testing Text Search...")
    
    # Search for "development"
    response = requests.get(f"{BASE_URL}/tasks/search?q=development")
    print_response(response, "Search for 'development'")
    
    # Search for "testing"
    response = requests.get(f"{BASE_URL}/tasks/search?q=testing")
    print_response(response, "Search for 'testing'")
    
    # Search for "database"
    response = requests.get(f"{BASE_URL}/tasks/search?q=database")
    print_response(response, "Search for 'database'")
    
    # Test 5: Combined Filtering and Sorting
    print("\n5. Testing Combined Filtering and Sorting...")
    
    # Filter by status and sort by priority
    response = requests.get(f"{BASE_URL}/tasks?status=pending&sort_field=priority&sort_order=desc")
    print_response(response, "Filter by Status (pending) + Sort by Priority (desc)")
    
    # Filter by priority and sort by due_date
    response = requests.get(f"{BASE_URL}/tasks?priority=high&sort_field=due_date&sort_order=asc")
    print_response(response, "Filter by Priority (high) + Sort by Due Date (asc)")
    
    # Test 6: Bulk Operations
    print("\n6. Testing Bulk Operations...")
    
    # Bulk update - mark pending tasks as in_progress
    bulk_update_data = {
        "task_ids": task_ids[:3],  # First 3 tasks
        "updates": {
            "status": "in_progress",
            "description": "Updated via bulk operation"
        }
    }
    response = requests.post(f"{BASE_URL}/tasks/bulk-update", json=bulk_update_data, headers=HEADERS)
    print_response(response, "Bulk Update - Mark Tasks as In Progress")
    
    # Verify bulk update
    response = requests.get(f"{BASE_URL}/tasks?status=in_progress")
    print_response(response, "Verify Bulk Update - Tasks with In Progress Status")
    
    # Test 7: Pagination with Advanced Features
    print("\n7. Testing Pagination with Advanced Features...")
    
    # Get first page with sorting
    response = requests.get(f"{BASE_URL}/tasks?skip=0&limit=2&sort_field=title&sort_order=asc")
    print_response(response, "Pagination Page 1 (2 items, sorted by title)")
    
    # Get second page with sorting
    response = requests.get(f"{BASE_URL}/tasks?skip=2&limit=2&sort_field=title&sort_order=asc")
    print_response(response, "Pagination Page 2 (2 items, sorted by title)")
    
    # Test 8: Complex Search and Filter Combinations
    print("\n8. Testing Complex Search and Filter Combinations...")
    
    # Search + Status filter
    response = requests.get(f"{BASE_URL}/tasks?q=development&status=in_progress")
    print_response(response, "Search 'development' + Status 'in_progress'")
    
    # Search + Priority filter + Sorting
    response = requests.get(f"{BASE_URL}/tasks?q=test&priority=low&sort_field=due_date&sort_order=asc")
    print_response(response, "Search 'test' + Priority 'low' + Sort by due_date")
    
    # Test 9: Bulk Delete
    print("\n9. Testing Bulk Delete...")
    
    # Bulk delete some tasks
    bulk_delete_data = {
        "task_ids": task_ids[-2:]  # Last 2 tasks
    }
    response = requests.post(f"{BASE_URL}/tasks/bulk-delete", json=bulk_delete_data, headers=HEADERS)
    print_response(response, "Bulk Delete - Delete Last 2 Tasks")
    
    # Verify bulk delete
    response = requests.get(f"{BASE_URL}/tasks")
    print_response(response, "Verify Bulk Delete - Remaining Tasks")
    
    print("\n✅ Advanced Features Testing Complete!")
    print("\n📖 You can also test these features using the interactive documentation at:")
    print("   http://localhost:8000/docs")


if __name__ == "__main__":
    try:
        test_advanced_features()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("   Make sure the API is running on http://localhost:8000")
        print("   Run: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}") 