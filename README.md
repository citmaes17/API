# Lead Flow AI – Segmentación y Nutrición de Leads con IA 🚀

**Lead Flow AI** es una aplicación académica desarrollada para gestionar leads comerciales,
segmentarlos automáticamente con soporte de **IA simulada**, y generar mensajes
de seguimiento según el **canal y el objetivo** de negocio.

> Objetivo principal: facilitar y automatizar la clasificación del lead dentro del funnel y la generación del copy comercial.

---

## 🧱 Arquitectura del Proyecto

\`\`\`
LeadFlowAI_FastAPI_Frontend/
│
├── backend/        → API con FastAPI + SQLite
│   ├── main.py
│   ├── database.py
│   ├── llm_service.py
│   ├── init_db.py
│   ├── models.sql
│   ├── requirements.txt
│
└── frontend/       → Panel visual HTML + CSS + JS
    ├── index.html
    ├── styles.css
    └── app.js
\`\`\`

📡 API local → `http://127.0.0.1:8000`  
🖥 Panel UI → `http://127.0.0.1:5500/index.html`  

---

## 🔍 Funcionalidades del Proyecto

### Backend
- Gestión completa de leads (CRUD)
- Registro de interacciones
- Segmentación automática mediante IA simulada
- Generación de mensajes para contacto directo
- Documentación interactiva en `/docs` (Swagger UI)

### Frontend
- Creación de leads
- Chips visuales de funnel y temperatura
- Botones para segmentación y mensajes IA
- Panel de visualización del resultado IA

---

## 🌐 Endpoints de la API

📌 Documentación: http://127.0.0.1:8000/docs

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /leads | Listar leads |
| POST | /leads | Crear lead |
| GET | /leads/{id} | Ver lead |
| PUT | /leads/{id} | Actualizar lead |
| DELETE | /leads/{id} | Eliminar lead |

### Interacciones

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /leads/{id}/interacciones | Ver historial |
| POST | /leads/{id}/interacciones | Registrar |

### IA

| Método | Ruta | Acción |
|--------|------|--------|
| POST | /leads/{id}/segmentar | Determina funnel + temperatura |
| POST | /leads/{id}/siguiente-mensaje | Genera copy comercial |

Ejemplo JSON:
\`\`\`json
{
  "canal": "email",
  "objetivo": "conseguir_llamada",
  "tono": "cercano_profesional"
}
\`\`\`

---

## ⚙️ Instalación y Ejecución

### Backend

\`\`\`bash
cd backend
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload
\`\`\`

📌 http://127.0.0.1:8000  
📌 http://127.0.0.1:8000/docs  

### Frontend

\`\`\`bash
cd frontend
python -m http.server 5500
\`\`\`

📌 http://127.0.0.1:5500/index.html

---

## 🗄 Modelo de Datos

### Tabla leads
- Información básica y comercial del contacto

### Tabla interacciones
- Registro de conversaciones y acciones

---

## 🚀 Roadmap

- Conectar a una LLM real como OpenAI
- Dashboard de métricas comerciales
- Filtros y búsqueda avanzada
- Roles y autenticación

---

## 📦 Tecnologías Utilizadas

| Capa | Herramientas |
|------|--------------|
| Backend | FastAPI + SQLite |
| Frontend | HTML5 + CSS3 + JavaScript |
| API Docs | Swagger / OpenAPI |

---

## 👩‍💻 Autora

**Cindy Tatiana Marín Espinosa**  
Bootcamp Ciencia de Datos — **The Bridge**, Valencia 🇪🇸  

> IA aplicada a marketing, ventas y automatización comercial.

---

⭐ Si este proyecto te fue útil, ¡déjame una estrella en GitHub! ⭐
