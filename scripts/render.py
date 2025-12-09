# # Import libraries
# from jinja2 import Template
# import os
# import webbrowser
# # -------------------------------
# # Create Inbox folder
# # -------------------------------
# os.makedirs("Inbox", exist_ok=True)

# # -------------------------------
# # Step 1: Read the Jinja2 email template
# # -------------------------------
# with open("Email_template.html", "r") as file:
#     template_str = file.read()

# jinja_template = Template(template_str)

# # -------------------------------
# # Step 2: Recipients (simulated)
# # -------------------------------
# people_data = [
#     {"name": "Dr. Maya H. Sullivan", "email": "jmaya.sullivan@trfuture.com"},
#     {"name": "Ronald Vega", "email": "ronald.vega@trfuture.com"},
#     {"name": "Ethan Valdez", "email": "ethan.valdez@trfuture.com"},
#      {"name": "Xavier Medy", "email": "xavier.medy@trfuture.com"},
#      {"name": "Nidra Hayes", "email": "nidra.hayes@trfuture.com"},
#      {"name": "Michelle Ortega", "email": "michelle.ortega@trfuture.com"},
#      {"name": "Kevin R. Martens", "email": "kevin.martens@trfuture.com"},
# ]

# # -------------------------------
# # Step 3: Generate FAKE emails (local only)
# # -------------------------------
# for person in people_data:

#     email_data = {
#         "subject": "Cybersecurity Simulation Demo",
#         "greeting": f"Hello {person['name']}!",
#         "message": (
#             "This email is part of a controlled cybersecurity simulation. "
#             "Please click the link below to open the demonstration landing page."
#         ),
#         "sender_name": "Jim Hariston",
#         "sender_role": "Information Technology Security Manager (IT SM)",
#         "demo_link": "http://localhost:8080/Landing-Page.html",
#         "link_text": "Open Simulation Landing Page",
#         "disclaimer": (
#             "⚠ Academic Cybersecurity Simulation — This is NOT a real login page. "
#             "No real credentials should be entered. No data is collected or transmitted."
#         )
#     }

#     # Render with Jinja2
#     email_content = jinja_template.render(email_data)

#     # Save email to Inbox folder
#     filename = f"Inbox/{person['name'].replace(' ', '_')}.html"
#     with open(filename, "w") as f:
#         f.write(email_content)

#     print(f"Saved fake email: {filename}")

# # -------------------------------
# # Step 4: Create Fake Inbox Viewer Page
# # -------------------------------
# email_files = [f for f in os.listdir("Inbox") if f.endswith(".html")]

# viewer_html = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Fake Inbox Viewer</title>
#     <style>
#         body { font-family: Arial; background: #1a1a1a; color: #e6e6e6; }
#         .email-list a { 
#             color: #4da6ff; 
#             font-size: 18px; 
#             display: block; 
#             margin: 10px 0;
#             text-decoration: none;
#         }
#         .email-list a:hover { text-decoration: underline; }
#         h1 { color: #fff; }
#     </style>
# </head>
# <body>
#     <h1>Fake Inbox Viewer</h1>
#     <p>Select an email to open:</p>
#     <div class="email-list">
# """

# for email in email_files:
#     if email != "inbox_viewer.html":
#         viewer_html += f'<a href="{email}" target="_blank">{email}</a>\n'

# viewer_html += """
#     </div>
# </body>
# </html>
# """

# with open("Inbox/inbox_viewer.html", "w") as f:
#     f.write(viewer_html)

# print("Fake Inbox Viewer created at Inbox/inbox_viewer.html")
# print("Simulation completed successfully.")

# # Get absolute path to inbox viewer
# inbox_viewer_path = os.path.abspath("Inbox/inbox_viewer.html")

# # Open in default browser
# webbrowser.open(f"file://{inbox_viewer_path}")

##merged into integrated_render.py