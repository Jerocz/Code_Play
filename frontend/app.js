'use strict';

/* ═══════════════════════════════════ ESTADO GLOBAL ═══════════════════════════════════ */
const estado = {
  lenguaje: null,
  modulos: [],
  progreso: { python: [], javascript: [], cpp: [], xp: 0, nivel: 1, nivel_info: {} },
  moduloActual: null,
  iaConfigurada: false,
  iaOcupada: false,
  corriendo: false,
};

const LANG_META = {
  python:     { icon: '🐍', nombre: 'Python',     total: 25, placeholder: '# Escribí tu código Python acá...' },
  javascript: { icon: '🟨', nombre: 'JavaScript', total: 10, placeholder: '// Escribí tu código JS acá...' },
  cpp:        { icon: '⚙️', nombre: 'C++',         total: 10, placeholder: '// Escribí tu código C++ acá...' },
};

/* ═══════════════════════════════════ INICIALIZACIÓN ══════════════════════════════════ */
document.addEventListener('DOMContentLoaded', async () => {
  await cargarProgreso();
  await verificarIA();
  configurarEditor();
});

async function cargarProgreso() {
  try {
    const data = await api('/api/progreso');
    estado.progreso = data;
    actualizarUIProgreso();
  } catch (e) {
    console.warn('No se pudo cargar el progreso:', e);
  }
}

function actualizarUIProgreso() {
  const p = estado.progreso;
  const nivel = p.nivel_info || {};

  // Pantalla inicio
  setText('nivel-titulo-inicio', nivel.titulo || 'Principiante');
  setText('xp-badge-inicio', `${p.xp || 0} XP`);

  // Barras de progreso por lenguaje en inicio
  for (const lang of ['python', 'javascript', 'cpp']) {
    const completados = (p[lang] || []).length;
    const total = LANG_META[lang].total;
    const pct = total > 0 ? (completados / total) * 100 : 0;
    setStyle('prog-' + lang, 'width', pct + '%');
    setText('prog-' + lang + '-texto', `${completados} / ${total} módulos`);
  }
}

/* ═══════════════════════════════════ NAVEGACIÓN ══════════════════════════════════════ */
function mostrarPantalla(id) {
  document.querySelectorAll('.pantalla').forEach(p => p.classList.remove('activa'));
  const el = document.getElementById(id);
  if (el) el.classList.add('activa');
  window.scrollTo(0, 0);
}

async function seleccionarLenguaje(lang) {
  estado.lenguaje = lang;
  const meta = LANG_META[lang];

  setText('modulos-lang-icon', meta.icon);
  setText('modulos-lang-nombre', meta.nombre);

  try {
    estado.modulos = await api(`/api/modulos/${lang}`);
  } catch (e) {
    toast('Error cargando módulos. Revisá que el servidor esté corriendo.', 'error');
    return;
  }

  renderizarModulos();
  actualizarProgresoModulos();
  mostrarPantalla('pantalla-modulos');
}

function irAInicio() {
  mostrarPantalla('pantalla-inicio');
}

function irAModulos() {
  mostrarPantalla('pantalla-modulos');
  limpiarChatIA();
}

/* ═══════════════════════════════════ PANTALLA MÓDULOS ════════════════════════════════ */
function renderizarModulos() {
  const lista = document.getElementById('modulos-lista');
  lista.innerHTML = '';

  const completados = estado.progreso[estado.lenguaje] || [];
  const bloques = agruparPorBloque(estado.modulos);

  for (const [bloque, modulos] of Object.entries(bloques)) {
    const seccion = document.createElement('div');
    seccion.className = 'bloque-section';

    const titulo = document.createElement('div');
    titulo.className = 'bloque-titulo';
    titulo.textContent = bloque;
    seccion.appendChild(titulo);

    for (const modulo of modulos) {
      const estaCompletado = completados.includes(modulo.id);
      const desbloqueado = esDesbloqueado(modulo.id, completados, estado.modulos);
      const card = crearCardModulo(modulo, estaCompletado, desbloqueado);
      seccion.appendChild(card);
    }

    lista.appendChild(seccion);
  }
}

