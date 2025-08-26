# Python for Modern Developers

This repository contains the **companion code and solutions** for the tutorial series **Python for Modern Developers: From Basics to AI-Driven Applications**.

The series is designed to take readers from the fundamentals of Python programming all the way to building **production-ready applications**, including **web apps, scalable systems, and AI/ML integrations**.

---

## 📂 Repository Structure

This repo is organized like a **mono-repo**.  
Each **section** in the series is represented as a top-level directory, and each **chapter** lives inside its section.

```
/
├── section_01_foundations/
│   ├── chapter_01_env_setup/
│   ├── chapter_02_syntax_core/
│   ├── chapter_03_files_io/
│   └── ...
├── section_02_web_apps/
│   ├── chapter_15_fastapi_intro/
│   ├── chapter_16_django_basics/
│   └── ...
├── section_03_databases/
│   └── ...
...
````

Within each **chapter directory**, you will find:

- `code/` → runnable code examples from the book
- `resources/` → datasets, sample files, or other supporting material
- `assignments/` → starter files and solutions for chapter assignments
- `README.md` → notes and usage instructions

---

## 📖 Tutorial Syllabus

The full syllabus is tracked in [`SYLLABUS.md`](SYLLABUS.md).  
Highlights include:

- **Foundations**: syntax, files, OOP, DSA, concurrency, design patterns
- **Web Development**: FastAPI, Django, API security
- **Databases**: SQL, NoSQL, ORMs
- **Async & Background Work**: asyncio, Celery
- **Scalability**: configuration, testing, packaging, deployment
- **Data & AI**: Pandas, NumPy, scikit-learn, LangChain
- **Production Readiness**: monitoring, event-driven, serverless

---

## 🚀 Getting Started

Clone the repo:

```bash
git clone https://github.com/WalidNewaz/python_tutorials.git
cd python_tutorials
````

Set up a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate   # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

Navigate into a section and run the examples:

```bash
cd section_01_foundations/chapter_02_syntax_core/code
python calculator.py
```



