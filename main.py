from fastapi import FastAPI
from getData import get_data  

app = FastAPI()

# Define a route to display the data
@app.get('/group10')
def get_temperature(date: str):
    # Call the function to get the data from the API
    data = get_data()
    for item in data:
        if item['date'] == date:
            return {"date": date, "temperature": item['temperature']}
    
    return {"message": "Data not found for the specified date"}

  

