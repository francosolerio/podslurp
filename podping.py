import requests
import sys
import urllib.parse
from datetime import datetime
import urllib.parse
import requests
import sys

def get_podpings(url):
    # Encode the URL for the API parameter
    encoded_url = urllib.parse.quote(url)
    
    # Construct the API URL
    api_url = f"https://api.podping.org/v2/pingslurp/podpings_by_iri/?iri={encoded_url}&skip=0&limit=100&show_tests=false"
    
    try:
        # Make the API request
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        try:
            response_data = response.json()
            if not isinstance(response_data, dict):
                print("Error: Unexpected response format - expected a dictionary")
                return

            if 'results' not in response_data:
                print("Error: Response missing 'results' field")
                return

            results = response_data['results']
            if not isinstance(results, list):
                print("Error: 'results' field is not a list")
                return

            if not results:
                print("No podpings found for this URL")
                return

            print("\nTimestamp                 | Reason")
            print("-" * 45)

            for item in results:
                if not isinstance(item, dict):
                    continue
                if 'timestamp' not in item or 'reason' not in item:
                    continue
                try:
                    timestamp = datetime.fromisoformat(item['timestamp'])
                    reason = item['reason']
                    print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {reason}")
                except ValueError:
                    continue

        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            return
            
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python podping.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    get_podpings(url)
