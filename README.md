# EduPro MVP (pc2)

MVP de plataforma de educación en línea usando Python (FastAPI), GitHub, GitHub Actions y Vercel.

## Endpoints principales

- `GET /health` – Verifica el estado de la API.
- `GET /courses` – Lista de cursos disponibles (datos simulados).
- `GET /students/{student_id}/progress` – Progreso del estudiante en los cursos (datos simulados).

## Desarrollo local

```bash
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload
