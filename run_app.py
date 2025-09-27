#!/usr/bin/env python3
"""
Simple server to run the MyMoney FIU application
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def find_free_port():
    """Find a free port to run the server"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/secure_fiu_app.html'
        return super().do_GET()

def main():
    # Change to the directory containing the HTML file
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if the HTML file exists
    if not os.path.exists('secure_fiu_app.html'):
        print("❌ Error: secure_fiu_app.html not found!")
        print("Make sure you're running this from the correct directory.")
        sys.exit(1)
    
    # Find a free port
    port = find_free_port()
    
    print("🚀 Starting MyMoney FIU Application...")
    print("=" * 50)
    print(f"📱 App URL: http://localhost:{port}")
    print(f"🌐 Server running on port {port}")
    print("=" * 50)
    print("💡 Features available:")
    print("   ✅ User signup/login with bank account validation")
    print("   ✅ Transaction management with AI analysis")
    print("   ✅ Detailed expense tracking with purposes")
    print("   ✅ Real-time budget insights")
    print("   ✅ Beautiful dark theme with glassmorphism")
    print("   ✅ Keyboard navigation (Enter key support)")
    print("=" * 50)
    print("🔧 Controls:")
    print("   • Press Ctrl+C to stop the server")
    print("   • The app will open automatically in your browser")
    print()
    
    try:
        # Create and start the server
        with socketserver.TCPServer(("", port), MyHTTPRequestHandler) as httpd:
            print(f"✅ Server started successfully!")
            
            # Open browser automatically
            webbrowser.open(f'http://localhost:{port}')
            print(f"🌐 Opening http://localhost:{port} in your browser...")
            print()
            print("🎯 Ready to use! Create an account or login to get started.")
            print()
            
            # Serve forever
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("Try running on a different port or check if the port is already in use.")

if __name__ == "__main__":
    main()