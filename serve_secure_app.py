#!/usr/bin/env python3
"""
Serve the secure FIU app with authentication
"""

import http.server
import socketserver
import webbrowser
import threading
import time

def start_secure_app():
    """Start the secure FIU app server"""
    PORT = 7777
    
    class SecureAppHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' or self.path == '':
                self.path = '/secure_fiu_app.html'
            return super().do_GET()
    
    with socketserver.TCPServer(("", PORT), SecureAppHandler) as httpd:
        print("=" * 60)
        print("SECURE FIU PLATFORM")
        print("=" * 60)
        print(f"App URL: http://localhost:{PORT}")
        print()
        print("Features:")
        print("- Secure login/signup with password")
        print("- Bank account registration during signup")
        print("- Complete financial management")
        print("- AI budget analysis")
        print("- Masumi blockchain integration")
        print()
        print("Demo Credentials:")
        print("Email: demo@fiu.com")
        print("Password: demo123")
        print()
        print("Press Ctrl+C to stop")
        print("=" * 60)
        
        def open_browser():
            time.sleep(2)
            webbrowser.open(f'http://localhost:{PORT}')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSecure app stopped")

if __name__ == "__main__":
    start_secure_app()