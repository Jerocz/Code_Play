'use strict';

/* ═══════════════════════════════════════════════════════════════════════
   Code Play — NEXUS. Mismos endpoints del backend:
     GET  /api/progreso                POST /api/progreso/completar
     GET  /api/modulos/:lang           POST /api/ejecutar
     GET  /api/proyectos/:lang         POST /api/proyectos/completar
     GET  /api/tienda                  POST /api/tienda/comprar
     GET  /ia/estado                   POST /ia/analizar  POST /ia/preguntar
   Los sectores del mapa se derivan del campo `bloque` de cada módulo.
   Insignias y errores resueltos se calculan acá (marcados con LOCAL).
   ═══════════════════════════════════════════════════════════════════════ */

/* ═══════════════ ICONOS (Phosphor, paths embebidos) ═══════════════ */

const ICONOS = {
  graph: 'M200,152a31.84,31.84,0,0,0-19.53,6.68l-23.11-18A31.65,31.65,0,0,0,160,128c0-.74,0-1.48-.08-2.21l13.23-4.41A32,32,0,1,0,168,104c0,.74,0,1.48.08,2.21l-13.23,4.41A32,32,0,0,0,128,96a32.59,32.59,0,0,0-5.27.44L115.89,81A32,32,0,1,0,96,88a32.59,32.59,0,0,0,5.27-.44l6.84,15.4a31.92,31.92,0,0,0-8.57,39.64L73.83,165.44a32.06,32.06,0,1,0,10.63,12l25.71-22.84a31.91,31.91,0,0,0,37.36-1.24l23.11,18A31.65,31.65,0,0,0,168,184a32,32,0,1,0,32-32Zm0-64a16,16,0,1,1-16,16A16,16,0,0,1,200,88ZM80,56A16,16,0,1,1,96,72,16,16,0,0,1,80,56ZM56,208a16,16,0,1,1,16-16A16,16,0,0,1,56,208Zm56-80a16,16,0,1,1,16,16A16,16,0,0,1,112,128Zm88,72a16,16,0,1,1,16-16A16,16,0,0,1,200,200Z',
  terminal: 'M128,128a8,8,0,0,1-3,6.25l-40,32a8,8,0,1,1-10-12.5L107.19,128,75,102.25a8,8,0,1,1,10-12.5l40,32A8,8,0,0,1,128,128Zm48,24H136a8,8,0,0,0,0,16h40a8,8,0,0,0,0-16Zm56-96V200a16,16,0,0,1-16,16H40a16,16,0,0,1-16-16V56A16,16,0,0,1,40,40H216A16,16,0,0,1,232,56ZM216,200V56H40V200H216Z',
  user: 'M224,40V76a8,8,0,0,1-16,0V48H180a8,8,0,0,1,0-16h36A8,8,0,0,1,224,40Zm-8,132a8,8,0,0,0-8,8v28H180a8,8,0,0,0,0,16h36a8,8,0,0,0,8-8V180A8,8,0,0,0,216,172ZM76,208H48V180a8,8,0,0,0-16,0v36a8,8,0,0,0,8,8H76a8,8,0,0,0,0-16ZM40,84a8,8,0,0,0,8-8V48H76a8,8,0,0,0,0-16H40a8,8,0,0,0-8,8V76A8,8,0,0,0,40,84Zm136,92a8,8,0,0,1-6.41-3.19,52,52,0,0,0-83.2,0,8,8,0,1,1-12.8-9.62A67.94,67.94,0,0,1,101,141.51a40,40,0,1,1,53.94,0,67.94,67.94,0,0,1,27.43,21.68A8,8,0,0,1,176,176Zm-48-40a24,24,0,1,0-24-24A24,24,0,0,0,128,136Z',
  package: 'M223.68,66.15,135.68,18a15.88,15.88,0,0,0-15.36,0l-88,48.17a16,16,0,0,0-8.32,14v95.64a16,16,0,0,0,8.32,14l88,48.17a15.88,15.88,0,0,0,15.36,0l88-48.17a16,16,0,0,0,8.32-14V80.18A16,16,0,0,0,223.68,66.15ZM128,32l80.34,44-29.77,16.3-80.35-44ZM128,120,47.66,76l33.9-18.56,80.34,44ZM40,90l80,43.78v85.79L40,175.82Zm176,85.78h0l-80,43.79V133.82l32-17.51V152a8,8,0,0,0,16,0V107.55L216,90v85.77Z',
  pulse: 'M240,128a8,8,0,0,1-8,8H204.94l-37.78,75.58A8,8,0,0,1,160,216h-.4a8,8,0,0,1-7.08-5.14L95.35,60.76,63.28,131.31A8,8,0,0,1,56,136H24a8,8,0,0,1,0-16H50.85L88.72,36.69a8,8,0,0,1,14.76.46l57.51,151,31.85-63.71A8,8,0,0,1,200,120h32A8,8,0,0,1,240,128Z',
  lightning: 'M215.79,118.17a8,8,0,0,0-5-5.66L153.18,90.9l14.66-73.33a8,8,0,0,0-13.69-7l-112,120a8,8,0,0,0,3,13l57.63,21.61L88.16,238.43a8,8,0,0,0,13.69,7l112-120A8,8,0,0,0,215.79,118.17ZM109.37,214l10.47-52.38a8,8,0,0,0-5-9.06L62,132.71l84.62-90.66L136.16,94.43a8,8,0,0,0,5,9.06l52.8,19.8Z',
  target: 'M221.87,83.16A104.1,104.1,0,1,1,195.67,49l22.67-22.68a8,8,0,0,1,11.32,11.32l-96,96a8,8,0,0,1-11.32-11.32l27.72-27.72a40,40,0,1,0,17.87,31.09,8,8,0,1,1,16-.9,56,56,0,1,1-22.38-41.65L184.3,60.39a87.88,87.88,0,1,0,23.13,29.67,8,8,0,0,1,14.44-6.9Z',
  cpu: 'M152,96H104a8,8,0,0,0-8,8v48a8,8,0,0,0,8,8h48a8,8,0,0,0,8-8V104A8,8,0,0,0,152,96Zm-8,48H112V112h32Zm88,0H216V112h16a8,8,0,0,0,0-16H216V56a16,16,0,0,0-16-16H160V24a8,8,0,0,0-16,0V40H112V24a8,8,0,0,0-16,0V40H56A16,16,0,0,0,40,56V96H24a8,8,0,0,0,0,16H40v32H24a8,8,0,0,0,0,16H40v40a16,16,0,0,0,16,16H96v16a8,8,0,0,0,16,0V216h32v16a8,8,0,0,0,16,0V216h40a16,16,0,0,0,16-16V160h16a8,8,0,0,0,0-16Zm-32,56H56V56H200v95.87s0,.09,0,.13,0,.09,0,.13V200Z',
  arrowLeft: 'M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z',
  check: 'M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z',
  caret: 'M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z',
  lock: 'M208,80H176V56a48,48,0,0,0-96,0V80H48A16,16,0,0,0,32,96V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V96A16,16,0,0,0,208,80ZM96,56a32,32,0,0,1,64,0V80H96ZM208,208H48V96H208V208Z',
  dashed: 'M96.26,37.05A8,8,0,0,1,102,27.29a104.11,104.11,0,0,1,52,0,8,8,0,0,1-2,15.75,8.15,8.15,0,0,1-2-.26,88.09,88.09,0,0,0-44,0A8,8,0,0,1,96.26,37.05ZM53.79,55.14a104.05,104.05,0,0,0-26,45,8,8,0,0,0,15.42,4.27,88,88,0,0,1,22-38.09A8,8,0,0,0,53.79,55.14ZM43.21,151.55a8,8,0,1,0-15.42,4.28,104.12,104.12,0,0,0,26,45,8,8,0,0,0,11.41-11.22A88.14,88.14,0,0,1,43.21,151.55ZM150,213.22a88,88,0,0,1-44,0,8,8,0,1,0-4,15.49,104.11,104.11,0,0,0,52,0,8,8,0,0,0-4-15.49ZM222.65,146a8,8,0,0,0-9.85,5.58,87.91,87.91,0,0,1-22,38.08,8,8,0,1,0,11.42,11.21,104,104,0,0,0,26-45A8,8,0,0,0,222.65,146Zm-9.86-41.54a8,8,0,0,0,15.42-4.28,104,104,0,0,0-26-45,8,8,0,1,0-11.41,11.22A88,88,0,0,1,212.79,104.45Z',
  warnFill: 'M227.31,80.23,175.77,28.69A16.13,16.13,0,0,0,164.45,24H91.55a16.13,16.13,0,0,0-11.32,4.69L28.69,80.23A16.13,16.13,0,0,0,24,91.55v72.9a16.13,16.13,0,0,0,4.69,11.32l51.54,51.54A16.13,16.13,0,0,0,91.55,232h72.9a16.13,16.13,0,0,0,11.32-4.69l51.54-51.54A16.13,16.13,0,0,0,232,164.45V91.55A16.13,16.13,0,0,0,227.31,80.23ZM120,80a8,8,0,0,1,16,0v56a8,8,0,0,1-16,0Zm8,104a12,12,0,1,1,12-12A12,12,0,0,1,128,184Z',
  search: 'M229.66,218.34l-50.07-50.06a88.11,88.11,0,1,0-11.31,11.31l50.06,50.07a8,8,0,0,0,11.32-11.32ZM40,112a72,72,0,1,1,72,72A72.08,72.08,0,0,1,40,112Z',
  send: 'M231.87,114l-168-95.89A16,16,0,0,0,40.92,37.34L71.55,128,40.92,218.67A16,16,0,0,0,56,240a16.15,16.15,0,0,0,7.93-2.1l167.92-96.05a16,16,0,0,0,.05-27.89ZM56,224a.56.56,0,0,0,0-.12L85.74,136H144a8,8,0,0,0,0-16H85.74L56.06,32.16A.46.46,0,0,0,56,32l168,95.83Z',
  shield: 'M208,40H48A16,16,0,0,0,32,56v56c0,52.72,25.52,84.67,46.93,102.19,23.06,18.86,46,25.26,47,25.53a8,8,0,0,0,4.2,0c1-.27,23.91-6.67,47-25.53C198.48,196.67,224,164.72,224,112V56A16,16,0,0,0,208,40Zm0,72c0,37.07-13.66,67.16-40.6,89.42A129.3,129.3,0,0,1,128,223.62a128.25,128.25,0,0,1-38.92-21.81C61.82,179.51,48,149.3,48,112l0-56,160,0ZM82.34,141.66a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32l-56,56a8,8,0,0,1-11.32,0Z',
  bug: 'M144,92a12,12,0,1,1,12,12A12,12,0,0,1,144,92ZM100,80a12,12,0,1,0,12,12A12,12,0,0,0,100,80Zm116,64A87.76,87.76,0,0,1,213,167l22.24,9.72A8,8,0,0,1,232,192a7.89,7.89,0,0,1-3.2-.67L207.38,182a88,88,0,0,1-158.76,0L27.2,191.33A7.89,7.89,0,0,1,24,192a8,8,0,0,1-3.2-15.33L43,167A87.76,87.76,0,0,1,40,144v-8H16a8,8,0,0,1,0-16H40v-8a87.76,87.76,0,0,1,3-23L20.8,79.33a8,8,0,1,1,6.4-14.66L48.62,74a88,88,0,0,1,158.76,0l21.42-9.36a8,8,0,0,1,6.4,14.66L213,89.05a87.76,87.76,0,0,1,3,23v8h24a8,8,0,0,1,0,16H216ZM56,120H200v-8a72,72,0,0,0-144,0Zm64,95.54V136H56v8A72.08,72.08,0,0,0,120,215.54ZM200,144v-8H136v79.54A72.08,72.08,0,0,0,200,144Z',
  key: 'M216.57,39.43A80,80,0,0,0,83.91,120.78L28.69,176A15.86,15.86,0,0,0,24,187.31V216a16,16,0,0,0,16,16H72a8,8,0,0,0,8-8V208H96a8,8,0,0,0,8-8V184h16a8,8,0,0,0,5.66-2.34l9.56-9.57A79.73,79.73,0,0,0,160,176h.1A80,80,0,0,0,216.57,39.43ZM224,98.1c-1.09,34.09-29.75,61.86-63.89,61.9H160a63.7,63.7,0,0,1-23.65-4.51,8,8,0,0,0-8.84,1.68L116.69,168H96a8,8,0,0,0-8,8v16H72a8,8,0,0,0-8,8v16H40V187.31l58.83-58.82a8,8,0,0,0,1.68-8.84A63.72,63.72,0,0,1,96,95.92c0-34.14,27.81-62.8,61.9-63.89A64,64,0,0,1,224,98.1ZM192,76a12,12,0,1,1-12-12A12,12,0,0,1,192,76Z',
  code: 'M69.12,94.15,28.5,128l40.62,33.85a8,8,0,1,1-10.24,12.29l-48-40a8,8,0,0,1,0-12.29l48-40a8,8,0,0,1,10.24,12.3Zm176,27.7-48-40a8,8,0,1,0-10.24,12.3L227.5,128l-40.62,33.85a8,8,0,1,0,10.24,12.29l48-40a8,8,0,0,0,0-12.29ZM162.73,32.48a8,8,0,0,0-10.25,4.79l-64,176a8,8,0,0,0,4.79,10.26A8.14,8.14,0,0,0,96,224a8,8,0,0,0,7.52-5.27l64-176A8,8,0,0,0,162.73,32.48Z',
  chart: 'M232,208a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V48a8,8,0,0,1,16,0v94.37L90.73,98a8,8,0,0,1,10.07-.38l58.81,44.11L218.73,90a8,8,0,1,1,10.54,12l-64,56a8,8,0,0,1-10.07.38L96.39,114.29,40,163.63V200H224A8,8,0,0,1,232,208Z',
  scan: 'M224,40V80a8,8,0,0,1-16,0V48H176a8,8,0,0,1,0-16h40A8,8,0,0,1,224,40ZM80,208H48V176a8,8,0,0,0-16,0v40a8,8,0,0,0,8,8H80a8,8,0,0,0,0-16Zm136-40a8,8,0,0,0-8,8v32H176a8,8,0,0,0,0,16h40a8,8,0,0,0,8-8V176A8,8,0,0,0,216,168ZM40,88a8,8,0,0,0,8-8V48H80a8,8,0,0,0,0-16H40a8,8,0,0,0-8,8V80A8,8,0,0,0,40,88ZM80,72h96a8,8,0,0,1,8,8v96a8,8,0,0,1-8,8H80a8,8,0,0,1-8-8V80A8,8,0,0,1,80,72Zm8,96h80V88H88Z',
  monitor: 'M208,40H48A24,24,0,0,0,24,64V176a24,24,0,0,0,24,24H208a24,24,0,0,0,24-24V64A24,24,0,0,0,208,40Zm8,136a8,8,0,0,1-8,8H48a8,8,0,0,1-8-8V64a8,8,0,0,1,8-8H208a8,8,0,0,1,8,8Zm-48,48a8,8,0,0,1-8,8H96a8,8,0,0,1,0-16h64A8,8,0,0,1,168,224Z',
  play: 'M232.4,114.49,88.32,26.35a16,16,0,0,0-16.2-.3A15.86,15.86,0,0,0,64,39.87V216.13A15.94,15.94,0,0,0,80,232a16.07,16.07,0,0,0,8.36-2.35L232.4,141.51a15.81,15.81,0,0,0,0-27ZM80,215.94V40l143.83,88Z',
};

