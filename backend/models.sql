-- Tabla de leads
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT,
    empresa TEXT,
    sector TEXT,
    fuente TEXT,
    mensaje_inicial TEXT,
    necesidades TEXT,
    etapa_funnel TEXT,   -- awareness / consideration / decision
    temperatura TEXT,    -- frio / tibio / caliente
    tipo_contacto TEXT,  -- lead / oportunidad / cliente
    estado TEXT,         -- nuevo / en_proceso / ganado / perdido
    creado_en TEXT       -- ISO timestamp
);

-- Tabla de interacciones
CREATE TABLE IF NOT EXISTS interacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER NOT NULL,
    canal TEXT,          -- email / whatsapp / linkedin
    rol TEXT,            -- agente / lead
    mensaje TEXT,
    tipo TEXT,           -- primer_contacto / seguimiento / cierre / reactivacion
    resultado TEXT,      -- sin_respuesta / respondio / rechazo / cerro_llamada
    fecha TEXT,          -- ISO timestamp
    FOREIGN KEY (lead_id) REFERENCES leads (id)
);
