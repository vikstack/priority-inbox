from groq import Groq
from fetch_email import get_emails
from dotenv import load_dotenv
import os
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#get_email = "Subject: Meeting tomorrow From: Vikas - Please join the team meeting at 9am tomorrow to discuss Q2 targets."

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
       #print("email sent to the groq api: ", get_emails()),
        {"role": "user", "content": f"Categorize this email as Action Today, Can Wait, or Noise. Then give one line summary. Email: {get_emails()}"}
    ]
)

print(response.choices[0].message.content)