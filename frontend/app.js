'use strict';

/* ═══════════════════════════════════ ESTADO GLOBAL ═══════════════════════════════════ */
const estado = {
  lenguaje: null,
  modulos: [],
  progreso: {
    python: [], javascript: [], cpp: [], xp: 0, nivel: 1, nivel_info: {}, racha: 0, mejor_racha: 0,
    proyectos: { python: [], javascript: [], cpp: [] }, proyectos_pasos: {},
  },
  moduloActual: null,
  iaConfigurada: false,
  iaOcupada: false,
  corriendo: false,
  proyectos: [],
  proyectosCargados: false,
  proyectoActual: null,
  iaOcupadaProyecto: false,
  corriendoProyecto: false,
};

const NIVEL_ICONS = ['🌱', '📘', '🎓', '💻', '⚡', '🔥', '👑'];
const NIVELES_INFO = [
  { nivel: 1, titulo: "Principiante", min_xp: 0 },
  { nivel: 2, titulo: "Aprendiz",     min_xp: 200 },
  { nivel: 3, titulo: "Estudiante",   min_xp: 500 },
  { nivel: 4, titulo: "Desarrollador",min_xp: 1000 },
  { nivel: 5, titulo: "Programador",  min_xp: 2000 },
  { nivel: 6, titulo: "Experto",      min_xp: 3000 },
  { nivel: 7, titulo: "Maestro",      min_xp: 4500 },
];

function getNivelIcon(nivel) {
  return NIVEL_ICONS[(nivel || 1) - 1] || '🌱';
}

const LANG_META = {
  python:     { icon: '🐍', nombre: 'Python',     total: 25, proyectosTotal: 5, placeholder: '# Escribí tu código Python acá...' },
  javascript: { icon: '🟨', nombre: 'JavaScript', total: 10, proyectosTotal: 5, placeholder: '// Escribí tu código JS acá...' },
  cpp:        { icon: '⚙️', nombre: 'C++',         total: 10, proyectosTotal: 5, placeholder: '// Escribí tu código C++ acá...' },
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
  const racha = p.racha || 0;

  setText('nivel-titulo-inicio', nivel.titulo || 'Principiante');
  setText('xp-badge-inicio', `${p.xp || 0} XP`);

  const rachaBadge = document.getElementById('racha-badge-inicio');
  if (rachaBadge) {
    if (racha > 0) {
      rachaBadge.textContent = `🔥 ${racha}`;
      rachaBadge.style.display = '';
    } else {
      rachaBadge.style.display = 'none';
    }
  }

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

  estado.proyectos = [];
  estado.proyectosCargados = false;

  renderizarModulos();
  actualizarProgresoModulos();
  mostrarTabModulos();
  mostrarPantalla('pantalla-modulos');
}

function irAInicio() {
  mostrarPantalla('pantalla-inicio');
}

function irAPerfil() {
  renderizarPerfil();
  mostrarPantalla('pantalla-perfil');
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
    for (const id of ['ia-estado-badge', 'proy-ia-estado-badge']) {
      const badge = document.getElementById(id);
      if (badge) {
        badge.textContent = data.configurada ? '● Activa' : '○ Sin config';
        badge.className = 'ia-estado ' + (data.configurada ? 'activa' : 'inactiva');
      }
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

    const nivelAnterior = estado.progreso.nivel || 1;

    estado.progreso = {
      ...estado.progreso,
      [estado.lenguaje]: data.completados,
      xp: data.xp_total,
      nivel: data.nivel_info.nivel,
      nivel_info: data.nivel_info,
      racha: data.racha,
      mejor_racha: data.mejor_racha,
    };

    actualizarUIProgreso();
    actualizarProgresoModulos();
    renderizarModulos();

    const btnEditor = document.getElementById('btn-completar-editor');
    btnEditor.textContent = '✓ Completado';
    btnEditor.classList.add('ya-completado');

    let msg;
    if (data.nivel_info.nivel > nivelAnterior) {
      msg = `🎉 ¡Subiste al nivel ${data.nivel_info.nivel} — ${data.nivel_info.titulo}!`;
    } else if (data.xp_bonus_racha > 0) {
      msg = `🔥 ¡Racha ${data.racha} días! +${data.xp_ganado} + ${data.xp_bonus_racha} bonus = +${data.xp_total_ganado} XP`;
    } else {
      msg = `⭐ +${data.xp_ganado} XP! Total: ${data.xp_total} XP`;
    }
    toast(msg, 'xp');

    hide('modal-overlay');
    document.body.style.overflow = '';
    moduloEnModal = null;

  } catch (e) {
    toast('Error guardando el progreso', 'error');
  }
}

