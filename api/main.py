# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="EduPro MVP API",
    version="0.1.0",
    description="MVP simple de EduPro: cursos y progreso de estudiantes."
)

# ====== Modelos Pydantic ======

class Course(BaseModel):
    id: int
    title: str
    description: str
    level: str


class Progress(BaseModel):
    student_id: int
    course_id: int
    completed_percent: float


# ====== Datos simulados (MVP, sin BD aún) ======

COURSES_DB = [
    Course(id=1, title="Python básico", description="Introducción a Python.", level="Beginner"),
    Course(id=2, title="Introducción a Web", description="HTML, CSS y fundamentos web.", level="Beginner"),
    Course(id=3, title="Algoritmos I", description="Estructuras de datos básicas.", level="Intermediate"),
]

PROGRESS_DB = [
    Progress(student_id=1, course_id=1, completed_percent=75.0),
    Progress(student_id=1, course_id=2, completed_percent=20.0),
    Progress(student_id=2, course_id=1, completed_percent=100.0),
]


# ====== Endpoints del MVP ======

@app.get("/health", tags=["system"])
def health_check():
    """
    Endpoint de salud para verificar que la API está viva.
    """
    return {"status": "ok", "service": "EduPro API", "version": "0.1.0"}


@app.get("/courses", response_model=List[Course], tags=["courses"])
def list_courses():
    """
    Devuelve el listado de cursos disponibles (simulado).
    """
    return COURSES_DB


@app.get(
    "/students/{student_id}/progress",
    response_model=List[Progress],
    tags=["progress"]
)
def get_student_progress(student_id: int):
    """
    Devuelve el progreso del estudiante en todos los cursos (simulado).
    """
    progress = [p for p in PROGRESS_DB if p.student_id == student_id]
    if not progress:
        raise HTTPException(status_code=404, detail="No se encontró progreso para este estudiante.")
    return progress
