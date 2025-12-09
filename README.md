
# Lead Flow AI – Segmentación y Nutrición de Leads con IA 🚀

**Lead Flow AI** es una aplicación académica desarrollada para gestionar leads comerciales, 
segmentarlos automáticamente con soporte de **IA simulada**, y generar mensajes 
de seguimiento según el **canal y el objetivo** de negocio.

> Objetivo principal: facilitar y automatizar la clasificación del lead dentro del funnel y 
> la creación del copy para su nutrición comercial.

---

## 🧱 Arquitectura del Proyecto

```
LeadFlowAI_FastAPI_Frontend/
│
├── backend/         → API con FastAPI + SQLite
│   ├── main.py
│   ├── database.py
│   ├── llm_service.py
│   ├── init_db.py
│   ├── models.sql
│   ├── requirements.txt
│
└── frontend/        → Panel visual HTML + CSS + JS
    ├── index.html
    ├── styles.css
    └── app.js
```

🔌 Comunicación mediante llamadas `fetch()` al backend  
📡 API local: `http://127.0.0.1:8000`  
🖥 Panel: `http://127.0.0.1:5500/index.html`  

---

## 🔍 Funcionalidades

### 🔹 Backend – FastAPI + SQLite

| Feature | Descripción |
|--------|-------------|
| CRUD de leads | Crear, listar, editar y borrar leads |
| Segmentación con IA | Clasifica temperatura y etapa del funnel |
| Generación de mensajes con IA | Mensajes por canal (email / WhatsApp) |
| Registro de interacciones | Historial por cada lead |
| Documentación automática | Disponible en `/docs` con Swagger UI |

> La lógica de IA está simulada con reglas, pero la estructura está lista para conectar una LLM real.

---

### 🎨 Frontend – HTML + CSS + JS

- Panel dividido en 3 módulos:
  1. **Crear nuevo lead**
  2. **Listado de leads con chips de funnel y temperatura**
  3. **Panel de resultado IA**
- UI en **modo oscuro**, moderna y limpia.
- Formularios con validación básica.
- Render dinámico de leads y de los mensajes generados por IA.

---

## ⚙️ Instalación y Ejecución

### 1️⃣ Backend

```bash
cd backend
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload
```

- API activa: `http://127.0.0.1:8000`  
- Docs: `http://127.0.0.1:8000/docs`  

### 2️⃣ Frontend

```bash
cd frontend
python -m http.server 5500
```

Abrir en el navegador:  
`http://127.0.0.1:5500/index.html`

> ⚠️ Asegúrate de que el backend esté ejecutándose en el puerto 8000 antes de abrir el frontend.

---

## 🗄 Modelo de Datos

### Tabla `leads`

Campos clave:

- Datos del contacto: `nombre`, `email`, `empresa`, `sector`, `fuente`
- Información comercial:
  - `mensaje_inicial`
  - `necesidades`
  - `etapa_funnel` → `awareness`, `consideration`, `decision`
  - `temperatura` → `frio`, `tibio`, `caliente`
  - `tipo_contacto` → `lead`, `oportunidad`, `cliente`
  - `estado` → `nuevo`, `en_proceso`, `ganado`, `perdido`
- Metadatos: `creado_en`

### Tabla `interacciones`

- `lead_id` (relación con `leads`)
- `canal` (`email`, `whatsapp`, `linkedin`)
- `rol` (`agente`, `lead`)
- `mensaje`
- `tipo` (`primer_contacto`, `seguimiento`, `cierre`, `reactivacion`)
- `resultado` (`sin_respuesta`, `respondio`, `rechazo`, `cerro_llamada`)
- `fecha`

---

## 📦 Tecnologías Utilizadas

| Capa | Tecnología |
|------|------------|
| Backend | Python, FastAPI, SQLite, Uvicorn |
| Frontend | HTML5, CSS3, JavaScript Vanilla |
| Documentación | Swagger / OpenAPI |

---

## 🚀 Roadmap (Mejoras Futuras)

- Conexión a modelo LLM real (OpenAI / local).
- Autenticación y roles de usuario.
- Dashboard con métricas de conversión.
- Filtros y búsqueda avanzada de leads.
- Guardar automáticamente los mensajes generados como interacciones.

---

## 👩‍💻 Autora del Proyecto

**Cindy Tatiana Marín Espinosa**  
Bootcamp Ciencia de Datos — The Bridge, Valencia 🇪🇸  

Desarrollo de soluciones Data + IA aplicada a marketing, segmentación de clientes y optimización de procesos comerciales.

---

## 📜 Licencia

Uso académico y libre con atribución.

---

⭐ Si este proyecto te ha sido útil, puedes dejar una estrella en mi GitHub 😄