function svg(nombre, size) {
  const d = ICONOS[nombre];
  if (!d) return '';
  const s = size || 16;
  return '<svg viewBox="0 0 256 256" fill="currentColor" width="' + s + '" height="' + s +
    '" style="width:' + s + 'px;height:' + s + 'px"><path d="' + d + '"></path></svg>';
}

/* Rellena todo [data-icono] del HTML estático. */
function pintarIconos(raiz) {
  (raiz || document).querySelectorAll('[data-icono]').forEach(el => {
    const n = el.dataset.icono;
    if (el.querySelector('svg')) return;
    const size = el.classList.contains('rail-btn') ? 19
      : el.classList.contains('aria-icono') ? 16
      : el.classList.contains('deposito-icono') ? 22
      : el.classList.contains('ascenso-icono') ? 32
      : el.classList.contains('perfil-avatar') ? 38
      : 15;
    el.insertAdjacentHTML('afterbegin', svg(n, size));
  });
}

/* ═══════════════ MUNDO: sectores derivados de los bloques ═══════════════ */

const SECTOR_LORE = {
  'Fundamentos': ['INIT', 'Núcleo de datos', 'Variables, tipos y entrada/salida. El sector que mantiene vivo al resto del sistema.'],
  'Strings': ['TEXT', 'Sala de transcripción', 'Todo lo que el NEXUS lee, escribe y reporta pasa por acá antes de llegar a un operador.'],
  'Decisiones': ['LOGIC', 'Puerta de control', 'Condicionales y operadores lógicos: las decisiones que el sistema toma sin preguntarle a nadie.'],
  'Loops': ['LOOPS', 'Anillo de repetición', 'Cuando el anillo falla, cada tarea repetida del NEXUS —barridos, reintentos, filtros— se detiene.'],
  'Estructuras de datos': ['DATA', 'Bóveda de estructuras', 'Listas, diccionarios y matrices. Todo lo que el NEXUS recuerda vive acá.'],
  'Funciones': ['FORGE', 'Taller de rutinas', 'Rutinas reutilizables: lo que hoy escribís a mano, mañana el sistema lo invoca solo.'],
  'Archivos y errores': ['TRACE', 'Sala de registros', 'Archivos, JSON y excepciones. Es donde el sistema deja constancia de lo que salió mal.'],
  'OOP': ['OOP', 'Fundición de objetos', 'Clases, herencia y polimorfismo. Modelar el mundo para poder mantenerlo.'],
  'Casos reales': ['LIVE', 'Sistemas en producción', 'Proyectos completos. Acá el código lo usa alguien más, y por eso no puede fallar.'],
  'Algoritmos': ['ALGO', 'Forja algorítmica', 'Búsqueda, orden, recursión y complejidad. Donde se decide qué es rápido y qué no.'],
  'Datos y texto': ['PARSE', 'Estación de análisis', 'Expresiones regulares y fechas: extraer señal de la telemetría cruda del NEXUS.'],
  'Asincronía': ['ASYNC', 'Torre de concurrencia', 'Muchas tareas a la vez sin que ninguna bloquee al resto. El pulso del sistema.'],
  'Arquitectura y buenas prácticas': ['ARCH', 'Mesa de diseño', 'Patrones y principios. Lo que decide si el sistema sobrevive al próximo cambio.'],
  'Redes': ['NET', 'Nodo de enlace', 'Sockets y protocolos: cómo dos programas del NEXUS se hablan a distancia.'],
};

const RANGOS = [
  { nivel: 1, nombre: 'NOVATO', min: 0, nota: 'Primer contacto con el sistema' },
  { nivel: 2, nombre: 'CADETE', min: 200, nota: 'Acceso a los sectores base' },
  { nivel: 3, nombre: 'JUNIOR', min: 500, nota: 'Operaciones sin supervisión' },
  { nivel: 4, nombre: 'DEVELOPER', min: 1000, nota: 'Proyectos de sector' },
  { nivel: 5, nombre: 'PROGRAMADOR', min: 2000, nota: 'Rutinas críticas del NEXUS' },
  { nivel: 6, nombre: 'ENGINEER', min: 3000, nota: 'Sistemas en producción' },
  { nivel: 7, nombre: 'ARCHITECT', min: 4500, nota: 'Diseño del NEXUS' },
];

const LANG = {
  python: { nombre: 'Python', archivo: 'mision.py', ext: 'PY', placeholder: '# Escribí tu solución acá\n', total: 25 },
  javascript: { nombre: 'JavaScript', archivo: 'mision.js', ext: 'JS', placeholder: '// Escribí tu solución acá\n', total: 10 },
  cpp: { nombre: 'C++', archivo: 'mision.cpp', ext: 'CPP', placeholder: '// Escribí tu solución acá\n', total: 10 },
};

const SKILLS = [
  ['LOGIC', ['Decisiones', 'Loops', 'Fundamentos']],
  ['ALGORITHMS', ['Algoritmos']],
  ['DEBUGGING', ['Archivos y errores']],
  ['OOP', ['OOP']],
  ['DATA', ['Estructuras de datos', 'Datos y texto']],
  ['PROBLEM SOLVING', null],
  ['SYSTEM DESIGN', ['Arquitectura y buenas prácticas', 'Casos reales', 'Redes', 'Asincronía']],
];

