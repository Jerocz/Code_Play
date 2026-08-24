# Code Play — frontend NEXUS

Reemplazo directo de la carpeta `frontend/` del repo Jerocz/Code_Play.

## Cómo instalarlo

Copiá estos tres archivos sobre los que ya tenés:

    frontend/index.html
    frontend/styles.css
    frontend/app.js

No hay nada más que cambiar. El backend queda igual: se sirven en las mismas
rutas (`/static/styles.css`, `/static/app.js`) y se consumen los mismos endpoints.

## Endpoints que usa (sin cambios)

    GET    /api/progreso              POST   /api/progreso/completar
    GET    /api/modulos/:lang         POST   /api/ejecutar
    GET    /api/tienda                POST   /api/tienda/comprar
    GET    /ia/estado                 POST   /ia/analizar
    DELETE /ia/historial              POST   /ia/preguntar

## Qué cambia respecto de la versión anterior

- El sendero lineal pasa a ser un **mapa de sectores**: cada `bloque` de
  `/api/modulos/:lang` se dibuja como un sector del NEXUS con su propia
  integridad (% de módulos cerrados). No hace falta tocar el backend.
- Los módulos se presentan como **operaciones con briefing**: contexto,
  objetivos (parseados de `ejercicio`), consecuencia y recompensa.
- El editor es una **estación de trabajo**: numeración de líneas, terminal con
  pestañas SALIDA / ERROR / ARIA y un **panel de error** que lee el `output`
  real de `/api/ejecutar` — extrae línea, clase de excepción y da una lectura
  del error en vez de un "respuesta incorrecta".
- El tutor pasa a ser **ARIA**, copiloto de sistema (mismos endpoints `/ia/*`).
  Si no hay `GEMINI_API_KEY`, cae a modo local y sigue explicando errores.
- La tienda es el **depósito de requisiciones** (mismos ítems del backend).
- El perfil es un **expediente**: rangos NOVATO → ARCHITECT sobre los mismos
  umbrales de XP del backend, y un perfil técnico calculado desde los bloques.
- Fondo animado en canvas (nodos, conexiones, glifos) que respeta
  `prefers-reduced-motion`.

## Lo que se calcula en el frontend (no en el backend)

Marcado en el código con `LOCAL`:

- **Insignias / certificaciones**: derivadas del progreso real.
- **Errores resueltos**: contador en `localStorage` (`cp_errores`).
- **Cachés de datos**: uno cada 5 operaciones cerradas.
- **Directiva diaria**: dos operaciones por día.

Si más adelante los guardás en el backend, reemplazá esos cálculos por la
lectura del endpoint correspondiente.

## Íconos y tipografías

Los íconos son Phosphor embebidos como paths SVG dentro de `app.js`: no hay
dependencia de CDN de íconos. Las tipografías (Inter + JetBrains Mono) se
cargan desde Google Fonts; si querés que funcione sin internet, descargalas y
serviilas desde `/static/`.
