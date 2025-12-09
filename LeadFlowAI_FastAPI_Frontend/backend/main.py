from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from database import get_db, row_to_dict
from llm_service import segment_lead_with_llm, generate_next_message_with_llm

import sqlite3

app = FastAPI(
    title="Lead Flow AI – Segmentación + Nutrición con Copy",
    description="API en FastAPI con SQLite y LLM (simulada) para segmentar leads y generar mensajes de nutrición.",
    version="1.0.0",
)

# CORS sencillo para permitir acceso desde el front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======== Pydantic Schemas ========

class LeadBase(BaseModel):
    nombre: str
    email: Optional[EmailStr] = None
    empresa: Optional[str] = None
    sector: Optional[str] = None
    fuente: Optional[str] = None
    mensaje_inicial: Optional[str] = None
    necesidades: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(LeadBase):
    etapa_funnel: Optional[str] = None
    temperatura: Optional[str] = None
    tipo_contacto: Optional[str] = None
    estado: Optional[str] = None


class LeadOut(LeadBase):
    id: int
    etapa_funnel: Optional[str] = None
    temperatura: Optional[str] = None
    tipo_contacto: Optional[str] = None
    estado: Optional[str] = None
    creado_en: str

    class Config:
        from_attributes = True


class InteraccionBase(BaseModel):
    canal: str           # email / whatsapp / linkedin
    rol: str             # agente / lead
    mensaje: str
    tipo: Optional[str] = None      # primer_contacto / seguimiento / cierre / reactivacion
    resultado: Optional[str] = None # sin_respuesta / respondio / rechazo / cerro_llamada


class InteraccionCreate(InteraccionBase):
    pass


class InteraccionOut(InteraccionBase):
    id: int
    lead_id: int
    fecha: str


class SegmentacionOut(BaseModel):
    etapa_funnel: str
    temperatura: str
    tipo_contacto: str
    siguiente_paso: str
    justificacion: str


class NextMessageRequest(BaseModel):
    canal: str                     # email / whatsapp / linkedin
    objetivo: str                  # conseguir_llamada / reactivar / seguimiento
    tono: Optional[str] = "cercano_profesional"


class NextMessageResponse(BaseModel):
    asunto: Optional[str]
    cuerpo: str
    canal: str
    generado_en: str
    etapa_funnel: Optional[str]
    temperatura: Optional[str]


# ======== Endpoints CRUD Leads ========

@app.get("/leads", response_model=List[LeadOut])
def list_leads(db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("SELECT * FROM leads ORDER BY creado_en DESC")
    rows = cur.fetchall()
    return [row_to_dict(r) for r in rows]


@app.post("/leads", response_model=LeadOut, status_code=201)
def create_lead(lead: LeadCreate, db: sqlite3.Connection = Depends(get_db)):
    ahora = datetime.now().isoformat(timespec="seconds")
    cur = db.execute(
        """
        INSERT INTO leads (
            nombre, email, empresa, sector, fuente,
            mensaje_inicial, necesidades,
            etapa_funnel, temperatura, tipo_contacto, estado, creado_en
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            lead.nombre,
            lead.email,
            lead.empresa,
            lead.sector,
            lead.fuente,
            lead.mensaje_inicial,
            lead.necesidades,
            None,
            None,
            "lead",
            "nuevo",
            ahora,
        ),
    )
    db.commit()
    new_id = cur.lastrowid
    cur = db.execute("SELECT * FROM leads WHERE id = ?", (new_id,))
    row = cur.fetchone()
    return row_to_dict(row)


@app.get("/leads/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: int, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    return row_to_dict(row)


@app.put("/leads/{lead_id}", response_model=LeadOut)
def update_lead(lead_id: int, lead: LeadUpdate, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    if cur.fetchone() is None:
        raise HTTPException(status_code=404, detail="Lead no encontrado")

    data = lead.dict(exclude_unset=True)
    if not data:
        cur = db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
        row = cur.fetchone()
        return row_to_dict(row)

    set_clause = ", ".join(f"{k} = ?" for k in data.keys())
    values = list(data.values())
    values.append(lead_id)

    db.execute(f"UPDATE leads SET {set_clause} WHERE id = ?", values)
    db.commit()

    cur = db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = cur.fetchone()
    return row_to_dict(row)


@app.delete("/leads/{lead_id}", status_code=204)
def delete_lead(lead_id: int, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    if cur.fetchone() is None:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    db.execute("DELETE FROM interacciones WHERE lead_id = ?", (lead_id,))
    db.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    db.commit()
    return


# ======== Endpoints Interacciones ========

@app.get("/leads/{lead_id}/interacciones", response_model=List[InteraccionOut])
def list_interacciones(lead_id: int, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("SELECT * FROM interacciones WHERE lead_id = ? ORDER BY fecha ASC", (lead_id,))
    rows = cur.fetchall()
    return [row_to_dict(r) for r in rows]


@app.post("/leads/{lead_id}/interacciones", response_model=InteraccionOut, status_code=201)
def create_interaccion(lead_id: int, inter: InteraccionCreate, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    if cur.fetchone() is None:
        raise HTTPException(status_code=404, detail="Lead no encontrado")

    ahora = datetime.now().isoformat(timespec="seconds")
    cur = db.execute(
        """
        INSERT INTO interacciones (
            lead_id, canal, rol, mensaje, tipo, resultado, fecha
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            lead_id,
            inter.canal,
            inter.rol,
            inter.mensaje,
            inter.tipo,
            inter.resultado,
            ahora,
        ),
    )
    db.commit()
    new_id = cur.lastrowid
    cur = db.execute("SELECT * FROM interacciones WHERE id = ?", (new_id,))
    row = cur.fetchone()
    return row_to_dict(row)


# ======== Endpoints IA: segmentación + siguiente mensaje ========

@app.post("/leads/{lead_id}/segmentar", response_model=SegmentacionOut)
def segmentar_lead(lead_id: int, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Lead no encontrado")

    lead_dict = row_to_dict(row)
    resultado = segment_lead_with_llm(lead_dict)

    # Guardar en la BD
    db.execute(
        """
        UPDATE leads
        SET etapa_funnel = ?, temperatura = ?, tipo_contacto = ?
        WHERE id = ?
        """,
        (
            resultado["etapa_funnel"],
            resultado["temperatura"],
            resultado["tipo_contacto"],
            lead_id,
        ),
    )
    db.commit()

    return resultado


@app.post("/leads/{lead_id}/siguiente-mensaje", response_model=NextMessageResponse)
def siguiente_mensaje(
    lead_id: int,
    req: NextMessageRequest,
    db: sqlite3.Connection = Depends(get_db),
):
    # Obtener lead
    cur = db.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    lead_dict = row_to_dict(row)

    # Últimas interacciones (por ahora no las usamos mucho, pero podrían usarse en la LLM)
    cur = db.execute(
        "SELECT * FROM interacciones WHERE lead_id = ? ORDER BY fecha DESC LIMIT 5",
        (lead_id,),
    )
    interacciones = [row_to_dict(r) for r in cur.fetchall()]

    mensaje = generate_next_message_with_llm(
        lead=lead_dict,
        last_interactions=interacciones,
        canal=req.canal,
        objetivo=req.objetivo,
        tono=req.tono,
    )

    return mensaje