const LECTURAS = [
  [/SyntaxError|expected|unexpected|parse error|error: expected/i, 'SYNTAX', 'El parser se detuvo acá, pero el problema casi siempre nace en la línea anterior: una sentencia quedó abierta.'],
  [/IndentationError|TabError/i, 'INDENT', 'El bloque no está alineado con su encabezado. En Python la indentación no es estética: es la estructura.'],
  [/NameError|is not defined|was not declared/i, 'NAME', 'El sistema buscó ese nombre y no existe todavía. Revisá si lo definiste antes de usarlo, y cómo lo escribiste.'],
  [/TypeError|no matching function/i, 'TYPE', 'La operación es válida, pero no para esos tipos. Mirá qué tipo llega realmente, no el que esperabas.'],
  [/ValueError|invalid literal/i, 'VALUE', 'El tipo es correcto pero el valor no. Suele venir de una conversión sobre datos que no validaste.'],
  [/IndexError|out of range|out of bounds/i, 'INDEX', 'Pediste una posición que la estructura no tiene. Contá desde 0 y revisá el límite del recorrido.'],
  [/KeyError/i, 'KEY', 'Esa clave no está en el diccionario. Verificá antes de leer, o usá un acceso con valor por defecto.'],
  [/ZeroDivisionError|division by zero/i, 'MATH', 'Una división llegó a cero. Es una guarda que falta antes de la operación.'],
  [/AttributeError/i, 'ATTR', 'El objeto existe pero no tiene ese atributo. Puede ser otro tipo del que creés.'],
  [/RecursionError|stack overflow/i, 'RECUR', 'La recursión no encontró su caso base. Definí primero cuándo tiene que dejar de llamarse.'],
  [/TimeoutError|timeout|tiempo/i, 'TIMEOUT', 'El proceso no terminó en el tiempo permitido. Buscá el bucle cuya condición de salida nunca se cumple.'],
];

const CONSEJOS = [
  'Leé el traceback de abajo hacia arriba: la última línea dice qué pasó, las de arriba dicen dónde empezó.',
  'Un error de sintaxis se reporta donde el parser se rinde, no donde te equivocaste.',
  'Antes de escribir código, escribí en una línea qué tiene que devolver. Si no podés, todavía no entendés el problema.',
  'Ejecutá a medias y seguido. Un programa entero escrito antes de la primera corrida es un programa entero para depurar.',
  'Nombrar bien una variable te ahorra tres comentarios y una relectura.',
  'Volvé mañana aunque sea diez minutos: la continuidad vale más que la sesión maratónica.',
];

/* ═══════════════ ESTADO ═══════════════ */

const estado = {
  pantalla: 'nexus',
  lang: 'python',
  progreso: { python: [], javascript: [], cpp: [], xp: 0, nivel: 1, nivel_info: {}, racha: 0, mejor_racha: 0, proyectos: {}, proyectos_pasos: {} },
  modulos: [],
  sectores: [],
  sector: null,
  modulo: null,
  proyectosLista: [],
  proyecto: null,
  modoIDE: 'nivel', // 'nivel' | 'proyecto'
  tienda: null,
  tab: 'ejercicio',
  vista: 'salida',
  iaActiva: false,
  iaOcupada: false,
  corriendo: false,
  consejo: 0,
  ultimoError: null,
  erroresResueltos: Number(localStorage.getItem('cp_errores') || 0), // LOCAL
};

/* ═══════════════ ARRANQUE ═══════════════ */

document.addEventListener('DOMContentLoaded', async () => {
  pintarIconos();
  conectarUI();
  fondoAnimado();
  await cargarProgreso();
  await verificarIA();
  await cargarLenguaje('python');
  nuevoConsejo();
});

function conectarUI() {
  document.querySelectorAll('[data-pantalla]').forEach(b => {
    b.addEventListener('click', () => irA(b.dataset.pantalla));
  });
  document.querySelectorAll('#seg-lenguajes .seg-opt').forEach(b => {
    b.addEventListener('click', () => cambiarLenguaje(b.dataset.lang));
  });
  document.getElementById('btn-consejo').addEventListener('click', nuevoConsejo);
  document.getElementById('btn-volver-mapa').addEventListener('click', cerrarIDE);
  document.getElementById('btn-pista').addEventListener('click', togglePista);
  document.getElementById('btn-limpiar').addEventListener('click', () => {
    const c = document.getElementById('code');
    c.value = '';
    sincronizarGutter();
    c.focus();
  });
  document.getElementById('btn-correr').addEventListener('click', ejecutar);
  document.getElementById('btn-completar').addEventListener('click', completarModulo);
  document.getElementById('btn-analizar').addEventListener('click', analizarError);
  document.getElementById('btn-ir-linea').addEventListener('click', irALinea);
  document.getElementById('btn-enviar').addEventListener('click', preguntarIA);
  document.getElementById('pregunta').addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); preguntarIA(); }
  });

  document.querySelectorAll('#terminal-tabs .mini-opt').forEach(b => {
    b.addEventListener('click', () => cambiarVista(b.dataset.vista));
  });
  document.querySelectorAll('#brief-tabs .mini-opt').forEach(b => {
    b.addEventListener('click', () => cambiarTab(b.dataset.tab));
  });

  document.getElementById('btn-splash-empezar').addEventListener('click', () => {
    document.getElementById('splash').classList.add('oculta');
    document.getElementById('app').classList.remove('oculta');
  });

  document.getElementById('brief-cerrar').addEventListener('click', cerrarBriefing);
  document.getElementById('briefing').addEventListener('click', e => {
    if (e.target.id === 'briefing') cerrarBriefing();
  });
  document.getElementById('brief-empezar').addEventListener('click', () => {
    cerrarBriefing();
    abrirIDENivel();
  });
  document.getElementById('ascenso-cerrar').addEventListener('click', () => {
    document.getElementById('ascenso').classList.add('oculta');
  });

  document.getElementById('estacion-modal').addEventListener('click', e => {
    if (e.target.id === 'estacion-modal') cerrarIDE();
  });

  document.getElementById('py-cerrar').addEventListener('click', cerrarProyectoDetalle);
  document.getElementById('proyecto-detalle').addEventListener('click', e => {
    if (e.target.id === 'proyecto-detalle') cerrarProyectoDetalle();
  });
  document.getElementById('py-abrir-ide').addEventListener('click', abrirIDEProyecto);
  document.getElementById('py-completar').addEventListener('click', completarProyecto);

  const code = document.getElementById('code');
  code.addEventListener('input', sincronizarGutter);
  code.addEventListener('scroll', () => {
    document.getElementById('gutter').scrollTop = code.scrollTop;
  });
  code.addEventListener('keydown', e => {
    if (e.key !== 'Tab') return;
    e.preventDefault();
    const t = e.target, i = t.selectionStart;
    t.value = t.value.slice(0, i) + '    ' + t.value.slice(t.selectionEnd);
    t.selectionStart = t.selectionEnd = i + 4;
    sincronizarGutter();
  });

  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    cerrarBriefing();
    cerrarProyectoDetalle();
    cerrarIDE();
    document.getElementById('ascenso').classList.add('oculta');
  });
}

/* ═══════════════ NAVEGACIÓN ═══════════════ */

function irA(pantalla) {
  estado.pantalla = pantalla;
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('activa'));
  document.getElementById('screen-' + pantalla).classList.add('activa');
  document.querySelectorAll('.rail-btn').forEach(b => b.classList.toggle('activo', b.dataset.pantalla === pantalla));
  window.scrollTo(0, 0);

  if (pantalla === 'deposito') cargarDeposito();
  if (pantalla === 'perfil') renderPerfil();
  if (pantalla === 'proyectos') renderProyectos();
  actualizarCabecera();
}

async function cambiarLenguaje(lang) {
  if (lang === estado.lang) return;
  document.querySelectorAll('#seg-lenguajes .seg-opt').forEach(b => b.classList.toggle('activo', b.dataset.lang === lang));
  await cargarLenguaje(lang);
  irA(estado.pantalla === 'proyectos' ? 'proyectos' : 'nexus');
}

async function cargarLenguaje(lang) {
  estado.lang = lang;
  estado.sector = null;
  try {
    estado.modulos = await api('/api/modulos/' + lang);
  } catch (e) {
    estado.modulos = [];
    aviso('No pude conectar con el NEXUS. ¿Está corriendo el backend?', true);
  }
  try {
    estado.proyectosLista = await api('/api/proyectos/' + lang);
  } catch (e) {
    estado.proyectosLista = [];
  }
  construirSectores();
  renderMapa();
  actualizarCabecera();
}

/* ═══════════════ PROGRESO ═══════════════ */

async function cargarProgreso() {
  try { estado.progreso = await api('/api/progreso'); } catch (e) { /* offline */ }
  actualizarSplashContinuar();
}

function actualizarSplashContinuar() {
  const el = document.getElementById('splash-continuar');
  if (!el) return;
  const xp = estado.progreso.xp || 0;
  if (xp > 0) {
    const r = rangoDe(xp);
    texto('splash-continuar', 'Continuás como ' + r.nombre + ' · ' + xp.toLocaleString('es-AR') + ' XP');
    el.classList.remove('oculta');
  } else {
    el.classList.add('oculta');
  }
}

function hechos() { return estado.progreso[estado.lang] || []; }

function rangoDe(xp) {
  let r = RANGOS[0];
  RANGOS.forEach(x => { if (xp >= x.min) r = x; });
  return r;
}

