#!/usr/bin/env python3
"""
Setup script for Task Management API
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_dependencies():
    """Install required dependencies"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")


def create_database():
    """Create database tables"""
    try:
        from app.database import create_db_and_tables
        create_db_and_tables()
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Setting up Task Management API")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create database
    if not create_database():
        print("❌ Setup failed during database creation")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the API: python main.py")
    print("2. Access the API at: http://localhost:8000/api/v1")
    print("3. View documentation at: http://localhost:8000/docs")
    print("4. Run tests: python test_api.py")
    print("\n🎉 Happy coding!")


if __name__ == "__main__":
    main() 