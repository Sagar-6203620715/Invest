#!/usr/bin/env python3
"""
Startup script for the Vehicle Registration Dashboard
This script starts both the Python backend and the React frontend
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

def run_command(command, cwd=None, shell=False):
    """Run a command in a subprocess"""
    try:
        process = subprocess.Popen(
            command,
            shell=shell,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Print output in real-time
        for line in iter(process.stdout.readline, ''):
            print(line.rstrip())
            
        process.wait()
        return process.returncode
    except Exception as e:
        print(f"Error running command: {e}")
        return 1

def install_python_dependencies():
    """Install Python dependencies"""
    print("🐍 Installing Python dependencies...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    # Check if virtual environment exists
    venv_dir = backend_dir / "venv"
    if not venv_dir.exists():
        print("📦 Creating virtual environment...")
        result = run_command([sys.executable, "-m", "venv", "venv"], cwd=backend_dir)
        if result != 0:
            print("❌ Failed to create virtual environment")
            return False
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        python_path = venv_dir / "Scripts" / "python.exe"
        pip_path = venv_dir / "Scripts" / "pip.exe"
    else:  # Linux/Mac
        python_path = venv_dir / "bin" / "python"
        pip_path = venv_dir / "bin" / "pip"
    
    print("📥 Installing requirements...")
    result = run_command([str(pip_path), "install", "-r", "requirements.txt"], cwd=backend_dir)
    if result != 0:
        print("❌ Failed to install Python dependencies")
        return False
    
    print("✅ Python dependencies installed successfully!")
    return True

def install_node_dependencies():
    """Install Node.js dependencies"""
    print("📦 Installing Node.js dependencies...")
    
    frontend_dir = Path("investor-fleet-vision")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    result = run_command(["npm", "install"], cwd=frontend_dir)
    if result != 0:
        print("❌ Failed to install Node.js dependencies")
        return False
    
    print("✅ Node.js dependencies installed successfully!")
    return True

def start_backend():
    """Start the Python backend"""
    print("🚀 Starting Python backend...")
    
    backend_dir = Path("backend")
    venv_dir = backend_dir / "venv"
    
    if os.name == 'nt':  # Windows
        python_path = venv_dir / "Scripts" / "python.exe"
    else:  # Linux/Mac
        python_path = venv_dir / "bin" / "python"
    
    # Start the backend server
    result = run_command([str(python_path), "run.py"], cwd=backend_dir)
    return result

def start_frontend():
    """Start the React frontend"""
    print("🚀 Starting React frontend...")
    
    frontend_dir = Path("investor-fleet-vision")
    result = run_command(["npm", "run", "dev"], cwd=frontend_dir)
    return result

def check_dependencies():
    """Check if required tools are available"""
    print("🔍 Checking dependencies...")
    
    # Check Python
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except:
        print("❌ Python not found!")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        print(f"✅ Node.js: {result.stdout.strip()}")
    except:
        print("❌ Node.js not found! Please install Node.js from https://nodejs.org/")
        return False
    
    # Check npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        print(f"✅ npm: {result.stdout.strip()}")
    except:
        print("❌ npm not found!")
        return False
    
    return True

def main():
    """Main function"""
    print("🚗 Vehicle Registration Dashboard Startup Script")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Missing dependencies. Please install the required tools.")
        return 1
    
    # Install dependencies
    if not install_python_dependencies():
        return 1
    
    if not install_node_dependencies():
        return 1
    
    print("\n🎉 All dependencies installed successfully!")
    print("\n🚀 Starting the application...")
    print("=" * 50)
    print("📊 Backend will be available at: http://localhost:8000")
    print("🌐 Frontend will be available at: http://localhost:5173")
    print("=" * 50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Wait a bit for backend to start
    print("⏳ Waiting for backend to start...")
    time.sleep(5)
    
    # Open browser to frontend
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://localhost:5173")
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start frontend (this will block)
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        return 0

if __name__ == "__main__":
    sys.exit(main())