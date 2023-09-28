import requests

def get_data(building_id, room_id):
    url = f'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata?room-id={room_id}&startTime=2023-02-01T00:00:00Z&endTime=2023-05-05T12:30:00Z&fields=temperature,humidity,co2,light,motion,vdd'
    headers = {
        'x-api-key': 'II6dsQDctGjWeoHgnT5wPjXlyJVmmUbvASnh2Zay',
    }
    
    try:
        response = requests.get(url, headers=headers, verify=False)  # Use verify=False with caution.
        response.raise_for_status()  # Raise an exception for non-2xx responses.

        # Parse JSON response if successful
        data = response.json()
        return data  # Return the fetched data
    except requests.exceptions.RequestException as e:
        return {"message": f"Request failed: {e}"}

# اطلاعات ساختمان و اتاق مورد نظر
building_id = '2'
room_id = 'YourRoomID'

# دریافت اطلاعات
data = get_data(building_id, room_id)
print(data)
