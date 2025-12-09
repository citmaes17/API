
# Lead Flow AI – Segmentación + Nutrición con Copy

Pequeño proyecto académico que muestra cómo usar **FastAPI + SQLite** para gestionar leads de marketing, simular una **LLM** que segmenta contactos y generar mensajes de seguimiento, junto con un **frontend simple en HTML/CSS/JS** para trabajar todo desde un panel único.

> Objetivo: tener una vista clara de en qué etapa del funnel está cada lead, qué temperatura tiene y qué mensaje enviarle según el canal.

---

## 🧱 Arquitectura del proyecto

```
LeadFlowAI_FastAPI_Frontend/
│
├── backend/
│   ├── database.py
│   ├── init_db.py
│   ├── llm_service.py
│   ├── main.py
│   ├── models.sql
│   ├── requirements.txt
│
└── frontend/
    ├── index.html
    ├── styles.css
    └── app.js
```

---

## 🚀 Funcionalidades

### Backend (FastAPI + SQLite)
- CRUD de leads
- Segmentación automática
- Generación de mensajes según canal
- SQLite como base local
- Documentación de API en `/docs`

### Frontend
- Formulario para crear leads
- Listado con chips de **funnel** y **temperatura**
- Botones de Segmentar y Mensajes IA
- Panel dedicado al resultado de IA

---

## 🛠 Tecnologías usadas

| Capa | Tecnología |
|------|------------|
| Backend | Python, FastAPI, SQLite, Uvicorn |
| Frontend | HTML, CSS, JavaScript Vanilla |

---

## ⚙️ Cómo ejecutar el proyecto

### 1️⃣ Backend

```bash
cd backend
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload
```

📌 Endpoints principales:  
http://127.0.0.1:8000  
📌 Documentación interactiva:  
http://127.0.0.1:8000/docs  

### 2️⃣ Frontend

```bash
cd frontend
python -m http.server 5500
```

Abrir en navegador:
http://127.0.0.1:5500/index.html

> Asegúrate de que el backend esté corriendo en el puerto 8000.

---

## 🗄 Modelo de datos

Tablas clave:
- `leads`: contactos a gestionar
- `interacciones`: mensajes relacionados a cada lead

---

## 🔮 Mejoras futuras
- Integrar una LLM real (OpenAI u otra)
- Autenticación y seguridad
- Dashboard con métricas
- Filtros y búsqueda en el listado

---

## 🧑‍💻 Autor del proyecto

Proyecto académico de práctica FastAPI + Frontend.
