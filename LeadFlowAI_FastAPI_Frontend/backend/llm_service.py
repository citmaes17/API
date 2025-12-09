from typing import Dict
from datetime import datetime


# ========= SEGMENTACIÓN "TIPO LLM" =========

def segment_lead_with_llm(lead: Dict) -> Dict:
    """
    Simula segmentación con LLM.
    Usa mensaje_inicial + necesidades + sector + fuente
    para inferir etapa, temperatura y tipo de contacto.
    """
    texto = (
        (lead.get("mensaje_inicial") or "")
        + " "
        + (lead.get("necesidades") or "")
        + " "
        + (lead.get("sector") or "")
        + " "
        + (lead.get("fuente") or "")
    ).lower()

    # ---- Temperatura / etapa según el tipo de frase ----

    # 1) Urgencia clara -> caliente / decision
    if any(p in texto for p in ["me urge", "urgente", "ya mismo", "lo antes posible", "este mes"]):
        temperatura = "caliente"
        etapa = "decision"
        siguiente_paso = "Proponer una llamada de cierre con una propuesta concreta y próximos pasos."

    # 2) Duda tipo “no sé si tiene sentido / quiero entender si tiene sentido”
    elif any(p in texto for p in ["tiene sentido", "si tiene sentido", "no sé si tiene sentido", "no se si tiene sentido"]):
        temperatura = "tibio"
        etapa = "awareness"
        siguiente_paso = "Ayudarle primero a entender el problema y si realmente tiene sentido hacer la inversión."

    # 3) Interés activo / está buscando opciones
    elif any(p in texto for p in ["me interesa", "quiero entender", "quiero saber", "estoy buscando", "evaluando opciones"]):
        temperatura = "tibio"
        etapa = "consideration"
        siguiente_paso = "Proponer una llamada corta para entender mejor el caso y adaptar la solución al negocio."

    # 4) Genérico / poco contexto
    else:
        temperatura = "frio"
        etapa = "awareness"
        siguiente_paso = "Enviar contenido educativo sencillo para que vea el valor antes de tomar una decisión."

    # Tipo de contacto (lead / oportunidad / cliente)
    if any(p in texto for p in ["cliente actual", "ya trabajo con", "renovar", "renovación", "renovacion"]):
        tipo_contacto = "cliente"
    elif any(p in texto for p in ["propuesta", "cotización", "cotizacion", "presupuesto"]):
        tipo_contacto = "oportunidad"
    else:
        tipo_contacto = "lead"

    return {
        "etapa_funnel": etapa,
        "temperatura": temperatura,
        "tipo_contacto": tipo_contacto,
        "siguiente_paso": siguiente_paso,
        "justificacion": (
            "Clasificación basada en expresiones de urgencia, duda e interés dentro del texto recibido. "
            "En un entorno real se podría sustituir por un modelo LLM entrenado."
        ),
    }


# ========= HELPERS PARA PERSONALIZAR MENSAJES =========

