# Podslurp

A command-line tool to fetch and display update history for podcast feeds using the Podping API. This tool helps podcast creators track when a podcast feed was updated, went live, or ended a live session.

## Features

- Fetches up to 100 recent updates for any podcast feed
- Displays timestamps and reasons for each update
- Supports timezone conversion for easier reading
- Clean, formatted output
- Handles various update types (live, liveEnd, update)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/francosolerio/podslurp.git
cd podslurp
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage (timestamps in UTC):
```bash
python podslurp.py <podcast_feed_url>
```

Convert timestamps to your timezone:
```bash
python podslurp.py <podcast_feed_url> --tz <timezone>
```

Example:
```bash
python podslurp.py https://feeds.podcastindex.org/pc20.xml --tz US/Pacific
```

### Timezone Examples

You can use any timezone from the IANA Time Zone Database. Common examples:
- `US/Pacific`
- `US/Eastern`
- `Europe/London`
- `Europe/Paris`
- `Asia/Tokyo`
- `Australia/Sydney`

For a complete list of valid timezones, visit: [List of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Sample Output

```
Timestamp                 | Reason
---------------------------------------------
2025-06-13 12:52 PDT | liveEnd
2025-06-13 12:50 PDT | liveEnd
2025-06-13 12:46 PDT | liveEnd
2025-06-13 10:27 PDT | live
2025-06-11 13:54 PDT | update
```

## Requirements

- Python 3.x
- `requests` library
- `pytz` library

## Error Handling

The tool includes error handling for:
- Invalid URLs
- Network connection issues
- Invalid timezone names
- Malformed API responses

## API Information

This tool uses the Podping API v2 endpoint:
```
https://api.podping.org/v2/pingslurp/podpings_by_iri/
```

## License

This project is open source and available under the MIT License.
