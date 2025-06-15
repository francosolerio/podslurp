import requests
import json
import sys
from datetime import datetime

def fetch_podping_data(url):
    """
    Fetches podping data for a given URL from the Podping API
    """
    base_url = "https://api.podping.org/v2/pingslurp/podpings_by_iri/"
    
    # URL encode the provided URL
    encoded_url = url.replace("/", "%2F").replace(":", "%3A").replace("?", "%3F")
    
    # Construct the full API URL
    api_url = f"{base_url}?iri={encoded_url}&skip=0&limit=10&show_tests=false"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def format_timestamp(timestamp):
    """
    Converts the timestamp to a readable format
    """
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return timestamp

def main():
    if len(sys.argv) != 2:
        print("Usage: python podping_scraper.py <podcast_feed_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    data = fetch_podping_data(url)
    
    if data and "data" in data:
        print("Timestamp\t\t\tReason")
        print("-" * 50)
        for item in data["data"]:
            timestamp = format_timestamp(item["timestamp"])
            reason = item["reason"]
            print(f"{timestamp}\t{reason}")
    else:
        print("No data found or error occurred.")

if __name__ == "__main__":
    main()