def _detectar_dolor(texto: str) -> str:
    """
    Detecta el dolor principal que menciona la persona
    (caos, tiempo, conversión, recurrencia, equipo, tech, etc.)
    y devuelve una frase ya lista para usar en el mensaje.
    """
    t = texto.lower()

    # Caos / desorden
    if any(p in t for p in ["desorden", "caos", "muchos mensajes", "se me pierden", "no doy abasto", "no alcanzo", "saturado"]):
        return (
            "bajar el caos de mensajes y tener claro en un solo sitio quién te escribió, "
            "qué pidió y en qué punto de la conversación se quedó."
        )

    # Tiempo
    if any(p in t for p in ["tiempo", "horas", "manual", "manualmente", "automatizar", "automatice", "automatización", "automatizacion"]):
        return (
            "dejar de hacerlo todo de forma manual y recuperar horas de trabajo, "
            "sin perder seguimiento de las oportunidades importantes."
        )

    # Conversión / ventas
    if any(p in t for p in ["no convierten", "no compran", "pocas ventas", "ventas", "cerrar", "cierres", "cierre", "tasa de conversión", "conversion"]):
        return (
            "entender qué contactos tienen más probabilidad de convertirse en venta "
            "y priorizarlos en lugar de tratar todo por igual."
        )

    # Recurrencia / fidelización
    if any(p in t for p in ["recurrente", "recurrentes", "que vuelvan", "fidelizar", "fidelidad", "retener", "retencion", "retención"]):
        return (
            "identificar quién ya te ha comprado y crear acciones específicas para que vuelvan, "
            "en lugar de vivir solo de clientes nuevos."
        )

    # Equipo / coordinación comercial
    if any(p in t for p in ["equipo", "vendedores", "agentes", "comercial", "equipo de ventas", "comerciales"]):
        return (
            "que todo el equipo comercial vea la misma información y no se dupliquen mensajes, "
            "evitando que dos personas contacten al mismo cliente sin saberlo."
        )

    # Tecnología / herramientas dispersas
    if any(p in t for p in ["excel", "hoja de cálculo", "hoja de calculo", "google sheets", "herramientas distintas", "múltiples sistemas", "varias herramientas"]):
        return (
            "pasar de tener la información repartida en mil sitios (Excel, chats, notas) "
            "a un flujo simple donde puedas seguir cada oportunidad."
        )

    # Genérico si no detecta nada claro
    return (
        "tener un flujo de seguimiento claro, sin depender solo de la memoria y sin perder oportunidades importantes por el camino."
    )


def _detectar_contexto_negocio(lead: Dict) -> str:
    """
    Devuelve una descripción del tipo de negocio / contexto
    para que el mensaje no hable solo de 'leads'.
    """
    empresa = (lead.get("empresa") or "").lower()
    sector = (lead.get("sector") or "").lower()
    fuente = (lead.get("fuente") or "").lower()
    texto = (
        (lead.get("mensaje_inicial") or "")
        + " "
        + (lead.get("necesidades") or "")
        + " "
        + empresa
        + " "
        + sector
        + " "
        + fuente
    ).lower()

    # Redes / Instagram / social media
    if any(p in texto for p in ["instagram", "dm", "redes", "facebook ads", "tiktok", "social"]):
        return (
            "cómo conectar lo que pasa en tus redes sociales (DM, comentarios, formularios) "
            "con un sistema donde no se pierdan las conversaciones valiosas."
        )

    # E-commerce
    if "ecommerce" in texto or "tienda online" in texto:
        return (
            "identificar qué personas pasan de solo mirar productos a realmente tener intención de compra "
            "y acompañarlas mejor hasta el pago."
        )

    # Academias / cursos / formaciones
    if "academia" in texto or "curso" in texto or "formación" in texto or "formacion" in texto or "webinar" in texto:
        return (
            "saber entre todos los registros de tus cursos y webinars quién está listo para una oferta de mayor valor, "
            "sin tener que revisar uno a uno."
        )

    # Hostelería / cafetería / restaurantes
    if "cafetería" in texto or "cafeteria" in texto or "hosteleria" in texto or "restaurante" in texto:
        return (
            "pasar de visitas puntuales a clientes recurrentes, "
            "sabiendo quién vuelve, cada cuánto y qué tipo de comunicación les funciona mejor."
        )

    # Servicios B2B / consultoría
    if "consultoría" in texto or "consultoria" in texto or "b2b" in texto or "empresa" in texto or "servicio" in texto:
        return (
            "tener visibilidad clara de en qué fase está cada empresa con la que hablas "
            "y priorizar a las que están más cerca de tomar una decisión."
        )

    # Genérico
    return (
        "organizar mejor tus oportunidades, tener claras las prioridades "
        "y no depender solo de la memoria o de revisar chats antiguos para saber qué sigue."
    )


def _beneficio_principal(etapa: str) -> str:
    """
    Según la etapa del funnel enfatizamos un beneficio distinto.
    """
    if etapa == "awareness":
        return "tener claridad sobre el problema y decidir con calma si tiene sentido avanzar"
    if etapa == "decision":
        return "tomar una decisión con datos claros y no solo por intuición o urgencia"
    # consideration por defecto
    return "bajar el caos actual y trabajar con un sistema sencillo que no te robe más tiempo"