/* ═══════════════════════════════════ PROYECTOS (catálogo) ═══════════════════════════ */
function mostrarTabModulos() {
  document.getElementById('tab-btn-modulos').classList.add('activo');
  document.getElementById('tab-btn-proyectos').classList.remove('activo');
  show('vista-modulos');
  hide('vista-proyectos');
}

async function mostrarTabProyectos() {
  document.getElementById('tab-btn-proyectos').classList.add('activo');
  document.getElementById('tab-btn-modulos').classList.remove('activo');
  hide('vista-modulos');
  show('vista-proyectos');

  if (!estado.proyectosCargados) {
    try {
      estado.proyectos = await api(`/api/proyectos/${estado.lenguaje}`);
      estado.proyectosCargados = true;
    } catch (e) {
      toast('Error cargando proyectos. Revisá que el servidor esté corriendo.', 'error');
      return;
    }
  }

  renderizarProyectos();
}

function renderizarProyectos() {
  const lista = document.getElementById('proyectos-lista');
  lista.innerHTML = '';

  const completados = (estado.progreso.proyectos && estado.progreso.proyectos[estado.lenguaje]) || [];
  const ordenados = [...estado.proyectos].sort((a, b) => a.id - b.id);

  for (const proyecto of ordenados) {
    const card = crearCardProyecto(proyecto, completados.includes(proyecto.id));
    lista.appendChild(card);
  }

  actualizarProgresoProyectos();
}

function crearCardProyecto(proyecto, completado) {
  const card = document.createElement('div');
  card.className = 'proyecto-card' + (completado ? ' completado' : '');

  const claseDificultad = normalizarDificultad(proyecto.dificultad);
  const conceptosHtml = proyecto.conceptos.map(c => `<span class="concepto-chip">${c}</span>`).join('');

  card.innerHTML = `
    <div class="proyecto-card-header">
      <span class="proyecto-titulo">${proyecto.titulo}</span>
      <span class="dificultad-badge ${claseDificultad}">${proyecto.dificultad}</span>
    </div>
    <p class="proyecto-desc">${proyecto.descripcion}</p>
    <div class="proyecto-conceptos">${conceptosHtml}</div>
    <div class="proyecto-footer">
      <span>⏱ ${proyecto.tiempo_estimado}</span>
      <span class="proyecto-xp-badge">${completado ? '✓ Completado' : '+' + proyecto.xp + ' XP'}</span>
    </div>
  `;
  card.onclick = () => abrirProyecto(proyecto);
  return card;
}

function normalizarDificultad(dificultad) {
  return dificultad.toLowerCase().replace('+', '').trim();
}

function actualizarProgresoProyectos() {
  const completados = (estado.progreso.proyectos && estado.progreso.proyectos[estado.lenguaje]) || [];
  const total = estado.proyectos.length;
  const pct = total > 0 ? (completados.length / total) * 100 : 0;
  const xpGanado = estado.proyectos
    .filter(p => completados.includes(p.id))
    .reduce((sum, p) => sum + p.xp, 0);

  setText('proy-completados', completados.length);
  setText('proy-total', total);
  setText('proy-xp-ganado', xpGanado);
  setStyle('proyectos-barra-fill', 'width', pct + '%');
}

