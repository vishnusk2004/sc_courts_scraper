#!/usr/bin/env python3
"""
Deployment script for SC Courts Django App
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main deployment function"""
    print("🚀 SC COURTS DJANGO APP DEPLOYMENT")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install requirements
    if not run_command("pip install -r requirements_django.txt", "Installing requirements"):
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        print("❌ Failed to create migrations")
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Running migrations"):
        print("❌ Failed to run migrations")
        sys.exit(1)
    
    # Create superuser (optional)
    print("\n🔧 ADMIN USER SETUP")
    print("You can create an admin user with: python manage.py createsuperuser")
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("❌ Failed to collect static files")
        sys.exit(1)
    
    print("\n✅ DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("\n🎯 NEXT STEPS:")
    print("1. Create admin user: python manage.py createsuperuser")
    print("2. Start the server: python manage.py runserver")
    print("3. Access the app at: http://localhost:8000")
    print("4. For production, use: gunicorn sc_courts_app.wsgi:application")

if __name__ == "__main__":
    main()
