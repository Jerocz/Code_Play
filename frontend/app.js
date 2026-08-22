'use strict';

/* ═══════════════════════════════════════════════════════════════════════
   Code Play — frontend. Usa los mismos endpoints que ya tenés:
     GET  /api/progreso                POST /api/progreso/completar
     GET  /api/modulos/:lang           POST /api/ejecutar
     GET  /api/proyectos/:lang         POST /api/proyectos/completar
     GET  /api/tienda                  POST /api/tienda/comprar
     GET  /ia/estado                   POST /ia/analizar  POST /ia/preguntar
   Lo único que no existe en el backend son los cofres y las insignias:
   se calculan acá a partir del progreso (marcados con COFRE / INSIGNIA).
   ═══════════════════════════════════════════════════════════════════════ */

const NIVELES = [
  { nivel: 1, titulo: 'Principiante', min: 0, icono: 'sprout' },
  { nivel: 2, titulo: 'Aprendiz', min: 200, icono: 'book-open' },
  { nivel: 3, titulo: 'Estudiante', min: 500, icono: 'graduation-cap' },
  { nivel: 4, titulo: 'Desarrollador', min: 1000, icono: 'laptop' },
  { nivel: 5, titulo: 'Programador', min: 2000, icono: 'zap' },
  { nivel: 6, titulo: 'Experto', min: 3000, icono: 'flame' },
  { nivel: 7, titulo: 'Maestro', min: 4500, icono: 'crown' },
];

const LANG = {
  python: { nombre: 'Python', archivo: 'mision.py', placeholder: '# Escribí tu código acá\n', total: 25 },
  javascript: { nombre: 'JavaScript', archivo: 'mision.js', placeholder: '// Escribí tu código acá\n', total: 10 },
  cpp: { nombre: 'C++', archivo: 'mision.cpp', placeholder: '// Escribí tu código acá\n', total: 10 },
};

const ICONO_ITEM = {
  tema_matrix: 'terminal', tema_oceano: 'waves', tema_fuego: 'flame', tema_sakura: 'flower-2',
  titulo_bug_hunter: 'bug', titulo_pythonista: 'git-branch', titulo_code_ninja: 'swords',
  titulo_hacker: 'shield-half', titulo_10x: 'rocket', racha_shield: 'shield',
  boost_xp: 'sparkles', llave_maestra: 'key-round', lluvia_codigo: 'cloud-rain',
};
const NOMBRE_CATEGORIA = { tema: 'Temas', titulo: 'Títulos', powerup: 'Objetos', cosmetico: 'Cosméticos' };

const CONSEJOS = [
  'Leé el error de abajo hacia arriba: la última línea casi siempre dice qué pasó.',
  'Si te trabás más de diez minutos, escribí en palabras lo que querés que haga el programa.',
  'Correr el código a medias es mejor que escribirlo entero y correrlo al final.',
  'Ponerle buen nombre a una variable te ahorra tres comentarios.',
  'Volvé mañana aunque sea diez minutos: la racha vale más que la sesión maratónica.',
];

const OFFSETS = [0, 118, 170, 118, 0, -118, -170, -118];

const estado = {
  pantalla: 'mapa',
  lang: 'python',
  progreso: { python: [], javascript: [], cpp: [], xp: 0, nivel: 1, nivel_info: {}, racha: 0, mejor_racha: 0, proyectos: {} },
  modulos: [],
  proyectos: [],
  tienda: null,
  modulo: null,
  tab: 'teoria',
  iaActiva: false,
  iaOcupada: false,
  corriendo: false,
  consejo: 0,
};

/* ═══════════════ ARRANQUE ═══════════════ */
document.addEventListener('DOMContentLoaded', async () => {
  conectarUI();
  await cargarProgreso();
  await verificarIA();
  await cargarLenguaje('python');
  nuevoConsejo();
  iconos();
});

