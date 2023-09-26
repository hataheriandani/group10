from fastapi import FastAPI
from testGet import get_data

app = FastAPI()

# Define a route to display data for a specific building and room using path parameters
@app.get('/get_data/{building_id}/{room_id}')
def display_data(building_id: int, room_id: int):
    # Call the function to get the data from the API
    data = get_data(building_id, room_id)
    if data is not None:
        return data
    else:
        return {"message": "Failed to fetch data from the API"}

# Define a route to display data for all buildings and rooms using query parameters
@app.get('/get_all_data')
def display_all_data(building_id: int = 1, room_id: int = 1):
    all_data = []
    for building_id in range(1, 3):  # Assuming you have two buildings (1 and 2)
        for room_id in range(1, 24):
            room_data = get_data(building_id, room_id)
            if room_data:
                all_data.append(room_data)
    return all_data
