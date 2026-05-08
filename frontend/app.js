const API = "http://127.0.0.1:8000";
let moduloActivo = null;

async function iniciar() {
    await verificarIA();
    await renderizarBloques();
}

// ══════════════════════════════════════════
// PROGRESO
// ══════════════════════════════════════════
async function cargarProgreso() {
    try {
        const res = await fetch(`${API}/progreso`);
        return await res.json();
    } catch { return { xp: 0, nivel: 1, modulos_completados: [] }; }
}

function actualizarStats(usuario) {
    document.getElementById("xp").textContent = usuario.xp;
    document.getElementById("nivel").textContent = usuario.nivel;
    const n = usuario.modulos_completados.length;
    document.getElementById("completados").textContent = n;
    const pct = Math.round((n / 25) * 100);
    document.getElementById("barra-progreso").style.width = pct + "%";
    document.getElementById("progreso-texto").textContent = `${n} de 25 módulos (${pct}%)`;
}

// ══════════════════════════════════════════
// RENDERIZAR BLOQUES Y MÓDULOS
// ══════════════════════════════════════════
async function renderizarBloques() {
    const [modulos, progreso] = await Promise.all([
        fetch(`${API}/python/modulos`).then(r => r.json()).catch(() => []),
        cargarProgreso()
    ]);

    if (!modulos.length) {
        document.getElementById("bloques-contenedor").innerHTML =
            "<p style='color:#f87171;padding:20px'>⚠ No se puede conectar al servidor. Asegurate de tener uvicorn corriendo.</p>";
        return;
    }

    actualizarStats(progreso);
    const completados = progreso.modulos_completados || [];

    // Agrupar por bloque
    const bloques = {};
    modulos.forEach(m => {
        if (!bloques[m.bloque]) bloques[m.bloque] = [];
        bloques[m.bloque].push(m);
    });

    const iconos = {
        "Fundamentos": "🧱", "Strings": "📝", "Decisiones": "🔀",
        "Loops": "🔁", "Estructuras de datos": "📦",
        "Funciones": "⚙️", "Archivos y errores": "💾",
        "OOP": "🏗️", "Casos reales": "🚀"
    };

    const contenedor = document.getElementById("bloques-contenedor");
    contenedor.innerHTML = "";

    Object.entries(bloques).forEach(([nombre, mods]) => {
        const totalBloque = mods.length;
        const hechos = mods.filter(m => completados.includes(m.id)).length;
        const bloqueCompleto = hechos === totalBloque;

        const seccion = document.createElement("div");
        seccion.className = "bloque-seccion";
        seccion.innerHTML = `
            <div class="bloque-header">
                <span class="bloque-icon">${iconos[nombre] || "📌"}</span>
                <span class="bloque-nombre">${nombre}</span>
                <span class="bloque-progreso">${hechos}/${totalBloque}</span>
                ${bloqueCompleto ? '<span class="bloque-badge">✓ Completado</span>' : ''}
            </div>
            <div class="modulos-grid" id="grid-${nombre.replace(/ /g,'_')}"></div>
        `;
        contenedor.appendChild(seccion);

        const grid = document.getElementById(`grid-${nombre.replace(/ /g,'_')}`);
        mods.forEach((m, idx) => {
            const estaCompleto = completados.includes(m.id);
            const anterior = m.id === 1 || completados.includes(m.id - 1);
            const bloqueado = !anterior && !estaCompleto;

            const card = document.createElement("div");
            card.className = "modulo-card" +
                (estaCompleto ? " completado" : "") +
                (bloqueado ? " bloqueado" : "");

            card.innerHTML = `
                <div class="modulo-num">${m.id}</div>
                <div class="modulo-info">
                    <div class="modulo-titulo">${m.titulo}</div>
                    <div class="modulo-desc">${m.descripcion}</div>
                </div>
                <div class="modulo-xp">${estaCompleto ? '✓' : '+' + m.xp + ' XP'}</div>
            `;

            if (!bloqueado) {
                card.style.cursor = "pointer";
                card.onclick = () => abrirModulo(m.id);
            }

            grid.appendChild(card);
        });
    });
}

// ══════════════════════════════════════════
// MODAL
// ══════════════════════════════════════════
async function abrirModulo(id) {
    moduloActivo = id;
    try {
        const [modulo, progreso] = await Promise.all([
            fetch(`${API}/python/modulos/${id}`).then(r => r.json()),
            cargarProgreso()
        ]);
        const estaCompleto = progreso.modulos_completados.includes(id);

        document.getElementById("modal-contenido").innerHTML = `
            <div class="modal-bloque">${modulo.bloque}</div>
            <div class="modal-titulo">${modulo.id}. ${modulo.titulo}</div>
            <div class="modal-xp">+${modulo.xp} XP</div>

            <div class="modal-seccion">
                <div class="modal-label">📖 Concepto</div>
                <div class="modal-teoria">${modulo.teoria}</div>
            </div>

            <div class="modal-seccion">
                <div class="modal-label">💻 Ejemplo</div>
                <pre class="modal-codigo">${modulo.ejemplo}</pre>
            </div>

            <div class="modal-seccion">
                <div class="modal-label">💪 Tu ejercicio</div>
                <div class="modal-ejercicio">${modulo.ejercicio}</div>
            </div>

            <div class="modal-pista" id="pista-box" style="display:none">
                <div class="modal-label">💡 Pista</div>
                <div style="color:#c0a060;font-size:13px;line-height:1.6">${modulo.pista}</div>
            </div>

            <div class="modal-acciones">
                <button onclick="togglePista()">💡 Ver pista</button>
                <button class="btn-ayuda" onclick="pedirAyuda(${modulo.id}, '${modulo.titulo}'); cerrarModal()">⚡ Preguntar al tutor</button>
                ${!estaCompleto
                    ? `<button class="btn-completar" onclick="completar(${modulo.id})">✓ Marcar como completado</button>`
                    : `<div class="badge-completado">✓ Ya completaste este módulo</div>`
                }
            </div>
        `;
        document.getElementById("modal-overlay").classList.add("visible");
    } catch { mostrarToast("No se pudo cargar el módulo", "error"); }
}