function conectarUI() {
  document.querySelectorAll('[data-pantalla]').forEach(b => {
    b.addEventListener('click', () => irA(b.dataset.pantalla));
  });
  document.querySelectorAll('#seg-lenguajes .seg-opt').forEach(b => {
    b.addEventListener('click', () => cambiarLenguaje(b.dataset.lang));
  });
  document.getElementById('btn-consejo').addEventListener('click', nuevoConsejo);
  document.getElementById('btn-volver-mapa').addEventListener('click', () => irA('mapa'));
  document.getElementById('btn-pista').addEventListener('click', togglePista);
  document.getElementById('btn-limpiar').addEventListener('click', () => {
    const c = document.getElementById('code'); c.value = ''; c.focus();
  });
  document.getElementById('btn-correr').addEventListener('click', ejecutar);
  document.getElementById('btn-completar').addEventListener('click', completarModulo);
  document.getElementById('btn-enviar').addEventListener('click', preguntarIA);
  document.getElementById('pregunta').addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); preguntarIA(); }
  });
  document.getElementById('dlg-cerrar').addEventListener('click', cerrarDialogo);
  document.getElementById('dialogo').addEventListener('click', e => {
    if (e.target.id === 'dialogo') cerrarDialogo();
  });
  document.getElementById('dlg-empezar').addEventListener('click', abrirEditor);
  document.querySelectorAll('.dialog-tabs .btn').forEach(b => {
    b.addEventListener('click', () => cambiarTab(b.dataset.tab));
  });
  document.getElementById('levelup-cerrar').addEventListener('click', () => {
    document.getElementById('levelup').classList.add('oculta');
  });
  document.getElementById('code').addEventListener('keydown', e => {
    if (e.key !== 'Tab') return;
    e.preventDefault();
    const t = e.target, i = t.selectionStart;
    t.value = t.value.slice(0, i) + '    ' + t.value.slice(t.selectionEnd);
    t.selectionStart = t.selectionEnd = i + 4;
  });
}

/* ═══════════════ NAVEGACIÓN ═══════════════ */
function irA(pantalla) {
  estado.pantalla = pantalla;
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('activa'));
  document.getElementById('screen-' + pantalla).classList.add('activa');
  document.querySelectorAll('.rail-btn').forEach(b => b.classList.toggle('activo', b.dataset.pantalla === pantalla));
  window.scrollTo(0, 0);

  if (pantalla === 'proyectos') cargarProyectos();
  if (pantalla === 'tienda') cargarTienda();
  if (pantalla === 'perfil') renderPerfil();
  actualizarCabecera();
}

async function cambiarLenguaje(lang) {
  if (lang === estado.lang) return;
  document.querySelectorAll('#seg-lenguajes .seg-opt').forEach(b => b.classList.toggle('activo', b.dataset.lang === lang));
  await cargarLenguaje(lang);
  irA('mapa');
}

async function cargarLenguaje(lang) {
  estado.lang = lang;
  estado.proyectos = [];
  try {
    estado.modulos = await api('/api/modulos/' + lang);
  } catch (e) {
    estado.modulos = [];
    aviso('No pude cargar los módulos. ¿Está corriendo el backend?', true);
  }
  renderMapa();
  actualizarCabecera();
}

/* ═══════════════ PROGRESO Y CABECERA ═══════════════ */
async function cargarProgreso() {
  try { estado.progreso = await api('/api/progreso'); } catch (e) { /* offline */ }
}

function nivelDe(xp) {
  let n = NIVELES[0];
  NIVELES.forEach(x => { if (xp >= x.min) n = x; });
  return n;
}

function actualizarCabecera() {
  const p = estado.progreso;
  const xp = p.xp || 0;
  const nivel = nivelDe(xp);
  const sig = NIVELES.find(n => n.min > xp);
  const pct = sig ? Math.round(((xp - nivel.min) / (sig.min - nivel.min)) * 100) : 100;
  const hechos = (p[estado.lang] || []).length;

  texto('hud-xp', xp);
  texto('hud-racha', p.racha || 0);
  texto('hud-nivel-titulo', nivel.titulo);
  texto('hud-nivel-falta', sig ? (sig.min - xp) + ' XP' : 'máximo');
  document.getElementById('hud-nivel-fill').style.width = pct + '%';
  document.getElementById('hud-nivel-icono').innerHTML = icono(nivel.icono, 18);

  const titulos = {
    mapa: 'El camino de ' + LANG[estado.lang].nombre,
    editor: estado.modulo ? estado.modulo.titulo : 'Misión',
    proyectos: 'Proyectos',
    tienda: 'Tienda',
    perfil: 'Tu perfil',
  };
  const subtitulos = {
    mapa: hechos + ' de ' + estado.modulos.length + ' misiones completadas',
    editor: 'Escribí, corré y reclamá la recompensa',
    proyectos: 'Construcciones largas para aplicar lo aprendido',
    tienda: 'Gastá XP en objetos que te acompañan',
    perfil: 'Todo lo que llevás construido',
  };
  texto('pantalla-titulo', titulos[estado.pantalla]);
  texto('pantalla-subtitulo', subtitulos[estado.pantalla]);
  iconos();
}

