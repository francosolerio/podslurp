import requests
import sys
import urllib.parse
from datetime import datetime
import urllib.parse
import requests
import sys
import pytz
import argparse

def get_podpings(url, timezone=None):
    # If timezone is specified, get the timezone object
    tz = None
    if timezone:
        try:
            tz = pytz.timezone(timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            print(f"Error: Unknown timezone '{timezone}'")
            print("For a list of valid timezones, visit: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
            return
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
                    # Parse timestamp and explicitly mark it as UTC
                    timestamp = datetime.fromisoformat(item['timestamp'])
                    reason = item['reason']
                    # Convert to specified timezone if provided
                    if tz:
                        # Make timestamp aware of UTC
                        utc_timestamp = timestamp.replace(tzinfo=pytz.UTC)
                        # Convert to target timezone
                        local_timestamp = utc_timestamp.astimezone(tz)
                        # Format with timezone name
                        formatted_time = local_timestamp.strftime('%Y-%m-%d %H:%M %Z')
                    else:
                        # Keep UTC if no timezone specified
                        formatted_time = timestamp.strftime('%Y-%m-%d %H:%M UTC')
                    print(f"{formatted_time} | {reason}")
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
    parser = argparse.ArgumentParser(description='Fetch podping updates for a podcast feed URL')
    parser.add_argument('url', help='The podcast feed URL to check')
    parser.add_argument('--tz', '-t', help='Convert timestamps to this timezone (e.g., US/Pacific, Europe/London)')
    args = parser.parse_args()

    get_podpings(args.url, args.tz)
