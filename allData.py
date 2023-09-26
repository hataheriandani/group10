# from fastapi import FastAPI
# from getData import get_data

# app = FastAPI()

# # Define a route to display all data
# @app.get('/')
# def display_data():
#     # Call the function to get the data from the API
#     data = get_data()
#     if data is not None:
#         return data
#     else:
#         return {"message": "Failed to fetch data from the API"}
from fastapi import FastAPI
from getData import get_data

app = FastAPI()

# Define a route to display data for a specific room
@app.get('/room/{room_id}')
def display_data(room_id: int):
    # Call the function to get the data from the API using the provided room_id
    data = get_data(room_id)
    if data is not None:
        return data
    else:
        return {"message": "Failed to fetch data from the API"}

# Run uvicorn allData:app --reload in and add  http://127.0.0.1:8000/room/{room_id} to see data room with this id: {room_id}

      