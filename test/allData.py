from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from getData import get_data

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # مسیر قالب‌های وب را تنظیم کنید.

# ...

# نمایش داده‌های مرتبط با اتاق
@app.post("/room/")
async def display_room_data(request: Request, room_id: int = Form(...), start_time: str = Form(...), end_time: str = Form(...)):
    data = get_data(room_id, start_time, end_time)
    if data is not None:
        return templates.TemplateResponse("result.html", {"request": request, "data": data, "room_id": room_id, "start_time": start_time, "end_time": end_time})
    else:
        return templates.TemplateResponse("error.html", {"request": request})
