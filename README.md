# LectorPDF Inteligente 🎧📄

LectorPDF es una aplicación web interactiva Full-Stack diseñada para transformar verdaderos mamotretos de estudio y libros en PDF en audiolibros interactivos, con cero fricción visual. A diferencia de lectores de pantalla tradicionales que leen números de página molestos o cabeceras repetitivas, nuestro LectorPDF limpia y reconstruye quirúrgicamente los párrafos reales brindando una visualización moderna fluida con sincronización estilo Karaoke.

## ✨ Características Principales

* 🧠 **Reconstrucción Táctil de Texto:** Detecta y corta algorítmicamente encabezados estadísticamente repetitivos y *footers*, arreglando sílabas separadas por el salto de línea.
* 🗣️ **Lectura Inteligente (Karaoke-Sync):** No te pierdas mientras escuchas. La interfaz en tiempo real ilumina en amarillo incandescente la frase exacta en la que se encuentra la voz robótica de tu computadora.
* 🛡️ **Seguridad Nativa Integrada:** Subidas cifradas protegidas contra Path Traversal, Falsificación de MIME Types y ataques de Carga (límite duro a 50MB por PDF).
* 🕹️ **Interfaz Premium Glassmorphism:** Entorno visual *dark mode*, reactivo, relajante e intuitivo para pasar páginas en fracciones de segundo.

## 🛠️ Stack Tecnológico

* **Frontend:** React + Vite + Javascript Nativo
* **Backend:** Python + FastAPI + pdfplumber
* **Suite de Testing (QA):** Vitest + React Testing Library (Front) y Pytest + httpx (Back)

---

## 🚀 Guía de Instalación y Uso

### A. Ejecución Express con Docker (Recomendado)
Para arrancar el proyecto directamente sin configurar ninguna librería ni instalar Node o Python, debes correr nuestro orquestador central (requiere que tengas instalada la aplicación [Docker Desktop](https://www.docker.com/products/docker-desktop/)):
```bash
git clone https://github.com/tu-usuario/LectorPDF.git
cd LectorPDF
docker-compose up --build
```
¡Ya está! Entra visualmente en `http://localhost:5173`. Tus APIs en Python arrancarán bajo un contenedor sellado y tu Frontend se empacará y servirá nativamente vía `Nginx`.

### B. Modo Desarrollo (Instalación Manual)

Si deseas modificar código y desarrollar la plataforma, necesitarás instalar ambos motores por separado.

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/LectorPDF.git
cd LectorPDF
```

#### 2. Levantar el Motor Backend (Python)
Abre un terminal y sitúate en la carpeta `/backend`:
```bash
cd backend
python -m venv venv
# Activar entorno (Windows):
.\venv\Scripts\activate

pip install .
python -m uvicorn app.main:app --reload
```
*La API quedará escuchando silenciosa y segura en `http://localhost:8000`.*

### 3. Levantar la Interfaz Frontend (React)
Abre otro terminar y sitúate en la carpeta `/frontend`:
```bash
cd frontend
npm install
npm run dev
```
*Se desplegará el entorno interactivo en `http://localhost:5173`. Abre este último enlace en tu navegador, sube un PDF y disfruta.*



## 🧪 Pruebas y Desarrollo (CI/CD Local)
Todas las herramientas para probar el sistema vienen integradas:
* **Pruebas de Seguridad Backend:** Estando en `/backend` corre `python -m pytest tests/`
* **Pruebas de DOM Frontend:** Estando en `/frontend` corre `npm run test`

---
*Desarrollado con pasión para hacer la lectura intensiva accesible a todos.*
