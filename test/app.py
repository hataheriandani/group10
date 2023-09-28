from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from getData import get_data

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # مسیر قالب‌های وب را تنظیم کنید.


@app.get("/")
async def read_form(request: Request):
    return templates.TemplateResponse("room_input.html", {"request": request})

@app.post("/get_room_data")
async def get_room_data(request: Request, room_number: int = Form(...)):
    # دریافت اطلاعات اتاق مورد نظر با استفاده از تابع get_data
    data = get_data(room_number)
    if data is not None:
        return templates.TemplateResponse("room_data.html", {"request": request, "data": data, "room_number": room_number})
    else:
        return templates.TemplateResponse("templates/room_input.html", {"request": request})
        


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