/* ═══════════════ MAPA ═══════════════ */
function renderMapa() {
  const cont = document.getElementById('sendero');
  const hechos = estado.progreso[estado.lang] || [];
  const actual = (estado.modulos.find(m => !hechos.includes(m.id)) || {}).id;
  let html = '';
  let bloque = null;
  let i = 0;

  estado.modulos.forEach(m => {
    if (m.bloque !== bloque) {
      bloque = m.bloque;
      html += '<div class="bloque-sep">' + escapar(bloque) + '</div>';
    }
    const hecho = hechos.includes(m.id);
    const abierto = m.id === 1 || hechos.includes(m.id - 1);
    const esActual = m.id === actual;
    const clase = hecho ? 'nodo-hecho' : (esActual ? 'nodo-actual' : (abierto ? '' : 'nodo-bloqueado'));

    html += '<div class="nodo-fila" style="transform:translateX(' + OFFSETS[i % OFFSETS.length] + 'px)">' +
      '<button class="nodo ' + clase + '" data-modulo="' + m.id + '">' +
        '<span class="nodo-circulo">' +
          (hecho ? icono('check', 30, 3.2) : m.id) +
          (abierto ? '' : '<span class="nodo-candado">' + icono('lock', 12, 3) + '</span>') +
        '</span>' +
        '<span class="nodo-texto">' +
          (esActual ? '<span class="tag tag-accent">Estás acá</span>' : '') +
          '<h3>' + escapar(m.titulo) + '</h3>' +
          '<p>' + escapar(m.descripcion) + '</p>' +
          '<span class="nodo-premio">' + (hecho ? 'Completada' : '+' + m.xp + ' XP') + '</span>' +
        '</span>' +
      '</button></div>';
    i++;

    // COFRE (visual, calculado desde el progreso)
    if (m.id % 5 === 0) {
      const listo = hechos.length >= m.id;
      html += '<div class="nodo-fila" style="transform:translateX(' + OFFSETS[i % OFFSETS.length] + 'px)">' +
        '<button class="nodo nodo-cofre ' + (listo ? '' : 'nodo-bloqueado') + '" data-cofre="' + m.id + '">' +
          '<span class="nodo-circulo">' + icono('gift', 30) + '</span>' +
          '<span class="nodo-texto"><h3>Cofre del bloque</h3>' +
          '<p>Se abre al terminar las ' + m.id + ' primeras misiones.</p>' +
          '<span class="nodo-premio">' + (listo ? 'Listo para abrir' : 'Bloqueado') + '</span></span>' +
        '</button></div>';
      i++;
    }
  });

  cont.innerHTML = html || '<p class="muted">No hay módulos para este lenguaje todavía.</p>';

  cont.querySelectorAll('[data-modulo]').forEach(b => {
    b.addEventListener('click', () => {
      if (b.classList.contains('nodo-bloqueado')) { aviso('Completá la misión anterior para abrir esta'); return; }
      abrirDialogo(Number(b.dataset.modulo));
    });
  });
  cont.querySelectorAll('[data-cofre]').forEach(b => {
    b.addEventListener('click', () => {
      if (b.classList.contains('nodo-bloqueado')) { aviso('Terminá el bloque para abrir el cofre'); return; }
      aviso('Cofre abierto: +100 XP y una insignia');
    });
  });

  renderLateral();
}

