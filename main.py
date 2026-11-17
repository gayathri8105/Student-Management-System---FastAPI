from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models import Student

app = FastAPI()
templates = Jinja2Templates(directory="templates")

db_students = [
    {"id": 1, "name": "Kavya", "age": 22, "gender": "Female", "marks": 99, "course": "Python", "attendance": "Present", "image_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"},
    {"id": 2, "name": "Sravya Veginati", "age": 23, "gender": "Female", "marks": 93, "course": "Mern", "attendance": "Absent", "image_url": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150"},
    {"id": 3, "name": "Sruthi", "age": 22, "gender": "Female", "marks": 95, "course": "Swift", "attendance": "Present", "image_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150"},
    {"id": 4, "name": "Jagadeesh", "age": 25, "gender": "Male", "marks": 88, "course": "Ruby", "attendance": "Present", "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150"},
    {"id": 5, "name": "Akhil", "age": 24, "gender": "Male", "marks": 82, "course": "Java", "attendance": "Present", "image_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150"},
    {"id": 6, "name": "Bhavya Gudavathi", "age": 23, "gender": "Female", "marks": 91, "course": "Python", "attendance": "Present", "image_url": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=150"},
    {"id": 7, "name": "Shiva Rama Krishna", "age": 26, "gender": "Male", "marks": 79, "course": "Mern", "attendance": "Absent", "image_url": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=150"},
    {"id": 8, "name": "Suverna", "age": 20, "gender": "Female", "marks": 78, "course": "Java", "attendance": "Present", "image_url": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150"},
    {"id": 9, "name": "Bhavya", "age": 23, "gender": "Female", "marks": 88, "course": "Mern", "attendance": "Present", "image_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150"},
    {"id": 10, "name": "Sreya", "age": 22, "gender": "Female", "marks": 88, "course": "Mern", "attendance": "Absent", "image_url": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150"}
]

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"students": db_students})

@app.get("/students/add")
def add_student_form(request: Request):
    return templates.TemplateResponse(request, "add_student.html")

@app.post("/students/add")
def create_student(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    marks: int = Form(...),
    course: str = Form(...),
    attendance: str = Form(...),
    image_url: Optional[str] = Form("")
):
    new_id = max([s["id"] for s in db_students], default=0) + 1
    student_data = {
        "id": new_id,
        "name": name,
        "age": age,
        "gender": gender,
        "marks": marks,
        "course": course,
        "attendance": attendance,
        "image_url": image_url
    }
    validated = Student(**student_data)
    db_students.append(validated.model_dump())
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/students/edit/{student_id}")
def edit_student_form(request: Request, student_id: int):
    student = next((s for s in db_students if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse(request, "edit_student.html", {"student": student})

@app.post("/students/update/{student_id}")
def update_student(
    student_id: int,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    marks: int = Form(...),
    course: str = Form(...),
    attendance: str = Form(...),
    image_url: Optional[str] = Form("")
):
    student = next((s for s in db_students if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.update({
        "name": name,
        "age": age,
        "gender": gender,
        "marks": marks,
        "course": course,
        "attendance": attendance,
        "image_url": image_url
    })
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/students/delete/{student_id}")
def delete_student(student_id: int):
    global db_students
    db_students = [s for s in db_students if s["id"] != student_id]
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)