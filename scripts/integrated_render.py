# integrated_render.py - UPDATED WITH CORRECT PATHS
from jinja2 import Template
import os
import webbrowser
import shutil
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import sys

# -------------------------------
# PATH CONFIGURATION
# -------------------------------
# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent  # Go up one level from scripts/

print(f"Script directory: {SCRIPT_DIR}")
print(f"Project root: {PROJECT_ROOT}")

# -------------------------------
# CSS SETUP FUNCTIONS
# -------------------------------
def setup_css_files():
    """Copy CSS files to Inbox folder and create proper structure"""
    # Create CSS directory in Inbox
    css_dir = PROJECT_ROOT / "Inbox/css"
    css_dir.mkdir(parents=True, exist_ok=True)
    
    # CSS files mapping - look in project root
    css_files = {
        "styles.css": "Main inbox viewer styles",
        "email_styles.css": "Email template styles", 
        "report_styles.css": "Intelligence report styles",
        "landing_styles.css": "Landing page styles"
    }
    
    copied_count = 0
    for css_file, description in css_files.items():
        source = PROJECT_ROOT / css_file
        if source.exists():
            shutil.copy(source, css_dir / css_file)
            print(f"Copied {css_file} ({description})")
            copied_count += 1
        else:
            print(f"Warning: {css_file} not found at {source}")
            
    if copied_count == 0:
        print("\nNo CSS files found! Please create them in project root.")
        print("Required files: styles.css, email_styles.css, etc.")
        print("Creating minimal CSS files automatically...")
        create_minimal_css_files(css_dir)
    
    return css_dir

def create_minimal_css_files(css_dir):
    """Create basic CSS files if they don't exist"""
    minimal_styles = """
/* styles.css - Minimal styles for simulation */
body { font-family: Arial, sans-serif; background: #f0f0f0; padding: 20px; }
.email-card { background: white; padding: 15px; margin: 10px; border-radius: 5px; }
.warning { background: yellow; padding: 10px; font-weight: bold; }
"""
    
    css_files = {
        "styles.css": minimal_styles,
        "email_styles.css": "body { font-family: Arial; padding: 20px; }",
        "report_styles.css": "body { font-family: Arial; background: #f5f5f5; }",
        "landing_styles.css": "body { font-family: Arial; background: white; }"
    }
    
    for filename, content in css_files.items():
        with open(css_dir / filename, "w") as f:
            f.write(content)
        print(f"Created minimal {filename}")

def update_css_paths(html_content, css_dir="css"):
    """Update CSS paths in HTML to use relative paths"""
    replacements = {
        'href="styles.css"': f'href="{css_dir}/styles.css"',
        'href="email_styles.css"': f'href="{css_dir}/email_styles.css"',
        'href="report_styles.css"': f'href="{css_dir}/report_styles.css"',
        'href="landing_styles.css"': f'href="{css_dir}/landing_styles.css"',
    }
    
    for old, new in replacements.items():
        html_content = html_content.replace(old, new)
    
    return html_content

# -------------------------------
# DATA COLLECTION FUNCTIONS
# -------------------------------
def scrape_employee_data():
    """Scrape employee data from GitHub Pages"""
    url = "https://xaviermedy.github.io"  # Your GitHub Pages URL
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Try to find employee data
        employees = soup.find_all("div", class_="employee")
        
        if not employees:
            # Try alternative selectors
            employees = soup.find_all(class_=lambda x: x and "employee" in x.lower())
        
        results = []
        
        for emp in employees:
            try:
                # Extract name
                name = emp.get_text(strip=True).split('\n')[0].strip()
                if not name:
                    continue
                    
                # Extract email (look for @ symbol)
                text = emp.get_text()
                email = None
                for word in text.split():
                    if '@' in word and '.' in word:
                        email = word.strip()
                        break
                
                if not email:
                    email = f"{name.lower().replace(' ', '.')}@trfuture.com"
                
                # Extract role
                role = "Employee"
                if "ceo" in text.lower():
                    role = "CEO"
                elif "manager" in text.lower():
                    role = "Manager"
                elif "director" in text.lower():
                    role = "Director"
                
                results.append({
                    "name": name,
                    "email": email,
                    "role": role,
                    "department": get_department_from_role(role)
                })
                
            except Exception as e:
                print(f"Error parsing employee: {e}")
                continue
        
        print(f"Scraped {len(results)} employees from GitHub Pages")
        return results
        
    except Exception as e:
        print(f"Could not scrape GitHub page: {e}")
        #return get_fallback_data() -- testing fallback

