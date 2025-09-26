#!/usr/bin/env python3
"""
Universal demo runner for AI Budget Planner
Works on any system with Python installed
"""

import os
import sys
import time
import socket
import subprocess
import webbrowser
from pathlib import Path

def find_free_port():
    """Find a free port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'pandas', 'sqlalchemy', 
        'python-dotenv', 'crewai', 'masumi'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\nInstalling missing packages...")
        
        for pkg in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
                print(f"Installed {pkg}")
            except subprocess.CalledProcessError:
                print(f"Failed to install {pkg}")
                return False
    
    return True

def start_backend():
    """Start the backend server"""
    print("Starting AI Budget Planner Backend...")
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print(".env file not found. Creating default .env file...")
        create_default_env()
    
    # Find free port
    port = find_free_port()
    
    # Set environment variable for the port
    os.environ['BACKEND_PORT'] = str(port)
    
    print(f"Backend will start on: http://localhost:{port}")
    print(f"API Documentation: http://localhost:{port}/docs")
    
    # Start the server
    try:
        import uvicorn
        from main import app
        
        print("Starting server...")
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
        
    except Exception as e:
        print(f"Failed to start backend: {e}")
        return False
    
    return True

def create_default_env():
    """Create a default .env file"""
    env_content = """# Payment Service
PAYMENT_SERVICE_URL=http://localhost:3001/api/v1
PAYMENT_API_KEY=demo_api_key

# Agent Configuration
AGENT_IDENTIFIER=demo_agent_identifier
PAYMENT_AMOUNT=10000000
PAYMENT_UNIT=lovelace
SELLER_VKEY=demo_seller_vkey

# OpenAI (REQUIRED - Add your key here)
OPENAI_API_KEY=your_openai_api_key_here

# Account Aggregator Configuration
AA_BASE_URL=https://sandbox.setu.co/api
AA_API_KEY=demo_aa_api_key
AA_CLIENT_ID=demo_aa_client_id

# Network
NETWORK=Preprod
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("Created default .env file")
    print("Please add your OpenAI API key to the .env file")

def open_demo():
    """Open the demo in browser"""
    demo_file = Path('demo.html').absolute()
    if demo_file.exists():
        print(f"Opening demo: {demo_file}")
        webbrowser.open(f'file://{demo_file}')
    else:
        print("demo.html not found")

def main():
    """Main function"""
    print("AI Budget Planner - Universal Demo Runner")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Check OpenAI API key
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print("OpenAI API key not configured!")
        print("Please add your OpenAI API key to the .env file")
        print("Get your key from: https://platform.openai.com/api-keys")
        
        key = input("\nEnter your OpenAI API key (or press Enter to continue with demo): ").strip()
        if key:
            # Update .env file
            env_lines = []
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('OPENAI_API_KEY='):
                        env_lines.append(f'OPENAI_API_KEY={key}\n')
                    else:
                        env_lines.append(line)
            
            with open('.env', 'w') as f:
                f.writelines(env_lines)
            
            print("OpenAI API key updated!")
    
    print("\nChoose an option:")
    print("1. Start Backend Server")
    print("2. Open Demo (HTML)")
    print("3. Start Backend + Open Demo")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        start_backend()
    elif choice == '2':
        open_demo()
    elif choice == '3':
        # Start backend in background and open demo
        print("Starting backend and opening demo...")
        
        # Start backend in a separate process
        import threading
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Wait a bit for backend to start
        time.sleep(3)
        
        # Open demo
        open_demo()
        
        print("\nDemo is running!")
        print("Press Ctrl+C to stop the backend server")
        
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()