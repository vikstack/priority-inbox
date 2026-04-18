from groq import Groq
from fetch_email import get_emails
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an email triage assistant. Categorize emails into exactly one category:

- 'Action Today': Requires YOUR response or action TODAY — explicit same-day urgency, or sender is blocked waiting on you
- 'Can Wait': Has a future deadline (days or weeks away), is informational, or needs a reply but not urgently  
- 'Noise': Promotional, automated, newsletter, CC-only, or no response needed

Rules:
- A deadline next week = 'Can Wait', NOT 'Action Today'
- Only use 'Action Today' if inaction TODAY causes a real problem
- When in doubt, use 'Can Wait'

Respond in this exact format (nothing else):
Category: <Action Today|Can Wait|Noise>
Summary: <one line, max 12 words>"""

emails = get_emails()

for email in emails:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Triage this email:\n\n{email}"}
        ],
        temperature=0
    )
    
    result = response.choices[0].message.content.strip()
    lines = result.splitlines()
    category = lines[0].replace("Category:", "").strip() if lines else "Unknown"
    summary = lines[1].replace("Summary:", "").strip() if len(lines) > 1 else ""
    
    print(f"[{category}] {summary}")
    print(f"  ↳ {email[:80]}..." if len(email) > 80 else f"  ↳ {email}")
    print("---")