function renderLateral() {
  const hechos = estado.progreso[estado.lang] || [];
  const hoy = Math.min(hechos.length, 2);
  texto('desafio-desc', 'Completá dos misiones hoy sin salir del camino de ' + LANG[estado.lang].nombre + '.');
  texto('desafio-progreso', hoy + ' de 2 hechas');
  document.getElementById('desafio-fill').style.width = (hoy / 2) * 100 + '%';

  // Liga: mientras no exista endpoint de ranking, los rivales son fijos.
  const yo = estado.progreso.xp || 0;
  const gente = [
    { nombre: 'Mara', xp: 1240 }, { nombre: 'Diego', xp: 980 },
    { nombre: 'Vos', xp: yo, yo: true }, { nombre: 'Sofi', xp: 210 }, { nombre: 'Nico', xp: 150 },
  ].sort((a, b) => b.xp - a.xp);

  document.getElementById('ranking').innerHTML = gente.map((g, i) =>
    '<div class="rank-fila' + (g.yo ? ' yo' : '') + '">' +
      '<span class="rank-puesto">' + (i + 1) + '</span>' +
      '<span class="rank-avatar">' + g.nombre[0] + '</span>' +
      '<span class="rank-nombre">' + g.nombre + '</span>' +
      '<span class="rank-xp">' + g.xp + ' XP</span>' +
    '</div>').join('');
}

function nuevoConsejo() {
  estado.consejo = (estado.consejo + 1) % CONSEJOS.length;
  texto('pip-consejo', CONSEJOS[estado.consejo]);
}

/* ═══════════════ DIÁLOGO DE MISIÓN ═══════════════ */
function abrirDialogo(id) {
  const m = estado.modulos.find(x => x.id === id);
  if (!m) return;
  estado.modulo = m;
  estado.tab = 'teoria';
  texto('dlg-bloque', m.bloque);
  texto('dlg-xp', '+' + m.xp + ' XP');
  texto('dlg-titulo', m.titulo);
  texto('dlg-desc', m.descripcion);
  cambiarTab('teoria');
  document.getElementById('dialogo').classList.remove('oculta');
  document.body.style.overflow = 'hidden';
  iconos();
}

function cambiarTab(tab) {
  estado.tab = tab;
  const m = estado.modulo;
  if (!m) return;
  document.querySelectorAll('.dialog-tabs .btn').forEach(b => b.classList.toggle('activo', b.dataset.tab === tab));
  const pre = document.getElementById('dlg-contenido');
  pre.classList.toggle('codigo', tab === 'ejemplo');
  pre.textContent = tab === 'teoria' ? m.teoria : (tab === 'ejercicio' ? m.ejercicio : m.ejemplo);
}

function cerrarDialogo() {
  document.getElementById('dialogo').classList.add('oculta');
  document.body.style.overflow = '';
}

/* ═══════════════ EDITOR ═══════════════ */
function abrirEditor() {
  const m = estado.modulo;
  if (!m) return;
  cerrarDialogo();

  texto('editor-mision-num', 'Misión ' + m.id);
  texto('editor-titulo', m.titulo);
  texto('editor-teoria', m.teoria);
  texto('editor-ejercicio', m.ejercicio);
  texto('editor-pista', m.pista);
  document.getElementById('editor-pista').classList.add('oculta');
  document.getElementById('btn-pista').innerHTML = icono('lightbulb', 15) + ' Ver una pista';

  texto('code-archivo', LANG[estado.lang].archivo);
  const code = document.getElementById('code');
  code.value = LANG[estado.lang].placeholder;
  code.placeholder = LANG[estado.lang].placeholder;

  document.getElementById('consola').textContent = 'Todavía no corriste nada.';
  marcarEstadoConsola('espera');
  texto('run-tiempo', '');

  const hecho = (estado.progreso[estado.lang] || []).includes(m.id);
  const btn = document.getElementById('btn-completar');
  btn.disabled = hecho;
  btn.innerHTML = icono('check', 16) + (hecho ? ' Ya completada' : ' Reclamar recompensa');

  reiniciarChat();
  irA('editor');
}

function togglePista() {
  const p = document.getElementById('editor-pista');
  const oculto = p.classList.toggle('oculta');
  document.getElementById('btn-pista').innerHTML = icono('lightbulb', 15) + (oculto ? ' Ver una pista' : ' Ocultar la pista');
  iconos();
}

