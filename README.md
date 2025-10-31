# Python Foundations Series

This repository contains the **companion code and solutions** for the tutorial series [Python Foundations Series](https://www.walidnewaz.com/learn/python/).

The series is designed to take readers from the fundamentals of Python programming all the way to building **production-ready applications**. This course will lay the groundwork for future courses focused on web applications, data analytics, machine learning, and artificial intelligence topics.

---

## 📂 Repository Structure

This repo is organized like a **mono-repo**.  
Each **section** in the series is represented as a top-level directory, and each **chapter** lives inside its section.

```
/
├── chapter_01_env_setup/
├── chapter_02_syntax_core/
├── chapter_03_files_io/
└── ...
````

---

## 📖 Tutorial Syllabus

The full syllabus is tracked in [`SYLLABUS.md`](SYLLABUS.md).  
Highlights include:

- Core Python Language
- Error Handling, Debugging and Testing
- Object-Oriented and Functional Python
- Python’s Built-in Tools
- Concurrency and Patterns
- Packaging, CLI, and Distribution

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
cd chapter_02_syntax_core
python calculator.py
```



