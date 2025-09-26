#!/usr/bin/env python3
"""
Simple HTTP server to serve the working demo
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import os

def start_server():
    """Start HTTP server"""
    PORT = 8080
    
    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
        
        def do_GET(self):
            if self.path == '/' or self.path == '':
                self.path = '/working_demo.html'
            return super().do_GET()
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"AI Budget Planner Demo Server running at:")
        print(f"http://localhost:{PORT}")
        print("\nPress Ctrl+C to stop the server")
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open(f'http://localhost:{PORT}')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

if __name__ == "__main__":
    start_server()