function cerrarModal() {
    document.getElementById("modal-overlay").classList.remove("visible");
}

function togglePista() {
    const pista = document.getElementById("pista-box");
    const visible = pista.style.display !== "none";
    pista.style.display = visible ? "none" : "block";
    event.target.textContent = visible ? "💡 Ver pista" : "🙈 Ocultar pista";
}

async function completar(id) {
    try {
        const res = await fetch(`${API}/progreso/completar/${id}`, { method: "POST" });
        const data = await res.json();
        if (data.error) { mostrarToast(data.error, "error"); return; }
        actualizarStats(data.usuario);
        await renderizarBloques();
        cerrarModal();
        mostrarToast(`🎉 ¡Módulo completado! +${data.usuario.xp} XP total`, "exito");
    } catch { mostrarToast("Error de conexión", "error"); }
}

function mostrarToast(texto, tipo) {
    const c = tipo === "exito"
        ? { bg: "#34d39915", color: "#34d399", border: "#34d39930" }
        : { bg: "#f8717115", color: "#f87171", border: "#f8717130" };
    const el = document.createElement("div");
    el.style.cssText = `position:fixed;bottom:24px;right:24px;background:${c.bg};color:${c.color};
        border:1px solid ${c.border};padding:14px 20px;border-radius:12px;font-size:14px;
        z-index:300;max-width:300px;line-height:1.5;`;
    el.textContent = texto;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 4000);
}

// ══════════════════════════════════════════
// TUTOR IA
// ══════════════════════════════════════════
async function verificarIA() {
    const el = document.getElementById("ia-estado");
    try {
        const res = await fetch(`${API}/ia/estado`);
        const data = await res.json();
        el.textContent = data.configurada ? "✓ IA lista" : "⚠ Falta API key";
        el.className = "ia-estado " + (data.configurada ? "ok" : "error");
    } catch {
        el.textContent = "✗ Sin conexión";
        el.className = "ia-estado error";
    }
}

function pedirAyuda(id, titulo) {
    moduloActivo = id;
    document.getElementById("pregunta").value = `Estoy haciendo el módulo "${titulo}" y `;
    document.getElementById("pregunta").focus();
    document.querySelector(".ia").scrollIntoView({ behavior: "smooth" });
}

function agregarMsg(texto, tipo) {
    const h = document.getElementById("chat-historial");
    const d = document.createElement("div");
    d.className = `msg ${tipo}`;
    d.innerHTML = `<div class="msg-label">${tipo === "user" ? "Vos" : tipo === "ia" ? "Tutor IA" : "Error"}</div>
                   <div class="msg-burbuja">${texto}</div>`;
    h.appendChild(d);
    h.scrollTop = h.scrollHeight;
}

function mostrarTyping() {
    const h = document.getElementById("chat-historial");
    const t = document.createElement("div");
    t.id = "typing"; t.className = "msg ia";
    t.innerHTML = `<div class="msg-label">Tutor IA</div>
                   <div class="typing"><span></span><span></span><span></span></div>`;
    h.appendChild(t); h.scrollTop = h.scrollHeight;
}

function quitarTyping() { document.getElementById("typing")?.remove(); }

async function preguntarIA() {
    const input = document.getElementById("pregunta");
    const msg = input.value.trim();
    if (!msg) return;
    const btn = document.getElementById("btn-preguntar");
    btn.disabled = true;
    input.value = "";
    agregarMsg(msg, "user");
    mostrarTyping();
    try {
        const res = await fetch(`${API}/ia/preguntar`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mensaje: msg, modulo_id: moduloActivo })
        });
        const data = await res.json();
        quitarTyping();
        agregarMsg(data.respuesta || data.error, data.error ? "error" : "ia");
    } catch {
        quitarTyping();
        agregarMsg("No se pudo conectar. ¿Está uvicorn corriendo?", "error");
    } finally {
        btn.disabled = false;
        input.focus();
    }
}

async function limpiarConversacion() {
    try { await fetch(`${API}/ia/historial`, { method: "DELETE" }); } catch {}
    document.getElementById("chat-historial").innerHTML = "";
    moduloActivo = null;
}

iniciar();