function actualizarCabecera() {
  const p = estado.progreso;
  const xp = p.xp || 0;
  const r = rangoDe(xp);
  const sig = RANGOS.find(x => x.min > xp);
  const pct = sig ? Math.round(((xp - r.min) / (sig.min - r.min)) * 100) : 100;
  const dosD = n => String(n).padStart(2, '0');

  texto('hud-xp', xp.toLocaleString('es-AR'));
  texto('hud-racha', p.racha || 0);
  texto('hud-rango', r.nombre + ' · LVL ' + dosD(r.nivel));
  texto('hud-falta', sig ? (sig.min - xp) + ' XP → ' + sig.nombre : 'RANGO MÁXIMO');
  document.getElementById('hud-fill').style.width = pct + '%';
  texto('rail-nivel', dosD(r.nivel));
  texto('rail-rango', r.nombre);

  const activos = estado.sectores.filter(s => s.abierto).length;
  const integridad = integridadGlobal();
  const proyectosHechos = (p.proyectos && p.proyectos[estado.lang]) || [];

  const titulos = {
    nexus: 'MAPA · sistemas del NEXUS',
    proyectos: 'PROYECTOS · ' + LANG[estado.lang].nombre,
    perfil: 'Expediente del operador',
    deposito: 'Depósito de requisiciones',
  };
  const subs = {
    nexus: activos + ' activos · ' + (estado.sectores.length - activos) + ' bloqueados · integridad ' + integridad + '%',
    proyectos: proyectosHechos.length + ' / ' + estado.proyectosLista.length + ' completados',
    perfil: 'RANGO ' + r.nombre + ' · ' + xp.toLocaleString('es-AR') + ' XP · RACHA ' + (p.racha || 0) + ' DÍAS',
    deposito: 'XP DISPONIBLE ' + xp.toLocaleString('es-AR'),
  };
  texto('pantalla-titulo', titulos[estado.pantalla]);
  texto('pantalla-subtitulo', subs[estado.pantalla]);

  const punto = document.getElementById('estado-punto');
  punto.className = 'estado-punto' + (estado.pantalla === 'nexus' && integridad < 60 ? ' warn' : '');
}

/* ═══════════════ SECTORES ═══════════════ */

function construirSectores() {
  const grupos = [];
  const idx = {};
  estado.modulos.forEach(m => {
    const b = m.bloque || 'Sistema';
    if (idx[b] == null) { idx[b] = grupos.length; grupos.push({ bloque: b, modulos: [] }); }
    grupos[idx[b]].modulos.push(m);
  });

  const hs = hechos();
  const primerPendiente = (estado.modulos.find(m => !hs.includes(m.id)) || {}).id;

  estado.sectores = grupos.map((g, i) => {
    const lore = SECTOR_LORE[g.bloque] || [sigla(g.bloque), g.bloque, 'Un sector del NEXUS que depende de este conjunto de rutinas.'];
    const cerradas = g.modulos.filter(m => hs.includes(m.id)).length;
    const integridad = Math.round((cerradas / g.modulos.length) * 100);
    const primerId = g.modulos[0].id;
    const abierto = primerId === 1 || hs.includes(primerId - 1) || cerradas > 0;
    const tieneActual = g.modulos.some(m => m.id === primerPendiente);

    return {
      id: 'S' + (i + 1),
      codigo: 'S-' + String(i + 1).padStart(2, '0'),
      sigla: lore[0],
      nombre: lore[1],
      resumen: lore[2],
      bloque: g.bloque,
      modulos: g.modulos,
      cerradas: cerradas,
      integridad: integridad,
      abierto: abierto,
      alerta: tieneActual,
      estado: !abierto ? 'BLOQUEADO' : integridad === 100 ? 'ESTABLE' : integridad >= 50 ? 'DEGRADADO' : integridad > 0 ? 'INESTABLE' : 'CAÍDO',
    };
  });

  if (!estado.sector || !estado.sectores.some(s => s.id === estado.sector)) {
    const act = estado.sectores.find(s => s.alerta) || estado.sectores[0];
    estado.sector = act ? act.id : null;
  }
}

function sigla(txt) {
  return String(txt).replace(/[^A-Za-zÁÉÍÓÚÑáéíóúñ ]/g, '').trim().split(/\s+/)[0].toUpperCase().slice(0, 5);
}

function colorEstado(s) {
  return s.estado === 'ESTABLE' ? 'var(--ok)'
    : s.estado === 'DEGRADADO' ? 'var(--warn)'
    : s.estado === 'INESTABLE' || s.estado === 'CAÍDO' ? 'var(--err)'
    : 'var(--faint)';
}

function integridadGlobal() {
  if (!estado.modulos.length) return 0;
  return Math.round((hechos().length / estado.modulos.length) * 100);
}

/* ═══════════════ MAPA ═══════════════ */

function renderMapa() {
  const nodos = document.getElementById('mapa-nodos');
  const svgEl = document.getElementById('mapa-svg');
  const n = estado.sectores.length;

  if (!n) {
    nodos.innerHTML = '<p class="muted" style="padding:22px">No hay sectores para este lenguaje todavía.</p>';
    svgEl.innerHTML = '';
    renderLateral();
    return;
  }

  /* Serpentina de 3 columnas: robusta para 4–14 sectores. */
  const cols = n <= 4 ? 2 : 3;
  const filas = Math.ceil(n / cols);
  const alto = Math.max(360, filas * 118 + 40);
  document.getElementById('mapa').style.height = alto + 'px';
  svgEl.setAttribute('viewBox', '0 0 900 ' + alto);

  const pos = estado.sectores.map((s, i) => {
    const fila = Math.floor(i / cols);
    let col = i % cols;
    if (fila % 2 === 1) col = cols - 1 - col;
    const xPct = cols === 2 ? [26, 74][col] : [17, 50, 83][col];
    const y = 26 + fila * 118;
    return { x: (xPct / 100) * 900, y: y + 46, xPct: xPct, yPx: y };
  });

  svgEl.innerHTML = estado.sectores.slice(0, -1).map((s, i) => {
    const a = pos[i], b = pos[i + 1];
    const viva = s.integridad > 0 && estado.sectores[i + 1].abierto;
    return '<path d="M ' + a.x.toFixed(0) + ' ' + a.y + ' L ' + b.x.toFixed(0) + ' ' + b.y + '" fill="none" stroke="' +
      (viva ? 'rgba(145,132,217,.55)' : 'rgba(89,93,108,.32)') + '" stroke-width="' + (viva ? 1.4 : 1) +
      '" stroke-dasharray="' + (viva ? 'none' : '3 6') + '"></path>';
  }).join('');

  nodos.innerHTML = estado.sectores.map((s, i) => {
    const p = pos[i];
    const cls = 'sector' + (s.id === estado.sector ? ' activo' : '') + (s.abierto ? '' : ' bloqueado') +
      (s.alerta && s.id !== estado.sector ? ' alerta' : '');
    return '<button class="' + cls + '" data-sector="' + s.id + '" style="left:' + p.xPct + '%;top:' + p.yPx + 'px">' +
      '<span class="sector-top">' +
        '<span class="sector-led" style="background:' + colorEstado(s) + '"></span>' +
        '<span>' + s.codigo + '</span><span class="sector-sigla">' + escapar(s.sigla) + '</span>' +
        '<span class="sector-pct">' + s.integridad + '%</span>' +
      '</span>' +
      '<span class="sector-nombre">' + escapar(s.nombre) + '</span>' +
      '<span class="sector-estado">' + s.estado + '</span>' +
      '<span class="barra"><span class="barra-fill" style="width:' + s.integridad + '%;background:' + colorEstado(s) + '"></span></span>' +
    '</button>';
  }).join('');

  nodos.querySelectorAll('[data-sector]').forEach(b => {
    b.addEventListener('click', () => {
      const s = estado.sectores.find(x => x.id === b.dataset.sector);
      if (!s.abierto) { aviso('Estabilizá el sector anterior para habilitar este', true); return; }
      estado.sector = s.id;
      renderMapa();
    });
  });

  texto('mapa-integridad', 'INTEGRIDAD GLOBAL ' + integridadGlobal() + '%');
  renderHud();
  renderLateral();
}

function renderHud() {
  const alerta = estado.sectores.find(s => s.alerta && s.integridad < 100);
  const cofres = Math.floor(hechos().length / 5); // LOCAL: cachés cada 5 operaciones
  document.getElementById('hud-mapa').innerHTML = [
    ['ALERTA ACTIVA', alerta ? alerta.sigla : 'NINGUNA',
      alerta ? 'Sector ' + alerta.estado.toLowerCase() + ' · ' + alerta.integridad + '% de integridad' : 'Todos los sectores estables',
      alerta ? 'var(--err)' : 'var(--ok)'],
    ['OPERACIONES CERRADAS', hechos().length + ' / ' + estado.modulos.length,
      LANG[estado.lang].nombre + ' · ' + estado.sectores.length + ' sectores', 'var(--text)'],
    ['CACHÉS DE DATOS', String(cofres),
      'Se abre uno cada 5 operaciones cerradas', 'var(--accent-400)'],
  ].map(([label, valor, nota, color]) =>
    '<div class="hud-card"><span class="kicker">' + label + '</span>' +
    '<strong style="color:' + color + '">' + escapar(valor) + '</strong>' +
    '<span>' + escapar(nota) + '</span></div>').join('');
}

function renderLateral() {
  const s = estado.sectores.find(x => x.id === estado.sector);
  if (!s) return;

  texto('sector-codigo', s.codigo + ' · ' + s.sigla);
  texto('sector-titulo', s.nombre);
  texto('sector-resumen', s.resumen);

  const hs = hechos();
  const primerPendiente = (estado.modulos.find(m => !hs.includes(m.id)) || {}).id;

  document.getElementById('operaciones').innerHTML = s.modulos.map((m, i) => {
    const cerrada = hs.includes(m.id);
    const abierta = m.id === 1 || hs.includes(m.id - 1);
    const curso = m.id === primerPendiente;
    const cls = cerrada ? 'cerrada' : curso ? 'curso' : abierta ? 'abierta' : 'bloqueada';
    const ic = cerrada ? 'check' : curso ? 'caret' : abierta ? 'dashed' : 'lock';
    return '<button class="op ' + cls + '" data-modulo="' + m.id + '">' +
      '<span class="op-icono">' + svg(ic, 12) + '</span>' +
      '<span class="op-cuerpo">' +
        '<span class="op-meta">' + codigoOp(s, i) +
          '<span class="op-premio">' + (cerrada ? 'CERRADA' : '+' + m.xp + ' XP') + '</span></span>' +
        '<span class="op-nombre">' + escapar(m.titulo) + '</span>' +
        '<span class="op-concepto">' + escapar(m.descripcion) + '</span>' +
      '</span></button>';
  }).join('');

  document.querySelectorAll('#operaciones [data-modulo]').forEach(b => {
    b.addEventListener('click', () => {
      if (b.classList.contains('bloqueada')) { aviso('Cerrá la operación anterior para abrir esta', true); return; }
      abrirBriefing(Number(b.dataset.modulo));
    });
  });

  const hoy = Math.min(hs.length, 2);
  texto('directiva-progreso', hoy + ' / 2 CERRADAS');
  document.getElementById('directiva-fill').style.width = (hoy / 2) * 100 + '%';
}

