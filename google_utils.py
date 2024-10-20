import requests

from config import GOOGLE_API_KEY, SEARCH_ENGINE_ID

def query_google(query: str, num_results = 10) -> str:
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        'key': GOOGLE_API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'num': num_results
    }

    # Send request to Google API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()
        if "items" in results:
            return results['items']
        else:
            return ""
    else:
        return f"Error: {response.status_code}"