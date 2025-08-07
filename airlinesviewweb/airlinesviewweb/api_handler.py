import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
AVIATIONSTACK_API_KEY = os.getenv('AVIATIONSTACK_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_URL = os.getenv('GROQ_URL')
GROQ_MODEL = os.getenv('GROQ_MODEL')


def get_flight_data(limit=100, pages=2):
    """Fetch flight data using pagination."""
    all_flights = []

    for i in range(pages):
        offset = i * limit
        url = 'http://api.aviationstack.com/v1/flights'
        params = {
            'access_key': AVIATIONSTACK_API_KEY,
            'limit': limit,
            'offset': offset
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json().get('data', [])
            all_flights.extend(data)
        else:
            print(f"❌ API Error (Page {i+1}): {response.status_code} - {response.text}")
            break

    return all_flights


def get_chatgpt_summary(flights):
    """Generate summary of flight data using GROQ AI."""
    if not flights:
        return "No flights found to summarize."

    flight_lines = [
        f"- {f.get('airline', {}).get('name', 'N/A')} | "
        f"{f.get('departure', {}).get('airport', 'N/A')} → "
        f"{f.get('arrival', {}).get('airport', 'N/A')} | "
        f"{f.get('flight_status', 'N/A')} | "
        f"{f.get('departure', {}).get('scheduled', 'N/A')}"
        for f in flights
    ]

    prompt = f"""
Analyze the following flight data and summarize the demand trends:

{chr(10).join(flight_lines)}

Please summarize:
1. Most popular routes
2. Frequently appearing airlines
3. Any noticeable patterns
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a travel data analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("GROQ API Error:", e)
        return "Failed to fetch summary from GROQ API."


def ask_flight_bot(question, flights):
    """Ask AI a question about the current flight data."""
    if not flights:
        return "No flight data available to answer."

    flight_lines = [
        f"- {f.get('airline', {}).get('name', 'N/A')} | "
        f"{f.get('departure', {}).get('airport', 'N/A')} → "
        f"{f.get('arrival', {}).get('airport', 'N/A')} | "
        f"{f.get('flight_status', 'N/A')} | "
        f"{f.get('departure', {}).get('scheduled', 'N/A')}"
        for f in flights
    ]

    prompt = f"""
You are a flight data assistant. Here is the current flight data:

{chr(10).join(flight_lines)}

Now answer this user question based on the above data:
{question}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that analyzes live flight data."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("Chatbot Error:", e)
        return "Failed to get response from chatbot."
