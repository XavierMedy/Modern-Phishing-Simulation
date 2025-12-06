# Modern-Phishing-Simulation
A comprehensive phishing simulation framework for cybersecurity education and penetration testing. This tool generates targeted phishing campaigns with realistic email templates and includes Kali Linux keyboard logging capabilities.|

This simulation demonstrates:
- Targeted email generation based on scraped employee data
- Department-specific phishing scenarios
- Kali Linux keyboard event logging


### Prerequisites
- Kali Linux (recommended) or any Linux distribution
- Python 3.8 or higher
- Git

### Installation
1. **Download and Install Kali Linux**
   - Download Kali Linux from [kali.org](https://www.kali.org/get-kali/)
   - Install on a VM

2. **Clone the Repository inside Kali Machine**
   git clone https://github.com/XavierMedy/Modern-Phishing-Simulation.git
   cd Modern-Phishing-Simulation

3. Set Up Python Environment
  # Create virtual environment
  python3 -m venv venv 
  
  # Activate virtual environment
  source venv/bin/activate

4. Install Dependencies
  pip install -r requirements.txt


####Running the Simulation####
Run: python scripts/integrated_render.py
 - This scraps employee data from https://xaviermedy.github.io/ github pages
 - Generates targeted phishing emails
 - Builds employee inbox for fake emails

Start the server:  python server.py
  - Server runs on http://localhost:8080
  - Landing page with keyboard logging
  - Keystroke data storage in keyboard_logs


Features
1. Automated Email Generation
- Scrapes employee data from GitHub Pages
- Creates department-specific phishing scenarios
- Uses Jinja2 templates for realistic email formatting
- Generates personalized greetings and content

2. Kali Linux Keyboard Logging
- Records all keyboard interactions on landing page
- Stores data locally in JSON format
- Web-based log viewer interface

3. Multi-Stage Email Simulation
- IT Department: Security certificate expiry notices
- Human Resources: Policy update reviews
- Finance: Invoice processing alerts
- Management: Executive dashboard access
- Marketing: Campaign analytics portals
- Operations: System maintenance notifications




  
  

   

