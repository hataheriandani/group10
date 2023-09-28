from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# تنظیم مسیر پیشفرض پوشه تمپلیت‌ها به مسیر مورد نظر
app.template_folder = 'C:\\Users\\Taheri\\Desktop\\group10\\test2'

# آدرس وب‌سایت مورد نظر برای دریافت اطلاعات
website_url = 'https://iot.research.hamk.fi/api/v1/hamk/rooms/tsdata'

# مسیر برای نمایش اطلاعات در تمپلیت
@app.route('/', methods=['GET', 'POST'])
def home():
    data = None  # تا زمانی که اطلاعات دریافت نشده است، مقدار data را None قرار می‌دهیم.

    if request.method == 'POST':
        # از فرم ارسال شده اطلاعات اتاق را دریافت می‌کنیم
        room_id = request.form['room_id']

        # پارامترهای مورد نیاز برای درخواست
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
            response = requests.get(website_url, headers=headers, params=params, verify=False)  # Use verify=False with caution.
            response.raise_for_status()  # Raise an exception for non-2xx responses.

            # Parse JSON response if successful
            data = response.json()
        except requests.exceptions.RequestException as e:
            return {"message": f"Request failed: {e}"}

    return render_template('home.html', data=data)

if __name__ == '__main__':
    app.run()
