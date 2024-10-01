import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def search_serper(query):
    """Function to search using Serper API."""
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY is not set in the environment variables.")

    url = "https://api.serper.dev/search"
    headers = {
        "X-API-KEY": api_key
    }
    params = {
        "q": query
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()

try:
    # Example usage of the search function
    query = "latest advancements in AI"
    results = search_serper(query)

    # Print search results
    print("Search Results:")
    for result in results.get("organic", []):  # Assuming 'organic' key contains the search results
        print(f"Title: {result.get('title')}")
        print(f"Link: {result.get('link')}")
        print(f"Snippet: {result.get('snippet')}\n")

except requests.exceptions.RequestException as e:
    print(f"HTTP Request Error: {e}")
except ValueError as e:
    print(f"Value Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
