from flask import Flask, render_template, request
import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler

app1 = Flask(__name__)

app1.template_folder = 'C:\\Users\\Taheri\\Desktop\\group10\\test2'

website_url = 'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata'

# ایجاد یک شیء از BackgroundScheduler
scheduler = BackgroundScheduler()

@app1.route('/', methods=['GET', 'POST'])
def home1():
    data = None

    if request.method == 'POST':
        room_id = request.form['room_id']

        params = {
            'room-id': room_id,
            'startTime': '2023-02-01T00:00:00Z',
            'endTime': '2023-05-05T12:30:00Z',
            'fields': 'temperature,humidity,co2,light,motion,vdd',
            'building-id': '2',
        }

        headers = {
            'x-api-key': 'II6dsQDctGjWeoHgnT5wPjXlyJVmmUbvASnh2Zay',
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
            return {"message": f"Request failed: {e}"}

    return render_template('home1.html', data=data)

# تعریف یک وظیفه برنامه زمان‌بندی برای به روز رسانی اطلاعات هر 15 دقیقه
def update_data():
    # اینجا کد به روز رسانی اطلاعات را قرار دهید (مشابه کد درون تابع home)
    pass

# اضافه کردن وظیفه به زمان‌بندی با فراخوانی تابع add_job
scheduler.add_job(update_data, 'interval', minutes=15)

if __name__ == '__main__':
    # شروع زمان‌بندی
    scheduler.start()
    app1.run()
