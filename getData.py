

# def get_data():
#     import requests
#     import json
#     import urllib3
#     room = int(input("Enter the room:"))
#     urllib3.disable_warnings()  # This disables SSL warnings; use it cautiously in production.
#     url = 'https://iot.research.hamk.fi/api/v1/hamk/buildings'
#     url = 'https://iot.research.hamk.fi/api/v1/hamk/rooms?building-id=<building-id>'
#     url = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={room}&startTime=2023-02-01T00:00:00Z&endTime=2023-05-05T12:30:00Z&fields=temperature,humidity,co2,light,motion,vdd'

# def get_data():
#     import requests
#     import json
#     import urllib3
#     room = int(input("Enter the room:"))

#     urllib3.disable_warnings()  # This disables SSL warnings; use it cautiously in production.

#     url = 'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={room}&startTime=2023-02-01T00:00:00Z&endTime=2023-05-05T12:30:00Z&fields=temperature,humidity,co2,light,motion,vdd'
#     headers = {
#         'x-api-key': 'II6dsQDctGjWeoHgnT5wPjXlyJVmmUbvASnh2Zay',
#     }
#     params = {
#         'building-id': '2',
#     }
#     try:
#         response = requests.get(url, headers=headers, params=params, verify=False)  # Use verify=False with caution.
#         response.raise_for_status()  # Raise an exception for non-2xx responses.

#         # Parse JSON response if successful
#         data = response.json()
#         return data  # Return the fetched data
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         return None
#     except json.JSONDecodeError as e:
#         print(f"JSON parsing failed: {e}")
#         return None
import requests
import json
import urllib3

def get_data(room_id):
    urllib3.disable_warnings()  # This disables SSL warnings; use it cautiously in production.

    # Use the provided room_id to customize the URL
    url = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={room_id}&startTime=2023-02-01T00:00:00Z&endTime=2023-05-05T12:30:00Z&fields=temperature,humidity,co2,light,motion,vdd'

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