async function ejecutar() {
  if (estado.corriendo) return;
  const codigo = document.getElementById('code').value.trim();
  if (!codigo) { aviso('Escribí algo primero', true); return; }

  estado.corriendo = true;
  const btn = document.getElementById('btn-correr');
  btn.disabled = true;
  btn.innerHTML = icono('loader', 16) + ' Corriendo…';
  iconos();

  const salida = document.getElementById('consola');
  salida.textContent = 'Ejecutando…';
  marcarEstadoConsola('espera');

  try {
    const r = await api('/api/ejecutar', 'POST', { lenguaje: estado.lang, codigo });
    salida.textContent = r.output;
    texto('run-tiempo', r.tiempo + 's');
    marcarEstadoConsola(r.exito ? 'ok' : 'error');
    if (estado.iaActiva && estado.modulo) analizarConIA(codigo, r);
  } catch (e) {
    salida.textContent = 'No pude conectar con el servidor. ¿Está corriendo el backend?';
    marcarEstadoConsola('error');
  } finally {
    estado.corriendo = false;
    btn.disabled = false;
    btn.innerHTML = icono('play', 16) + ' Correr';
    iconos();
  }
}

function marcarEstadoConsola(tipo) {
  const t = document.getElementById('consola-estado');
  t.className = 'tag' + (tipo === 'ok' ? ' tag-ok' : (tipo === 'error' ? ' tag-error' : ''));
  t.textContent = tipo === 'ok' ? 'Sin errores' : (tipo === 'error' ? 'Con errores' : 'En espera');
}

async function completarModulo() {
  const m = estado.modulo;
  if (!m) return;
  try {
    const data = await api('/api/progreso/completar', 'POST', { lenguaje: estado.lang, modulo_id: m.id });
    if (data.ya_estaba) { aviso('Esta misión ya estaba completada'); return; }

    const antes = nivelDe(estado.progreso.xp || 0).nivel;
    estado.progreso = Object.assign({}, estado.progreso, {
      [estado.lang]: data.completados,
      xp: data.xp_total,
      nivel: data.nivel_info.nivel,
      nivel_info: data.nivel_info,
      racha: data.racha,
      mejor_racha: data.mejor_racha,
    });

    const btn = document.getElementById('btn-completar');
    btn.disabled = true;
    btn.innerHTML = icono('check', 16) + ' Ya completada';

    renderMapa();
    actualizarCabecera();

    if (data.nivel_info.nivel > antes) mostrarLevelUp(data.nivel_info);
    else {
      const bonus = data.xp_bonus_racha ? ' (+' + data.xp_bonus_racha + ' de racha)' : '';
      aviso('+' + (data.xp_total_ganado || data.xp_ganado) + ' XP — misión completada' + bonus);
      irA('mapa');
    }
    iconos();
  } catch (e) {
    aviso('No pude guardar el progreso', true);
  }
}

function mostrarLevelUp(info) {
  const n = NIVELES.find(x => x.nivel === info.nivel) || NIVELES[0];
  document.getElementById('levelup-icono').innerHTML = icono(n.icono, 44, 2.5);
  texto('levelup-titulo', info.titulo || n.titulo);
  texto('levelup-msg', 'Nuevas misiones y objetos disponibles. Tu racha de ' + (estado.progreso.racha || 0) + ' días sigue viva.');
  document.getElementById('levelup').classList.remove('oculta');
  irA('mapa');
  iconos();
}

/* ═══════════════ TUTOR IA ═══════════════ */
async function verificarIA() {
  try {
    const d = await api('/ia/estado');
    estado.iaActiva = !!d.configurada;
  } catch (e) { estado.iaActiva = false; }
  texto('tutor-estado', estado.iaActiva ? 'Tu tutor de código' : 'Sin configurar (GEMINI_API_KEY)');
}

function reiniciarChat() {
  document.getElementById('chat').innerHTML = '';
  mensaje('bot', 'Hola. Corré el código cuando quieras y te digo qué veo. Si algo no cierra, preguntame.');
  api('/ia/historial', 'DELETE').catch(() => {});
}