function codigoOp(sector, i) {
  return 'OP-' + sector.sigla.slice(0, 2) + String(i + 1).padStart(2, '0');
}

function nuevoConsejo() {
  estado.consejo = (estado.consejo + 1) % CONSEJOS.length;
  texto('aria-consejo', CONSEJOS[estado.consejo]);
}

/* ═══════════════ BRIEFING ═══════════════ */

function sectorDe(id) {
  return estado.sectores.find(s => s.modulos.some(m => m.id === id));
}

function abrirBriefing(id) {
  const m = estado.modulos.find(x => x.id === id);
  if (!m) return;
  const s = sectorDe(id);
  const i = s.modulos.findIndex(x => x.id === id);

  estado.modulo = Object.assign({}, m, { sector: s, codigo: codigoOp(s, i) });
  estado.tab = 'ejercicio';

  const hs = hechos();
  const primerPendiente = (estado.modulos.find(x => !hs.includes(x.id)) || {}).id;
  const prioridad = hs.includes(id) ? 'BAJA' : id === primerPendiente ? 'ALTA' : 'MEDIA';

  texto('brief-codigo', estado.modulo.codigo);
  texto('brief-prioridad', 'PRIORIDAD ' + prioridad);
  texto('brief-titulo', m.titulo);
  texto('brief-contexto', s.resumen + ' Esta operación cubre una rutina puntual del sector: ' +
    m.descripcion.charAt(0).toLowerCase() + m.descripcion.slice(1) + '.');
  texto('brief-consecuencia', 'El sector ' + s.sigla + ' queda al ' + s.integridad +
    '% de integridad y las operaciones que dependen de esta rutina no pueden ejecutarse.');
  texto('brief-recompensa', '+' + m.xp + ' XP · ' + s.sigla + ' +1');

  document.getElementById('brief-datos').innerHTML = [
    ['SECTOR', s.codigo + ' ' + s.sigla, ''],
    ['INTEGRIDAD', s.integridad + '%', s.integridad < 30 ? 'err' : s.integridad < 70 ? 'warn' : ''],
    ['OPERACIÓN', (i + 1) + ' DE ' + s.modulos.length, ''],
  ].map(([l, v, cls]) => '<div class="brief-dato ' + cls + '"><span class="kicker">' + l + '</span><span>' + escapar(v) + '</span></div>').join('');

  document.getElementById('brief-objetivos').innerHTML = (m.ejercicio || '')
    .split('\n')
    .map(l => l.replace(/^[•\-\*\s]+/, '').trim())
    .filter(l => l.length > 3)
    .slice(0, 4)
    .map((l, k) => '<div class="brief-obj"><span>' + String(k + 1).padStart(2, '0') + '</span><span>' + escapar(l) + '</span></div>')
    .join('') || '<div class="brief-obj"><span>01</span><span>' + escapar(m.descripcion) + '</span></div>';

  document.getElementById('brief-conceptos').innerHTML =
    conceptosDe(m).map(c => '<span class="chip fuerte">' + escapar(c) + '</span>').join('');

  cambiarTab('ejercicio');
  document.getElementById('briefing').classList.remove('oculta');
  document.body.style.overflow = 'hidden';
  pintarIconos(document.getElementById('briefing'));
}

function conceptosDe(m) {
  const base = String(m.titulo).toLowerCase().split(/[\s,/·]+/).filter(w => w.length > 3).slice(0, 3);
  return base.length ? base : [m.bloque.toLowerCase()];
}

function cambiarTab(tab) {
  estado.tab = tab;
  const m = estado.modulo;
  if (!m) return;
  document.querySelectorAll('#brief-tabs .mini-opt').forEach(b => b.classList.toggle('activo', b.dataset.tab === tab));
  const pre = document.getElementById('brief-contenido');
  pre.textContent = tab === 'teoria' ? (m.teoria || '') : tab === 'ejemplo' ? (m.ejemplo || '') : (m.ejercicio || '');
}

function cerrarBriefing() {
  document.getElementById('briefing').classList.add('oculta');
  document.body.style.overflow = '';
}

/* ═══════════════ PROYECTOS ═══════════════ */

function proyectosHechosLang() {
  return (estado.progreso.proyectos && estado.progreso.proyectos[estado.lang]) || [];
}

function renderProyectos() {
  const lista = estado.proyectosLista || [];
  const hechos = proyectosHechosLang();
  texto('proyectos-resumen', hechos.length + ' / ' + lista.length + ' COMPLETADOS');

  const cont = document.getElementById('proyectos-lista');
  if (!lista.length) {
    cont.innerHTML = '<p class="muted" style="padding:22px">No hay proyectos cargados para este lenguaje todavía.</p>';
    return;
  }

  cont.innerHTML = lista.map(py => {
    const hecho = hechos.includes(py.id);
    const clave = estado.lang + '_' + py.id;
    const pasosHechos = ((estado.progreso.proyectos_pasos || {})[clave] || []).length;
    const totalPasos = (py.pasos || []).length;
    return '<article class="proyecto-card' + (hecho ? ' hecho' : '') + '" data-proyecto="' + py.id + '">' +
      '<div class="proyecto-card-top">' +
        '<span class="tag' + (hecho ? ' tag-ok' : ' tag-acento') + '">' + (hecho ? 'COMPLETADO' : py.dificultad || 'PROYECTO') + '</span>' +
      '</div>' +
      '<strong>' + escapar(py.titulo) + '</strong>' +
      '<p>' + escapar(py.descripcion || '') + '</p>' +
      '<div class="proyecto-card-pie">' +
        '<span>' + totalPasos + ' pasos · ' + pasosHechos + ' marcados</span>' +
        '<span class="acento">+' + py.xp + ' XP</span>' +
      '</div>' +
    '</article>';
  }).join('');

  cont.querySelectorAll('[data-proyecto]').forEach(el => {
    el.addEventListener('click', () => abrirProyecto(Number(el.dataset.proyecto)));
  });
}

function abrirProyecto(id) {
  const py = (estado.proyectosLista || []).find(p => p.id === id);
  if (!py) return;
  estado.proyecto = py;

  const hecho = proyectosHechosLang().includes(py.id);
  const clave = estado.lang + '_' + py.id;
  const pasosHechos = new Set((estado.progreso.proyectos_pasos || {})[clave] || []);

  texto('py-dificultad', py.dificultad || '—');
  texto('py-tiempo', py.tiempo_estimado || '');
  texto('py-titulo', py.titulo);
  texto('py-objetivo', py.objetivo || py.descripcion || '');
  texto('py-recompensa', '+' + py.xp + ' XP');

  document.getElementById('py-pasos').innerHTML = (py.pasos || []).map((paso, i) => {
    const marcado = pasosHechos.has(i);
    return '<button class="py-paso' + (marcado ? ' hecho' : '') + '" data-paso="' + i + '">' +
      '<span class="py-paso-check">' + svg(marcado ? 'check' : 'dashed', 14) + '</span>' +
      '<span class="py-paso-cuerpo">' +
        '<span class="py-paso-titulo">' + escapar(paso.titulo) + '</span>' +
        '<span class="py-paso-desc">' + escapar(paso.descripcion || '') + '</span>' +
        (paso.pista ? '<span class="py-paso-pista">' + svg('search', 11) + ' ' + escapar(paso.pista) + '</span>' : '') +
      '</span></button>';
  }).join('') || '<p class="muted">Este proyecto no tiene pasos detallados.</p>';

  document.getElementById('py-pasos').querySelectorAll('[data-paso]').forEach(b => {
    b.addEventListener('click', () => toggleProyectoPaso(Number(b.dataset.paso)));
  });

  document.getElementById('py-conceptos').innerHTML =
    (py.conceptos || []).map(c => '<span class="chip fuerte">' + escapar(c) + '</span>').join('');

  document.getElementById('py-requisitos').innerHTML =
    (py.requisitos || []).map(r => '<div>· ' + escapar(r) + '</div>').join('') || 'Sin requisitos previos registrados.';

  const btnCompletar = document.getElementById('py-completar');
  const todoMarcado = (py.pasos || []).length > 0 && (py.pasos || []).every((_, i) => pasosHechos.has(i));
  btnCompletar.disabled = hecho || !todoMarcado;
  btnCompletar.innerHTML = svg('check', 14) + (hecho ? ' YA COMPLETADO' : ' MARCAR COMO COMPLETADO');
  btnCompletar.title = !hecho && !todoMarcado ? 'Marcá todos los pasos antes de cerrar el proyecto' : '';

  document.getElementById('proyecto-detalle').classList.remove('oculta');
  document.body.style.overflow = 'hidden';
  pintarIconos(document.getElementById('proyecto-detalle'));
}

function cerrarProyectoDetalle() {
  document.getElementById('proyecto-detalle').classList.add('oculta');
  document.body.style.overflow = '';
}

async function toggleProyectoPaso(index) {
  const py = estado.proyecto;
  if (!py) return;
  const clave = estado.lang + '_' + py.id;
  const actuales = new Set((estado.progreso.proyectos_pasos || {})[clave] || []);
  const completado = !actuales.has(index);

  try {
    const d = await api('/api/proyectos/paso', 'POST', {
      lenguaje: estado.lang, proyecto_id: py.id, paso_index: index, completado: completado,
    });
    estado.progreso.proyectos_pasos = Object.assign({}, estado.progreso.proyectos_pasos, { [clave]: d.pasos_completados });
    abrirProyecto(py.id);
    renderProyectos();
  } catch (e) {
    aviso('No pude guardar el paso', true);
  }
}

async function completarProyecto() {
  const py = estado.proyecto;
  if (!py) return;
  try {
    const data = await api('/api/proyectos/completar', 'POST', { lenguaje: estado.lang, proyecto_id: py.id });
    if (data.ya_estaba) { aviso('Este proyecto ya estaba completado'); return; }

    const antes = rangoDe(estado.progreso.xp || 0).nivel;

    estado.progreso = Object.assign({}, estado.progreso, {
      xp: data.xp_total,
      nivel: data.nivel_info.nivel,
      nivel_info: data.nivel_info,
      racha: data.racha,
      mejor_racha: data.mejor_racha,
      proyectos: Object.assign({}, estado.progreso.proyectos, { [estado.lang]: data.completados }),
    });

    aviso('Proyecto completado · +' + (data.xp_total_ganado || data.xp_ganado) + ' XP');
    cerrarProyectoDetalle();
    renderProyectos();
    actualizarCabecera();

    if (data.nivel_info.nivel > antes) mostrarAscenso(data.nivel_info);
  } catch (e) {
    aviso('No pude registrar el proyecto en el sistema', true);
  }
}