def _construir_cta(objetivo: str, temperatura: str, canal: str) -> str:
    """
    CTA según objetivo + temperatura y canal.
    """
    if objetivo == "conseguir_llamada":
        base = "¿Te viene bien una llamada corta de 15 minutos para ver tu caso concreto?"
    elif objetivo == "reactivar":
        base = "Si sigues interesado, dime y retomamos desde donde lo dejamos."
    else:  # seguimiento / contenido
        base = "Si te parece útil, dímelo y te comparto un ejemplo aplicado a un caso parecido al tuyo."

    if temperatura == "caliente":
        base = base.replace("en algún momento", "en estos días") if "en algún momento" in base else base
    elif temperatura == "frio":
        base = base.replace("para ver tu caso concreto", "cuando tú veas que tiene sentido, sin compromiso")

    if canal == "whatsapp":
        return base.replace("dímelo", "me dices") + " 🙂"
    return base


def _saludo_y_cierre(canal: str, nombre: str):
    """
    Devuelve (saludo, cierre) adaptado al canal.
    """
    if canal in ("email", "linkedin"):
        saludo = f"Hola {nombre},"
        cierre = "Un saludo,\nEquipo ABC Ideas"
    else:
        saludo = f"Hola {nombre} 👋"
        cierre = "Quedo pendiente,\nEquipo ABC Ideas"
    return saludo, cierre


# ========= GENERACIÓN DE MENSAJE "TIPO LLM" =========

def generate_next_message_with_llm(
    lead: Dict,
    last_interactions: Dict,
    canal: str,
    objetivo: str,
    tono: str,
) -> Dict:
    """
    Genera mensaje de nutrición adaptado al segmento, usando:
    - nombre
    - empresa / sector / fuente
    - mensaje_inicial / necesidades
    - etapa_funnel + temperatura
    """
    nombre = lead.get("nombre", "allí")
    empresa = lead.get("empresa") or ""
    etapa = lead.get("etapa_funnel") or "consideration"
    temp = lead.get("temperatura") or "tibio"

    saludo, cierre = _saludo_y_cierre(canal, nombre)

    texto_completo = (
        (lead.get("mensaje_inicial") or "")
        + " "
        + (lead.get("necesidades") or "")
        + " "
        + (lead.get("sector") or "")
        + " "
        + (lead.get("fuente") or "")
    )

    dolor = _detectar_dolor(texto_completo)
    contexto = _detectar_contexto_negocio(lead)
    beneficio = _beneficio_principal(etapa)
    cta = _construir_cta(objetivo, temp, canal)

    # Cuerpo principal según etapa
    if etapa == "awareness":
        cuerpo_base = (
            f"Por lo que comentaste, estás empezando a explorar cómo mejorar el día a día en {empresa or 'tu negocio'}. "
            f"Podemos ayudarte a {contexto}. La idea es que ganes claridad y {beneficio}, sin presión."
        )
    elif etapa == "decision":
        cuerpo_base = (
            f"Por lo que nos has contado, ya tienes bastante claro el problema y estás cerca de tomar una decisión. "
            f"Si trabajamos en {dolor}, aplicado a tu contexto, podrás {beneficio}."
        )
    else:  # consideration
        cuerpo_base = (
            f"En {empresa or 'tu negocio'} ya has visto que {dolor}. "
            f"Ahora estás valorando opciones para mejorar la forma en que gestionas tu flujo de oportunidades. "
            f"Si empezamos por ahí, será más fácil {beneficio} y, sobre esa base, podremos ver {contexto}."
        )

    cuerpo = f"{saludo}\n\n{cuerpo_base}\n\n{cta}\n\n{cierre}"

    # Asunto para email / linkedin
    if canal in ("email", "linkedin"):
        if objetivo == "conseguir_llamada":
            asunto = "¿Vemos juntos cómo ordenar mejor tu flujo de oportunidades?"
        elif objetivo == "reactivar":
            asunto = "¿Retomamos la conversación sobre tu sistema de seguimiento?"
        else:
            asunto = "Ideas para mejorar tu flujo de trabajo comercial"
    else:
        asunto = None

    return {
        "asunto": asunto,
        "cuerpo": cuerpo,
        "canal": canal,
        "generado_en": datetime.now().isoformat(timespec="seconds"),
        "etapa_funnel": etapa,
        "temperatura": temp,
    }