function agruparPorBloque(modulos) {
  const grupos = {};
  for (const m of modulos) {
    if (!grupos[m.bloque]) grupos[m.bloque] = [];
    grupos[m.bloque].push(m);
  }
  return grupos;
}

function esDesbloqueado(id, completados, modulos) {
  const idx = modulos.findIndex(m => m.id === id);
  if (idx === 0) return true;
  const anterior = modulos[idx - 1];
  return completados.includes(anterior.id);
}

function crearCardModulo(modulo, completado, desbloqueado) {
  const card = document.createElement('div');
  card.className = 'modulo-card' +
    (completado ? ' completado' : '') +
    (!desbloqueado ? ' bloqueado' : '');

  const numEl = document.createElement('div');
  numEl.className = 'modulo-num';
  numEl.textContent = completado ? '✓' : modulo.id;

  const info = document.createElement('div');
  info.className = 'modulo-info';

  const titulo = document.createElement('div');
  titulo.className = 'modulo-titulo';
  titulo.textContent = modulo.titulo;

  const desc = document.createElement('div');
  desc.className = 'modulo-desc';
  desc.textContent = modulo.descripcion;

  info.appendChild(titulo);
  info.appendChild(desc);

  const xpBadge = document.createElement('div');
  xpBadge.className = 'modulo-xp-badge';
  xpBadge.textContent = completado ? '✓ Completado' : `+${modulo.xp} XP`;

  card.appendChild(numEl);
  card.appendChild(info);
  card.appendChild(xpBadge);

  if (!desbloqueado) {
    const lock = document.createElement('div');
    lock.className = 'modulo-lock';
    lock.textContent = '🔒';
    card.appendChild(lock);
  }

  if (desbloqueado) {
    card.onclick = () => abrirModal(modulo, completado);
  }

  return card;
}

function actualizarProgresoModulos() {
  const completados = (estado.progreso[estado.lenguaje] || []).length;
  const total = estado.modulos.length;
  const pct = total > 0 ? (completados / total) * 100 : 0;
  const xpGanado = calcularXPGanado();
  const nivel = estado.progreso.nivel_info || {};

  setText('mod-completados', completados);
  setText('mod-total', total);
  setText('mod-xp-ganado', xpGanado);
  setStyle('modulos-barra-fill', 'width', pct + '%');

  setText('modulos-nivel-titulo', nivel.titulo || 'Principiante');
  setText('modulos-xp-valor', `${estado.progreso.xp || 0} XP`);
  setStyle('modulos-xp-fill', 'width', (nivel.progreso_pct || 0) + '%');
}

function calcularXPGanado() {
  if (!estado.lenguaje) return 0;
  const completados = estado.progreso[estado.lenguaje] || [];
  return completados.reduce((sum, id) => {
    const mod = estado.modulos.find(m => m.id === id);
    return sum + (mod ? mod.xp : 0);
  }, 0);
}

/* ═══════════════════════════════════ MODAL ═══════════════════════════════════════════ */
let moduloEnModal = null;

function abrirModal(modulo, completado) {
  moduloEnModal = modulo;

  setText('modal-bloque', modulo.bloque);
  setText('modal-xp', `+${modulo.xp} XP`);
  setText('modal-titulo', modulo.titulo);
  setText('modal-desc', modulo.descripcion);
  setText('modal-teoria-text', modulo.teoria);
  setText('modal-codigo', modulo.ejemplo);
  setText('modal-ejercicio-text', modulo.ejercicio);
  setText('modal-pista-text', modulo.pista);

  // Resetear tabs
  switchTab('teoria', document.querySelector('.modal-tab'));

  // Ocultar pista
  hide('modal-pista-text');
  setText('btn-pista-modal', '💡 Ver pista');

  // Botón completar
  const btnCompletar = document.getElementById('btn-modal-completar');
  if (completado) {
    btnCompletar.textContent = '✓ Ya completado';
    btnCompletar.classList.add('ya-completado');
  } else {
    btnCompletar.textContent = '✓ Marcar completado';
    btnCompletar.classList.remove('ya-completado');
  }

  // Si ya está completado, agregar botón repetir
  const footer = document.querySelector('.modal-footer');
  const existeRepetir = footer.querySelector('.btn-repetir');
  if (existeRepetir) existeRepetir.remove();

  if (completado) {
    const btnRepetir = document.createElement('button');
    btnRepetir.className = 'btn-modal-practicar btn-repetir';
    btnRepetir.style.background = 'var(--blue)';
    btnRepetir.textContent = '🔁 Repetir';
    btnRepetir.onclick = abrirEditor;
    footer.insertBefore(btnRepetir, footer.firstChild);
  }

  show('modal-overlay');
  document.body.style.overflow = 'hidden';
}