# def get_fallback_data(): -- testing fallback
#     """Fallback data if scraping fails"""
#     return [
#         {"name": "Dr. Maya H. Sullivan", "email": "maya.sullivan@trfuture.com", "role": "CEO", "department": "Management"},
#         {"name": "Ronald Vega", "email": "ronald.vega@trfuture.com", "role": "IT Manager", "department": "IT Department"},
#         {"name": "Ethan Valdez", "email": "ethan.valdez@trfuture.com", "role": "HR Director", "department": "Human Resources"},
#         {"name": "Xavier Medy", "email": "xavier.medy@trfuture.com", "role": "Finance Analyst", "department": "Finance"},
#         {"name": "Nidra Hayes", "email": "nidra.hayes@trfuture.com", "role": "Marketing Specialist", "department": "Marketing"},
#         {"name": "Michelle Ortega", "email": "michelle.ortega@trfuture.com", "role": "Software Engineer", "department": "IT Department"},
#         {"name": "Kevin R. Martens", "email": "kevin.martens@trfuture.com", "role": "Operations Manager", "department": "Operations"},
#     ]

def get_department_from_role(role):
    """Map roles to departments"""
    role_lower = role.lower()
    if "hr" in role_lower or "human" in role_lower:
        return "Human Resources"
    elif "finance" in role_lower or "accounting" in role_lower:
        return "Finance"
    elif "it" in role_lower or "tech" in role_lower or "engineer" in role_lower:
        return "IT Department"
    elif "manager" in role_lower or "director" in role_lower or "ceo" in role_lower:
        return "Management"
    elif "market" in role_lower:
        return "Marketing"
    else:
        return "Operations"

def sanitize_filename(name):
    
    # Remove or replace characters that cause issues in Windows filenames
    invalid_chars = '<>:"/\\|?*:'
    for char in invalid_chars:
        name = name.replace(char, '_')
    # Also replace periods that aren't part of file extension
    name = name.replace('.', '_')
    return name


