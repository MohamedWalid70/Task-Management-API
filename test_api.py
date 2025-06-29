#!/usr/bin/env python3
"""
Test script for the Task Management API
This script demonstrates the API functionality with example requests.
"""

import requests
import json
from datetime import datetime, timedelta

# API Configuration
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}


def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            print("Response:")
            print(json.dumps(response.json(), indent=2))
        except:
            print("Response:", response.text)
    print(f"{'='*50}")


def test_api():
    """Test the API endpoints"""
    
    print("🚀 Starting Task Management API Tests")
    print("Make sure the API is running on http://localhost:8000")
    
    # Test 1: Get API Information
    print("\n1. Testing API Information...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "API Information")
    
    # Test 2: Health Check
    print("\n2. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")
    
    # Test 3: Create Tasks
    print("\n3. Creating Test Tasks...")
    
    # Task 1
    task1_data = {
        "title": "Complete API Documentation",
        "description": "Write comprehensive documentation for the task management API",
        "priority": "high",
        "due_date": (datetime.utcnow() + timedelta(days=5)).isoformat() + "Z",
        "assigned_to": "John Doe"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task1_data, headers=HEADERS)
    print_response(response, "Create Task 1")
    task1_id = response.json().get("id") if response.status_code == 201 else None
    
    # Task 2
    task2_data = {
        "title": "Implement User Authentication",
        "description": "Add JWT-based authentication to the API",
        "priority": "medium",
        "status": "in_progress",
        "assigned_to": "Jane Smith"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task2_data, headers=HEADERS)
    print_response(response, "Create Task 2")
    task2_id = response.json().get("id") if response.status_code == 201 else None
    
    # Task 3
    task3_data = {
        "title": "Add Unit Tests",
        "description": "Write comprehensive unit tests for all endpoints",
        "priority": "low",
        "due_date": (datetime.utcnow() + timedelta(days=10)).isoformat() + "Z"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task3_data, headers=HEADERS)
    print_response(response, "Create Task 3")
    task3_id = response.json().get("id") if response.status_code == 201 else None
    
    # Test 4: List All Tasks
    print("\n4. Listing All Tasks...")
    response = requests.get(f"{BASE_URL}/tasks")
    print_response(response, "List All Tasks")
    
    # Test 5: Get Specific Task
    if task1_id:
        print(f"\n5. Getting Task {task1_id}...")
        response = requests.get(f"{BASE_URL}/tasks/{task1_id}")
        print_response(response, f"Get Task {task1_id}")
    
    # Test 6: Update Task
    if task2_id:
        print(f"\n6. Updating Task {task2_id}...")
        update_data = {
            "status": "completed",
            "description": "JWT-based authentication has been successfully implemented"
        }
        response = requests.put(f"{BASE_URL}/tasks/{task2_id}", json=update_data, headers=HEADERS)
        print_response(response, f"Update Task {task2_id}")
    
    # Test 7: Filter Tasks by Status
    print("\n7. Filtering Tasks by Status...")
    response = requests.get(f"{BASE_URL}/tasks/status/pending")
    print_response(response, "Tasks with Status: pending")
    
    response = requests.get(f"{BASE_URL}/tasks/status/completed")
    print_response(response, "Tasks with Status: completed")
    
    # Test 8: Filter Tasks by Priority
    print("\n8. Filtering Tasks by Priority...")
    response = requests.get(f"{BASE_URL}/tasks/priority/high")
    print_response(response, "Tasks with Priority: high")
    
    # Test 9: List Tasks with Pagination
    print("\n9. Testing Pagination...")
    response = requests.get(f"{BASE_URL}/tasks?skip=0&limit=2")
    print_response(response, "Tasks with Pagination (skip=0, limit=2)")
    
    # Test 10: Validation Error Test
    print("\n10. Testing Validation Errors...")
    invalid_task_data = {
        "title": "",  # Empty title should fail validation
        "priority": "invalid_priority"  # Invalid priority should fail validation
    }
    response = requests.post(f"{BASE_URL}/tasks", json=invalid_task_data, headers=HEADERS)
    print_response(response, "Validation Error Test")
    
    # Test 11: Get Non-existent Task
    print("\n11. Testing 404 Error...")
    response = requests.get(f"{BASE_URL}/tasks/99999")
    print_response(response, "Get Non-existent Task")
    
    # Test 12: Delete Task
    if task3_id:
        print(f"\n12. Deleting Task {task3_id}...")
        response = requests.delete(f"{BASE_URL}/tasks/{task3_id}")
        print_response(response, f"Delete Task {task3_id}")
        
        # Verify deletion
        response = requests.get(f"{BASE_URL}/tasks/{task3_id}")
        print_response(response, f"Verify Task {task3_id} Deletion")
    
    print("\n✅ API Testing Complete!")
    print("\n📖 You can also test the API using the interactive documentation at:")
    print("   http://localhost:8000/docs")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("   Make sure the API is running on http://localhost:8000")
        print("   Run: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}") 