function cerrarModal(e) {
  if (e && e.target !== document.getElementById('modal-overlay')) return;
  hide('modal-overlay');
  document.body.style.overflow = '';
  moduloEnModal = null;
}

function switchTab(tab, btn) {
  document.querySelectorAll('.modal-tab').forEach(t => t.classList.remove('activo'));
  if (btn) btn.classList.add('activo');

  hide('modal-teoria');
  hide('modal-ejemplo');
  hide('modal-ejercicio');
  show('modal-' + tab);
}

function togglePistaModal() {
  const pista = document.getElementById('modal-pista-text');
  const btn = document.getElementById('btn-pista-modal');
  if (pista.classList.contains('oculta')) {
    show('modal-pista-text');
    btn.textContent = '💡 Ocultar pista';
  } else {
    hide('modal-pista-text');
    btn.textContent = '💡 Ver pista';
  }
}

async function marcarCompletadoDesdeModal() {
  if (!moduloEnModal) return;
  const btn = document.getElementById('btn-modal-completar');
  if (btn.classList.contains('ya-completado')) return;
  await marcarModuloCompletado(moduloEnModal.id);
}

/* ═══════════════════════════════════ EDITOR ══════════════════════════════════════════ */
function configurarEditor() {
  const editor = document.getElementById('code-editor');

  editor.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = editor.selectionStart;
      const end = editor.selectionEnd;
      editor.value = editor.value.substring(0, start) + '    ' + editor.value.substring(end);
      editor.selectionStart = editor.selectionEnd = start + 4;
    }
  });
}

function abrirEditor() {
  const modulo = moduloEnModal;
  if (!modulo) return;

  estado.moduloActual = modulo;
  const completado = (estado.progreso[estado.lenguaje] || []).includes(modulo.id);
  const meta = LANG_META[estado.lenguaje];

  // Actualizar header
  setText('editor-modulo-numero', `#${modulo.id}`);
  setText('editor-modulo-titulo', modulo.titulo);

  // Columna izquierda
  setText('editor-teoria', modulo.teoria);
  setText('editor-ejercicio', modulo.ejercicio);
  setText('editor-pista', modulo.pista);
  hide('editor-pista');
  setText('btn-pista', '💡 Mostrar pista');

  // Badge de lenguaje
  setText('code-lang-badge', meta.nombre);
  document.getElementById('code-editor').placeholder = meta.placeholder;

  // Botón completar
  const btnCompletar = document.getElementById('btn-completar-editor');
  if (completado) {
    btnCompletar.textContent = '✓ Completado';
    btnCompletar.classList.add('ya-completado');
  } else {
    btnCompletar.textContent = '✓ Marcar completado';
    btnCompletar.classList.remove('ya-completado');
  }

  // Limpiar output
  const outputPre = document.getElementById('output-pre');
  outputPre.textContent = 'El output aparecerá aquí...';
  outputPre.className = 'output-pre';
  setText('output-status', '');
  setText('run-tiempo', '');

  cerrarModal();
  mostrarPantalla('pantalla-editor');
}

function togglePista() {
  const pista = document.getElementById('editor-pista');
  const btn = document.getElementById('btn-pista');
  if (pista.classList.contains('oculta')) {
    show('editor-pista');
    btn.textContent = '💡 Ocultar pista';
  } else {
    hide('editor-pista');
    btn.textContent = '💡 Mostrar pista';
  }
}

function limpiarEditor() {
  document.getElementById('code-editor').value = '';
  document.getElementById('code-editor').focus();
}