function irAProyectos() {
  mostrarPantalla('pantalla-modulos');
  mostrarTabProyectos();
}

/* ═══════════════════════════════════ PROYECTO GUIADO ═════════════════════════════════ */
function abrirProyecto(proyecto) {
  estado.proyectoActual = proyecto;
  const meta = LANG_META[estado.lenguaje];
  const claseDificultad = normalizarDificultad(proyecto.dificultad);

  const badge = document.getElementById('proy-dificultad-badge');
  badge.textContent = proyecto.dificultad;
  badge.className = 'dificultad-badge ' + claseDificultad;

  setText('proy-titulo-header', proyecto.titulo);
  setText('proy-objetivo', proyecto.objetivo);

  document.getElementById('proy-requisitos').innerHTML = proyecto.requisitos.map(r => `<li>${r}</li>`).join('');
  document.getElementById('proy-criterios').innerHTML = proyecto.criterios.map(c => `<li>${c}</li>`).join('');
  document.getElementById('proy-retos').innerHTML = proyecto.retos_extra.map(r => `<li>${r}</li>`).join('');

  renderizarPasosProyecto(proyecto);

  setText('proy-code-lang-badge', meta.nombre);
  const editor = document.getElementById('proy-code-editor');
  editor.placeholder = meta.placeholder;
  editor.value = '';

  const completados = (estado.progreso.proyectos && estado.progreso.proyectos[estado.lenguaje]) || [];
  const completado = completados.includes(proyecto.id);
  const btnCompletar = document.getElementById('btn-completar-proyecto');
  if (completado) {
    btnCompletar.textContent = '✓ Proyecto completado';
    btnCompletar.classList.add('ya-completado');
  } else {
    btnCompletar.textContent = '✓ Marcar proyecto completado';
    btnCompletar.classList.remove('ya-completado');
  }

  const outputPre = document.getElementById('proy-output-pre');
  outputPre.textContent = 'El output aparecerá aquí...';
  outputPre.className = 'output-pre';
  setText('proy-output-status', '');
  setText('proy-run-tiempo', '');

  limpiarChatIAProyecto();
  mostrarPantalla('pantalla-proyecto');
}

function renderizarPasosProyecto(proyecto) {
  const cont = document.getElementById('proy-pasos');
  const clave = `${estado.lenguaje}_${proyecto.id}`;
  const completados = (estado.progreso.proyectos_pasos && estado.progreso.proyectos_pasos[clave]) || [];

  cont.innerHTML = proyecto.pasos.map((paso, i) => {
    const hecho = completados.includes(i);
    return `
      <div class="proy-paso${hecho ? ' completado' : ''}">
        <div class="proy-paso-header">
          <input type="checkbox" class="proy-paso-check" ${hecho ? 'checked' : ''} onclick="togglePasoProyecto(event, ${i})">
          <div class="proy-paso-titulos">
            <div class="proy-paso-num">Paso ${i + 1}</div>
            <div class="proy-paso-titulo">${paso.titulo}</div>
            <div class="proy-paso-desc">${paso.descripcion}</div>
            <button class="btn-pista-paso" id="proy-btn-pista-${i}" onclick="togglePistaPaso(${i})">💡 Ver pista</button>
            <div class="proy-paso-pista oculta" id="proy-pista-${i}">${paso.pista}</div>
          </div>
        </div>
      </div>`;
  }).join('');
}

async function togglePasoProyecto(event, index) {
  event.stopPropagation();
  const checkbox = event.target;
  const completado = checkbox.checked;
  const proyecto = estado.proyectoActual;
  if (!proyecto) return;

  const pasoEl = checkbox.closest('.proy-paso');
  pasoEl.classList.toggle('completado', completado);

  try {
    const data = await api('/api/proyectos/paso', 'POST', {
      lenguaje: estado.lenguaje,
      proyecto_id: proyecto.id,
      paso_index: index,
      completado,
    });
    const clave = `${estado.lenguaje}_${proyecto.id}`;
    if (!estado.progreso.proyectos_pasos) estado.progreso.proyectos_pasos = {};
    estado.progreso.proyectos_pasos[clave] = data.pasos_completados;
  } catch (e) {
    checkbox.checked = !completado;
    pasoEl.classList.toggle('completado', !completado);
    toast('Error guardando el paso', 'error');
  }
}

