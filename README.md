# Smart LectorPDF

LectorPDF is a Full-Stack interactive web application designed to transform hefty study books and PDFs into interactive audiobooks, with zero visual friction. Unlike traditional screen readers that annoyingly read page numbers or repetitive headers, our LectorPDF surgically cleans and reconstructs the real paragraphs, providing a fluid modern visualization with Karaoke-style synchronization.

## Core Features

* **Tactile Text Reconstruction:** Algorithmically detects and cuts out statistically repetitive headers and footers, fixing syllables broken by line breaks.
* **Smart Reading (Karaoke-Sync):** Don't lose your place while listening. The real-time interface illuminates the exact phrase the robotic voice of your computer is currently reading in glowing yellow.
* **Native Built-in Security:** Encrypted uploads protected against Path Traversal, MIME Type Spoofing, and Payload attacks (hard limit to 50MB per PDF).
* **Premium Glassmorphism Interface:** Dark mode visual environment, reactive, relaxing, and intuitive to turn pages in fractions of a second.

## Tech Stack

* **Frontend:** React + Vite + Vanilla Javascript
* **Backend:** Python + FastAPI + pdfplumber
* **Testing Suite (QA):** Vitest + React Testing Library (Front) and Pytest + httpx (Back)

---

## Installation & Usage Guide

### A. Express Execution via Docker (Recommended)
To run the project directly without configuring any libraries or installing Node/Python, you must run our central orchestrator (requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) to be installed):
```bash
git clone https://github.com/your-username/LectorPDF.git
cd LectorPDF
docker-compose up --build
```
That's it! Enter visually at `http://localhost:5173`. Your Python APIs will boot under an isolated container and your Frontend will be packaged and served natively via `Nginx`.

### B. Development Mode (Manual Installation)

If you wish to modify code and develop the platform, you will need to install both engines separately.

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/LectorPDF.git
cd LectorPDF
```

#### 2. Boot the Backend Engine (Python)
Open a terminal and navigate to the `/backend` folder:
```bash
cd backend
python -m venv venv
# Activate environment (Windows):
.\venv\Scripts\activate

pip install .
python -m uvicorn app.main:app --reload
```
*The API will listen silently and securely on `http://localhost:8000`.*

### 3. Boot the Frontend Interface (React)
Open another terminal and navigate to the `/frontend` folder:
```bash
cd frontend
npm install
npm run dev
```
*The interactive environment will be deployed at `http://localhost:5173`. Open this link in your browser, upload a PDF, and enjoy.*

## Testing and Development (Local CI/CD)
All tools to test the system come built-in:
* **Backend Security Tests:** Inside `/backend` run `python -m pytest tests/`
* **Frontend DOM Tests:** Inside `/frontend` run `npm run test`

---
*Developed with passion to make intensive reading accessible to everyone.*
