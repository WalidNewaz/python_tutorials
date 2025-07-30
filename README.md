# Python for Modern Developers – Tutorial Example Project

This repository contains example code from the **Python for Modern Developers** tutorial series by Walid S Newaz.

## 🧱 Sections Covered

- CLI tools and core syntax
- FastAPI and Django apps
- Async programming and task queues
- SQL/NoSQL DB interactions
- ML/AI integration
- Cloud deployment and Docker

## 🚀 Running the FastAPI App

### Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Using Docker

```bash
docker-compose up --build
```

## 🧪 Running Tests

```bash
pytest
```

## 📦 Project Structure

- `app/` – FastAPI backend app code
- `tests/` – Unit and integration tests
- `shared_libs/` – Reusable modules (utils, DB, AI)
- `.env` – Configuration
- `docker-compose.yml` – Dev environment setup
