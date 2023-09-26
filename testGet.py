import requests
import json
import urllib3
from fastapi import FastAPI

urllib3.disable_warnings()  # This disables SSL warnings; use it cautiously in production.

base_url = 'https://iot.research.hamk.fi/api/v1/hamk/'

def get_data(building_id, room_id):
    headers = {
        'x-api-key': 'II6dsQDctGjWeoHgnT5wPjXlyJVmmUbvASnh2Zay',
    }
    params = {
        'building-id': building_id,
    }

    # Get list of buildings
    buildings_url = base_url + 'buildings'
    try:
        response = requests.get(buildings_url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        buildings = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")
        return None

    # Loop through buildings and rooms
    all_data = []
    for building in buildings:
        building_id = building.get('id')  # از `get` استفاده شده تا در صورت عدم وجود کلید 'id'، مقدار `None` برگردانده شود
        if building_id is None:
            continue  # اگر 'id' موجود نباشد، به مرحله بعد برو

        rooms_url = base_url + f'rooms?building-id={building_id}'
        try:
            response = requests.get(rooms_url, headers=headers, params=params, verify=False)
            response.raise_for_status()
            rooms = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {e}")
            return None

        for room in rooms:
            room_id = room.get('id')  # از `get` استفاده شده تا در صورت عدم وجود کلید 'id'، مقدار `None` برگردانده شود
            if room_id is None:
                continue  # اگر 'id' موجود نباشد، به مرحله بعد برو

            tsdata_url = base_url + f'rooms/tsdata?room-id={room_id}&startTime=2023-02-01T00:00:00Z&endTime=2023-05-05T12:30:00Z&fields=temperature,humidity,co2,light,motion,vdd'
            try:
                response = requests.get(tsdata_url, headers=headers, params=params, verify=False)
                response.raise_for_status()
                room_data = response.json()
                all_data.append(room_data)
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            except json.JSONDecodeError as e:
                print(f"JSON parsing failed: {e}")

    return all_data