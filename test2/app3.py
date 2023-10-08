from flask import Flask, render_template, request
import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app3 = Flask(__name__)

app3.template_folder = 'C:\\Users\\Taheri\\Desktop\\group10\\test2'

website_url = 'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata'

scheduler = BackgroundScheduler()

@app3.route('/', methods=['GET', 'POST'])
def home3():
    return render_template('home3.html')

headers = {
    'x-api-key': 'II6dsQDctGjWeoHgnT5wPjXlyJVmmUbvASnh2Zay',
}

@app3.route('/hotel_rooms', methods=['GET', 'POST'])
def hotel_rooms():
    data = None

    if request.method == 'POST':
        print("Form submitted via POST method")
        room_id = request.form['room_id']
        start_time_str = request.form['start_time']

        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        
        end_time = start_time + timedelta(days=365)

        params = {
            'room-id': room_id,
            'startTime': start_time_str,
            'endTime': end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'fields': 'temperature,humidity,co2,light,motion,vdd',
            'building-id': '2',
        }

        try:
            response = requests.get(website_url, headers=headers, params=params, verify=False)
            response.raise_for_status()
            raw_data = response.json()

            # Extract the 'results' key from the JSON
            results = raw_data.get("results")

            if results and len(results) > 0:
                # Take the first result
                first_result = results[0]

                # Extract 'series' from the first result
                series = first_result.get("series")

                if series and len(series) > 0:
                    # Take the first series
                    first_series = series[0]

                    # Extract 'columns' and 'values' from the first series
                    columns = first_series.get("columns")
                    values = first_series.get("values")

                    # Now you can pass 'columns' and 'values' to the template for rendering

                    data = {
                        "columns": columns,
                        "values": values
                    }

        except requests.exceptions.RequestException as e:
            error_message = f"Request failed: {e}"
            return render_template('error.html', error_message=error_message)

    return render_template('hotel_rooms.html')




# تعریف یک وظیفه برنامه زمان‌بندی برای به روز رسانی اطلاعات هر 15 دقیقه
def update_data():
    # اینجا کد به روز رسانی اطلاعات را قرار دهید (مشابه کد درون تابع home)
    pass

# اضافه کردن وظیفه به زمان‌بندی با فراخوانی تابع add_job
scheduler.add_job(update_data, 'interval', minutes=15)

if __name__ == '__main__':
    # شروع زمان‌بندی
    scheduler.start()
    app3.run()