function togglePistaPaso(index) {
  const pista = document.getElementById('proy-pista-' + index);
  const btn = document.getElementById('proy-btn-pista-' + index);
  if (pista.classList.contains('oculta')) {
    show(pista);
    btn.textContent = '💡 Ocultar pista';
  } else {
    hide(pista);
    btn.textContent = '💡 Ver pista';
  }
}

function limpiarEditorProyecto() {
  document.getElementById('proy-code-editor').value = '';
  document.getElementById('proy-code-editor').focus();
}

function obtenerPasoActualProyecto() {
  if (!estado.proyectoActual) return 0;
  const clave = `${estado.lenguaje}_${estado.proyectoActual.id}`;
  const completados = (estado.progreso.proyectos_pasos && estado.progreso.proyectos_pasos[clave]) || [];
  for (let i = 0; i < estado.proyectoActual.pasos.length; i++) {
    if (!completados.includes(i)) return i;
  }
  return estado.proyectoActual.pasos.length - 1;
}

/* ═══════════════════════════════════ EJECUCIÓN Y IA — PROYECTO ═══════════════════════ */
async function ejecutarCodigoProyecto() {
  if (estado.corriendoProyecto) return;

  const codigo = document.getElementById('proy-code-editor').value.trim();
  if (!codigo) {
    toast('Escribí algo de código primero!', 'error');
    return;
  }

  estado.corriendoProyecto = true;
  const btnRun = document.getElementById('proy-btn-run');
  btnRun.disabled = true;
  btnRun.textContent = '⟳ Corriendo...';
  btnRun.classList.add('corriendo');

  const outputPre = document.getElementById('proy-output-pre');
  const outputStatus = document.getElementById('proy-output-status');
  const runTiempo = document.getElementById('proy-run-tiempo');

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

    if (estado.iaConfigurada && estado.proyectoActual) {
      await analizarConIAProyecto(codigo, resultado);
    }

  } catch (e) {
    outputPre.textContent = 'Error conectando con el servidor. ¿Está corriendo el backend?';
    outputPre.className = 'output-pre error';
    outputStatus.textContent = '✗ Error';
    outputStatus.className = 'output-status error';
  } finally {
    estado.corriendoProyecto = false;
    btnRun.disabled = false;
    btnRun.textContent = '▶ Correr';
    btnRun.classList.remove('corriendo');
  }
}

async function analizarConIAProyecto(codigo, resultado) {
  if (!estado.iaConfigurada || estado.iaOcupadaProyecto) return;

  const proyecto = estado.proyectoActual;
  const pasoIdx = obtenerPasoActualProyecto();
  const paso = proyecto.pasos[pasoIdx];

  agregarMensajeIAEn('proy-ia-chat', 'proy-ia-cargando', 'assistant', '...analizando tu código 🔍', true);

  try {
    const data = await api('/ia/analizar', 'POST', {
      codigo,
      output: resultado.output,
      exito: resultado.exito,
      modulo_titulo: `Proyecto: ${proyecto.titulo} — Paso ${pasoIdx + 1}: ${paso.titulo}`,
      modulo_ejercicio: `[PROYECTO GUIADO: guiá con preguntas y pistas graduales, NUNCA des el código completo de la solución] Objetivo del proyecto: ${proyecto.objetivo} — Paso actual: ${paso.descripcion}`,
      lenguaje: estado.lenguaje,
    });

    reemplazarUltimoMensajeIAEn('proy-ia-chat', 'proy-ia-cargando', data.respuesta);
  } catch (e) {
    reemplazarUltimoMensajeIAEn('proy-ia-chat', 'proy-ia-cargando', '(El mentor IA no pudo analizar en este momento)');
  }
}

