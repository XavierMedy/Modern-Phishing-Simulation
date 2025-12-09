import json
import glob
import os
from datetime import datetime
from collections import defaultdict

def phishing_rate_calculation():
    #Calculating phishing rates from keyboard logs
    
    print("-------Phishing Rate Calculation-------")
    
    # Check if keyboard logs exist
    if not os.path.exists('keyboard_logs'):
        print("ERROR: No keyboard_logs directory found!")
        print("Make sure you've run the server and visited landing pages.")
        return
    
    log_files = glob.glob('keyboard_logs/*.json')
    
    if not log_files:
        print("ERROR: No log files found in keyboard_logs/")
        print("Users need to visit landing pages and type in forms.")
        return
    
    print(f"Found {len(log_files)} session log(s)")
    
    # Initialize counters for calculation
    total_sessions = 0
    sessions_with_submission = 0
    departments = defaultdict(lambda: {'sessions': 0, 'submissions': 0})
    
   
    print("-------Checking each session for form submissions-------")

    
    for log_file in log_files:
        try:
            with open(log_file, 'r') as f:
                data = json.load(f)
            
            total_sessions += 1
            
            # Get department from URL parameters or form data
            dept = "General"
            # Try to extract department from form data if available
            keystrokes = data.get('keystrokes', [])
            for event in keystrokes:
                if event.get('type') == 'form_submit' and 'form_data' in event:
                    form_data = event.get('form_data', {})
                    if 'department' in form_data:
                        dept = form_data['department']
                        break
            
            departments[dept]['sessions'] += 1
            
            # Check for form submission
            has_submission = any(
                event.get('type') == 'form_submit'
                for event in keystrokes
            )
            
            if has_submission:
                sessions_with_submission += 1
                departments[dept]['submissions'] += 1
            
            # Print session summary
            filename = os.path.basename(log_file)
            print(f"\nFile: {filename}")
            print(f"   Submitted form: {'YES' if has_submission else 'No'}")
            
        except Exception as e:
            print(f"\nError reading {log_file}: {e}")
            continue
    
 
    print("-------Phishing Rate Results-------")
    
    if total_sessions == 0:
        print("No sessions to analyze")
        return
    
    # Calculating phishing rate
    phishing_rate = (sessions_with_submission / total_sessions) * 100
    
    print(f"\nSummary:")
    print(f"   Total sessions: {total_sessions}")
    print(f"   Sessions with form submission: {sessions_with_submission}")
    
    print(f"\nPhishing Rate: {phishing_rate:.1f}%")
    
    # Risk level based on phishing rate
    if phishing_rate >= 20:
        risk_level = "CRITICAL RISK"
    elif phishing_rate >= 10:
        risk_level = "HIGH RISK"
    elif phishing_rate >= 5:
        risk_level = "MEDIUM RISK"
    elif phishing_rate >= 1:
        risk_level = "LOW RISK"
    else:
        risk_level = "VERY LOW RISK"
    
    print(f"\nRisk Assessment: {risk_level}")
    
    
    # Generate simple report file
    generate_report(total_sessions, sessions_with_submission, phishing_rate, risk_level)
    
    print(f"\nReport saved to: phishing_report.txt")

def generate_report(total, submissions, phishing_rate, risk):
    
    report = f"""Phishing Simulation Report

Summary:
Total simulated sessions: {total}
Sessions with form submission: {submissions}

Phishing Rate: {phishing_rate:.1f}%

RISK ASSESSMENT:
Risk Level: {risk}
"""
    
    
    with open('phishing_report.txt', 'w') as f:
        f.write(report)
    
    return report

if __name__ == "__main__":
    phishing_rate_calculation()