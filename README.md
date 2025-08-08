# AI-Powered Job Application & Resume Optimizer Agent

A Django-based web application that tailors resumes and generates personalized cover letters for any job description using **LangChain**, **OpenAI/Claude**, and **ATS keyword optimization**.  
This project demonstrates an **Agentic AI workflow** that automates resume tailoring and job application preparation, making it ideal for candidates applying to multiple roles.

---

## 🚀 Features
- **Resume Upload & Parsing:** Upload resumes in PDF/DOCX format, automatically extract text using `PyMuPDF` or `docx2txt`.
- **Job Description Analysis:** Paste job descriptions or upload them as files for parsing and skill extraction.
- **ATS Score Analysis:** Detect missing keywords, evaluate formatting, and compute an ATS score.
- **AI-Powered Resume Tailoring:** Suggests improvements to summary, skills, and work experience sections to match the job description.
- **Cover Letter Generation:** Generates a professional, tailored cover letter in seconds.
- **Downloadable Outputs:** Download optimized resume text and cover letter as `.docx` or `.txt`.
- **Asynchronous Processing:** Heavy LLM tasks handled asynchronously using **Celery + Redis**.
- **Deployment-Ready:** Containerized with **Docker** and easily deployable on Render/Railway/AWS.

---

## 🛠 Tech Stack
- **Backend:** Django, Celery, Redis
- **Frontend:** Django Templates (or React optional)
- **AI & NLP:** LangChain, OpenAI/Claude API, spaCy (for skill extraction)
- **File Parsing:** PyMuPDF, python-docx
- **Database:** PostgreSQL (default: SQLite for dev)
- **Deployment:** Docker, Render/Railway/AWS