async function enviarPreguntaIAProyecto() {
  if (estado.iaOcupadaProyecto) return;

  const input = document.getElementById('proy-ia-input');
  const mensaje = input.value.trim();
  if (!mensaje) return;

  input.value = '';

  agregarMensajeIAEn('proy-ia-chat', null, 'user', mensaje);
  agregarMensajeIAEn('proy-ia-chat', 'proy-ia-cargando', 'assistant', '...pensando 💭', true);

  estado.iaOcupadaProyecto = true;
  document.getElementById('proy-btn-ia-enviar').disabled = true;

  const proyecto = estado.proyectoActual;
  let contexto;
  if (proyecto) {
    const pasoIdx = obtenerPasoActualProyecto();
    const paso = proyecto.pasos[pasoIdx];
    contexto = `[PROYECTO GUIADO: guiá con preguntas y pistas graduales, NUNCA des el código completo de la solución] Proyecto: ${proyecto.titulo} — Paso ${pasoIdx + 1}: ${paso.titulo}`;
  }

  try {
    const data = await api('/ia/preguntar', 'POST', {
      mensaje,
      contexto_modulo: contexto,
      lenguaje: estado.lenguaje,
    });
    reemplazarUltimoMensajeIAEn('proy-ia-chat', 'proy-ia-cargando', data.respuesta);
  } catch (e) {
    if (e.message.includes('503') || e.message.includes('GEMINI')) {
      reemplazarUltimoMensajeIAEn('proy-ia-chat', 'proy-ia-cargando', 'El mentor IA no está configurado. Configurá la variable GEMINI_API_KEY para activarlo.');
    } else {
      reemplazarUltimoMensajeIAEn('proy-ia-chat', 'proy-ia-cargando', 'Error conectando con el mentor IA. Intentá de nuevo.');
    }
  } finally {
    estado.iaOcupadaProyecto = false;
    document.getElementById('proy-btn-ia-enviar').disabled = false;
  }
}

function iaInputKeydownProyecto(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    enviarPreguntaIAProyecto();
  }
}

