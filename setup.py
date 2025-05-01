#!/usr/bin/env python
"""
TechLearn Setup Script

This script helps with initial setup of the TechLearn application.
It creates necessary directories, database tables, and initial data.
"""

import os
import sys
import subprocess
import getpass
from pathlib import Path

def ensure_directories():
    """Ensure all necessary directories exist."""
    directories = [
        'instance',
        'migrations',
        'logs',
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Ensured directory exists: {directory}")

def setup_environment():
    """Set up environment variables if .env doesn't exist."""
    if not os.path.exists('.env'):
        print("\nSetting up environment variables...")
        
        env_vars = {
            'FLASK_APP': 'main.py',
            'FLASK_ENV': 'development',
            'SESSION_SECRET': 'dev_key_replace_in_production',
        }
        
        # Database URL
        db_name = input("Enter database name [techlearn]: ") or "techlearn"
        db_user = input("Enter database username [postgres]: ") or "postgres"
        db_pass = getpass.getpass("Enter database password: ")
        db_host = input("Enter database host [localhost]: ") or "localhost"
        db_port = input("Enter database port [5432]: ") or "5432"
        
        env_vars['DATABASE_URL'] = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        
        # Write to .env file
        with open('.env', 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        print("✓ Created .env file with environment variables")
    else:
        print("✓ Environment file (.env) already exists")

def install_dependencies():
    """Install Python dependencies."""
    print("\nInstalling dependencies...")
    
    if os.path.exists('requirements-github.txt'):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-github.txt"])
            print("✓ Installed dependencies from requirements-github.txt")
            # Rename the file to standard name
            os.rename('requirements-github.txt', 'requirements.txt')
            print("✓ Renamed requirements-github.txt to requirements.txt")
        except subprocess.CalledProcessError:
            print("✗ Failed to install dependencies. Please run: pip install -r requirements-github.txt")
    else:
        print("✗ requirements-github.txt not found")

def initialize_database():
    """Initialize the database with Flask-Migrate."""
    print("\nInitializing database...")
    
    try:
        # Import Flask app and initialize
        subprocess.check_call([sys.executable, "-m", "flask", "db", "init"])
        subprocess.check_call([sys.executable, "-m", "flask", "db", "migrate", "-m", "Initial migration"])
        subprocess.check_call([sys.executable, "-m", "flask", "db", "upgrade"])
        print("✓ Database initialized successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Database initialization failed: {e}")
        print("Please ensure your database credentials are correct and the database exists.")

def main():
    """Run the setup process."""
    print("========================================")
    print("TechLearn Setup")
    print("========================================")
    
    ensure_directories()
    setup_environment()
    install_dependencies()
    initialize_database()
    
    print("\n========================================")
    print("Setup complete!")
    print("To run the application:")
    print("  flask run")
    print("========================================")

if __name__ == "__main__":
    main()