/* ═══════════════ IDE (overlay de trabajo) ═══════════════ */

function mostrarIDE() {
  document.getElementById('estacion-modal').classList.remove('oculta');
  document.body.style.overflow = 'hidden';
  pintarIconos(document.getElementById('estacion-modal'));
}

function cerrarIDE() {
  document.getElementById('estacion-modal').classList.add('oculta');
  document.body.style.overflow = '';
  if (estado.modoIDE === 'proyecto' && estado.proyecto) {
    abrirProyecto(estado.proyecto.id);
  }
}

function abrirIDENivel() {
  const m = estado.modulo;
  if (!m) return;
  estado.modoIDE = 'nivel';
  document.getElementById('btn-completar').classList.remove('oculta');

  const cerrada = hechos().includes(m.id);

  texto('op-codigo', m.sector.sigla + ' · ' + m.codigo);
  texto('op-titulo', m.titulo);
  texto('op-contexto', m.descripcion);
  texto('op-recompensa', '+' + m.xp + ' XP · ' + m.sector.sigla + ' +1');
  document.getElementById('op-estado').textContent = cerrada ? 'CERRADA' : 'EN CURSO';
  document.getElementById('op-estado').className = 'tag ' + (cerrada ? 'tag-ok' : 'tag-acento');

  document.getElementById('op-objetivos').innerHTML = (m.ejercicio || '')
    .split('\n')
    .map(l => l.replace(/^[•\-\*\s]+/, '').trim())
    .filter(l => l.length > 3)
    .slice(0, 5)
    .map((l, i) => '<div class="objetivo ' + (i === 0 ? 'activo' : '') + '">' +
      svg(i === 0 ? 'dashed' : 'dashed', 15) + '<span>' + escapar(l) + '</span></div>')
    .join('') || '<div class="objetivo activo">' + svg('dashed', 15) + '<span>' + escapar(m.descripcion) + '</span></div>';

  document.getElementById('op-conceptos').innerHTML =
    conceptosDe(m).map(c => '<span class="chip">' + escapar(c) + '</span>').join('');

  texto('op-pista', m.pista || 'Esta operación no tiene lectura previa. Corré el código y leé lo que devuelve el sistema.');
  document.getElementById('op-pista').classList.add('oculta');
  document.getElementById('btn-pista').innerHTML = svg('search', 15) + ' VER LA LECTURA DE ARIA';

  texto('code-archivo', LANG[estado.lang].archivo);
  texto('code-lang', LANG[estado.lang].ext);
  const code = document.getElementById('code');
  code.value = LANG[estado.lang].placeholder;
  sincronizarGutter();

  estado.ultimoError = null;
  estado.vista = 'salida';
  cambiarVista('salida');
  document.getElementById('panel-error').classList.add('oculta');
  terminal([['> ide listo. ejecutá cuando quieras_', 'dim']]);
  marcarBuild('espera');

  const btn = document.getElementById('btn-completar');
  btn.disabled = cerrada;
  btn.innerHTML = svg('check', 14) + (cerrada ? ' YA CERRADA' : ' VALIDAR');

  reiniciarChat();
  mostrarIDE();
}

function abrirIDEProyecto() {
  const py = estado.proyecto;
  if (!py) return;
  estado.modoIDE = 'proyecto';
  estado.modulo = null;
  document.getElementById('btn-completar').classList.add('oculta');

  const completado = ((estado.progreso.proyectos || {})[estado.lang] || []).includes(py.id);
  const clave = estado.lang + '_' + py.id;
  const pasosHechos = new Set((estado.progreso.proyectos_pasos || {})[clave] || []);

  texto('op-codigo', 'PROYECTO · ' + LANG[estado.lang].nombre);
  texto('op-titulo', py.titulo);
  texto('op-contexto', py.objetivo || py.descripcion || '');
  texto('op-recompensa', '+' + py.xp + ' XP');
  document.getElementById('op-estado').textContent = completado ? 'COMPLETADO' : 'EN CURSO';
  document.getElementById('op-estado').className = 'tag ' + (completado ? 'tag-ok' : 'tag-acento');

  document.getElementById('op-objetivos').innerHTML = (py.pasos || [])
    .map((paso, i) => '<div class="objetivo ' + (pasosHechos.has(i) ? 'hecho' : '') + '">' +
      svg('dashed', 15) + '<span>' + escapar(paso.titulo) + '</span></div>')
    .join('') || '<div class="objetivo">' + svg('dashed', 15) + '<span>' + escapar(py.descripcion || '') + '</span></div>';

  document.getElementById('op-conceptos').innerHTML =
    (py.conceptos || []).map(c => '<span class="chip">' + escapar(c) + '</span>').join('');

  const pistas = (py.pasos || []).map((p, i) => p.pista ? ((i + 1) + ') ' + p.pista) : null).filter(Boolean);
  texto('op-pista', pistas.length ? pistas.join('  ') : 'Este proyecto no tiene lecturas adicionales: revisá los pasos en el detalle del proyecto.');
  document.getElementById('op-pista').classList.add('oculta');

  texto('code-archivo', LANG[estado.lang].archivo);
  texto('code-lang', LANG[estado.lang].ext);
  const code = document.getElementById('code');
  code.value = LANG[estado.lang].placeholder;
  sincronizarGutter();

  estado.ultimoError = null;
  estado.vista = 'salida';
  cambiarVista('salida');
  document.getElementById('panel-error').classList.add('oculta');
  terminal([['> ide listo. ejecutá cuando quieras_', 'dim']]);
  marcarBuild('espera');

  document.getElementById('btn-pista').innerHTML = svg('search', 15) + ' VER PISTAS DE LOS PASOS';
  reiniciarChat();
  mostrarIDE();
}

function sincronizarGutter() {
  const code = document.getElementById('code');
  const n = code.value.split('\n').length;
  const errLinea = estado.ultimoError ? estado.ultimoError.linea : -1;
  let html = '';
  for (let i = 1; i <= Math.max(n, 14); i++) {
    html += '<b' + (i === errLinea ? ' class="err"' : '') + '>' + i + '</b>';
  }
  document.getElementById('gutter').innerHTML = html;
}

function togglePista() {
  const p = document.getElementById('op-pista');
  const oculto = p.classList.toggle('oculta');
  const etiqueta = estado.modoIDE === 'proyecto' ? 'PISTAS DE LOS PASOS' : 'LA LECTURA DE ARIA';
  document.getElementById('btn-pista').innerHTML = svg('search', 15) + ' ' + (oculto ? 'VER ' : 'OCULTAR ') + etiqueta;
}

function marcarBuild(tipo, tiempo) {
  const el = document.getElementById('build-estado');
  el.className = 'build' + (tipo === 'ok' ? ' ok' : tipo === 'err' ? ' err' : '');
  el.textContent = tipo === 'ok' ? ('BUILD OK' + (tiempo ? ' · ' + tiempo + 's' : ''))
    : tipo === 'err' ? ('BUILD DETENIDO · 1 ERROR' + (tiempo ? ' · ' + tiempo + 's' : ''))
    : 'BUILD EN ESPERA';
}

function terminal(lineas) {
  document.getElementById('terminal').innerHTML = lineas
    .map(([t, c]) => '<div' + (c ? ' class="' + c + '"' : '') + '>' + escapar(t) + '</div>').join('');
}

function cambiarVista(vista) {
  estado.vista = vista;
  document.querySelectorAll('#terminal-tabs .mini-opt').forEach(b => b.classList.toggle('activo', b.dataset.vista === vista));
  const e = estado.ultimoError;

  if (vista === 'error') {
    terminal(e
      ? [['> ' + e.comando, 'dim'], [e.crudo, 'err'], ['build detenido · el sector sigue esperando', 'dim']]
      : [['> sin errores registrados en esta sesión', 'dim']]);
  } else if (vista === 'aria') {
    terminal(e
      ? [['> aria --explain ' + e.codigo, 'dim'], [e.lectura, ''], ['> el error se reporta donde el parser se rinde, no donde se originó', 'acc']]
      : [['> aria --status', 'dim'], [estado.iaActiva ? 'copiloto activo · listo para analizar tu próxima ejecución' : 'copiloto sin configurar (GEMINI_API_KEY)', 'dim']]);
  } else {
    terminal(estado.ultimaSalida || [['> ide listo. ejecutá cuando quieras_', 'dim']]);
  }
}

/* ═══════════════ EJECUTAR ═══════════════ */

async function ejecutar() {
  if (estado.corriendo) return;
  const codigo = document.getElementById('code').value.trim();
  if (!codigo) { aviso('Escribí algo antes de ejecutar', true); return; }

  estado.corriendo = true;
  const btn = document.getElementById('btn-correr');
  btn.disabled = true;
  btn.innerHTML = svg('dashed', 14) + ' EJECUTANDO…';
  marcarBuild('espera');
  estado.ultimaSalida = [['> compilando ' + LANG[estado.lang].archivo + '…', 'dim']];
  cambiarVista('salida');

  try {
    const r = await api('/api/ejecutar', 'POST', { lenguaje: estado.lang, codigo: codigo });
    const cmd = comando() + ' ' + LANG[estado.lang].archivo;

    if (r.exito) {
      estado.ultimoError = null;
      document.getElementById('panel-error').classList.add('oculta');
      estado.ultimaSalida = [['> ' + cmd, 'dim']]
        .concat(String(r.output).split('\n').map(l => [l, '']))
        .concat([['✓ ejecución sin errores · ' + r.tiempo + 's', 'ok']]);
      marcarBuild('ok', r.tiempo);
      estado.vista = 'salida';
    } else {
      estado.ultimoError = leerError(String(r.output), cmd);
      mostrarPanelError();
      estado.ultimaSalida = [['> ' + cmd, 'dim']]
        .concat(String(r.output).split('\n').map(l => [l, 'err']))
        .concat([['build detenido · ' + r.tiempo + 's', 'dim']]);
      marcarBuild('err', r.tiempo);
      estado.vista = 'error';
    }
    cambiarVista(estado.vista);
    sincronizarGutter();
    actualizarCabecera();

    if (estado.iaActiva && estado.modulo) analizarConIA(codigo, r);
  } catch (e) {
    estado.ultimaSalida = [['✗ no pude conectar con el NEXUS. ¿Está corriendo el backend?', 'err']];
    cambiarVista('salida');
    marcarBuild('err');
  } finally {
    estado.corriendo = false;
    btn.disabled = false;
    btn.innerHTML = svg('play', 14) + ' EJECUTAR';
  }
}

