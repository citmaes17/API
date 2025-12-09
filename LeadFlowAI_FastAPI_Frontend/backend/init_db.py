import sqlite3
from datetime import datetime

DB_PATH = "leadflow.db"


def create_tables(conn):
    with open("models.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.commit()


def seed_data(conn):
    ahora = datetime.now().isoformat(timespec="seconds")

    leads = [
        # 1) E-commerce redes – caliente / decision
        (
            "Laura Gómez",
            "laura@example.com",
            "Tienda Verde Online",
            "ecommerce",
            "Instagram Ads",
            "Me urge ordenar todos los mensajes que llegan por Instagram este mes, ya no doy abasto.",
            "Quiero dejar de perder conversaciones en el DM y tener claro quién está listo para comprar.",
            None,
            None,
            "lead",
            "nuevo",
            ahora,
        ),
        # 2) Academia / webinars – consideration (tibio)
        (
            "Carlos Pérez",
            "carlos@example.com",
            "Academia Digital XYZ",
            "educacion",
            "LinkedIn",
            "Busco una forma de hacer seguimiento a las personas que llegan por webinars.",
            "Me interesa entender mejor quién está listo para pasar a un curso premium.",
            None,
            None,
            "lead",
            "nuevo",
            ahora,
        ),
        # 3) Cafetería – awareness con duda “tiene sentido”
        (
            "Ana Martínez",
            "ana@example.com",
            "Cafetería Hola Café",
            "hosteleria",
            "Formulario web",
            "Dejé mis datos porque quiero entender si tiene sentido invertir en campañas.",
            "Quiero que la gente no venga solo una vez, sino que vuelva más a menudo.",
            None,
            None,
            "lead",
            "nuevo",
            ahora,
        ),
        # 4) Agencia B2B – frío / awareness, problema de tiempo
        (
            "Javier López",
            "javier@example.com",
            "Agencia B2B Norte",
            "servicios b2b",
            "Recomendación",
            "Ahora mismo llevo todo en Excels y notas sueltas.",
            "Pierdo mucho tiempo copiando datos a mano y siento que se me escapan oportunidades.",
            None,
            None,
            "lead",
            "nuevo",
            ahora,
        ),
        # 5) Cliente actual – renovación (cliente)
        (
            "Marta Ruiz",
            "marta@example.com",
            "Consultora M&R",
            "consultoria",
            "Cliente actual",
            "Ya soy cliente actual y estamos revisando cómo renovar el servicio.",
            "Quiero ver si tiene sentido ampliar lo que ya tenemos para mi equipo comercial.",
            None,
            None,
            "cliente",
            "activo",
            ahora,
        ),
        # 6) Oportunidad con propuesta enviada
        (
            "Diego Sánchez",
            "diego@example.com",
            "Eventos DS",
            "eventos",
            "Email directo",
            "Estoy esperando la cotización final que me comentaste.",
            "Necesito decidir esta semana qué proveedor elijo.",
            None,
            None,
            "oportunidad",
            "en_propuesta",
            ahora,
        ),
    ]

    conn.executemany(
        """
        INSERT INTO leads (
            nombre, email, empresa, sector, fuente,
            mensaje_inicial, necesidades,
            etapa_funnel, temperatura, tipo_contacto, estado, creado_en
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        leads,
    )

    conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    seed_data(conn)
    conn.close()
    print("✅ Base de datos creada y poblada: leadflow.db")