function agregarMensajeIAEn(chatId, cargandoId, role, texto, esCargando = false) {
  const chat = document.getElementById(chatId);

  const div = document.createElement('div');
  div.className = 'ia-mensaje' + (role === 'user' ? ' usuario' : '') + (esCargando ? ' ia-cargando' : '');
  if (esCargando && cargandoId) div.id = cargandoId;

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

function reemplazarUltimoMensajeIAEn(chatId, cargandoId, texto) {
  const cargando = document.getElementById(cargandoId);
  if (cargando) {
    cargando.removeAttribute('id');
    cargando.classList.remove('ia-cargando');
    const burbuja = cargando.querySelector('.ia-burbuja');
    if (burbuja) burbuja.textContent = texto;
  } else {
    agregarMensajeIAEn(chatId, null, 'assistant', texto);
  }
  const chat = document.getElementById(chatId);
  chat.scrollTop = chat.scrollHeight;
}

async function limpiarChatIAProyecto() {
  const chat = document.getElementById('proy-ia-chat');
  chat.innerHTML = '';
  agregarMensajeIAEn('proy-ia-chat', null, 'assistant', '¡Hola! Soy tu mentor para este proyecto. Te voy a guiar con preguntas, pistas y explicaciones, pero la solución la construís vos. ¡Empecemos!');
  try {
    await api('/ia/historial', 'DELETE');
  } catch (e) { /* silencioso */ }
}

/* ═══════════════════════════════════ COMPLETAR PROYECTO ══════════════════════════════ */
async function marcarProyectoCompletado() {
  if (!estado.proyectoActual) return;
  const btn = document.getElementById('btn-completar-proyecto');
  if (btn.classList.contains('ya-completado')) return;

  try {
    const data = await api('/api/proyectos/completar', 'POST', {
      lenguaje: estado.lenguaje,
      proyecto_id: estado.proyectoActual.id,
    });

    if (data.ya_estaba) {
      toast('Ya tenías este proyecto completado ✓', 'ok');
      return;
    }

    const nivelAnterior = estado.progreso.nivel || 1;
    const proyectosPrevios = estado.progreso.proyectos || {};

    estado.progreso = {
      ...estado.progreso,
      proyectos: { ...proyectosPrevios, [estado.lenguaje]: data.completados },
      xp: data.xp_total,
      nivel: data.nivel_info.nivel,
      nivel_info: data.nivel_info,
      racha: data.racha,
      mejor_racha: data.mejor_racha,
    };

    actualizarUIProgreso();

    btn.textContent = '✓ Proyecto completado';
    btn.classList.add('ya-completado');

    let msg;
    if (data.nivel_info.nivel > nivelAnterior) {
      msg = `🎉 ¡Subiste al nivel ${data.nivel_info.nivel} — ${data.nivel_info.titulo}!`;
    } else if (data.xp_bonus_racha > 0) {
      msg = `🔥 ¡Racha ${data.racha} días! +${data.xp_ganado} + ${data.xp_bonus_racha} bonus = +${data.xp_total_ganado} XP`;
    } else {
      msg = `⭐ +${data.xp_ganado} XP! Total: ${data.xp_total} XP`;
    }
    toast(msg, 'xp');

  } catch (e) {
    toast('Error guardando el progreso del proyecto', 'error');
  }
}

/* ═══════════════════════════════════ PERFIL ══════════════════════════════════════════ */
function renderizarPerfil() {
  const p = estado.progreso;
  const nivel = p.nivel_info || {};
  const racha = p.racha || 0;
  const mejorRacha = p.mejor_racha || 0;
  const xp = p.xp || 0;

  const totalCompletados = ['python', 'javascript', 'cpp']
    .reduce((sum, lang) => sum + (p[lang] || []).length, 0);

  let xpMeta;
  if ((nivel.nivel || 1) < 7) {
    const xpRestante = (nivel.xp_siguiente || 0) - xp;
    xpMeta = `Faltan ${xpRestante} XP para ${NIVELES_INFO[nivel.nivel] ? NIVELES_INFO[nivel.nivel].titulo : 'el siguiente nivel'}`;
  } else {
    xpMeta = '¡Nivel máximo alcanzado!';
  }

  const bonusStr = rachaBonus(racha);

  document.getElementById('perfil-contenido').innerHTML = `
    <div class="perfil-hero">
      <div class="perfil-avatar-grande">${getNivelIcon(nivel.nivel)}</div>
      <div class="perfil-nivel-titulo">${nivel.titulo || 'Principiante'}</div>
      <div class="perfil-xp-total">${xp.toLocaleString()} XP</div>
      <div class="perfil-xp-barra-wrap">
        <div class="perfil-xp-barra-fill" style="width:${nivel.progreso_pct || 0}%"></div>
      </div>
      <div class="perfil-xp-meta">${xpMeta}</div>
    </div>

    <div class="perfil-stats-grid">
      <div class="perfil-stat-card${racha >= 2 ? ' racha-card' : ''}">
        <div class="perfil-stat-icono">🔥</div>
        <div class="perfil-stat-valor">${racha}</div>
        <div class="perfil-stat-label">Racha actual</div>
        ${racha >= 2 ? `<div class="perfil-stat-bonus">+${bonusStr}% XP bonus</div>` : ''}
      </div>
      <div class="perfil-stat-card">
        <div class="perfil-stat-icono">🏆</div>
        <div class="perfil-stat-valor">${mejorRacha}</div>
        <div class="perfil-stat-label">Mejor racha</div>
      </div>
      <div class="perfil-stat-card">
        <div class="perfil-stat-icono">📚</div>
        <div class="perfil-stat-valor">${totalCompletados}<span class="perfil-de-total">/45</span></div>
        <div class="perfil-stat-label">Módulos</div>
      </div>
      <div class="perfil-stat-card">
        <div class="perfil-stat-icono">⭐</div>
        <div class="perfil-stat-valor">${nivel.nivel || 1}<span class="perfil-de-total">/7</span></div>
        <div class="perfil-stat-label">Nivel</div>
      </div>
    </div>

    <div class="perfil-section">
      <h3 class="perfil-section-titulo">Progreso por lenguaje</h3>
      ${renderLangStat('🐍', 'Python', 25, (p.python || []).length)}
      ${renderLangStat('🟨', 'JavaScript', 10, (p.javascript || []).length)}
      ${renderLangStat('⚙️', 'C++', 10, (p.cpp || []).length)}
    </div>

    <div class="perfil-section">
      <h3 class="perfil-section-titulo">Progreso en proyectos</h3>
      ${renderLangStat('🐍', 'Python', 5, ((p.proyectos || {}).python || []).length, 'proyectos')}
      ${renderLangStat('🟨', 'JavaScript', 5, ((p.proyectos || {}).javascript || []).length, 'proyectos')}
      ${renderLangStat('⚙️', 'C++', 5, ((p.proyectos || {}).cpp || []).length, 'proyectos')}
    </div>

    <div class="perfil-section">
      <h3 class="perfil-section-titulo">Mapa de niveles</h3>
      <div class="niveles-mapa">
        ${renderNivelesMapa(xp, nivel.nivel || 1)}
      </div>
    </div>

    <div class="perfil-section perfil-racha-info">
      <h3 class="perfil-section-titulo">Bonus de racha diaria</h3>
      <div class="racha-tabla">
        ${renderRachaFila('🔥 2+ días', '10% más XP', racha >= 2)}
        ${renderRachaFila('🔥 5+ días', '25% más XP', racha >= 5)}
        ${renderRachaFila('🔥 10+ días', '50% más XP', racha >= 10)}
      </div>
    </div>
  `;
}

function rachaBonus(racha) {
  if (racha >= 10) return 50;
  if (racha >= 5)  return 25;
  if (racha >= 2)  return 10;
  return 0;
}

function renderLangStat(icon, nombre, total, completados, unidad = 'módulos') {
  const pct = total > 0 ? Math.round((completados / total) * 100) : 0;
  return `
    <div class="perfil-lang-stat">
      <div class="perfil-lang-header">
        <span>${icon} ${nombre}</span>
        <span class="perfil-lang-nums">${completados}/${total} ${unidad} · ${pct}%</span>
      </div>
      <div class="perfil-lang-bar">
        <div class="perfil-lang-bar-fill" style="width:${pct}%"></div>
      </div>
    </div>`;
}

function renderNivelesMapa(xp, nivelActual) {
  return NIVELES_INFO.map(n => {
    const alcanzado = xp >= n.min_xp;
    const esCurrent = n.nivel === nivelActual;
    return `
      <div class="nivel-mapa-item${alcanzado ? ' alcanzado' : ''}${esCurrent ? ' actual' : ''}">
        ${esCurrent ? '<div class="nivel-mapa-current-badge">Aquí</div>' : ''}
        <div class="nivel-mapa-icono">${getNivelIcon(n.nivel)}</div>
        <div class="nivel-mapa-titulo">${n.titulo}</div>
        <div class="nivel-mapa-xp">${n.min_xp} XP</div>
      </div>`;
  }).join('');
}

function renderRachaFila(label, bonus, activo) {
  return `
    <div class="racha-fila${activo ? ' activa' : ''}">
      <span class="racha-fila-label">${label}</span>
      <span class="racha-fila-bonus">${bonus}</span>
      ${activo ? '<span class="racha-fila-check">✓ Activo</span>' : ''}
    </div>`;
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