/* ═══════════════════════════════════ EJECUCIÓN DE CÓDIGO ════════════════════════════ */
async function ejecutarCodigo() {
  if (estado.corriendo) return;

  const codigo = document.getElementById('code-editor').value.trim();
  if (!codigo) {
    toast('Escribí algo de código primero!', 'error');
    return;
  }

  estado.corriendo = true;
  const btnRun = document.getElementById('btn-run');
  btnRun.disabled = true;
  btnRun.textContent = '⟳ Corriendo...';
  btnRun.classList.add('corriendo');

  const outputPre = document.getElementById('output-pre');
  const outputStatus = document.getElementById('output-status');
  const runTiempo = document.getElementById('run-tiempo');

  outputPre.textContent = 'Ejecutando...';
  outputPre.className = 'output-pre';
  outputStatus.textContent = '';
  outputStatus.className = 'output-status';
  runTiempo.textContent = '';

  try {
    const resultado = await api('/api/ejecutar', 'POST', {
      lenguaje: estado.lenguaje,
      codigo: codigo,
    });

    outputPre.textContent = resultado.output;
    runTiempo.textContent = `${resultado.tiempo}s`;

    if (resultado.exito) {
      outputPre.className = 'output-pre ok';
      outputStatus.textContent = '✓ OK';
      outputStatus.className = 'output-status ok';
    } else {
      outputPre.className = 'output-pre error';
      outputStatus.textContent = '✗ Error';
      outputStatus.className = 'output-status error';
    }

    // Análisis automático de IA
    if (estado.iaConfigurada && estado.moduloActual) {
      await analizarConIA(codigo, resultado);
    }

  } catch (e) {
    outputPre.textContent = 'Error conectando con el servidor. ¿Está corriendo el backend?';
    outputPre.className = 'output-pre error';
    outputStatus.textContent = '✗ Error';
    outputStatus.className = 'output-status error';
  } finally {
    estado.corriendo = false;
    btnRun.disabled = false;
    btnRun.textContent = '▶ Correr';
    btnRun.classList.remove('corriendo');
  }
}

/* ═══════════════════════════════════ TUTOR IA ═══════════════════════════════════════ */
async function verificarIA() {
  try {
    const data = await api('/ia/estado');
    estado.iaConfigurada = data.configurada;
    const badge = document.getElementById('ia-estado-badge');
    if (badge) {
      badge.textContent = data.configurada ? '● Activa' : '○ Sin config';
      badge.className = 'ia-estado ' + (data.configurada ? 'activa' : 'inactiva');
    }
  } catch (e) {
    estado.iaConfigurada = false;
  }
}

async function analizarConIA(codigo, resultado) {
  if (!estado.iaConfigurada || estado.iaOcupada) return;

  const modulo = estado.moduloActual;
  agregarMensajeIA('assistant', '...analizando tu código 🔍', true);

  try {
    const data = await api('/ia/analizar', 'POST', {
      codigo,
      output: resultado.output,
      exito: resultado.exito,
      modulo_titulo: modulo?.titulo,
      modulo_ejercicio: modulo?.ejercicio,
      lenguaje: estado.lenguaje,
    });

    reemplazarUltimoMensajeIA(data.respuesta);
  } catch (e) {
    reemplazarUltimoMensajeIA('(El tutor IA no pudo analizar en este momento)');
  }
}

async function enviarPreguntaIA() {
  if (estado.iaOcupada) return;

  const input = document.getElementById('ia-input');
  const mensaje = input.value.trim();
  if (!mensaje) return;

  input.value = '';

  agregarMensajeIA('user', mensaje);
  agregarMensajeIA('assistant', '...pensando 💭', true);

  estado.iaOcupada = true;
  document.getElementById('btn-ia-enviar').disabled = true;

  try {
    const data = await api('/ia/preguntar', 'POST', {
      mensaje,
      contexto_modulo: estado.moduloActual?.titulo,
      lenguaje: estado.lenguaje,
    });
    reemplazarUltimoMensajeIA(data.respuesta);
  } catch (e) {
    if (e.message.includes('503') || e.message.includes('GEMINI')) {
      reemplazarUltimoMensajeIA('El tutor IA no está configurado. Configurá la variable GEMINI_API_KEY para activarlo.');
    } else {
      reemplazarUltimoMensajeIA('Error conectando con el tutor IA. Intentá de nuevo.');
    }
  } finally {
    estado.iaOcupada = false;
    document.getElementById('btn-ia-enviar').disabled = false;
  }
}

function iaInputKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    enviarPreguntaIA();
  }
}

function agregarMensajeIA(role, texto, esCargando = false) {
  const chat = document.getElementById('ia-chat');

  const div = document.createElement('div');
  div.className = 'ia-mensaje' + (role === 'user' ? ' usuario' : '') + (esCargando ? ' ia-cargando' : '');
  if (esCargando) div.id = 'ia-cargando';

  const avatar = document.createElement('span');
  avatar.className = 'ia-avatar';
  avatar.textContent = role === 'user' ? '🧑' : '🤖';

  const burbuja = document.createElement('div');
  burbuja.className = 'ia-burbuja';
  burbuja.textContent = texto;

  div.appendChild(avatar);
  div.appendChild(burbuja);
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function reemplazarUltimoMensajeIA(texto) {
  const cargando = document.getElementById('ia-cargando');
  if (cargando) {
    cargando.id = '';
    cargando.classList.remove('ia-cargando');
    const burbuja = cargando.querySelector('.ia-burbuja');
    if (burbuja) burbuja.textContent = texto;
  } else {
    agregarMensajeIA('assistant', texto);
  }
  const chat = document.getElementById('ia-chat');
  chat.scrollTop = chat.scrollHeight;
}

async function limpiarChatIA() {
  const chat = document.getElementById('ia-chat');
  chat.innerHTML = '';
  agregarMensajeIA('assistant', '¡Hola! Soy tu tutor IA. Corrí tu código y te voy a dar feedback automático. También podés preguntarme cualquier duda sobre el módulo.');
  try {
    await api('/ia/historial', 'DELETE');
  } catch (e) { /* silencioso */ }
}

/* ═══════════════════════════════════ PROGRESO ════════════════════════════════════════ */
async function marcarCompletado() {
  if (!estado.moduloActual) return;
  await marcarModuloCompletado(estado.moduloActual.id);
}

async function marcarModuloCompletado(moduloId) {
  try {
    const data = await api('/api/progreso/completar', 'POST', {
      lenguaje: estado.lenguaje,
      modulo_id: moduloId,
    });

    if (data.ya_estaba) {
      toast('Ya tenías este módulo completado ✓', 'ok');
      return;
    }

    estado.progreso = {
      ...estado.progreso,
      [estado.lenguaje]: data.completados,
      xp: data.xp_total,
      nivel: data.nivel_info.nivel,
      nivel_info: data.nivel_info,
    };

    actualizarUIProgreso();
    actualizarProgresoModulos();
    renderizarModulos();

    // Actualizar botón en editor
    const btnEditor = document.getElementById('btn-completar-editor');
    btnEditor.textContent = '✓ Completado';
    btnEditor.classList.add('ya-completado');

    // Mostrar celebración
    const msg = data.nivel_info.nivel > (estado.progreso.nivel || 1)
      ? `🎉 ¡Subiste al nivel ${data.nivel_info.nivel} — ${data.nivel_info.titulo}!`
      : `⭐ +${data.xp_ganado} XP ganados! Total: ${data.xp_total} XP`;
    toast(msg, 'xp');

    // Cerrar modal si está abierto
    hide('modal-overlay');
    document.body.style.overflow = '';
    moduloEnModal = null;

  } catch (e) {
    toast('Error guardando el progreso', 'error');
  }
}

/* ═══════════════════════════════════ UTILIDADES ══════════════════════════════════════ */
async function api(url, method = 'GET', body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);

  const resp = await fetch(url, opts);
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: resp.statusText }));
    throw new Error(`${resp.status}: ${err.detail || resp.statusText}`);
  }
  return resp.json();
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function setStyle(id, prop, value) {
  const el = document.getElementById(id);
  if (el) el.style[prop] = value;
}

function show(id) {
  const el = typeof id === 'string' ? document.getElementById(id) : id;
  if (el) el.classList.remove('oculta');
}

function hide(id) {
  const el = typeof id === 'string' ? document.getElementById(id) : id;
  if (el) el.classList.add('oculta');
}

let toastTimer = null;
function toast(msg, tipo = '') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'toast' + (tipo ? ' ' + tipo : '');
  el.classList.remove('oculta');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.add('oculta'), 3500);
}
