#!/usr/bin/env python3
"""
FIU Platform Launcher
Complete Financial Information User platform with AI agent integration
"""

import os
import sys
import time
import webbrowser
import threading
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['fastapi', 'uvicorn', 'sqlalchemy', 'pandas']
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Installing missing packages...")
        import subprocess
        for pkg in missing_packages:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
        print("Dependencies installed successfully!")

def start_fiu_platform():
    """Start the FIU platform"""
    print("=" * 60)
    print("FIU PLATFORM - AI FINANCIAL MANAGEMENT")
    print("=" * 60)
    print()
    print("Features included:")
    print("- User Account Management")
    print("- Bank Account Integration") 
    print("- Money Transfer (Masumi Integration)")
    print("- Income & Expense Tracking")
    print("- Transaction History")
    print("- Balance Management")
    print("- AI Budget Analysis")
    print("- Personalized Financial Insights")
    print()
    
    # Check dependencies
    check_dependencies()
    
    # Start the server
    try:
        from fiu_main import app, find_free_port
        import uvicorn
        
        port = find_free_port()
        
        print(f"Starting FIU Platform on port {port}...")
        print(f"Dashboard: http://localhost:{port}")
        print(f"API Docs: http://localhost:{port}/docs")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Open browser after delay
        def open_browser():
            time.sleep(3)
            webbrowser.open(f'http://localhost:{port}')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Start server
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
        
    except KeyboardInterrupt:
        print("\nFIU Platform stopped")
    except Exception as e:
        print(f"Error starting FIU Platform: {e}")

if __name__ == "__main__":
    start_fiu_platform()