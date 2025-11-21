# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse

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

@app.get("/", response_class=HTMLResponse, tags=["ui"])
def home():
    """
    Página sencilla que consume las APIs de cursos y progreso.
    """
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8" />
        <title>EduPro - MVP</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 1.5rem;
                background: #0f172a;
                color: #e5e7eb;
            }
            h1, h2 {
                color: #38bdf8;
            }
            .card {
                background: #111827;
                border-radius: 8px;
                padding: 1rem 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 0.5rem;
            }
            th, td {
                padding: 0.5rem;
                border-bottom: 1px solid #1f2937;
            }
            th {
                text-align: left;
                color: #93c5fd;
            }
            input, button {
                padding: 0.4rem 0.6rem;
                border-radius: 4px;
                border: 1px solid #4b5563;
                background: #020617;
                color: #e5e7eb;
            }
            button {
                cursor: pointer;
                background: #22c55e;
                border-color: #16a34a;
                margin-left: 0.4rem;
            }
            button:hover {
                background: #16a34a;
            }
            .tag {
                display: inline-block;
                font-size: 0.75rem;
                padding: 0.15rem 0.45rem;
                border-radius: 999px;
                background: #1d4ed8;
                color: #e5e7eb;
            }
            .muted {
                color: #9ca3af;
                font-size: 0.9rem;
            }
        </style>
    </head>
    <body>
        <h1>EduPro – MVP</h1>
        <p class="muted">
            Demo mínima conectada a la API Python desplegada en Vercel.
        </p>

        <div class="card">
            <h2>📚 Catálogo de cursos</h2>
            <p class="muted">Datos obtenidos desde <code>GET /courses</code>.</p>
            <table id="courses-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Curso</th>
                        <th>Descripción</th>
                        <th>Nivel</th>
                    </tr>
                </thead>
                <tbody id="courses-body">
                    <tr><td colspan="4">Cargando cursos...</td></tr>
                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>📈 Progreso por estudiante</h2>
            <p class="muted">
                Consulta el progreso simulado usando <code>GET /students/&lt;id&gt;/progress</code>.
            </p>
            <div style="margin-bottom: 0.5rem;">
                <label for="student-id">ID de estudiante:</label>
                <input type="number" id="student-id" value="1" min="1" />
                <button onclick="loadProgress()">Ver progreso</button>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Curso</th>
                        <th>Porcentaje completado</th>
                    </tr>
                </thead>
                <tbody id="progress-body">
                    <tr><td colspan="2">Ingresa un ID de estudiante y presiona "Ver progreso".</td></tr>
                </tbody>
            </table>
        </div>

        <script>
            async function loadCourses() {
                const tbody = document.getElementById('courses-body');
                try {
                    const res = await fetch('/courses');
                    if (!res.ok) throw new Error('Error al cargar cursos');
                    const courses = await res.json();
                    if (!Array.isArray(courses) || courses.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="4">No hay cursos disponibles.</td></tr>';
                        return;
                    }
                    tbody.innerHTML = courses.map(c => `
                        <tr>
                            <td>${c.id}</td>
                            <td>${c.title}</td>
                            <td>${c.description}</td>
                            <td><span class="tag">${c.level}</span></td>
                        </tr>
                    `).join('');
                } catch (err) {
                    tbody.innerHTML = '<tr><td colspan="4">Error al obtener cursos.</td></tr>';
                    console.error(err);
                }
            }

            async function loadProgress() {
                const studentId = document.getElementById('student-id').value;
                const tbody = document.getElementById('progress-body');
                if (!studentId) {
                    tbody.innerHTML = '<tr><td colspan="2">Ingresa un ID de estudiante.</td></tr>';
                    return;
                }
                tbody.innerHTML = '<tr><td colspan="2">Cargando progreso...</td></tr>';
                try {
                    const res = await fetch(`/students/${studentId}/progress`);
                    if (res.status === 404) {
                        tbody.innerHTML = '<tr><td colspan="2">No hay progreso registrado para este estudiante.</td></tr>';
                        return;
                    }
                    if (!res.ok) throw new Error('Error al cargar progreso');
                    const progress = await res.json();
                    if (!Array.isArray(progress) || progress.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="2">Sin datos de progreso.</td></tr>';
                        return;
                    }
                    tbody.innerHTML = progress.map(p => `
                        <tr>
                            <td>${p.course_id}</td>
                            <td>${p.completed_percent}%</td>
                        </tr>
                    `).join('');
                } catch (err) {
                    tbody.innerHTML = '<tr><td colspan="2">Error al obtener progreso.</td></tr>';
                    console.error(err);
                }
            }

            // Cargar cursos al abrir la página
            loadCourses();
        </script>
    </body>
    </html>
    """


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