function comando() {
  return estado.lang === 'python' ? 'python3' : estado.lang === 'javascript' ? 'node' : 'g++ -o build &&';
}

/* Lee el output real del backend y lo convierte en un informe legible. */
function leerError(salida, cmd) {
  const linea = (salida.match(/l[ií]nea?\s+(\d+)/i) || salida.match(/line\s+(\d+)/i) || salida.match(/:(\d+):/) || [])[1];
  const clase = (salida.match(/([A-Z][A-Za-z]*(?:Error|Exception|Warning))/) || [])[1];

  let codigo = 'RUNTIME';
  let lectura = 'El sistema no pudo terminar la ejecución. Leé la última línea del output: dice qué pasó; las de arriba, dónde empezó.';
  for (const [re, cod, txt] of LECTURAS) {
    if (re.test(salida)) { codigo = cod; lectura = txt; break; }
  }

  return {
    crudo: salida.trim(),
    comando: cmd,
    linea: linea ? Number(linea) : null,
    clase: clase || 'RuntimeError',
    codigo: codigo + '_' + String(linea || '00').padStart(3, '0'),
    lectura: lectura,
    tipo: codigo === 'SYNTAX' || codigo === 'INDENT' ? 'COMPILATION ERROR' : 'RUNTIME ERROR',
  };
}

function mostrarPanelError() {
  const e = estado.ultimoError;
  document.getElementById('panel-error').classList.remove('oculta');
  const tipo = document.getElementById('error-tipo');
  tipo.innerHTML = svg('warnFill', 15) + ' ' + e.tipo;
  texto('error-codigo', 'ERROR CODE: ' + e.codigo);
  texto('error-linea', e.linea != null ? e.linea : '—');
  texto('error-clase', e.clase);
  texto('error-lectura', e.lectura);
  texto('error-contador', 'ERRORES RESUELTOS · ' + estado.erroresResueltos);
  document.getElementById('btn-ir-linea').textContent = e.linea != null ? ('IR A LA LÍNEA ' + e.linea) : 'VER EL OUTPUT';
}

function analizarError() {
  cambiarVista('aria');
  const e = estado.ultimoError;
  if (!e) return;
  mensaje('bot', e.tipo + ' · ' + e.codigo + '\n\n' + e.lectura +
    (e.linea ? '\n\nEl sistema apunta a la línea ' + e.linea + '. Si es un error de sintaxis, empezá revisando la anterior.' : ''));
}

function irALinea() {
  const e = estado.ultimoError;
  const code = document.getElementById('code');
  code.focus();
  if (!e || e.linea == null) return;
  const lineas = code.value.split('\n');
  const objetivo = Math.max(0, Math.min(e.linea - 1, lineas.length - 1));
  const desde = lineas.slice(0, objetivo).join('\n').length + (objetivo ? 1 : 0);
  code.setSelectionRange(desde, desde + lineas[objetivo].length);
}

/* ═══════════════ VALIDAR ═══════════════ */

async function completarModulo() {
  const m = estado.modulo;
  if (!m) return;
  try {
    const data = await api('/api/progreso/completar', 'POST', { lenguaje: estado.lang, modulo_id: m.id });
    if (data.ya_estaba) { aviso('Esta operación ya estaba cerrada'); return; }

    const antes = rangoDe(estado.progreso.xp || 0).nivel;

    if (estado.ultimoError) { // LOCAL: contador de errores superados
      estado.erroresResueltos += 1;
      localStorage.setItem('cp_errores', String(estado.erroresResueltos));
      estado.ultimoError = null;
      document.getElementById('panel-error').classList.add('oculta');
    }

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
    btn.innerHTML = svg('check', 14) + ' YA CERRADA';

    const s = m.sector;
    estado.ultimaSalida = [
      ['> validando contra el sector ' + s.sigla + '…', 'dim'],
      ['✓ operación aceptada · integridad del sector recalculada', 'ok'],
      ['+' + (data.xp_total_ganado || data.xp_ganado) + ' XP' + (data.xp_bonus_racha ? ' (+' + data.xp_bonus_racha + ' de continuidad)' : ''), 'acc'],
    ];
    cambiarVista('salida');
    marcarBuild('ok');

    construirSectores();
    renderMapa();
    actualizarCabecera();

    if (data.nivel_info.nivel > antes) mostrarAscenso(data.nivel_info);
    else {
      aviso('Operación cerrada · +' + (data.xp_total_ganado || data.xp_ganado) + ' XP');
      cerrarIDE();
      irA('nexus');
    }
  } catch (e) {
    aviso('No pude registrar la operación en el sistema', true);
  }
}

function mostrarAscenso(info) {
  const r = RANGOS.find(x => x.nivel === info.nivel) || RANGOS[0];
  texto('ascenso-titulo', r.nombre);
  texto('ascenso-msg', 'Tu autorización subió de rango. ' + r.nota +
    '. La continuidad de ' + (estado.progreso.racha || 0) + ' días sigue activa.');
  document.getElementById('estacion-modal').classList.add('oculta');
  document.getElementById('proyecto-detalle').classList.add('oculta');
  document.body.style.overflow = '';
  document.getElementById('ascenso').classList.remove('oculta');
  pintarIconos(document.getElementById('ascenso'));
  irA('nexus');
}

/* ═══════════════ ARIA (tutor IA) ═══════════════ */

async function verificarIA() {
  try {
    const d = await api('/ia/estado');
    estado.iaActiva = !!d.configurada;
  } catch (e) { estado.iaActiva = false; }
  texto('aria-estado', estado.iaActiva ? 'COPILOTO · NO ESCRIBE POR VOS' : 'SIN CONFIGURAR (GEMINI_API_KEY)');
  texto('aria-nombre', estado.iaActiva ? 'ARIA · COPILOTO DE SISTEMA' : 'ARIA · MODO LOCAL');
  document.getElementById('aria-led').className = 'aria-led' + (estado.iaActiva ? '' : ' off');
}

function reiniciarChat() {
  document.getElementById('chat').innerHTML = '';
  mensaje('bot', estado.iaActiva
    ? 'IDE abierto. Ejecutá cuando quieras y te doy la lectura de lo que devuelva el sistema. No escribo la solución por vos.'
    : 'Estoy en modo local: puedo darte la lectura de los errores que devuelva el sistema, pero no analizar tu código sin GEMINI_API_KEY.');
  api('/ia/historial', 'DELETE').catch(() => {});
}

function mensaje(rol, txt, cargando) {
  const chat = document.getElementById('chat');
  const div = document.createElement('div');
  div.className = 'msg' + (rol === 'yo' ? ' yo' : '') + (cargando ? ' cargando' : '');
  if (cargando) div.id = 'msg-cargando';
  div.textContent = txt;
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
  mensaje('bot', 'Leyendo la ejecución…', true);
  try {
    const d = await api('/ia/analizar', 'POST', {
      codigo: codigo, output: resultado.output, exito: resultado.exito,
      modulo_titulo: estado.modulo.titulo, modulo_ejercicio: estado.modulo.ejercicio,
      lenguaje: estado.lang,
    });
    reemplazarCargando(d.respuesta);
  } catch (e) {
    reemplazarCargando(estado.ultimoError ? estado.ultimoError.lectura : 'No pude analizar la ejecución en este momento.');
  } finally { estado.iaOcupada = false; }
}

async function preguntarIA() {
  const input = document.getElementById('pregunta');
  const q = input.value.trim();
  if (!q || estado.iaOcupada) return;
  input.value = '';
  mensaje('yo', q);
  mensaje('bot', 'Procesando…', true);
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
    reemplazarCargando('El copiloto no está disponible. Configurá GEMINI_API_KEY para activarlo.');
  } finally {
    estado.iaOcupada = false;
    document.getElementById('btn-enviar').disabled = false;
  }
}

/* ═══════════════ PERFIL ═══════════════ */

