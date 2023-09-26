# update_data.py
import schedule
import time
from getData import get_data

def update_data():
    data = get_data()  # فراخوانی تابع برای دریافت داده‌ها
    if data is not None:
        # انجام عملیات آپدیت داده‌ها اینجا
        print("Data updated successfully.")
    else:
        print("Failed to fetch data from the API.")

# تعیین زمان اجرای تابع آپدیت
schedule.every(15).minutes.do(update_data)

while True:
    schedule.run_pending()
    time.sleep(1)
