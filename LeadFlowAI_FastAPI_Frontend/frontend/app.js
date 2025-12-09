const API_BASE = "http://127.0.0.1:8000";

const leadsContainer = document.getElementById("leads-container");
const outputIA = document.getElementById("output-ia");
const btnRefresh = document.getElementById("btn-refresh");
const leadForm = document.getElementById("lead-form");

// ================== Helpers de UI ==================

async function fetchLeads() {
    leadsContainer.innerHTML = "<p>Cargando leads...</p>";
    try {
        const res = await fetch(`${API_BASE}/leads`);
        const data = await res.json();
        renderLeads(data);
    } catch (err) {
        console.error(err);
        leadsContainer.innerHTML = "<p>Error al cargar leads.</p>";
    }
}

function renderLeads(leads) {
    if (!leads.length) {
        leadsContainer.innerHTML = "<p>No hay leads aún.</p>";
        return;
    }
    leadsContainer.innerHTML = "";
    leads.forEach((lead) => {
        const card = document.createElement("div");
        card.className = "lead-card";

        const header = document.createElement("div");
        header.className = "lead-header";

        const info = document.createElement("div");
        const name = document.createElement("div");
        name.className = "lead-name";
        name.textContent = `${lead.nombre} (${lead.id})`;

        const meta = document.createElement("div");
        meta.className = "lead-meta";
        meta.textContent = `${lead.empresa || "Sin empresa"} · ${lead.sector || "Sin sector"} · ${lead.fuente || "Sin fuente"}`;

        info.appendChild(name);
        info.appendChild(meta);

        const tags = document.createElement("div");
        if (lead.etapa_funnel) {
            const chipEtapa = document.createElement("span");
            chipEtapa.className = "chip";
            chipEtapa.textContent = `Funnel: ${lead.etapa_funnel}`;
            tags.appendChild(chipEtapa);
        }
        if (lead.temperatura) {
            const chipTemp = document.createElement("span");
            chipTemp.className = "chip";
            chipTemp.textContent = `Temp: ${lead.temperatura}`;
            tags.appendChild(chipTemp);
        }
        if (!lead.etapa_funnel && !lead.temperatura) {
            const chip = document.createElement("span");
            chip.className = "chip";
            chip.textContent = "Sin segmentar";
            tags.appendChild(chip);
        }

        header.appendChild(info);
        header.appendChild(tags);

        const body = document.createElement("div");
        body.className = "lead-body";
        const mensaje = document.createElement("p");
        mensaje.className = "lead-meta";
        mensaje.textContent = lead.mensaje_inicial || "(Sin mensaje inicial)";
        body.appendChild(mensaje);

        const acciones = document.createElement("div");
        acciones.className = "lead-actions";

        const btnSeg = document.createElement("button");
        btnSeg.textContent = "🧠 Segmentar";
        btnSeg.onclick = () => segmentLead(lead.id);

        const btnMsgEmail = document.createElement("button");
        btnMsgEmail.textContent = "✉️ Mensaje email";
        btnMsgEmail.onclick = () => nextMessage(lead.id, "email", "conseguir_llamada");

        const btnMsgWhats = document.createElement("button");
        btnMsgWhats.textContent = "📱 Mensaje WhatsApp";
        btnMsgWhats.onclick = () => nextMessage(lead.id, "whatsapp", "conseguir_llamada");

        acciones.appendChild(btnSeg);
        acciones.appendChild(btnMsgEmail);
        acciones.appendChild(btnMsgWhats);

        card.appendChild(header);
        card.appendChild(body);
        card.appendChild(acciones);

        leadsContainer.appendChild(card);
    });
}

// ================== Format helpers ==================

function formatMessage(data, canal) {
    if (canal === "email") {
        const asunto =
            data.asunto ||
            "¿Vemos juntos cómo ordenar mejor tu flujo de oportunidades?";

        return (
            "📧 Email sugerido:\n\n" +
            `Asunto: ${asunto}\n\n` +
            data.cuerpo
        );
    }

    // WhatsApp por defecto
    return "📱 WhatsApp sugerido:\n\n" + data.cuerpo;
}

function formatSegmentation(data) {
    return (
        "🔍 Segmentación del contacto\n\n" +
        `- Etapa del funnel: ${data.etapa_funnel}\n` +
        `- Temperatura: ${data.temperatura}\n` +
        `- Tipo de contacto: ${data.tipo_contacto}\n` +
        `- Siguiente paso sugerido:\n  ${data.siguiente_paso}\n\n` +
        "Justificación:\n" +
        data.justificacion
    );
}

// ================== Acciones IA ==================

async function segmentLead(id) {
    outputIA.textContent = "Segmentando lead...";
    try {
        const res = await fetch(`${API_BASE}/leads/${id}/segmentar`, {
            method: "POST",
        });
        if (!res.ok) {
            throw new Error("Error en la segmentación");
        }
        const data = await res.json();
        outputIA.textContent = formatSegmentation(data);
        fetchLeads();
    } catch (err) {
        console.error(err);
        outputIA.textContent = "Error al segmentar el lead.";
    }
}

async function nextMessage(id, canal, objetivo) {
    outputIA.textContent = "Generando mensaje...";
    try {
        const res = await fetch(`${API_BASE}/leads/${id}/siguiente-mensaje`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                canal,
                objetivo,
                tono: "cercano_profesional",
            }),
        });
        if (!res.ok) {
            throw new Error("Error al generar mensaje");
        }
        const data = await res.json();
        outputIA.textContent = formatMessage(data, canal);
    } catch (err) {
        console.error(err);
        outputIA.textContent = "Error al generar el mensaje.";
    }
}

// ================== Crear lead nuevo ==================

leadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(leadForm);
    const payload = Object.fromEntries(formData.entries());

    if (!payload.nombre) {
        alert("El nombre es obligatorio");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/leads`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        if (!res.ok) throw new Error("Error al crear lead");
        leadForm.reset();
        fetchLeads();
    } catch (err) {
        console.error(err);
        alert("Error al crear el lead");
    }
});

btnRefresh.addEventListener("click", fetchLeads);

// Primera carga
fetchLeads();
