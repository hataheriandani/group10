import requests
import json
import urllib3

def get_data(room_id, start_time, end_time):
    urllib3.disable_warnings()  # This disables SSL warnings; use it cautiously in production.

    # Use the provided room_id, start_time, and end_time to customize the URL
    url = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={room_id}&startTime={start_time}&endTime={end_time}&fields=temperature,humidity,co2,light,motion,vdd'

    headers = {
        'x-api-key': 'II6dsQDctGjWeoHgnT5wPjXlyJVmmUbvASnh2Zay',
    }
    params = {
        'building-id': '2',
    }
    try:
        response = requests.get(url, headers=headers, params=params, verify=False)  # Use verify=False with caution.
        response.raise_for_status()  # Raise an exception for non-2xx responses.

        # Parse JSON response if successful
        data = response.json()
        return data  # Return the fetched data
    except requests.exceptions.RequestException as e:
        return {"message": f"Request failed: {e}"}
    except json.JSONDecodeError as e:
        return {"message": f"JSON parsing failed: {e}"}
