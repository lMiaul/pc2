# tests/test_api.py
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_check():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "EduPro API"


def test_list_courses():
    resp = client.get("/courses")
    assert resp.status_code == 200
    data = resp.json()
    # tenemos al menos un curso
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "title" in data[0]


def test_student_progress_found():
    resp = client.get("/students/1/progress")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # en el mock, student_id = 1 tiene al menos un curso
    assert len(data) >= 1
    assert data[0]["student_id"] == 1


def test_student_progress_not_found():
    resp = client.get("/students/999/progress")
    assert resp.status_code == 404

def test_home_page_loads():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    assert "EduPro – MVP" in html
    assert "Catálogo de cursos" in html
    assert "Progreso por estudiante" in html

def test_home_page_has_courses_table():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    # La tabla de cursos debería existir
    assert 'id="courses-table"' in html
    assert 'id="courses-body"' in html
    # Texto que indica que viene del endpoint /courses
    assert "GET /courses" in html


def test_home_page_has_progress_controls():
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    # Campo para ingresar el ID de estudiante
    assert 'id="student-id"' in html
    # Botón para consultar progreso
    assert "Ver progreso" in html
    # Texto que indica que usa /students/<id>/progress
    assert "GET /students&lt;id&gt;/progress" in html
