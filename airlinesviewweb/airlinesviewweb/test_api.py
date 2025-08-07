import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('AVIATIONSTACK_API_KEY')


def test_api_call(limit=5):
    """Test AviationStack API and print flight info."""
    url = 'http://api.aviationstack.com/v1/flights'
    params = {
        'access_key': API_KEY,
        'limit': limit
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        flights = response.json().get('data', [])
        print(f"{'Airline':30} | {'Departure':25} → {'Arrival':25} | Date")
        print("-" * 100)
        for f in flights:
            airline = f.get('airline', {}).get('name', 'N/A')
            dep = f.get('departure', {}).get('airport', 'N/A')
            arr = f.get('arrival', {}).get('airport', 'N/A')
            date = f.get('departure', {}).get('scheduled', 'N/A')[:10] if f.get('departure', {}).get('scheduled') else 'N/A'
            print(f"{airline:30} | {dep:25} → {arr:25} | {date}")
    else:
        print("❌ API call failed!")
        print("Status Code:", response.status_code)
        print("Response:", response.text)


# Run the test
if __name__ == "__main__":
    test_api_call()