function mensaje(rol, texto, cargando) {
  const chat = document.getElementById('chat');
  const div = document.createElement('div');
  div.className = 'msg' + (rol === 'yo' ? ' yo' : '') + (cargando ? ' cargando' : '');
  if (cargando) div.id = 'msg-cargando';
  div.textContent = texto;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function reemplazarCargando(txt) {
  const el = document.getElementById('msg-cargando');
  if (el) { el.removeAttribute('id'); el.classList.remove('cargando'); el.textContent = txt; }
  else mensaje('bot', txt);
  const chat = document.getElementById('chat');
  chat.scrollTop = chat.scrollHeight;
}

async function analizarConIA(codigo, resultado) {
  if (estado.iaOcupada) return;
  estado.iaOcupada = true;
  mensaje('bot', 'Mirando tu código…', true);
  try {
    const d = await api('/ia/analizar', 'POST', {
      codigo, output: resultado.output, exito: resultado.exito,
      modulo_titulo: estado.modulo.titulo, modulo_ejercicio: estado.modulo.ejercicio,
      lenguaje: estado.lang,
    });
    reemplazarCargando(d.respuesta);
  } catch (e) {
    reemplazarCargando('No pude analizar el código en este momento.');
  } finally { estado.iaOcupada = false; }
}

async function preguntarIA() {
  const input = document.getElementById('pregunta');
  const q = input.value.trim();
  if (!q || estado.iaOcupada) return;
  input.value = '';
  mensaje('yo', q);
  mensaje('bot', 'Pensando…', true);
  estado.iaOcupada = true;
  document.getElementById('btn-enviar').disabled = true;
  try {
    const d = await api('/ia/preguntar', 'POST', {
      mensaje: q,
      contexto_modulo: estado.modulo ? estado.modulo.titulo : null,
      lenguaje: estado.lang,
    });
    reemplazarCargando(d.respuesta);
  } catch (e) {
    reemplazarCargando('El tutor no está disponible. Configurá GEMINI_API_KEY para activarlo.');
  } finally {
    estado.iaOcupada = false;
    document.getElementById('btn-enviar').disabled = false;
  }
}

/* ═══════════════ PROYECTOS ═══════════════ */
async function cargarProyectos() {
  if (!estado.proyectos.length) {
    try { estado.proyectos = await api('/api/proyectos/' + estado.lang); }
    catch (e) { aviso('No pude cargar los proyectos', true); return; }
  }
  const hechos = (estado.progreso.proyectos || {})[estado.lang] || [];
  document.getElementById('proyectos').innerHTML = estado.proyectos
    .slice().sort((a, b) => a.id - b.id)
    .map(p => {
      const dif = p.dificultad.startsWith('Principiante') ? 'facil' : (p.dificultad.startsWith('Intermedio') ? 'media' : 'dura');
      const hecho = hechos.includes(p.id);
      return '<article class="card proyecto">' +
        '<span class="blob dif-' + dif + '"></span>' +
        '<div class="proyecto-top">' +
          '<span class="tag dif-' + dif + '">' + escapar(p.dificultad) + '</span>' +
          '<span class="meta">' + icono('clock', 13) + ' ' + escapar(p.tiempo_estimado) + '</span>' +
        '</div>' +
        '<h3>' + escapar(p.titulo) + '</h3>' +
        '<p class="muted">' + escapar(p.descripcion) + '</p>' +
        '<div class="proyecto-chips">' + p.conceptos.map(c => '<span class="tag">' + escapar(c) + '</span>').join('') + '</div>' +
        '<span class="meta">' + icono('footprints', 14) + ' ' + p.pasos.length + ' pasos guiados</span>' +
        '<div class="proyecto-pie">' +
          '<span class="proyecto-premio">' + (hecho ? 'Completado' : '+' + p.xp + ' XP') + '</span>' +
          '<button class="btn btn-primary" data-proyecto="' + p.id + '">Ver el plan</button>' +
        '</div>' +
      '</article>';
    }).join('');

  document.querySelectorAll('[data-proyecto]').forEach(b => {
    b.addEventListener('click', () => {
      const p = estado.proyectos.find(x => x.id === Number(b.dataset.proyecto));
      aviso(p.titulo + ': ' + p.pasos.length + ' pasos guiados');
    });
  });
  iconos();
}

/* ═══════════════ TIENDA ═══════════════ */
async function cargarTienda() {
  try { estado.tienda = await api('/api/tienda'); }
  catch (e) { aviso('No pude cargar la tienda', true); return; }
  renderTienda();
}

function renderTienda() {
  const t = estado.tienda;
  if (!t) return;
  const xp = t.xp != null ? t.xp : (estado.progreso.xp || 0);
  texto('tienda-xp', xp + ' XP');

  const cats = {};
  t.items.forEach(i => { (cats[i.categoria] = cats[i.categoria] || []).push(i); });

  document.getElementById('tienda').innerHTML = Object.keys(cats).map(cat =>
    '<section class="tienda-cat"><h3>' + (NOMBRE_CATEGORIA[cat] || cat) + '</h3><div class="tienda-grid">' +
    cats[cat].map(i => {
      const tiene = i.unico && t.inventario.includes(i.id);
      const alcanza = xp >= i.precio;
      const clase = tiene ? 'tenes' : (alcanza ? 'comprable' : 'sin-xp');
      return '<article class="card item' + (!alcanza && !tiene ? ' caro' : '') + '">' +
        '<span class="item-icono">' + icono(ICONO_ITEM[i.id] || 'package', 22) + '</span>' +
        '<h4>' + escapar(i.nombre) + '</h4>' +
        '<p>' + escapar(i.descripcion) + '</p>' +
        '<span class="lore">' + escapar(i.lore || '') + '</span>' +
        '<button class="btn ' + clase + '" data-item="' + i.id + '"' + (tiene || !alcanza ? ' disabled' : '') + '>' +
          '<span>' + (tiene ? 'En tu inventario' : (alcanza ? 'Cambiar' : 'Te falta XP')) + '</span>' +
          '<span>' + (tiene ? '✓' : i.precio + ' XP') + '</span>' +
        '</button>' +
      '</article>';
    }).join('') + '</div></section>').join('');

  document.querySelectorAll('[data-item]').forEach(b => {
    b.addEventListener('click', () => comprar(b.dataset.item));
  });
  iconos();
}

async function comprar(itemId) {
  try {
    const d = await api('/api/tienda/comprar', 'POST', { item_id: itemId });
    estado.progreso.xp = d.xp_restante;
    estado.tienda.xp = d.xp_restante;
    estado.tienda.inventario = d.inventario;
    aviso(d.message);
    renderTienda();
    actualizarCabecera();
  } catch (e) {
    aviso(e.message.replace(/^\d+:\s*/, ''), true);
  }
}

/* ═══════════════ PERFIL ═══════════════ */
function renderPerfil() {
  const p = estado.progreso;
  const xp = p.xp || 0;
  const nivel = nivelDe(xp);
  const sig = NIVELES.find(n => n.min > xp);
  const pct = sig ? Math.round(((xp - nivel.min) / (sig.min - nivel.min)) * 100) : 100;
  const hechos = ['python', 'javascript', 'cpp'].reduce((s, k) => s + (p[k] || []).length, 0);
  const total = 97; // 37 python + 34 javascript + 26 cpp (módulos del sendero)
  const objetos = ((estado.tienda || {}).inventario || []).length;

  // INSIGNIA: calculadas acá; si mañana las guardás en el backend, leelas de p.insignias.
  const insignias = [
    { nombre: 'Primer print', desc: 'Corriste tu primera línea de código', icono: 'play', ok: hechos >= 1 },
    { nombre: 'Dos días seguidos', desc: 'Volviste al día siguiente', icono: 'calendar-check', ok: (p.mejor_racha || 0) >= 2 },
    { nombre: 'Bloque completo', desc: 'Terminaste un bloque entero del mapa', icono: 'flag', ok: (p.python || []).length >= 6 },
    { nombre: 'Cazador de bugs', desc: 'Arreglaste 10 errores por tu cuenta', icono: 'bug', ok: false },
    { nombre: 'Constructor', desc: 'Terminaste tu primer proyecto largo', icono: 'hammer', ok: Object.keys(p.proyectos || {}).some(k => (p.proyectos[k] || []).length > 0) },
    { nombre: 'Trilingüe', desc: 'Tocaste los tres lenguajes', icono: 'languages', ok: ['python', 'javascript', 'cpp'].every(k => (p[k] || []).length > 0) },
  ];

  document.getElementById('perfil').className = 'perfil';
  document.getElementById('perfil').innerHTML =
    '<div class="perfil-hero"><span class="blob blob-sage"></span>' +
      '<div class="perfil-avatar">' + icono(nivel.icono, 42, 2.5) + '</div>' +
      '<div class="perfil-datos">' +
        '<h2>' + nivel.titulo + '</h2>' +
        '<p class="muted">' + (sig ? 'Te faltan ' + (sig.min - xp) + ' XP para ' + sig.titulo : 'Llegaste al nivel máximo') + '</p>' +
        '<div class="barra"><div class="barra-fill" style="width:' + pct + '%"></div></div>' +
      '</div>' +
      '<div class="perfil-stats">' +
        stat('flame', p.racha || 0, 'Racha') +
        stat('check-check', hechos + '/' + total, 'Misiones') +
        stat('package', objetos, 'Objetos') +
      '</div>' +
    '</div>' +

    '<section class="perfil-seccion"><h3>Insignias</h3><div class="insignias">' +
      insignias.map(b =>
        '<div class="insignia' + (b.ok ? ' ganada' : '') + '">' +
          '<span class="insignia-medalla">' + icono(b.icono, 24) + '</span>' +
          '<h4>' + b.nombre + '</h4><p>' + b.desc + '</p>' +
        '</div>').join('') +
    '</div></section>' +

    '<section class="perfil-seccion"><h3>Camino de niveles</h3><div class="niveles">' +
      NIVELES.map(n => {
        const cls = n.nivel === nivel.nivel ? 'actual' : (xp >= n.min ? 'alcanzado' : '');
        return '<div class="nivel-card ' + cls + '">' +
          (cls === 'actual' ? '<span class="tag tag-accent">Acá estás</span>' : '') +
          '<span class="nivel-card-icono">' + icono(n.icono, 21) + '</span>' +
          '<h4>' + n.titulo + '</h4><span>' + n.min + ' XP</span></div>';
      }).join('') +
    '</div></section>' +

    '<section class="perfil-seccion"><h3>Progreso por lenguaje</h3>' +
      ['python', 'javascript', 'cpp'].map(k => {
        const h = (p[k] || []).length, t = LANG[k].total;
        const pc = Math.round((h / t) * 100);
        return '<div class="lang-stat"><div class="lang-stat-top">' +
          '<strong>' + LANG[k].nombre + '</strong><span>' + h + '/' + t + ' misiones · ' + pc + '%</span></div>' +
          '<div class="barra"><div class="barra-fill sage" style="width:' + pc + '%"></div></div></div>';
      }).join('') +
    '</section>';

  iconos();
}

function stat(ic, valor, label) {
  return '<div class="perfil-stat">' + icono(ic, 19) + '<strong>' + valor + '</strong><span>' + label + '</span></div>';
}

/* ═══════════════ UTILIDADES ═══════════════ */
async function api(url, method = 'GET', body = null) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body) opts.body = JSON.stringify(body);
  const r = await fetch(url, opts);
  if (!r.ok) {
    const err = await r.json().catch(() => ({ detail: r.statusText }));
    throw new Error(r.status + ': ' + (err.detail || r.statusText));
  }
  return r.json();
}

function icono(nombre, size = 18, stroke = 2.75) {
  return '<i data-lucide="' + nombre + '" width="' + size + '" height="' + size + '" stroke-width="' + stroke + '"></i>';
}

function iconos() {
  if (window.lucide) window.lucide.createIcons();
}

function texto(id, txt) {
  const el = document.getElementById(id);
  if (el) el.textContent = txt;
}

function escapar(s) {
  return String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

let avisoTimer = null;
function aviso(msg, esError) {
  const el = document.getElementById('toast');
  el.innerHTML = icono(esError ? 'triangle-alert' : 'sparkles', 16) + ' ' + escapar(msg);
  el.className = 'toast' + (esError ? ' error' : '');
  iconos();
  clearTimeout(avisoTimer);
  avisoTimer = setTimeout(() => el.classList.add('oculta'), 3200);
}
