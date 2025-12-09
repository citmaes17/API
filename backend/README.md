# Lead Flow AI – Segmentación + Nutrición con Copy

Proyecto de FastAPI + SQLite + lógica tipo IA para segmentar leads de marketing y generar mensajes de nutrición personalizados.

## Objetivo

- Clasificar leads según su etapa en el funnel (awareness / consideration / decision)
  y su temperatura (frio / tibio / caliente).
- Generar el siguiente mensaje de contacto (copy) adaptado al canal y al objetivo.
- Mostrar un front-end sencillo para gestionar leads y disparar segmentación + generación de mensajes.

## Tecnologías

- FastAPI
- SQLite
- Pydantic
- (Opcional) OpenAI LLM
- Front-end: HTML + CSS + JavaScript (fetch API)

## Cómo ejecutar

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload
```

La API quedará disponible en:

- http://127.0.0.1:8000
- Documentación automática: http://127.0.0.1:8000/docs

### 2. Frontend

En otra terminal:

```bash
cd frontend
# Opción simple: abrir index.html directamente en el navegador (doble click)
# Si tu navegador bloquea peticiones por CORS desde file://, levanta un server simple:
python -m http.server 5500
```

Luego abre:

- http://127.0.0.1:5500/index.html

Asegúrate de que el backend siga corriendo en http://127.0.0.1:8000.

## Endpoints principales

- `GET /leads`
- `POST /leads`
- `GET /leads/{id}`
- `PUT /leads/{id}`
- `GET /leads/{id}/interacciones`
- `POST /leads/{id}/interacciones`
- `POST /leads/{id}/segmentar`
- `POST /leads/{id}/siguiente-mensaje`

## Trabajo futuro

- Sustituir la lógica de segmentación simple por una LLM real (OpenAI).
- Añadir autenticación básica (API key).
- Crear un frontend más avanzado (React, diseño profesional).
- Métricas: tasas de respuesta por segmento/temperatura.
