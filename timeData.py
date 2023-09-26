from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from getData import get_data

app = FastAPI()

# Define a route to display data for a specific date_time
@app.get('/get-data/{date_time}', response_class=HTMLResponse)
def get_data_for_date_time(date_time: str):
    # Call the function to get the data from the API
    data = get_data()
    if data is not None:
        # convert data to a HTML table
        html_table = "<table><tr><th>Time</th><th>Temperature</th><th>Humidity</th><th>CO2</th><th>Light</th><th>Motion</th><th>VDD</th></tr>"
        for entry in data["results"][0]["series"][0]["values"]:
            if entry[0] == date_time:  # بررسی تاریخ و زمان
                time, temperature, humidity, co2, light, motion, vdd = entry
                html_table += f"<tr><td>{time}</td><td>{temperature}</td><td>{humidity}</td><td>{co2}</td><td>{light}</td><td>{motion}</td><td>{vdd}</td></tr>"
        html_table += "</table>"
        
        # Return the HTML table as the response
        return HTMLResponse(content=html_table, status_code=200)
    else:
        return {"message": "Failed to fetch data from the API"}
