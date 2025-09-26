#!/usr/bin/env python3
"""
Simple HTTP server to serve the FIU demo
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import os

def start_demo_server():
    """Start HTTP server for FIU demo"""
    PORT = 9090
    
    class DemoHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
        
        def do_GET(self):
            if self.path == '/' or self.path == '':
                self.path = '/working_fiu_demo.html'
            return super().do_GET()
    
    with socketserver.TCPServer(("", PORT), DemoHTTPRequestHandler) as httpd:
        print("=" * 60)
        print("FIU PLATFORM DEMO SERVER")
        print("=" * 60)
        print(f"Server running at: http://localhost:{PORT}")
        print("Features demonstrated:")
        print("- Legitimate bank account validation")
        print("- Income and expense tracking")
        print("- Bank account synchronization")
        print("- AI budget analysis")
        print("- Masumi blockchain integration")
        print("- Real-time financial dashboard")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 60)
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open(f'http://localhost:{PORT}')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nDemo server stopped")
            httpd.shutdown()

if __name__ == "__main__":
    start_demo_server()