function renderPerfil() {
  const p = estado.progreso;
  const xp = p.xp || 0;
  const r = rangoDe(xp);
  const sig = RANGOS.find(x => x.min > xp);
  const pct = sig ? Math.round(((xp - r.min) / (sig.min - r.min)) * 100) : 100;
  const cerradas = ['python', 'javascript', 'cpp'].reduce((s, k) => s + (p[k] || []).length, 0);
  const objetos = ((estado.tienda || {}).inventario || []).length;

  const porBloque = {};
  estado.modulos.forEach(m => {
    const b = m.bloque || 'Sistema';
    porBloque[b] = porBloque[b] || { total: 0, hechos: 0 };
    porBloque[b].total++;
    if (hechos().includes(m.id)) porBloque[b].hechos++;
  });

  const skills = SKILLS.map(([label, bloques]) => {
    if (!bloques) return [label, integridadGlobal()];
    let t = 0, h = 0;
    bloques.forEach(b => { if (porBloque[b]) { t += porBloque[b].total; h += porBloque[b].hechos; } });
    return [label, t ? Math.round((h / t) * 100) : 0];
  });

  // LOCAL: insignias calculadas desde el progreso real.
  const insignias = [
    ['Primer build limpio', 'Ejecutaste código sin errores por primera vez', 'check', cerradas >= 1],
    ['Lector de errores', 'Superaste 10 fallos leyendo el informe del sistema', 'search', estado.erroresResueltos >= 10],
    ['Continuidad', 'Dos días seguidos dentro del NEXUS', 'pulse', (p.mejor_racha || 0) >= 2],
    ['Sector estabilizado', 'Llevaste un sector al 100% de integridad', 'shield', estado.sectores.some(s => s.integridad === 100)],
    ['Operador trilingüe', 'Cerraste operaciones en los tres lenguajes', 'code', ['python', 'javascript', 'cpp'].every(k => (p[k] || []).length > 0)],
    ['Arquitecto de sistema', 'Cerraste una operación del sector LIVE', 'chart',
      estado.sectores.some(s => s.sigla === 'LIVE' && s.cerradas > 0)],
  ];

  document.getElementById('perfil').className = 'perfil';
  document.getElementById('perfil').innerHTML =
    '<div class="perfil-top">' +
      '<div class="perfil-hero">' +
        '<div class="perfil-avatar">' + svg('shield', 38) + '</div>' +
        '<div class="perfil-datos">' +
          '<span class="kicker acento">RANGO ACTUAL · OPERADOR #' + String(1000 + xp % 9000) + '</span>' +
          '<h2>' + r.nombre + '</h2>' +
          '<p class="muted">' + (sig ? (sig.min - xp) + ' XP para ' + sig.nombre + ' · ' + sig.nota : 'Rango máximo del NEXUS') + '</p>' +
          '<div class="barra"><div class="barra-fill acento" style="width:' + pct + '%"></div></div>' +
        '</div>' +
      '</div>' +
      '<div class="perfil-stats">' +
        stat('pulse', p.racha || 0, 'Racha (días)') +
        stat('check', cerradas, 'Operaciones') +
        stat('bug', estado.erroresResueltos, 'Errores resueltos') +
        stat('graph', estado.sectores.filter(s => s.integridad === 100).length + '/' + estado.sectores.length, 'Sectores') +
      '</div>' +
    '</div>' +

    '<div class="perfil-medio">' +
      '<section class="perfil-seccion"><span class="kicker">PERFIL TÉCNICO</span>' +
        skills.map(([label, v]) =>
          '<div class="skill' + (v >= 50 ? ' alto' : '') + '"><div class="skill-top">' +
          '<span>' + label + '</span><span>' + v + ' / 100</span></div>' +
          '<div class="barra gruesa"><div class="barra-fill' + (v >= 50 ? ' acento' : '') + '" style="width:' + v + '%"></div></div></div>').join('') +
      '</section>' +

      '<section class="perfil-seccion corta"><span class="kicker">RUTA DE RANGOS</span><div class="rangos">' +
        RANGOS.map((x, i) => {
          const cls = x.nivel === r.nivel ? 'actual' : xp >= x.min ? 'hecho' : '';
          return '<div class="rango-fila ' + cls + '">' +
            '<div class="rango-linea"><span class="rango-punto"></span>' +
            (i === RANGOS.length - 1 ? '' : '<span class="rango-tallo"></span>') + '</div>' +
            '<div class="rango-texto"><span class="rango-nombre">' + x.nombre + '</span>' +
            '<span class="rango-nota">' + (cls === 'actual' ? 'Estás acá · ' + xp.toLocaleString('es-AR') + ' XP' : x.min + ' XP · ' + x.nota) + '</span></div></div>';
        }).join('') +
      '</div></section>' +
    '</div>' +

    '<section><span class="kicker" style="margin-bottom:12px">CERTIFICACIONES</span><div class="insignias">' +
      insignias.map(([n, d, ic, ok]) =>
        '<div class="insignia' + (ok ? ' ganada' : '') + '">' + svg(ic, 20) +
        '<strong>' + n + '</strong><p>' + d + '</p></div>').join('') +
    '</div></section>';
}

function stat(ic, valor, label) {
  return '<div class="perfil-stat">' + svg(ic, 17) + '<strong>' + escapar(valor) + '</strong><span>' + label + '</span></div>';
}

/* ═══════════════ DEPÓSITO ═══════════════ */

const CAT_NOMBRE = { tema: 'Entorno de trabajo', titulo: 'Distintivos', powerup: 'Herramientas de diagnóstico', cosmetico: 'Ambiente' };
const CAT_ICONO = { tema: 'monitor', titulo: 'shield', powerup: 'search', cosmetico: 'chart' };
const ITEM_ICONO = {
  tema_matrix: 'terminal', tema_oceano: 'monitor', tema_fuego: 'monitor', tema_sakura: 'monitor',
  titulo_bug_hunter: 'bug', titulo_pythonista: 'code', titulo_code_ninja: 'shield',
  titulo_hacker: 'key', titulo_10x: 'lightning', racha_shield: 'shield',
  boost_xp: 'lightning', llave_maestra: 'key', lluvia_codigo: 'chart',
};

async function cargarDeposito() {
  try { estado.tienda = await api('/api/tienda'); }
  catch (e) { aviso('No pude abrir el depósito', true); return; }
  renderDeposito();
}

function renderDeposito() {
  const t = estado.tienda;
  if (!t) return;
  const xp = t.xp != null ? t.xp : (estado.progreso.xp || 0);
  texto('deposito-xp', xp.toLocaleString('es-AR') + ' XP');

  const cats = {};
  t.items.forEach(i => { (cats[i.categoria] = cats[i.categoria] || []).push(i); });

  document.getElementById('deposito').innerHTML = Object.keys(cats).map(cat =>
    '<section class="deposito-cat"><span class="kicker">' + (CAT_NOMBRE[cat] || cat) + '</span><div class="deposito-grid">' +
    cats[cat].map((i, k) => {
      const tiene = i.unico && t.inventario.includes(i.id);
      const alcanza = xp >= i.precio;
      const cls = tiene ? 'tenes' : alcanza ? '' : 'caro';
      const accion = tiene ? 'EN INVENTARIO' : alcanza ? 'REQUERIR' : 'XP INSUFICIENTE';
      return '<article class="req ' + cls + '">' +
        '<div class="req-top">' +
          '<span class="req-icono">' + svg(ITEM_ICONO[i.id] || CAT_ICONO[cat] || 'package', 16) + '</span>' +
          '<span class="req-codigo">REQ-' + String(k + 1).padStart(2, '0') + '</span>' +
          '<span class="req-precio">' + i.precio + ' XP</span>' +
        '</div>' +
        '<strong>' + escapar(i.nombre) + '</strong>' +
        '<p>' + escapar(i.descripcion) + '</p>' +
        (i.lore ? '<span class="lore">' + escapar(i.lore) + '</span>' : '') +
        '<button class="btn' + (alcanza && !tiene ? ' btn-primary' : '') + '" data-item="' + i.id + '"' +
          (tiene || !alcanza ? ' disabled' : '') + '>' +
          '<span>' + accion + '</span><span>' + (tiene ? '✓' : i.precio + ' XP') + '</span>' +
        '</button>' +
      '</article>';
    }).join('') + '</div></section>').join('');

  document.querySelectorAll('[data-item]').forEach(b => {
    b.addEventListener('click', () => requerir(b.dataset.item));
  });
}

async function requerir(itemId) {
  try {
    const d = await api('/api/tienda/comprar', 'POST', { item_id: itemId });
    estado.progreso.xp = d.xp_restante;
    estado.tienda.xp = d.xp_restante;
    estado.tienda.inventario = d.inventario;
    aviso(d.message);
    renderDeposito();
    actualizarCabecera();
  } catch (e) {
    aviso(String(e.message).replace(/^\d+:\s*/, ''), true);
  }
}

/* ═══════════════ FONDO ANIMADO ═══════════════ */

function fondoAnimado() {
  const cv = document.getElementById('fondo');
  if (!cv || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const ctx = cv.getContext('2d');
  const glifos = ['{ }', '[ ]', '( )', '< >', '=>', '#', ';', '::', '/*', 'i++'];
  let w = 0, h = 0, nodos = [], trozos = [];
  const mouse = { x: -999, y: -999 };

  function medir() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = cv.clientWidth; h = cv.clientHeight;
    cv.width = w * dpr; cv.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    nodos = Array.from({ length: Math.round((w * h) / 26000) }, () => ({
      x: Math.random() * w, y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.16, vy: (Math.random() - 0.5) * 0.16,
      r: Math.random() * 1.3 + 0.6, z: Math.random(),
    }));
    trozos = Array.from({ length: 10 }, () => ({
      x: Math.random() * w, y: Math.random() * h,
      vy: -(Math.random() * 0.12 + 0.04),
      t: glifos[Math.floor(Math.random() * glifos.length)],
      a: Math.random() * 0.1 + 0.03, s: Math.random() * 5 + 9,
    }));
  }

  window.addEventListener('resize', medir);
  window.addEventListener('pointermove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });
  medir();

  (function paso() {
    ctx.clearRect(0, 0, w, h);
    trozos.forEach(t => {
      t.y += t.vy;
      if (t.y < -20) { t.y = h + 20; t.x = Math.random() * w; }
      ctx.fillStyle = 'rgba(145,132,217,' + t.a + ')';
      ctx.font = '400 ' + t.s.toFixed(0) + 'px "JetBrains Mono", monospace';
      ctx.fillText(t.t, t.x, t.y);
    });
    for (let i = 0; i < nodos.length; i++) {
      const a = nodos[i];
      a.x += a.vx; a.y += a.vy;
      if (a.x < 0 || a.x > w) a.vx *= -1;
      if (a.y < 0 || a.y > h) a.vy *= -1;
      const dmx = a.x - mouse.x, dmy = a.y - mouse.y;
      const dm = Math.hypot(dmx, dmy);
      if (dm < 130) { a.x += (dmx / dm) * 0.5; a.y += (dmy / dm) * 0.5; }
      for (let j = i + 1; j < nodos.length; j++) {
        const b = nodos[j];
        const d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < 132) {
          ctx.strokeStyle = 'rgba(145,132,217,' + (0.09 * (1 - d / 132)).toFixed(3) + ')';
          ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        }
      }
      ctx.fillStyle = dm < 130 ? 'rgba(181,171,252,.5)' : 'rgba(147,151,171,' + (0.13 + a.z * 0.16).toFixed(2) + ')';
      ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2); ctx.fill();
    }
    requestAnimationFrame(paso);
  })();
}

/* ═══════════════ UTILIDADES ═══════════════ */

async function api(url, method, body) {
  const opts = { method: method || 'GET', headers: { 'Content-Type': 'application/json' } };
  if (body) opts.body = JSON.stringify(body);
  const r = await fetch(url, opts);
  if (!r.ok) {
    const err = await r.json().catch(() => ({ detail: r.statusText }));
    throw new Error(r.status + ': ' + (err.detail || r.statusText));
  }
  return r.json();
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
  el.innerHTML = svg(esError ? 'warnFill' : 'lightning', 15) + ' ' + escapar(msg);
  el.className = 'toast' + (esError ? ' error' : '');
  clearTimeout(avisoTimer);
  avisoTimer = setTimeout(() => el.classList.add('oculta'), 3400);
}
