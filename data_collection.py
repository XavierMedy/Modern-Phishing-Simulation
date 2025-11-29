import requests
from bs4 import BeautifulSoup

#GitHub Pages website URL
url = "https://xaviermedy.github.io"   # <-- change to your actual page URL

#Fetch page
response = requests.get(url)
response.raise_for_status()  # raises an error if request failed

#Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

#Find all employee blocks
employees = soup.find_all("div", class_="employee")

results = []

for emp in employees:
    #Extract role text (e.g., "CEO:")
    role = emp.find("span", class_="role").get_text(strip=True).replace(":", "")

    #Extract name 
    text = emp.get_text(" ", strip=True)

    #Split around the email arrow "—"
    parts = text.split("—")
    
    left = parts[0].strip()

    #Remove the role part from the left side
    name = left.replace(emp.find("span", class_="role").get_text(strip=True), "").strip()

    #Extract email from the <a> tag
    email_tag = emp.find("a", href=True)
    email = email_tag.get_text(strip=True) if email_tag else None

    results.append({
        "role": role,
        "name": name,
        "email": email
    })

# Print extracted data
for i in results:
    print(i)
    ###