def main():
    print("-------Phishing Simulation Project-------")
    print("\nSetting up environment")
          
    print("Css files setup")
    #Setup folders and CSS
    inbox_dir = PROJECT_ROOT / "Inbox"
    inbox_dir.mkdir(exist_ok=True)
    
    #Setting up CSS files 
    css_dir = setup_css_files()
    
    #Load and prepare templates
    print("\n-------Loading templates-------")
    
    # Look for email template in multiple locations
    template_paths = [
        PROJECT_ROOT / "Email_template.html",
        PROJECT_ROOT / "templates" / "Email_template.html",
        SCRIPT_DIR / "Email_template.html"
    ]
    
    email_template_path = None
    for path in template_paths:
        if path.exists():
            email_template_path = path
            break
    
    if not email_template_path:
        print("Email_template.html not found!")
        print("Looking in:")
        for path in template_paths:
            print(f" - {path}")
        print("\nPlease create Email_template.html or place it in the correct location.")
        return
    
    print(f"Found template at: {email_template_path}")
    
    with open(email_template_path, "r", encoding='utf-8') as file:
        email_template_str = file.read()
    
    # Update CSS paths in email template
    email_template_str = update_css_paths(email_template_str, "css")
    jinja_template = Template(email_template_str)
    
    # Reconnaissance, for employee data
    print("\n-------Gathering target data-------")
    people_data = scrape_employee_data()
    
    # Defining phishing scenarios for each department
    phishing_scenarios = {
        "IT Department": {
            "subject": "Urgent: Security Certificate Expiry Notice",
            "pretext": "Your admin credentials need verification",
            "urgency": "Immediate action required to avoid service interruption"
        },
        "Human Resources": {
            "subject": "HR: Mandatory Policy Update Review",
            "pretext": "New employee training module access required",
            "urgency": "Review needed by end of day"
        },
        "Finance": {
            "subject": "Finance: Q4 Report & Invoice Processing",
            "pretext": "Accounting portal access verification needed",
            "urgency": "Time-sensitive financial material"
        },
        "Management": {
            "subject": "Confidential: Executive Dashboard Access",
            "pretext": "Leadership portal credential update required",
            "urgency": "Priority access required for Q1 planning"
        },
        "Marketing": {
            "subject": "Marketing: Campaign Analytics Portal",
            "pretext": "Marketing dashboard credential verification",
            "urgency": "Access needed for campaign review"
        },
        "Operations": {
            "subject": "Operations: System Maintenance Notification",
            "pretext": "Operations portal login verification",
            "urgency": "Please complete within 24 hours"
        },
        "default": {
            "subject": "Action Required: System Update Verification",
            "pretext": "Company portal login verification",
            "urgency": "Please complete within 24 hours"
        }
    }
    
    # Generating targeted emails
    print("\n-------Generating targeted emails-------")
    email_files = {}  # Store mapping of person to filename
    
    for person in people_data:
        scenario = phishing_scenarios.get(person["department"], phishing_scenarios["default"])
        
        # Customize greeting based on role
        if "CEO" in person["role"] or "Director" in person["role"]:
            greeting = f"Dear {person['name']},"
            formality = "As a key member of leadership,"
        elif "Manager" in person["role"]:
            greeting = f"Hello {person['name']},"
            formality = "As a department manager,"
        else:
            greeting = f"Hi {person['name']},"
            formality = "As part of our ongoing security measures,"
        
        email_data = {
            "subject": scenario["subject"],
            "greeting": greeting,
            "message": f"""
            {formality} {scenario["pretext"]} for the {person["department"]}.
            
            {scenario["urgency"]}. Please use the link below to verify your access credentials.
            
            This is a standard security procedure to ensure all accounts are properly authenticated
            and to maintain compliance with our security policies.
            
            <strong>Note:</strong> Failure to verify may result in temporary access restrictions.
            """,
            "sender_name": "IT Security Team",
            "sender_role": "Information Technology Department",
            "demo_link": "http://localhost:8080/Landing-Page.html",
            "link_text": f"Verify {person['department']} Credentials",
            "target_info": f"Target: {person['name']} ({person['role']}, {person['department']})"
        }

        # Render email with CSS
        email_content = jinja_template.render(email_data)
        
        # Save email with sanitized filename ()
        safe_name = sanitize_filename(person['name'])
        safe_dept = sanitize_filename(person['department'])
        filename = inbox_dir / f"{safe_name}_{safe_dept}.html"
        
        with open(filename, "w", encoding='utf-8') as f:
            f.write(email_content)
        
        # Store the filename for the viewer
        email_files[person['name']] = f"{safe_name}_{safe_dept}.html"
        
        print(f"  {person['name']:30} -> {person['department']}")
    

    # Creating inbox viewer with target and department counts
    print("\nCreating inbox viewer page") 
    viewer_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phishing Simulation</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f8f9fa;
            color: #333;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eaeaea;
        }}
        .warning {{
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            margin: 20px 0;
            font-weight: bold;
            border-left: 4px solid #ffeaa7;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
        }}
        .stat {{
            text-align: center;
            padding: 20px;
            background: #e9ecef;
            border-radius: 8px;
            min-width: 120px;
        }}
        .stat .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #004080;
            margin-bottom: 5px;
        }}
        .email-list {{
            margin: 30px 0;
        }}
        .email-item {{
            padding: 15px;
            margin: 10px 0;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            display: block;
            text-decoration: none;
            color: #0066cc;
            transition: all 0.2s;
        }}
        .email-item:hover {{
            background: #e9ecef;
            border-color: #0066cc;
        }}
        .email-name {{
            font-weight: bold;
            color: #004080;
        }}
        .email-meta {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Phishing Simulation</h1>
        </div>
        
        <div class="warning">
            ACADEMIC SIMULATION - NO REAL EMAILS SENT
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="number">{len(people_data)}</div>
                <div>Targets</div>
            </div>
            <div class="stat">
                <div class="number">{len(set(p["department"] for p in people_data))}</div>
                <div>Departments</div>
            </div>
        </div>
        
        <h3>Generated Emails:</h3>
        <div class="email-list">
'''
    
    # Add emails using the stored filenames
    for person in people_data:
        filename = email_files.get(person['name'], f"{sanitize_filename(person['name'])}_{sanitize_filename(person['department'])}.html")
        viewer_html += f'''
            <a href="{filename}" class="email-item" target="_blank">
                <div class="email-name">{person['name']}</div>
                <div class="email-meta">
                    {person['department']} • {person['role']}
                </div>
            </a>
        '''
    
    viewer_html += '''
        </div>
        
        <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 0.9em;">
            <p>Cybersecurity Phishing Project</p>
            <p><em>All data was obtained from fake company: http://xaviermedy.github.io/</em></p>
        </div>
    </div>
</body>
</html>'''
    
    # Save viewer
    with open(inbox_dir / "inbox_viewer.html", "w", encoding='utf-8') as f:
        f.write(viewer_html)
    
    

    # Open in browser
    inbox_viewer_path = inbox_dir / "inbox_viewer.html"
    if inbox_viewer_path.exists():
        webbrowser.open(f"file://{inbox_viewer_path.resolve()}")
    else:
        print(f"Could not find {inbox_viewer_path}")

if __name__ == "__main__":
    main()