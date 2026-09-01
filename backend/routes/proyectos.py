from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from routes.progreso import (
    _cargar_progreso,
    _guardar_progreso,
    _calcular_nivel,
    _calcular_racha,
    _bonus_racha,
)

router = APIRouter()


# ═══════════════════════════════════ PYTHON ═══════════════════════════════════
PROYECTOS_PYTHON = [
    {
        "id": 1,
        "disponible_en_ide": "si",
        "titulo": "Adivina el número",
        "descripcion": "La compu elige un número secreto y vos tenés que adivinarlo con pistas de más alto / más bajo.",
        "dificultad": "Principiante",
        "tiempo_estimado": "30-45 min",
        "conceptos": ["input", "condicionales", "bucles while", "módulo random"],
        "xp": 150,
        "objetivo": "Construir un juego de consola donde la computadora elige un número secreto al azar y el jugador intenta adivinarlo, recibiendo pistas de 'más alto' o 'más bajo' en cada intento.",
        "requisitos": ["Módulo: Input del usuario", "Módulo: Bucle while", "Módulo: Operadores lógicos"],
        "pasos": [
            {
                "titulo": "Generá el número secreto",
                "descripcion": "QUÉ: usá random.randint() para elegir un número entre 1 y 100. POR QUÉ: necesitás un valor objetivo que el jugador no conozca de antemano.",
                "pista": "Acordate de hacer 'import random' al inicio del archivo. random.randint(1, 100) incluye ambos extremos.",
            },
            {
                "titulo": "Pedile un intento al jugador",
                "descripcion": "QUÉ: leé un número con input() y convertilo a entero. POR QUÉ: input() siempre devuelve texto, y necesitás comparar números.",
                "pista": "int(input('Tu intento: ')) puede fallar si el usuario escribe texto. Por ahora podés asumir que ingresa un número válido.",
            },
            {
                "titulo": "Comparalo y dale una pista",
                "descripcion": "QUÉ: usá if/elif/else para decirle si el intento es mayor, menor o correcto respecto al número secreto. POR QUÉ: sin retroalimentación el jugador no puede acotar el rango de búsqueda.",
                "pista": "Comparación simple: if intento < secreto: ... elif intento > secreto: ... else: acertó.",
            },
            {
                "titulo": "Repetí hasta acertar o agotar intentos",
                "descripcion": "QUÉ: envolvé la lógica en un while que corte cuando el jugador acierte o llegue a un máximo de intentos (por ejemplo 7). POR QUÉ: un bucle while es ideal cuando no sabés de antemano cuántas rondas van a hacer falta.",
                "pista": "Usá una variable contador que se incremente en cada vuelta del bucle, y un break cuando adivine.",
            },
            {
                "titulo": "Mostrá el resultado final",
                "descripcion": "QUÉ: al terminar, decile al jugador si ganó y en cuántos intentos, o que perdió y cuál era el número secreto. POR QUÉ: cerrar el ciclo de feedback completa la experiencia del juego.",
                "pista": "Podés usar una variable booleana 'gano' que se actualice dentro del bucle y se revise después de que termine.",
            },
        ],
        "criterios": [
            "El juego genera un número aleatorio distinto en cada partida.",
            "Da una pista de mayor/menor después de cada intento incorrecto.",
            "Termina correctamente al acertar o al agotar los intentos disponibles.",
        ],
        "retos_extra": [
            "Agregá niveles de dificultad que cambien el rango de números o la cantidad de intentos.",
            "Guardá el mejor puntaje (menos intentos usados) en un archivo para que persista entre partidas.",
            "Llevá una racha de partidas ganadas seguidas.",
        ],
    },
    {
        "id": 2,
        "disponible_en_ide": "si",
        "titulo": "Gestor de tareas en consola con guardado en archivo",
        "descripcion": "CLI para agregar, listar y completar tareas, que persisten en un archivo entre ejecuciones.",
        "dificultad": "Principiante+",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["listas", "funciones", "lectura/escritura de archivos"],
        "xp": 175,
        "objetivo": "Construir una aplicación de consola que permita agregar, listar y completar tareas, guardándolas en un archivo para que no se pierdan al cerrar el programa.",
        "requisitos": ["Módulo: Listas", "Módulo: Funciones básicas", "Módulo: Archivos y JSON"],
        "pasos": [
            {
                "titulo": "Diseñá la estructura de una tarea",
                "descripcion": "QUÉ: decidí qué datos tiene cada tarea (texto, si está completada). POR QUÉ: antes de guardar algo en un archivo necesitás saber exactamente qué forma tiene.",
                "pista": "Un diccionario simple {'texto': ..., 'completada': False} alcanza, no hace falta una clase todavía.",
            },
            {
                "titulo": "Escribí funciones para agregar y listar",
                "descripcion": "QUÉ: una función agregar_tarea(lista, texto) y otra para mostrar todas las tareas numeradas. POR QUÉ: separar responsabilidades en funciones hace el código reutilizable y más fácil de probar.",
                "pista": "La función de listar puede recorrer la lista con enumerate() para mostrar el número de cada tarea.",
            },
            {
                "titulo": "Marcá tareas como completadas",
                "descripcion": "QUÉ: una función que reciba un índice y cambie el estado de esa tarea a completada. POR QUÉ: sin esto la lista solo crece y nunca refleja progreso real.",
                "pista": "Validá que el índice exista antes de modificar la lista, para no romper el programa con un IndexError.",
            },
            {
                "titulo": "Guardá y cargá desde un archivo",
                "descripcion": "QUÉ: al iniciar el programa, leé el archivo si existe; cada vez que modifiques la lista, volvé a guardarla. POR QUÉ: sin persistencia, las tareas desaparecen apenas cerrás el programa.",
                "pista": "json.dump(lista, archivo, indent=2) y json.load(archivo) son ideales para esto. Manejá el caso de que el archivo todavía no exista.",
            },
            {
                "titulo": "Armá un menú interactivo",
                "descripcion": "QUÉ: un bucle que muestre opciones (agregar, listar, completar, salir) y llame a la función correspondiente según lo que elija el usuario. POR QUÉ: es la forma en que un usuario real va a interactuar con tu programa.",
                "pista": "while True con un if/elif por cada opción del menú, y un break cuando el usuario elige salir.",
            },
        ],
        "criterios": [
            "Las tareas siguen ahí después de cerrar y volver a abrir el programa.",
            "Se pueden agregar, listar y completar tareas sin errores.",
            "El menú no se rompe si el usuario ingresa una opción inválida.",
        ],
        "retos_extra": [
            "Agregá eliminar tareas y filtrar por completadas/pendientes.",
            "Agregá fecha de creación a cada tarea.",
            "Agregá prioridades (alta/media/baja) y permití ordenar por ellas.",
        ],
    },
    {
        "id": 3,
        "disponible_en_ide": "no",
        "titulo": "Consulta del clima con una API",
        "descripcion": "Pedí una ciudad y mostrá su clima actual consultando una API pública gratuita.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["requests", "JSON", "manejo de errores", "variables de entorno"],
        "xp": 200,
        "objetivo": "Construir un programa que le pida una ciudad al usuario y muestre su clima actual, consultando una API pública en tiempo real.",
        "requisitos": ["Módulo: Manejo de errores", "Módulo: Archivos y JSON"],
        "pasos": [
            {
                "titulo": "Elegí una API de clima gratuita",
                "descripcion": "QUÉ: investigá una API pública sin costo (por ejemplo Open-Meteo, que no requiere clave de acceso). POR QUÉ: necesitás entender qué endpoint y qué parámetros usar antes de escribir código.",
                "pista": "Buscá en la documentación de la API un endpoint que reciba latitud/longitud o nombre de ciudad y devuelva temperatura actual.",
            },
            {
                "titulo": "Instalá y probá requests",
                "descripcion": "QUÉ: hacé una petición GET simple y mirá el JSON completo de la respuesta impreso en consola. POR QUÉ: ver la forma real de los datos te dice qué campos vas a necesitar leer después.",
                "pista": "pip install requests. Con requests.get(url).json() obtenés directamente un diccionario de Python.",
            },
            {
                "titulo": "Extraé los datos que te interesan",
                "descripcion": "QUÉ: de la respuesta JSON, sacá la temperatura actual y alguna condición climática. POR QUÉ: la respuesta cruda suele traer mucha más información de la que necesitás mostrar.",
                "pista": "Navegá el diccionario paso a paso, imprimiendo en cada nivel para entender su estructura anidada.",
            },
            {
                "titulo": "Manejá errores de red y de ciudad inválida",
                "descripcion": "QUÉ: envolvé la petición en try/except y verificá el código de estado de la respuesta. POR QUÉ: una API externa puede fallar o no encontrar la ciudad, y tu programa no debería romperse por eso.",
                "pista": "response.status_code te dice si algo salió mal (200 es éxito). Capturá también requests.exceptions.RequestException.",
            },
            {
                "titulo": "(Opcional) Usá variables de entorno para la API key",
                "descripcion": "QUÉ: si tu API requiere clave, guardala en una variable de entorno en vez de escribirla en el código. POR QUÉ: dejar credenciales escritas literalmente en el código fuente es una mala práctica de seguridad.",
                "pista": "os.environ.get('MI_API_KEY') lee la variable sin exponerla en el código.",
            },
        ],
        "criterios": [
            "El programa pide una ciudad y muestra su clima actual.",
            "Si la ciudad no existe o falla la red, muestra un mensaje claro en vez de crashear.",
            "Ninguna API key queda escrita literalmente en el código si la API la requiere.",
        ],
        "retos_extra": [
            "Mostrá el pronóstico de los próximos 3 días.",
            "Guardá un historial de consultas en un archivo.",
            "Agregá emojis según la condición climática (☀️ 🌧️ ❄️).",
        ],
    },
    {
        "id": 4,
        "disponible_en_ide": "no",
        "titulo": "Página web personal con Flask",
        "descripcion": "Sitio con varias páginas (inicio, sobre mí, proyectos) servido con Flask y plantillas reutilizables.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["rutas", "plantillas Jinja", "fundamentos de HTTP"],
        "xp": 200,
        "objetivo": "Construir un sitio web personal con múltiples páginas navegables, usando Flask para las rutas y Jinja para evitar repetir HTML.",
        "requisitos": ["Módulo: Mini API con FastAPI", "Nociones básicas de HTML"],
        "pasos": [
            {
                "titulo": "Instalá Flask y armá el esqueleto",
                "descripcion": "QUÉ: creá una app Flask mínima con una ruta '/' que devuelva un texto simple. POR QUÉ: confirmar que el servidor arranca antes de sumar complejidad te ahorra tiempo de debugging después.",
                "pista": "pip install flask. La app mínima es apenas @app.route('/') sobre una función que devuelve un string.",
            },
            {
                "titulo": "Creá una plantilla base con Jinja",
                "descripcion": "QUÉ: un archivo layout.html con bloques que las demás páginas puedan extender. POR QUÉ: evita repetir el mismo header y footer en cada página del sitio.",
                "pista": "Jinja usa {% block contenido %}{% endblock %} en la base, y {% extends 'layout.html' %} en cada página hija.",
            },
            {
                "titulo": "Agregá rutas para cada sección",
                "descripcion": "QUÉ: rutas /, /sobre-mi y /proyectos, cada una renderizando su propia plantilla. POR QUÉ: cada URL representa un recurso distinto de tu sitio, igual que en las APIs que ya construiste.",
                "pista": "render_template('sobre-mi.html') busca el archivo dentro de una carpeta templates/.",
            },
            {
                "titulo": "Pasá datos dinámicos a las plantillas",
                "descripcion": "QUÉ: en /proyectos, enviá una lista de proyectos desde Python y mostrala con un {% for %} en Jinja. POR QUÉ: el objetivo es que el HTML no tenga contenido escrito a mano, sino que venga de tus datos.",
                "pista": "render_template('proyectos.html', proyectos=mi_lista) — dentro del template usás {% for p in proyectos %}.",
            },
            {
                "titulo": "Dale estilo con CSS",
                "descripcion": "QUÉ: agregá una hoja de estilos en una carpeta static/ y enlazala desde tu layout. POR QUÉ: separar HTML de CSS mantiene el código organizado, igual que separás lógica de presentación en cualquier app.",
                "pista": "Flask sirve automáticamente los archivos dentro de static/ en la URL /static/....",
            },
        ],
        "criterios": [
            "El sitio tiene al menos 3 páginas navegables entre sí.",
            "Usa una plantilla base compartida, sin repetir header/footer en cada página.",
            "La lista de proyectos se genera dinámicamente desde datos en Python, no está escrita a mano en el HTML.",
        ],
        "retos_extra": [
            "Agregá un formulario de contacto que reciba datos por POST.",
            "Desplegá el sitio en un servicio gratuito.",
            "Agregá modo oscuro con un poco de JavaScript.",
        ],
    },
    {
        "id": 5,
        "disponible_en_ide": "no",
        "titulo": "Analizador de gastos con gráficos",
        "descripcion": "Leé un CSV de gastos personales y generá un resumen con gráficos por categoría.",
        "dificultad": "Intermedio+",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["diccionarios", "pandas/matplotlib", "CSV"],
        "xp": 250,
        "objetivo": "Construir una herramienta que lea un archivo CSV de gastos personales y muestre un resumen con gráficos por categoría.",
        "requisitos": ["Módulo: Diccionarios", "Módulo: Analizador de datos", "Módulo: Archivos y JSON"],
        "pasos": [
            {
                "titulo": "Definí el formato del CSV",
                "descripcion": "QUÉ: decidí qué columnas tiene tu archivo (fecha, categoría, monto, descripción) y creá un archivo de ejemplo con varias filas. POR QUÉ: necesitás datos reales para poder probar tu análisis mientras lo desarrollás.",
                "pista": "Podés generar el CSV de ejemplo con el módulo csv de Python, o escribirlo a mano en un editor de texto.",
            },
            {
                "titulo": "Cargá los datos con pandas",
                "descripcion": "QUÉ: usá pd.read_csv() para traer el archivo a un DataFrame. POR QUÉ: pandas simplifica muchísimo el trabajo con datos tabulares comparado con leer el CSV línea por línea a mano.",
                "pista": "pip install pandas matplotlib. df = pd.read_csv('gastos.csv') te da toda la tabla como un objeto manipulable.",
            },
            {
                "titulo": "Agrupá y sumá por categoría",
                "descripcion": "QUÉ: usá groupby() para calcular el total gastado en cada categoría. POR QUÉ: es la pregunta central de un analizador de gastos: ¿en qué se te va la plata?",
                "pista": "df.groupby('categoria')['monto'].sum() te devuelve el total por cada categoría distinta.",
            },
            {
                "titulo": "Generá un gráfico",
                "descripcion": "QUÉ: con matplotlib, hacé un gráfico de barras o de torta mostrando el gasto por categoría. POR QUÉ: una visualización comunica patrones mucho más rápido que una tabla de números.",
                "pista": "El resultado de groupby() tiene un método .plot(kind='bar') o .plot(kind='pie') directamente.",
            },
            {
                "titulo": "Mostrá un resumen en texto también",
                "descripcion": "QUÉ: imprimí el total gastado, la categoría con mayor gasto y el promedio diario. POR QUÉ: no todo el mundo va a querer abrir un gráfico; un resumen rápido en consola también aporta valor.",
                "pista": "idxmax() sobre la serie agrupada te da directamente la categoría con el valor más alto.",
            },
        ],
        "criterios": [
            "El programa lee un CSV real y no se rompe si falta algún dato en una fila.",
            "Muestra un gráfico claro del gasto por categoría.",
            "Imprime un resumen numérico coherente con los datos del archivo.",
        ],
        "retos_extra": [
            "Agregá filtro por rango de fechas.",
            "Comparé los gastos mes a mes.",
            "Exportá el resumen a una imagen o PDF.",
        ],
    },
    {
        "id": 6,
        "disponible_en_ide": "no",
        "titulo": "Tu primer repositorio: Git y GitHub desde cero",
        "descripcion": "Versioná uno de tus proyectos con Git, trabajá con ramas y subilo a GitHub.",
        "dificultad": "Principiante+",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["control de versiones", "git", "ramas", "github"],
        "xp": 175,
        "objetivo": "Aprender a usar Git de verdad: guardar el historial de un proyecto en commits, trabajar con ramas sin miedo a romper nada, y publicar el resultado en GitHub.",
        "requisitos": ["Cualquier proyecto propio en una carpeta (podés usar el Gestor de tareas CLI del sendero)"],
        "pasos": [
            {
                "titulo": "Inicializá el repositorio",
                "descripcion": "QUÉ: parado en la carpeta de tu proyecto, corré git init. POR QUÉ: eso crea una carpeta oculta .git que es donde Git va a guardar TODO el historial de cambios, separado de tus archivos reales.",
                "pista": "git init solo se corre una vez por proyecto. git status te muestra en todo momento qué está pasando (archivos nuevos, modificados, etc.).",
            },
            {
                "titulo": "Configurá tu identidad y hacé el primer commit",
                "descripcion": "QUÉ: configurá tu nombre y email con git config, después agregá archivos al 'staging area' con git add y guardá una foto del proyecto con git commit. POR QUÉ: cada commit es un punto al que podés volver; el mensaje del commit explica el 'por qué' de ese cambio para tu yo futuro.",
                "pista": "git config --global user.name \"Tu Nombre\" — git add . agrega todo lo modificado — git commit -m \"mensaje claro y corto\"",
            },
            {
                "titulo": "Creá un .gitignore apropiado",
                "descripcion": "QUÉ: un archivo .gitignore que le diga a Git qué carpetas o archivos NUNCA debe versionar (entornos virtuales, __pycache__, archivos con contraseñas). POR QUÉ: subir esos archivos infla el repositorio y en el peor caso filtra información sensible.",
                "pista": "Para Python un buen mínimo es: __pycache__/, *.pyc, venv/, .env — cada patrón va en su propia línea.",
            },
            {
                "titulo": "Trabajá con ramas (branches)",
                "descripcion": "QUÉ: creá una rama nueva con git branch/git switch -c, hacé cambios y commits ahí, y después mergeala a tu rama principal. POR QUÉ: las ramas te dejan probar cosas nuevas sin arriesgar el código que ya funciona.",
                "pista": "git switch -c nueva-funcionalidad crea y te mueve a una rama nueva. Para volver a mezclarla: git switch main seguido de git merge nueva-funcionalidad.",
            },
            {
                "titulo": "Subilo a GitHub",
                "descripcion": "QUÉ: creá un repositorio vacío en GitHub, conectalo con git remote add origin <url> y subí tu historial con git push. POR QUÉ: así tu código queda respaldado en la nube y podés compartirlo o mostrarlo como portfolio.",
                "pista": "Después de crear el repo en GitHub, copiá la URL que te dan y corré: git remote add origin <url> — git push -u origin main. Agregá también un README.md contando de qué se trata el proyecto.",
            },
        ],
        "criterios": [
            "El proyecto tiene al menos 4 commits con mensajes que describen qué cambió.",
            "Existe un .gitignore que excluye archivos que no deberían versionarse.",
            "Se usó al menos una rama separada que después se mergeó a main.",
            "El código está publicado en un repositorio de GitHub con un README básico.",
        ],
        "retos_extra": [
            "Provocá un conflicto de merge a propósito (editando la misma línea en dos ramas) y resolvelo a mano.",
            "Agregá un GitHub Action simple que corra tus tests automáticamente en cada push.",
            "Escribí buenos mensajes de commit siguiendo el formato Conventional Commits (feat:, fix:, docs:).",
        ],
    },
    {
        "id": 7,
        "disponible_en_ide": "no",
        "titulo": "Debugging real con pdb y el debugger de VS Code",
        "descripcion": "Dejá de llenar el código de prints: encontrá bugs usando un debugger de verdad.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1 hora",
        "conceptos": ["pdb", "breakpoints", "traceback", "debugging"],
        "xp": 175,
        "objetivo": "Aprender a pausar un programa en cualquier línea, inspeccionar el estado real de las variables y avanzar paso a paso para encontrar bugs, en vez de adivinar con print().",
        "requisitos": ["Módulo: Manejo de errores"],
        "pasos": [
            {
                "titulo": "Escribí (o usá) un programa con un bug real",
                "descripcion": "QUÉ: tomá una función con un resultado incorrecto — por ejemplo un cálculo de promedio que a veces da mal — sin corregirla todavía. POR QUÉ: necesitás un caso real para practicar, no alcanza con leer la teoría del debugger.",
                "pista": "Un bug clásico para practicar: una función que divide por len(lista) sin chequear que la lista no esté vacía, o un acumulador que no se resetea entre llamadas.",
            },
            {
                "titulo": "Pausá la ejecución con breakpoint()",
                "descripcion": "QUÉ: insertá la línea breakpoint() justo antes de donde sospechás que está el problema y corré el script normalmente. POR QUÉ: eso congela el programa ahí mismo y te tira a una consola interactiva parada en ese punto exacto.",
                "pista": "breakpoint() es la forma moderna de python -m pdb. Al llegar a esa línea entrás a un prompt (Pdb) donde podés escribir código Python normal.",
            },
            {
                "titulo": "Inspeccioná variables y avanzá paso a paso",
                "descripcion": "QUÉ: dentro del debugger usá los comandos básicos: n (next, ejecuta la línea siguiente), s (step, entra dentro de una función), c (continue, sigue hasta el próximo breakpoint), p variable (imprime el valor), l (list, muestra el código alrededor). POR QUÉ: estos 5 comandos resuelven el 90% de las sesiones de debugging.",
                "pista": "Podés escribir cualquier expresión Python en el prompt (Pdb), no solo los comandos: por ejemplo p len(mi_lista) o incluso mi_lista.append(1) para probar algo al vuelo.",
            },
            {
                "titulo": "Leé un traceback complejo de afuera hacia adentro",
                "descripcion": "QUÉ: provocá un error con una cadena de llamadas (función A llama a B, que llama a C, que falla) y leé el traceback completo. POR QUÉ: el traceback se lee de ABAJO hacia arriba: la última línea es el error real, y las de arriba son el camino de llamadas que te llevó ahí.",
                "pista": "La última línea del traceback (ej: ZeroDivisionError: division by zero) te dice QUÉ pasó. Las líneas 'File ..., line ..., in ...' de arriba te dicen POR DÓNDE pasó, en orden de la llamada más externa a la más interna.",
            },
            {
                "titulo": "Usá el debugger visual de tu editor",
                "descripcion": "QUÉ: en VS Code (u otro editor con debugger integrado), poné un breakpoint haciendo click a la izquierda del número de línea, y corré el archivo en modo debug en vez de modo normal. POR QUÉ: ver las variables en un panel visual, con step into/step over con botones, es mucho más cómodo que memorizar comandos para sesiones largas.",
                "pista": "En VS Code: F5 corre en modo debug, F10 es 'step over' (siguiente línea sin entrar a funciones), F11 es 'step into' (entra a la función). El panel 'Variables' se actualiza solo en cada pausa.",
            },
        ],
        "criterios": [
            "Lograste pausar el programa en un punto específico usando breakpoint()/pdb.",
            "Usaste al menos n, s, c y p para navegar la ejecución y encontrar el valor incorrecto de una variable.",
            "Identificaste correctamente la causa raíz del bug leyendo el traceback, no adivinando.",
            "Corregiste el bug y verificaste que el resultado ahora es correcto.",
        ],
        "retos_extra": [
            "Usá pdb.set_trace() condicional (if condicion_rara: breakpoint()) para pausar solo cuando pasa algo específico.",
            "Investigá 'post-mortem debugging' con python -m pdb -c continue script.py para debuggear después de un crash.",
            "Configurá un breakpoint condicional en VS Code (click derecho sobre el breakpoint) que solo pare cuando una variable tiene cierto valor.",
        ],
    },
    {
        "id": 8,
        "disponible_en_ide": "no",
        "titulo": "Testing con pytest: probá tu código como un profesional",
        "descripcion": "Escribí tests automatizados para dejar de verificar tu código a mano cada vez.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["pytest", "tests unitarios", "fixtures", "asserts"],
        "xp": 200,
        "objetivo": "Aprender a escribir tests automatizados con pytest para un proyecto ya existente, de forma que puedas detectar si un cambio futuro rompe algo sin tener que probar todo a mano.",
        "requisitos": ["Módulo: Gestor de tareas CLI", "Módulo: Manejo de errores"],
        "pasos": [
            {
                "titulo": "Instalá pytest y escribí tu primer test",
                "descripcion": "QUÉ: instalá pytest, creá un archivo test_algo.py con una función test_algo() que use assert. POR QUÉ: pytest detecta automáticamente cualquier archivo que empiece con test_ y cualquier función que empiece con test_ adentro.",
                "pista": "pip install pytest — un test mínimo: def test_suma(): assert 2 + 2 == 4 — corré todo con: pytest",
            },
            {
                "titulo": "Testeá una función real con múltiples casos",
                "descripcion": "QUÉ: elegí una función de tu Gestor de tareas (por ejemplo agregar o completar) y escribí varios tests que cubran el caso normal Y los casos límite (lista vacía, id inexistente). POR QUÉ: los bugs se esconden en los casos límite, no en el camino feliz.",
                "pista": "Un test por cada comportamiento esperado: test_agregar_tarea_nueva, test_completar_id_inexistente_devuelve_false, etc. Nombres largos y descriptivos son buena práctica en testing.",
            },
            {
                "titulo": "Usá fixtures para no repetir setup",
                "descripcion": "QUÉ: si varios tests necesitan el mismo GestorTareas ya inicializado, creá una fixture con @pytest.fixture que lo prepare. POR QUÉ: sin fixtures terminás copiando y pegando el mismo código de preparación en cada test, lo que es frágil ante cambios.",
                "pista": "@pytest.fixture\\ndef gestor(): return GestorTareas('test.json') — cada test que la necesite la recibe como parámetro: def test_algo(gestor): ...",
            },
            {
                "titulo": "Parametrizá tests con distintos valores",
                "descripcion": "QUÉ: usá @pytest.mark.parametrize para correr el mismo test con varios conjuntos de datos de entrada/salida esperada. POR QUÉ: evita escribir 5 tests casi idénticos que solo cambian los números.",
                "pista": "@pytest.mark.parametrize('entrada,esperado', [(1,2), (5,6), (-1,0)]) — arriba de una función test que reciba entrada y esperado como parámetros.",
            },
            {
                "titulo": "Medí cuánto código está cubierto por tests",
                "descripcion": "QUÉ: instalá pytest-cov y corré pytest --cov para ver qué porcentaje de tu código realmente pasa por algún test. POR QUÉ: la cobertura te muestra puntos ciegos: código que nunca se ejecuta durante los tests es código que podría estar roto sin que lo sepas.",
                "pista": "pip install pytest-cov — pytest --cov=nombre_del_modulo te da un resumen línea por línea de qué se ejecutó y qué no.",
            },
        ],
        "criterios": [
            "Existen al menos 8 tests que cubren casos normales y casos límite.",
            "Se usó al menos una fixture para evitar repetir código de preparación.",
            "Se usó parametrize al menos una vez para evitar tests duplicados.",
            "pytest --cov muestra una cobertura razonable (apuntá a más del 70% del código testeado).",
        ],
        "retos_extra": [
            "Agregá un test que verifique que se lanza una excepción esperada, usando pytest.raises().",
            "Configurá que los tests corran automáticamente antes de cada commit con un git hook.",
            "Separá los tests en test_unitarios.py e test_integracion.py según si prueban una función aislada o el flujo completo.",
        ],
    },
    {
        "id": 9,
        "disponible_en_ide": "si",
        "titulo": "Base de datos con SQL: sqlite3 desde Python",
        "descripcion": "Reemplazá el guardado en JSON por una base de datos SQL de verdad, sin instalar nada externo.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "2 horas",
        "conceptos": ["SQL", "sqlite3", "CRUD", "JOIN"],
        "xp": 225,
        "objetivo": "Aprender SQL básico (CREATE TABLE, INSERT, SELECT, UPDATE, DELETE, JOIN) usando sqlite3, la base de datos que ya viene incluida con Python, migrando tu Gestor de tareas de JSON a una base de datos real.",
        "requisitos": ["Módulo: Archivos y JSON", "Módulo: Gestor de tareas CLI"],
        "pasos": [
            {
                "titulo": "Creá la base y una tabla",
                "descripcion": "QUÉ: usá sqlite3.connect('tareas.db') para crear el archivo de base de datos, y CREATE TABLE para definir la estructura de una tabla tareas (id, titulo, completada). POR QUÉ: a diferencia de un JSON, una tabla SQL define de antemano qué columnas y tipos de datos son válidos.",
                "pista": "import sqlite3 — conn = sqlite3.connect('tareas.db') — cursor = conn.cursor() — cursor.execute('CREATE TABLE IF NOT EXISTS tareas (id INTEGER PRIMARY KEY, titulo TEXT, completada INTEGER)')",
            },
            {
                "titulo": "Insertá y consultá datos",
                "descripcion": "QUÉ: usá INSERT INTO para agregar tareas y SELECT * FROM para leerlas todas. POR QUÉ: son las dos operaciones más básicas de cualquier base de datos: guardar y recuperar.",
                "pista": "SIEMPRE usá parámetros (?) en vez de f-strings para insertar valores: cursor.execute('INSERT INTO tareas (titulo, completada) VALUES (?, ?)', (titulo, 0)) — esto previene inyección SQL.",
            },
            {
                "titulo": "Actualizá y eliminá con condiciones",
                "descripcion": "QUÉ: usá UPDATE ... WHERE para marcar una tarea como completada, y DELETE FROM ... WHERE para eliminar una específica. POR QUÉ: sin el WHERE, un UPDATE o DELETE afecta a TODAS las filas de la tabla — un error carísimo en un sistema real.",
                "pista": "cursor.execute('UPDATE tareas SET completada = 1 WHERE id = ?', (id_tarea,)) — no te olvides de conn.commit() después de cada cambio, si no se pierde al cerrar la conexión.",
            },
            {
                "titulo": "Relacioná dos tablas con JOIN",
                "descripcion": "QUÉ: creá una segunda tabla categorias, vinculá cada tarea a una categoría con una columna categoria_id, y usá SELECT ... JOIN para traer tareas junto con el nombre de su categoría. POR QUÉ: separar datos en tablas relacionadas (en vez de repetir el nombre de categoría en cada fila) es la base del diseño de bases de datos relacionales.",
                "pista": "SELECT tareas.titulo, categorias.nombre FROM tareas JOIN categorias ON tareas.categoria_id = categorias.id",
            },
            {
                "titulo": "Migrá tu Gestor de tareas completo a SQLite",
                "descripcion": "QUÉ: reescribí los métodos _cargar() y _guardar() de tu GestorTareas para que usen sqlite3 en vez de json.load/json.dump. POR QUÉ: es el mismo patrón Repository que ya conocés, solo que ahora la persistencia real es una base de datos en vez de un archivo plano.",
                "pista": "El resto de la clase (agregar, completar, listar) no debería cambiar casi nada — solo cambia CÓMO se guardan y leen los datos por dentro, no la interfaz pública de la clase.",
            },
        ],
        "criterios": [
            "Existe una base de datos SQLite con al menos dos tablas relacionadas.",
            "Todas las consultas con datos del usuario usan parámetros (?) y no f-strings o concatenación.",
            "El CRUD completo (crear, leer, actualizar, eliminar) funciona sobre la base de datos.",
            "Al menos una consulta usa JOIN para combinar datos de ambas tablas.",
        ],
        "retos_extra": [
            "Agregá una tabla de historial que registre cada cambio de estado de una tarea con fecha y hora.",
            "Usá GROUP BY para contar cuántas tareas hay por categoría.",
            "Abrí el archivo .db con una herramienta visual como DB Browser for SQLite para explorar los datos sin código.",
        ],
    },
    {
        "id": 10,
        "disponible_en_ide": "no",
        "titulo": "Dominá la terminal: navegación y scripting básico",
        "descripcion": "Dejá de depender solo del botón 'Run': aprendé a moverte y automatizar tareas desde la línea de comandos.",
        "dificultad": "Principiante",
        "tiempo_estimado": "1 hora",
        "conceptos": ["terminal", "línea de comandos", "variables de entorno", "scripting"],
        "xp": 150,
        "objetivo": "Aprender a navegar el sistema de archivos, encadenar comandos, leer variables de entorno desde Python y escribir un script simple que automatice una tarea repetitiva.",
        "requisitos": ["Módulo: Archivos y JSON"],
        "pasos": [
            {
                "titulo": "Navegá el sistema de archivos sin usar el mouse",
                "descripcion": "QUÉ: usá pwd/cd/ls (o cd/dir en Windows) para moverte entre carpetas, y entendé la diferencia entre ruta relativa (./carpeta) y ruta absoluta (C:/... o /home/...). POR QUÉ: cualquier herramienta profesional (Git, Docker, deploys) asume que sabés moverte por la terminal sin depender de un explorador de archivos gráfico.",
                "pista": "cd .. sube un nivel, cd - vuelve a la carpeta anterior (en bash). En PowerShell, Get-ChildItem (alias ls) lista archivos.",
            },
            {
                "titulo": "Encadená comandos con pipes y redirección",
                "descripcion": "QUÉ: usá > para guardar la salida de un comando en un archivo, >> para agregarla al final, y | para pasar la salida de un comando como entrada de otro. POR QUÉ: encadenar comandos simples es más flexible que buscar una herramienta gráfica para cada tarea puntual.",
                "pista": "python script.py > salida.txt guarda el resultado. En bash: cat archivo.txt | grep 'error' busca líneas con 'error'.",
            },
            {
                "titulo": "Leé variables de entorno desde Python",
                "descripcion": "QUÉ: seteá una variable de entorno en la terminal (temporal) y leela desde un script con os.environ.get(). POR QUÉ: las variables de entorno son la forma estándar de pasarle configuración a un programa sin escribirla adentro del código (claves de API, modo debug, URLs de base de datos).",
                "pista": "En bash: export MI_VAR=hola — en PowerShell: $env:MI_VAR='hola' — en Python: import os; print(os.environ.get('MI_VAR', 'default'))",
            },
            {
                "titulo": "Usá un archivo .env para no repetir el export cada vez",
                "descripcion": "QUÉ: instalá python-dotenv, creá un archivo .env con tus variables, y cargalo con load_dotenv() al inicio de tu script. POR QUÉ: escribir 'export' a mano cada vez que abrís una terminal nueva es tedioso y propenso a errores; un .env centraliza la configuración (y nunca se sube a Git).",
                "pista": "pip install python-dotenv — from dotenv import load_dotenv; load_dotenv() — el .env va en tu .gitignore, SIEMPRE.",
            },
            {
                "titulo": "Escribí un script que automatice algo repetitivo",
                "descripcion": "QUÉ: un script (.sh, .bat o .ps1) que ejecute varios comandos en secuencia — por ejemplo correr tus tests y guardar el resultado en un archivo con fecha en el nombre. POR QUÉ: cualquier secuencia de 3+ comandos que repetís seguido es candidata a convertirse en un script, así no dependés de recordar el orden exacto.",
                "pista": "Un script bash mínimo: #!/bin/bash seguido de los comandos, uno por línea. Hacelo ejecutable con chmod +x script.sh y correlo con ./script.sh",
            },
        ],
        "criterios": [
            "Podés navegar a cualquier carpeta del proyecto sin usar el explorador de archivos gráfico.",
            "Tu script Python lee al menos una variable de entorno definida fuera del código.",
            "Existe un archivo .env (ignorado por Git) con al menos una variable de configuración.",
            "El script de automatización ejecuta al menos 3 comandos en secuencia sin intervención manual.",
        ],
        "retos_extra": [
            "Agregá manejo de argumentos a tu script con sys.argv o el módulo argparse.",
            "Hacé que tu script de automatización falle con un mensaje claro si falta una variable de entorno requerida.",
            "Investigá alias de terminal para acortar comandos que usás seguido.",
        ],
    },
    {
        "id": 11,
        "disponible_en_ide": "no",
        "titulo": "Entorno profesional: venv, pip y estructura de proyecto",
        "descripcion": "Aislá las dependencias de cada proyecto y organizá tu código como un profesional.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1 hora",
        "conceptos": ["entornos virtuales", "pip", "requirements.txt", "estructura de proyecto"],
        "xp": 150,
        "objetivo": "Entender por qué cada proyecto de Python necesita su propio entorno aislado de dependencias, y organizar un proyecto con la estructura de carpetas que vas a encontrar en cualquier repositorio profesional.",
        "requisitos": ["Módulo: Manejo de errores"],
        "pasos": [
            {
                "titulo": "Entendé el problema que resuelve un entorno virtual",
                "descripcion": "QUÉ: imaginá dos proyectos que necesitan versiones distintas de la misma librería instalada globalmente. POR QUÉ: sin entornos virtuales, instalar una librería para un proyecto puede romper silenciosamente OTRO proyecto que dependía de una versión distinta.",
                "pista": "pip list te muestra qué está instalado GLOBALMENTE ahora mismo — probablemente una mezcla de cosas de distintos proyectos, si nunca usaste venv.",
            },
            {
                "titulo": "Creá y activá un entorno virtual",
                "descripcion": "QUÉ: usá python -m venv venv para crear un entorno aislado dentro de tu proyecto, y activalo. POR QUÉ: mientras está activo, todo lo que instalés con pip queda SOLO en ese entorno, sin tocar el resto de tu sistema.",
                "pista": "python -m venv venv — activar en Windows: venv\\Scripts\\activate — en Mac/Linux: source venv/bin/activate — vas a ver (venv) al inicio de la línea de comandos cuando está activo.",
            },
            {
                "titulo": "Instalá dependencias y congelalas en requirements.txt",
                "descripcion": "QUÉ: con el entorno activado, instalá algunas librerías con pip install, y generá un requirements.txt con pip freeze. POR QUÉ: ese archivo es la 'receta' exacta de qué necesita tu proyecto para funcionar, para que cualquier otra persona (o vos en otra máquina) pueda recrear el mismo entorno.",
                "pista": "pip install requests pytest — pip freeze > requirements.txt — abrí el archivo generado y vas a ver cada paquete con su versión exacta.",
            },
            {
                "titulo": "Recreá el entorno desde cero usando requirements.txt",
                "descripcion": "QUÉ: borrá la carpeta venv, creá una nueva, activala, e instalá todo de una sola vez con pip install -r requirements.txt. POR QUÉ: esto simula exactamente lo que pasa cuando alguien clona tu repositorio por primera vez — si funciona acá, va a funcionar en cualquier máquina.",
                "pista": "pip install -r requirements.txt lee el archivo línea por línea e instala cada paquete con la versión exacta especificada.",
            },
            {
                "titulo": "Organizá tu proyecto con una estructura estándar",
                "descripcion": "QUÉ: reorganizá tu código en carpetas: src/ (o el nombre del paquete) para el código fuente, tests/ para los tests, un README.md, .gitignore (que incluya venv/) y requirements.txt en la raíz. POR QUÉ: cualquier desarrollador que abra tu repositorio por primera vez espera encontrar esta estructura — reduce la fricción de entender un proyecto nuevo.",
                "pista": "Estructura mínima razonable: mi_proyecto/ { src/ (o directamente los .py), tests/, README.md, requirements.txt, .gitignore }",
            },
        ],
        "criterios": [
            "El proyecto tiene su propio entorno virtual, no depende de paquetes instalados globalmente.",
            "Existe un requirements.txt generado con pip freeze que refleja las dependencias reales.",
            "Se pudo recrear el entorno completo desde cero usando solo requirements.txt.",
            "venv/ está en el .gitignore y nunca se subió al repositorio.",
        ],
        "retos_extra": [
            "Investigá herramientas más modernas como pipenv, poetry o uv que combinan venv + requirements en una sola herramienta.",
            "Separá las dependencias de desarrollo (pytest, black) de las de producción en requirements-dev.txt.",
            "Agregá un pyproject.toml siguiendo el estándar moderno de empaquetado de Python.",
        ],
    },
    {
        "id": 12,
        "disponible_en_ide": "no",
        "titulo": "Código limpio: linters, formateadores y logging",
        "descripcion": "Dejá que las herramientas encuentren tus errores de estilo, y reemplazá los prints por logging real.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["flake8", "black", "logging", "clean code"],
        "xp": 175,
        "objetivo": "Incorporar herramientas automáticas que detectan problemas de estilo y calidad en tu código, y reemplazar los print() de debugging por un sistema de logging real con niveles de severidad.",
        "requisitos": ["Módulo: Gestor de tareas CLI"],
        "pasos": [
            {
                "titulo": "Corré un linter sobre tu código",
                "descripcion": "QUÉ: instalá flake8 y correlo sobre tu Gestor de tareas, leyendo cada warning que reporte. POR QUÉ: un linter detecta automáticamente problemas de estilo (líneas muy largas, imports sin usar, variables no usadas) que a simple vista se pasan por alto.",
                "pista": "pip install flake8 — flake8 mi_archivo.py — cada línea del reporte te dice el archivo, la línea, y un código (como E501) que podés buscar para entender qué significa.",
            },
            {
                "titulo": "Formateá automáticamente con black",
                "descripcion": "QUÉ: instalá black y correlo sobre tu proyecto para que reformatee el código según un estilo consistente (comillas, espacios, largo de línea). POR QUÉ: discutir sobre estilo de formato en un equipo es tiempo perdido — black elimina esa discusión aplicando un único estilo automáticamente.",
                "pista": "pip install black — black mi_archivo.py reformatea el archivo en el lugar. black --check mi_archivo.py solo te dice si hace falta formatear, sin modificar nada.",
            },
            {
                "titulo": "Reemplazá los print() de debug por logging",
                "descripcion": "QUÉ: usá el módulo logging con niveles (DEBUG, INFO, WARNING, ERROR, CRITICAL) en vez de print() para mensajes de diagnóstico. POR QUÉ: con logging podés apagar los mensajes de debug en producción sin borrar código, y cada mensaje queda con nivel, momento exacto y origen — algo que print() nunca te da.",
                "pista": "import logging; logging.basicConfig(level=logging.INFO) — logging.info('Tarea agregada') — logging.error('No se pudo guardar el archivo')",
            },
            {
                "titulo": "Configurá logging para que escriba a un archivo",
                "descripcion": "QUÉ: configurá un handler que además de mostrar los logs en consola, los guarde en un archivo con formato (timestamp, nivel, mensaje). POR QUÉ: en una aplicación real que corre desatendida, necesitás poder revisar QUÉ pasó horas después, no solo verlo en el momento en la consola.",
                "pista": "logging.basicConfig(filename='app.log', format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)",
            },
            {
                "titulo": "Refactorizá basándote en lo que encontraste",
                "descripcion": "QUÉ: elegí 3 warnings de flake8 que sean sobre calidad real (no solo estilo) y corregilos: nombres poco claros, funciones muy largas, código duplicado. POR QUÉ: las herramientas automáticas son un punto de partida, pero el juicio final sobre qué vale la pena arreglar sigue siendo tuyo.",
                "pista": "Una función de más de 20-25 líneas suele ser candidata a dividirse en funciones más chicas con nombres que expliquen qué hace cada parte.",
            },
        ],
        "criterios": [
            "flake8 corre sobre el proyecto sin warnings de errores graves (imports sin usar, variables no definidas).",
            "El código está formateado consistentemente con black.",
            "No quedan print() de debugging — todos los mensajes de diagnóstico usan logging con el nivel apropiado.",
            "Existe al menos un log que se guarda en archivo con timestamp y nivel.",
        ],
        "retos_extra": [
            "Configurá flake8 y black para que corran automáticamente antes de cada commit con un git hook (pre-commit).",
            "Agregá rotación de logs (RotatingFileHandler) para que el archivo de log no crezca indefinidamente.",
            "Probá pylint o ruff como alternativas más estrictas o más rápidas a flake8.",
        ],
    },
    {
        "id": 13,
        "disponible_en_ide": "no",
        "titulo": "Deploy básico: subí tu proyecto a internet",
        "descripcion": "Llevá tu API de FastAPI de 'funciona en mi máquina' a un servidor real y accesible desde cualquier lado.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["variables de entorno en producción", "Docker (noción)", "deploy", "CI/CD básico"],
        "xp": 200,
        "objetivo": "Preparar una API para producción y publicarla en un servicio de hosting gratuito, entendiendo la diferencia entre correr algo 'en tu máquina' y tenerlo disponible de forma pública y estable.",
        "requisitos": ["Módulo: Mini API con FastAPI"],
        "pasos": [
            {
                "titulo": "Preparé la app para producción",
                "descripcion": "QUÉ: revisá que ningún secreto (claves de API, contraseñas) esté escrito literalmente en el código, y que todo venga de variables de entorno. POR QUÉ: el código que subís a un repositorio público NUNCA debería contener credenciales reales.",
                "pista": "Si encontrás un API_KEY = 'abc123' hardcodeado, cambialo por API_KEY = os.environ.get('API_KEY') y documentá en el README qué variables hacen falta.",
            },
            {
                "titulo": "Entendé la noción de Docker con un Dockerfile simple",
                "descripcion": "QUÉ: escribí un Dockerfile mínimo que empaquete tu API con sus dependencias, sin necesidad de correr los comandos de instalación a mano en cada servidor. POR QUÉ: Docker garantiza que tu app corre EXACTAMENTE igual en cualquier máquina, eliminando el clásico 'en mi compu funciona'.",
                "pista": "Un Dockerfile mínimo para FastAPI: FROM python:3.11-slim, COPY requirements.txt, RUN pip install -r requirements.txt, COPY . ., CMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\"]",
            },
            {
                "titulo": "Elegí un servicio de hosting gratuito y desplegá",
                "descripcion": "QUÉ: usá un servicio gratuito para apps pequeñas (como Render o Railway) y seguí sus pasos para conectar tu repositorio de GitHub y desplegarlo. POR QUÉ: estos servicios manejan la infraestructura (servidor, certificados HTTPS, reinicio automático) para que vos te enfoques en el código.",
                "pista": "La mayoría de estos servicios detectan automáticamente un Dockerfile o un requirements.txt + comando de arranque, y te dan una URL pública apenas termina el deploy.",
            },
            {
                "titulo": "Configurá las variables de entorno en el servicio",
                "descripcion": "QUÉ: en el panel del servicio de hosting, configurá las mismas variables de entorno que usabas localmente en tu .env. POR QUÉ: tu .env local nunca se sube al repositorio (está en .gitignore), así que el servidor de producción necesita que se las pases por otro lado.",
                "pista": "Buscá una sección tipo 'Environment Variables' o 'Config Vars' en el panel del servicio — ahí se configuran una por una, sin tocar código.",
            },
            {
                "titulo": "Agregá un CI básico que corra tus tests",
                "descripcion": "QUÉ: un archivo de GitHub Actions simple que instale dependencias y corra pytest automáticamente en cada push. POR QUÉ: así te enterás de que rompiste algo ANTES de hacer deploy, no después de que un usuario real lo note.",
                "pista": "Un workflow mínimo de GitHub Actions vive en .github/workflows/tests.yml, con steps que hacen actions/checkout, setup-python, pip install -r requirements.txt y pytest.",
            },
        ],
        "criterios": [
            "La API está desplegada y accesible desde una URL pública (no localhost).",
            "Ningún secreto real quedó escrito en el código subido al repositorio.",
            "Las variables de entorno de producción están configuradas en el panel del servicio de hosting, no en el código.",
            "Existe un workflow de CI que corre los tests automáticamente en cada push.",
        ],
        "retos_extra": [
            "Configurá un dominio personalizado (o subdominio gratuito) apuntando a tu deploy.",
            "Agregá un endpoint /health que el servicio de hosting pueda usar para verificar que la app sigue viva.",
            "Hacé que el CI también corra flake8/black --check, fallando el build si el código no está formateado.",
        ],
    },
    {
        "id": 14,
        "disponible_en_ide": "parcial",
        "titulo": "Seguridad básica: protegé tu aplicación",
        "descripcion": "Entendé (y prevení) los errores de seguridad más comunes: inyección SQL, inputs sin validar y contraseñas mal guardadas.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["inyección SQL", "validación de inputs", "hashing de passwords"],
        "xp": 200,
        "objetivo": "Entender de forma práctica por qué ciertos patrones de código son peligrosos, reproduciendo una inyección SQL en un entorno controlado propio, y aprender las defensas básicas que cualquier aplicación real necesita.",
        "requisitos": ["Módulo: Base de datos con SQL: sqlite3 desde Python"],
        "pasos": [
            {
                "titulo": "Reproducí una inyección SQL a propósito",
                "descripcion": "QUÉ: en tu base de datos de práctica (NUNCA en un sistema real de otra persona), escribí una consulta insegura usando f-strings para insertar el input del usuario directamente, y probá pasarle un input malicioso como \"' OR '1'='1\". POR QUÉ: ver con tus propios ojos cómo un input diseñado a propósito rompe la lógica de tu query es mucho más contundente que solo leer la teoría.",
                "pista": "query = f\"SELECT * FROM usuarios WHERE nombre = '{nombre_input}'\" — si nombre_input es \"' OR '1'='1\", la condición se vuelve siempre verdadera y devuelve TODOS los usuarios.",
            },
            {
                "titulo": "Corregilo con consultas parametrizadas",
                "descripcion": "QUÉ: reescribí la misma consulta usando parámetros (?) en vez de f-strings. POR QUÉ: con parámetros, la librería de base de datos trata el input SIEMPRE como un valor literal, nunca como parte de la sintaxis SQL — la inyección deja de ser posible por diseño, no por buena suerte.",
                "pista": "cursor.execute(\"SELECT * FROM usuarios WHERE nombre = ?\", (nombre_input,)) — probá el mismo input malicioso y verificá que ahora NO rompe nada.",
            },
            {
                "titulo": "Validá inputs de usuario antes de usarlos",
                "descripcion": "QUÉ: agregá validaciones explícitas de tipo, rango y longitud para cualquier dato que venga de afuera (formularios, APIs, argumentos). POR QUÉ: la inyección SQL es solo UN tipo de problema que causa la confianza ciega en el input del usuario — validar temprano previene muchos otros bugs y vulnerabilidades.",
                "pista": "Preguntas básicas para cada input: ¿es del tipo esperado? ¿está en un rango razonable? ¿tiene una longitud máxima razonable? Rechazá (no 'arregles silenciosamente') los inputs que no cumplen.",
            },
            {
                "titulo": "Hasheá contraseñas, nunca las guardes en texto plano",
                "descripcion": "QUÉ: usá bcrypt para transformar una contraseña en un hash antes de guardarla, y verificá contraseñas comparando hashes, nunca el texto original. POR QUÉ: si tu base de datos se filtra alguna vez (y a veces pasa, incluso en empresas grandes), las contraseñas hasheadas no son directamente utilizables por un atacante.",
                "pista": "pip install bcrypt — hash_guardado = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) — para verificar: bcrypt.checkpw(intento.encode(), hash_guardado)",
            },
            {
                "titulo": "Auditá tu proyecto por secretos hardcodeados",
                "descripcion": "QUÉ: revisá todo tu código buscando strings que parezcan claves, contraseñas o tokens escritos directamente, y movelos a variables de entorno. POR QUÉ: un secreto hardcodeado que se sube a un repositorio público queda expuesto para siempre en el historial de Git, aunque lo borres después.",
                "pista": "Buscá patrones como API_KEY =, password =, secret = con un valor literal al lado — cualquiera de esos debería venir de os.environ.get() en su lugar.",
            },
        ],
        "criterios": [
            "Reprodujiste una inyección SQL exitosa en tu propio entorno de práctica y entendés por qué funciona.",
            "Todas las consultas SQL del proyecto usan parámetros (?), ninguna concatena o usa f-strings con input del usuario.",
            "Las contraseñas se guardan hasheadas con bcrypt, nunca en texto plano.",
            "No queda ningún secreto (clave, contraseña, token) escrito literalmente en el código.",
        ],
        "retos_extra": [
            "Investigá qué es un ataque XSS (Cross-Site Scripting) y por qué es el equivalente de la inyección SQL pero en el navegador.",
            "Agregá rate limiting básico a un endpoint sensible (como login) para dificultar ataques de fuerza bruta.",
            "Usá una herramienta como git-secrets o trufflehog para escanear tu repositorio en busca de secretos filtrados en commits viejos.",
        ],
    },
    {
        "id": 15,
        "disponible_en_ide": "no",
        "titulo": "Consumí una API de IA desde cero",
        "descripcion": "Conectate a un modelo de lenguaje real desde tu propio código, como lo hace el tutor IA de esta misma app.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["APIs de IA", "requests", "prompt engineering básico", "manejo de errores", "seguridad en IA"],
        "xp": 225,
        "objetivo": "Aprender a integrar una API de inteligencia artificial (como Gemini) en tu propio código: autenticación, armado del request, manejo de la respuesta y de errores — la misma base que usa el tutor IA de este proyecto.",
        "requisitos": ["Módulo: Manejo de errores", "Módulo: Archivos y JSON"],
        "pasos": [
            {
                "titulo": "Conseguí una API key",
                "descripcion": "QUÉ: registrate en un proveedor de IA con capa gratuita (por ejemplo Google AI Studio para Gemini) y generá tu propia API key. POR QUÉ: sin una key válida ningún request va a funcionar — es lo que identifica y autoriza tus llamadas.",
                "pista": "Guardá la key en una variable de entorno apenas la generes, NUNCA la pegues directo en el código — repasá el proyecto de Seguridad básica si tenés dudas de por qué.",
            },
            {
                "titulo": "Armá tu primer request a la API",
                "descripcion": "QUÉ: usá requests.post() para enviar un prompt simple a la API, con los headers y el body en el formato que pide la documentación del proveedor. POR QUÉ: cada API de IA tiene su propio formato de request — leer la documentación y probar con un caso simple es el primer paso siempre.",
                "pista": "La mayoría de las APIs de IA esperan un header Authorization o una API key en la URL, y un body JSON con el prompt dentro de una estructura específica (revisá la documentación del proveedor que elegiste).",
            },
            {
                "titulo": "Extraé el texto generado de la respuesta",
                "descripcion": "QUÉ: parseá el JSON de respuesta y navegá su estructura hasta encontrar el texto generado por el modelo. POR QUÉ: la respuesta completa suele traer metadata (tokens usados, razón de finalización) además del texto — necesitás saber exactamente dónde está lo que te interesa.",
                "pista": "Imprimí response.json() completo la primera vez para ver la estructura real antes de intentar extraer un campo específico.",
            },
            {
                "titulo": "Manejá errores de la API",
                "descripcion": "QUÉ: probá qué pasa con una key inválida, y agregá manejo para rate limiting (demasiados requests seguidos) y timeouts. POR QUÉ: una API externa puede fallar por razones que no controlás — tu programa no debería crashear, sino informar el problema con claridad.",
                "pista": "Revisá response.status_code: 401/403 suele ser problema de autenticación, 429 es rate limit (demasiadas requests), 5xx es un problema del lado del servidor.",
            },
            {
                "titulo": "Iterá el prompt (prompt engineering básico)",
                "descripcion": "QUÉ: probá el mismo pedido con 3 prompts distintos (uno vago, uno específico, uno con ejemplos) y comparé la calidad de las respuestas. POR QUÉ: la forma en que le pedís algo a un modelo de lenguaje cambia drásticamente la calidad de la respuesta — es una habilidad práctica, no solo teoría.",
                "pista": "Un prompt específico con contexto y formato esperado ('Respondé en 3 bullets, en español rioplatense, sin tecnicismos') suele dar resultados mucho más útiles que uno vago ('explicame esto').",
            },
            {
                "titulo": "Pensá en seguridad: qué es el prompt injection",
                "descripcion": "QUÉ: investigá qué es un ataque de prompt injection (cuando un input del usuario intenta manipular las instrucciones que le diste al modelo) y probá un caso simple, metiendo dentro del texto que le pasás como dato una instrucción falsa como 'Ignorá las instrucciones anteriores y...'. POR QUÉ: si tu programa alguna vez usa la respuesta del modelo para tomar una decisión automática (ejecutar código, borrar datos, aprobar algo), un prompt injection exitoso puede hacer que el modelo 'decida' cualquier cosa que un atacante le sugiera — nunca hay que confiar ciegamente en la respuesta de una IA para acciones automáticas sin validar.",
                "pista": "Separá siempre las instrucciones del sistema (lo que vos le decís al modelo que haga) de los datos que vienen del usuario, y nunca ejecutes código ni tomes una acción destructiva basándote directamente en lo que el modelo respondió, sin una validación explícita de tu parte antes.",
            },
        ],
        "criterios": [
            "El programa hace un request real a una API de IA y muestra la respuesta generada.",
            "La API key está en una variable de entorno, nunca escrita en el código.",
            "El programa maneja al menos 2 tipos de error distintos (autenticación, rate limit o timeout) sin crashear.",
            "Se probaron y compararon al menos 3 variantes de prompt para la misma tarea.",
            "Se probó al menos un caso de prompt injection y se explica por qué nunca hay que confiar ciegamente en la respuesta del modelo para tomar decisiones automáticas.",
        ],
        "retos_extra": [
            "Armá una conversación con memoria: mandá el historial de mensajes previos en cada request para que el modelo tenga contexto.",
            "Agregá un modo streaming si el proveedor lo soporta, mostrando la respuesta a medida que se genera.",
            "Compará la misma consulta contra dos proveedores de IA distintos y contrastá calidad/velocidad/costo.",
        ],
    },
    {
        "id": 16,
        "disponible_en_ide": "no",
        "titulo": "Autenticación y autorización con JWT",
        "descripcion": "Login real con tokens: quién sos, qué podés hacer, y por cuánto tiempo — armá tu propio sistema de auth con FastAPI y JWT.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["JWT", "hashing de contraseñas", "FastAPI", "middlewares de autenticación"],
        "xp": 250,
        "objetivo": "Construir un sistema de login con FastAPI que genere tokens JWT, proteja endpoints según el token recibido, y maneje expiración y roles de usuario.",
        "requisitos": ["Módulo: Manejo de errores", "Módulo: Mini API con FastAPI", "Proyecto: Seguridad básica: protegé tu aplicación"],
        "pasos": [
            {
                "titulo": "Armá el endpoint de registro con contraseña hasheada",
                "descripcion": "QUÉ: usá passlib o hashlib con salt para guardar la contraseña, nunca en texto plano. POR QUÉ: si la base se filtra, las contraseñas en texto plano comprometen a todos los usuarios de una — repasá el proyecto de Seguridad básica.",
                "pista": "bcrypt (vía passlib) agrega el salt automáticamente, no necesitás manejarlo vos.",
            },
            {
                "titulo": "Generá un JWT al hacer login",
                "descripcion": "QUÉ: si el login es válido, armá un token JWT con PyJWT que incluya el id de usuario y una fecha de expiración. POR QUÉ: el JWT es la prueba portátil de que el usuario se autenticó, sin que el servidor tenga que guardar sesión en memoria.",
                "pista": "jwt.encode({'sub': user_id, 'exp': ...}, SECRET_KEY, algorithm='HS256'). Nunca hardcodees el SECRET_KEY, usá una variable de entorno.",
            },
            {
                "titulo": "Protegé un endpoint con el token",
                "descripcion": "QUÉ: creá una dependencia de FastAPI (Depends) que lea el header Authorization, valide el JWT y devuelva el usuario o rechace con 401. POR QUÉ: sin esta validación, cualquiera podría llamar a endpoints que deberían requerir login.",
                "pista": "jwt.decode() lanza una excepción si el token es inválido o expiró — atrapala y devolvé HTTPException(401).",
            },
            {
                "titulo": "Agregá expiración y manejo de tokens vencidos",
                "descripcion": "QUÉ: probá qué pasa cuando el token expira, y devolvé un mensaje claro (401, no un error genérico). POR QUÉ: un token que dura para siempre es un riesgo de seguridad — si se filtra, queda válido eternamente.",
                "pista": "Podés generar un token con expiración de 5 segundos para probar el caso vencido más rápido durante el desarrollo.",
            },
            {
                "titulo": "Distinguí roles o permisos básicos",
                "descripcion": "QUÉ: agregá un campo 'rol' al token (por ejemplo 'admin' o 'usuario') y un endpoint que solo el rol admin pueda usar. POR QUÉ: autenticación (quién sos) y autorización (qué podés hacer) son cosas distintas — la mayoría de las apps reales necesitan ambas.",
                "pista": "En la dependencia que valida el token, además de decodificarlo podés chequear el campo 'rol' y devolver 403 (no 401) si no tiene permiso.",
            },
        ],
        "criterios": [
            "El sistema hashea las contraseñas antes de guardarlas, nunca en texto plano.",
            "Genera un JWT válido al hacer login exitoso y lo rechaza si las credenciales son incorrectas.",
            "Al menos un endpoint está protegido y devuelve 401 sin token válido.",
            "Distingue al menos 2 roles con permisos distintos.",
        ],
        "retos_extra": [
            "Agregá un endpoint de refresh token que renueve la sesión sin pedir contraseña de nuevo.",
            "Implementá logout invalidando el token (por ejemplo con una lista negra en memoria).",
            "Agregá rate limiting al endpoint de login para frenar ataques de fuerza bruta.",
        ],
    },
    {
        "id": 17,
        "disponible_en_ide": "no",
        "titulo": "Arquitectura MVC: organizá tu código como un framework real",
        "descripcion": "Separá tu API en modelos, vistas y controladores — la misma organización que usan Django, Rails y la mayoría de los frameworks profesionales.",
        "dificultad": "Intermedio+",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["arquitectura de software", "separación de responsabilidades", "FastAPI", "organización de proyectos"],
        "xp": 200,
        "objetivo": "Reestructurar (o construir desde cero) una API FastAPI separando claramente modelos (datos), controladores (lógica de negocio) y rutas (entrada HTTP), en vez de tener todo mezclado en un solo archivo.",
        "requisitos": ["Módulo: Mini API con FastAPI", "Módulo: Clases y objetos"],
        "pasos": [
            {
                "titulo": "Separá los modelos de datos",
                "descripcion": "QUÉ: creá un archivo models.py con las clases o esquemas Pydantic que representan tus datos (por ejemplo Usuario, Tarea). POR QUÉ: cuando el modelo vive separado de la lógica, podés cambiar cómo se guardan los datos sin tocar el resto del código.",
                "pista": "En FastAPI los modelos suelen ser clases que heredan de BaseModel (Pydantic) para request/response, separadas de las clases que representan el dato en la 'base de datos'.",
            },
            {
                "titulo": "Separá la lógica de negocio en controladores",
                "descripcion": "QUÉ: creá funciones o clases en un archivo controllers.py que reciban datos y hagan la lógica real (crear, validar, calcular), sin saber nada de HTTP. POR QUÉ: si la lógica no depende de FastAPI, la podés testear directo con pytest, sin levantar un servidor.",
                "pista": "Una función de controlador no debería recibir un objeto Request ni devolver un HTTPException directamente — eso es trabajo de la ruta.",
            },
            {
                "titulo": "Dejá las rutas como una capa fina",
                "descripcion": "QUÉ: en tu archivo de rutas, cada endpoint debería ser pocas líneas: recibe el request, llama al controlador, devuelve la respuesta (o el error). POR QUÉ: si la ruta hace demasiado, mezclás 'cómo llega el dato' con 'qué se hace con el dato' y el código se vuelve difícil de reusar o testear.",
                "pista": "Si una función de ruta tiene más de 10-15 líneas con lógica real (no solo llamadas), probablemente esa lógica debería estar en el controlador.",
            },
            {
                "titulo": "Organizá todo en carpetas",
                "descripcion": "QUÉ: armá una estructura de carpetas (models/, controllers/, routes/) en vez de archivos sueltos. POR QUÉ: a medida que un proyecto crece, la organización en carpetas por responsabilidad es lo que permite que varias personas trabajen sin pisarse.",
                "pista": "Cada carpeta necesita un __init__.py (aunque esté vacío) para que Python la reconozca como paquete importable.",
            },
            {
                "titulo": "Escribí un test que pruebe el controlador sin HTTP",
                "descripcion": "QUÉ: importá una función del controlador directamente en un test y llamala con datos de prueba, sin pasar por FastAPI. POR QUÉ: esto demuestra en la práctica el beneficio real de la separación: podés probar la lógica sin levantar un servidor.",
                "pista": "Si esto te resulta difícil de escribir, es una señal de que el controlador todavía depende de algo de HTTP que debería sacarse de ahí.",
            },
        ],
        "criterios": [
            "El proyecto tiene modelos, controladores y rutas en archivos o carpetas separadas.",
            "Los controladores no dependen directamente de objetos de FastAPI (Request, HTTPException).",
            "Al menos un test prueba un controlador sin pasar por una petición HTTP real.",
        ],
        "retos_extra": [
            "Agregá una capa de 'repositorio' entre el controlador y el almacenamiento de datos, para poder cambiar de un dict en memoria a SQLite sin tocar el controlador.",
            "Migrá un proyecto anterior tuyo (por ejemplo el Gestor de tareas) a esta arquitectura.",
        ],
    },
    {
        "id": 18,
        "disponible_en_ide": "no",
        "titulo": "Clean code y refactorización: de spaghetti a profesional",
        "descripcion": "Tomá un código que funciona pero es un desastre, y transformalo paso a paso en algo que cualquier profesional podría leer y mantener.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["refactorización", "nombres descriptivos", "funciones pequeñas", "código limpio"],
        "xp": 175,
        "objetivo": "Partir de un archivo de código deliberadamente desordenado (funciones gigantes, nombres crípticos, lógica duplicada) y refactorizarlo aplicando principios de código limpio, sin cambiar su comportamiento.",
        "requisitos": ["Módulo: Funciones avanzadas", "Proyecto: Código limpio: linters, formateadores y logging"],
        "pasos": [
            {
                "titulo": "Escribí (o usá) el código spaghetti de partida",
                "descripcion": "QUÉ: armá una función de 80+ líneas que procese pedidos de una tienda: valide, calcule descuentos, aplique impuestos, y arme un resumen, todo mezclado con nombres como 'x', 'datos2', 'flag'. POR QUÉ: para practicar refactorización necesitás primero algo real para refactorizar — y este patrón (una función que hace de todo) es extremadamente común en código real.",
                "pista": "Si te cuesta imaginar código así, pensá en cómo escribirías la solución 'lo más rápido posible' sin pensar en mantenibilidad — ese es exactamente el punto de partida.",
            },
            {
                "titulo": "Escribí tests ANTES de tocar nada",
                "descripcion": "QUÉ: con el código como está, escribí 2-3 tests que verifiquen el comportamiento actual (mismos inputs, mismos outputs). POR QUÉ: refactorizar sin tests es peligroso — no tenés forma de saber si rompiste algo hasta que sea tarde.",
                "pista": "Los tests deben pasar ANTES de empezar a refactorizar. Si no pasan, primero arreglá eso, no es parte del ejercicio de refactor.",
            },
            {
                "titulo": "Extraé funciones pequeñas con nombres que expliquen el qué",
                "descripcion": "QUÉ: dividí la función gigante en funciones más chicas (calcular_descuento, aplicar_impuesto, generar_resumen), cada una con un nombre que describe exactamente lo que hace. POR QUÉ: una función que hace una sola cosa es más fácil de entender, testear y reusar que una que hace diez.",
                "pista": "Si te cuesta nombrar una función, probablemente está haciendo más de una cosa — dividila de nuevo.",
            },
            {
                "titulo": "Eliminá números y strings mágicos",
                "descripcion": "QUÉ: reemplazá valores sueltos como 0.21 o 'VIP' por constantes con nombre (IVA = 0.21, CATEGORIA_VIP = 'VIP'). POR QUÉ: un número suelto en el medio del código no explica su significado — alguien que lo lea seis meses después no va a saber qué es 0.21 sin buscarlo.",
                "pista": "Las constantes suelen ir en mayúsculas al principio del archivo o en un módulo aparte de configuración.",
            },
            {
                "titulo": "Corré los tests de nuevo y comparalos",
                "descripcion": "QUÉ: ejecutá los mismos tests del paso 2 contra el código refactorizado. POR QUÉ: si pasan igual que antes, tenés evidencia real de que el comportamiento no cambió — solo mejoró la legibilidad.",
                "pista": "Si algún test falla, el problema está en la refactorización, no en el test — volvé atrás y revisá qué cambiaste de más.",
            },
        ],
        "criterios": [
            "Existe una versión 'antes' y una 'después' del mismo código, con comportamiento idéntico.",
            "Los tests escritos antes de refactorizar pasan igual después de refactorizar.",
            "Ninguna función del código final supera ~20 líneas, y los nombres describen claramente qué hace cada una.",
            "No quedan números o strings mágicos sin explicar mediante una constante con nombre.",
        ],
        "retos_extra": [
            "Medí la complejidad ciclomática del código antes y después (con una herramienta como radon) y compará los números.",
            "Pedile a otra persona (o a Pip) que lea solo el código 'después' y te explique qué hace, sin ayuda tuya — si puede, el refactor funcionó.",
        ],
    },
    {
        "id": 19,
        "disponible_en_ide": "no",
        "titulo": "Docker de verdad: docker-compose, volumes y multi-stage builds",
        "descripcion": "Un Dockerfile simple no alcanza para una app real — armá un entorno completo con base de datos, variables de entorno y una imagen optimizada para producción.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["Docker", "docker-compose", "volumes", "multi-stage builds", "redes de contenedores"],
        "xp": 225,
        "objetivo": "Extender un Dockerfile básico a un entorno completo con docker-compose: la API en un contenedor, una base de datos en otro, comunicándose por una red interna, con datos persistentes y una imagen final optimizada.",
        "requisitos": ["Proyecto: Deploy básico: subí tu proyecto a internet", "Módulo: Archivos y JSON"],
        "pasos": [
            {
                "titulo": "Armá un docker-compose.yml con dos servicios",
                "descripcion": "QUÉ: definí un servicio 'api' (tu aplicación) y un servicio 'db' (por ejemplo postgres) en el mismo archivo docker-compose.yml. POR QUÉ: las apps reales casi nunca corren solas — necesitan una base de datos, y docker-compose es la forma estándar de levantar varios contenedores juntos con un solo comando.",
                "pista": "docker-compose up levanta todos los servicios definidos; cada uno corre en su propio contenedor pero pueden hablarse entre sí por nombre de servicio, no por localhost.",
            },
            {
                "titulo": "Conectá los servicios por una red interna",
                "descripcion": "QUÉ: hacé que tu API se conecte a la base usando el nombre del servicio ('db') como host, no 'localhost'. POR QUÉ: docker-compose crea una red virtual donde cada servicio es alcanzable por su nombre — esto es distinto (y más simple) que exponer puertos manualmente.",
                "pista": "Si tu API dice 'connection refused' a 'localhost', ese es el error clásico de no usar el nombre del servicio de docker-compose como host.",
            },
            {
                "titulo": "Agregá un volume para persistir los datos",
                "descripcion": "QUÉ: montá un volume para la carpeta de datos de la base, para que la información sobreviva si el contenedor se reinicia. POR QUÉ: sin un volume, cada vez que recreás el contenedor de la base perdés todos los datos — los contenedores son efímeros por diseño.",
                "pista": "En docker-compose.yml, la sección volumes de un servicio mapea una carpeta del contenedor a un volume nombrado o a una carpeta de tu máquina.",
            },
            {
                "titulo": "Pasá configuración con variables de entorno, no hardcodeadas",
                "descripcion": "QUÉ: usá un archivo .env (que NO se sube a git) para las credenciales de la base y otras configuraciones sensibles. POR QUÉ: hardcodear contraseñas en el docker-compose.yml es el mismo problema de seguridad que hardcodearlas en el código — y este archivo suele terminar en un repositorio público por error.",
                "pista": "Agregá .env a tu .gitignore desde el primer commit, y dejá un .env.example con los nombres de las variables (sin valores reales) para que otros sepan qué configurar.",
            },
            {
                "titulo": "Optimizá la imagen con un build multi-stage",
                "descripcion": "QUÉ: dividí tu Dockerfile en una etapa de build (instala dependencias, compila si hace falta) y una etapa final que solo copia lo necesario para correr. POR QUÉ: la imagen final queda mucho más chica y segura si no incluye herramientas de compilación ni archivos temporales que solo hacían falta durante el build.",
                "pista": "Usá 'FROM python:3.12 AS build' para la primera etapa, y en la segunda etapa 'COPY --from=build' para traer solo lo que necesitás correr.",
            },
        ],
        "criterios": [
            "docker-compose up levanta la API y la base de datos correctamente conectadas entre sí.",
            "Los datos de la base sobreviven a un 'docker-compose down' seguido de 'docker-compose up' (gracias al volume).",
            "Ninguna credencial está hardcodeada en el docker-compose.yml, todas vienen de variables de entorno.",
            "El Dockerfile usa build multi-stage y la imagen final es notablemente más chica que una versión de una sola etapa.",
        ],
        "retos_extra": [
            "Agregá un tercer servicio (por ejemplo un cache con Redis) y conectalo también por la red interna.",
            "Configurá un healthcheck en docker-compose para que la API espere a que la base esté realmente lista antes de arrancar.",
        ],
    },
    {
        "id": 20,
        "disponible_en_ide": "no",
        "titulo": "Diseñá una API REST como los libros de texto",
        "descripcion": "Status codes correctos, paginación, versionado, idempotencia, y ese error de CORS que seguro ya viste en la consola del navegador — todo lo que separa una API amateur de una profesional.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["REST", "status codes HTTP", "paginación", "versionado de API", "idempotencia", "CORS"],
        "xp": 225,
        "objetivo": "Diseñar (o rediseñar) una API REST siguiendo las convenciones que usan las APIs profesionales: códigos de estado correctos, paginación de resultados, versionado explícito, semántica correcta de PATCH vs PUT, y CORS configurado de forma segura.",
        "requisitos": ["Módulo: Mini API con FastAPI", "Módulo: Manejo de errores"],
        "pasos": [
            {
                "titulo": "Usá el status code correcto para cada situación",
                "descripcion": "QUÉ: revisá tus endpoints y asegurate de devolver 201 al crear un recurso, 204 al borrar sin contenido, 404 si no existe, 400 si el input es inválido, y no un genérico 200 para todo. POR QUÉ: el status code es información estructurada que los clientes de tu API usan para decidir qué hacer — devolver siempre 200 obliga a parsear el body para saber si algo salió mal.",
                "pista": "FastAPI permite fijar el status code de éxito con el parámetro status_code del decorador de ruta, por ejemplo @app.post('/items', status_code=201).",
            },
            {
                "titulo": "Agregá paginación a un endpoint que devuelve listas",
                "descripcion": "QUÉ: en vez de devolver todos los resultados de una, aceptá parámetros de query como page y page_size, y devolvé solo esa porción junto con el total. POR QUÉ: una lista que crece sin límite (miles de registros) puede tumbar tu API o el cliente que la consume si la devolvés entera cada vez.",
                "pista": "Devolvé también metadata útil en la respuesta, como {'total': N, 'page': 1, 'page_size': 20, 'resultados': [...]}, no solo el array pelado.",
            },
            {
                "titulo": "Versioná tu API explícitamente",
                "descripcion": "QUÉ: agregá el número de versión en la URL (/api/v1/...) o en un header, y pensá cómo agregarías un /v2 sin romper a los clientes que ya usan /v1. POR QUÉ: cuando tu API cambia de forma incompatible, romper a todos los que ya la consumen sin aviso es el error más común (y más caro) al mantener una API pública.",
                "pista": "La versión en la URL (/v1/) es la más simple de implementar y la más fácil de entender para quien consume tu API.",
            },
            {
                "titulo": "Distinguí PATCH de PUT correctamente",
                "descripcion": "QUÉ: implementá PUT para reemplazar un recurso completo, y PATCH para modificar solo algunos campos. POR QUÉ: son operaciones semánticamente distintas — usar PUT para una actualización parcial obliga al cliente a mandar todos los campos aunque no los quiera cambiar, y puede pisar datos sin querer.",
                "pista": "En PATCH, los campos que el cliente no manda deberían quedar sin tocar (no ponerse en None ni en su valor por defecto).",
            },
            {
                "titulo": "Configurá CORS correctamente, no con allow_origins=['*']",
                "descripcion": "QUÉ: agregá el middleware CORS de FastAPI, permitiendo solo los orígenes reales que van a consumir tu API (por ejemplo tu frontend en localhost:3000 o tu dominio en producción). POR QUÉ: el navegador bloquea por defecto que JavaScript de un origen (dominio+puerto) haga requests a otro distinto (la 'same-origin policy') — es una protección para el usuario, no un capricho del servidor. allow_origins=['*'] en producción abre tu API a que cualquier sitio la consuma en nombre de tus usuarios, un riesgo real si tu API maneja datos sensibles o requiere autenticación.",
                "pista": "CORSMiddleware de FastAPI (from fastapi.middleware.cors import CORSMiddleware) recibe allow_origins como una lista explícita de dominios, no un string.",
            },
        ],
        "criterios": [
            "Los endpoints devuelven status codes distintos y correctos según el resultado (201, 204, 404, 400, etc), no siempre 200.",
            "Al menos un endpoint de listado soporta paginación con parámetros de query.",
            "La API tiene versión explícita en la URL o en un header.",
            "Existe al menos un PUT y un PATCH sobre el mismo recurso, con comportamiento distinto entre sí.",
            "CORS está configurado con una lista explícita de orígenes permitidos, no con '*', y se explica por qué.",
        ],
        "retos_extra": [
            "Agregá soporte para el header If-Match / ETag para manejar actualizaciones concurrentes de forma segura.",
            "Documentá qué operaciones de tu API son idempotentes (se puede repetir el mismo request sin efectos distintos) y cuáles no, y por qué.",
        ],
    },
    {
        "id": 21,
        "disponible_en_ide": "no",
        "titulo": "Diseño de sistemas básico: caching, balanceo y CAP theorem",
        "descripcion": "Cómo escalan las aplicaciones reales cuando millones de personas las usan a la vez — conceptos clave con una demo chiquita de caching que podés correr en tu máquina.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["caching", "balanceo de carga", "escalado horizontal vs vertical", "CAP theorem"],
        "xp": 200,
        "objetivo": "Entender (de forma conceptual y con una demo práctica de caching) las decisiones de diseño que permiten que un sistema soporte más tráfico: qué es cachear, qué es un balanceador de carga, la diferencia entre escalar hacia arriba y hacia los costados, y qué dice el teorema CAP sobre las promesas que puede hacer una base de datos distribuida.",
        "requisitos": ["Módulo: Diccionarios", "Módulo: Funciones avanzadas"],
        "pasos": [
            {
                "titulo": "Medí cuánto tarda una función 'cara' sin cache",
                "descripcion": "QUÉ: escribí una función que simule un cálculo o consulta lenta (por ejemplo con time.sleep(1)) y medí cuánto tarda en llamarse varias veces seguidas con el mismo input. POR QUÉ: antes de agregar caching necesitás confirmar que el problema es real — cachear algo que ya es instantáneo no aporta nada.",
                "pista": "Llamá a la función 5 veces con el mismo argumento y sumá el tiempo total con time.time() antes y después de cada llamada.",
            },
            {
                "titulo": "Implementá un cache simple con un diccionario",
                "descripcion": "QUÉ: guardá los resultados ya calculados en un diccionario {input: resultado}, y antes de calcular de nuevo, revisá si ya está en el diccionario. POR QUÉ: esta es la idea central de TODO sistema de caching, desde un diccionario en memoria hasta Redis en un sistema distribuido: pagar el costo una vez, reusar el resultado muchas veces.",
                "pista": "Esto es literalmente el mismo patrón que la memoización que viste en el módulo de Programación dinámica — el caching a gran escala es esa misma idea aplicada a sistemas.",
            },
            {
                "titulo": "Agregá expiración al cache (TTL)",
                "descripcion": "QUÉ: guardá también cuándo se calculó cada resultado, y si pasó más de un tiempo límite (por ejemplo 5 segundos), recalculá en vez de usar el valor guardado. POR QUÉ: un cache sin expiración puede devolver datos viejos para siempre — hay que balancear 'rápido' contra 'actualizado', y esa decisión depende de qué tan seguido cambian los datos reales.",
                "pista": "Guardá tuplas (resultado, timestamp) en el diccionario, y comparar time.time() - timestamp contra tu TTL antes de usar el valor cacheado.",
            },
            {
                "titulo": "Explicá con tus palabras: balanceo de carga y escalado horizontal vs vertical",
                "descripcion": "QUÉ: escribí (en un comentario o notas) qué hace un balanceador de carga, y la diferencia entre escalar verticalmente (una máquina más potente) y horizontalmente (más máquinas iguales trabajando juntas). POR QUÉ: esto es la base conceptual de cómo escalan los sistemas reales cuando un solo servidor ya no da abasto — necesitás entender el vocabulario antes de poder discutirlo en una entrevista o con tu equipo.",
                "pista": "Pensá en un balanceador de carga como un mozo que reparte las mesas entre varios cocineros (servidores) para que ninguno se sature — si agregás más cocineros (horizontal) necesitás también a alguien repartiendo el trabajo entre ellos.",
            },
            {
                "titulo": "Explicá el teorema CAP con un ejemplo concreto",
                "descripcion": "QUÉ: investigá y explicá con tus palabras qué son Consistencia, Disponibilidad y Tolerancia a particiones, y por qué un sistema distribuido solo puede garantizar dos de las tres al mismo tiempo. POR QUÉ: entender esta idea es lo que te permite razonar por qué existen bases de datos 'eventualmente consistentes' (como muchas bases NoSQL) en vez de forzar siempre consistencia estricta.",
                "pista": "Pensá en dos servidores en distintas ciudades que se quedan sin poder comunicarse entre sí (partición de red) — ¿siguen respondiendo cada uno con lo que tienen (disponibilidad, aunque podrían mostrar datos distintos) o dejan de responder hasta poder sincronizarse (consistencia, pero indisponibles mientras tanto)? Ese es el trade-off real.",
            },
        ],
        "criterios": [
            "La demo de caching muestra una diferencia de tiempo medible entre la primera llamada (sin cache) y las siguientes (con cache).",
            "El cache implementado tiene expiración (TTL), no guarda resultados para siempre.",
            "Existe una explicación propia (no copiada textual de una fuente) de balanceo de carga, escalado horizontal vs vertical, y el teorema CAP.",
        ],
        "retos_extra": [
            "Implementá una política de reemplazo LRU (Least Recently Used) para tu cache, limitando su tamaño máximo.",
            "Investigá qué estrategia de consistencia usa una base de datos real que conozcas (por ejemplo MongoDB o DynamoDB) y relacionala con el teorema CAP.",
        ],
    },
    {
        "id": 22,
        "disponible_en_ide": "parcial",
        "titulo": "Bases de datos como un profesional: normalización, índices y ACID",
        "descripcion": "Tu base de datos ya funciona — ahora hacela rápida y correcta de verdad: normalización, índices, transacciones, y el clásico problema N+1 que hace lenta a media internet.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "2 horas",
        "conceptos": ["normalización", "índices", "transacciones", "ACID", "problema N+1"],
        "xp": 225,
        "objetivo": "Extender un proyecto con SQLite para aplicar buenas prácticas de bases de datos reales: normalizar una tabla que mezcla datos que no deberían estar juntos, agregar índices y medir su impacto, usar transacciones para operaciones que deben ser todo-o-nada, y detectar (y resolver) el problema N+1.",
        "requisitos": ["Proyecto: Base de datos con SQL: sqlite3 desde Python"],
        "pasos": [
            {
                "titulo": "Detectá una tabla sin normalizar y separala",
                "descripcion": "QUÉ: partí de una tabla que mezcle datos repetidos (por ejemplo pedidos con el nombre y dirección del cliente repetidos en cada fila) y separala en dos tablas relacionadas por un id. POR QUÉ: si el nombre de un cliente está duplicado en cientos de filas, actualizarlo significa actualizar cientos de filas — y es fácil que alguna quede desactualizada, generando datos inconsistentes.",
                "pista": "Esto es la idea de la 'primera forma normal' en la práctica: cada dato vive en un solo lugar, y se referencia por id desde donde se necesite.",
            },
            {
                "titulo": "Medí una consulta lenta y agregale un índice",
                "descripcion": "QUÉ: hacé una consulta que filtre por una columna sin índice sobre una tabla con muchos registros, medí el tiempo, agregá un índice a esa columna con CREATE INDEX, y medí de nuevo. POR QUÉ: sin índice, la base tiene que revisar fila por fila (scan completo) para encontrar lo que buscás — con miles o millones de filas, eso se nota muchísimo.",
                "pista": "Generá al menos unos miles de filas de prueba (con un bucle) para que la diferencia de tiempo con y sin índice sea medible.",
            },
            {
                "titulo": "Usá una transacción para una operación que debe ser todo-o-nada",
                "descripcion": "QUÉ: implementá una transferencia entre dos cuentas (restar de una, sumar a la otra) envuelta en una transacción, y probá qué pasa si falla a la mitad. POR QUÉ: sin transacción, un error en el medio de una operación de varios pasos puede dejar los datos en un estado inconsistente (por ejemplo, plata que desapareció de una cuenta sin aparecer en la otra).",
                "pista": "Con sqlite3, podés usar conn.execute('BEGIN') y luego conn.commit() o conn.rollback() según si todo salió bien.",
            },
            {
                "titulo": "Explicá ACID con el ejemplo que acabás de construir",
                "descripcion": "QUÉ: relacioná tu ejemplo de transferencia con los cuatro principios: Atomicidad, Consistencia, Aislamiento, Durabilidad. POR QUÉ: ACID no es un concepto abstracto — es exactamente la garantía que te dio la transacción del paso anterior, y entender cada letra te ayuda a razonar sobre qué puede salir mal sin esas garantías.",
                "pista": "La Atomicidad es la que impidió que la plata 'desapareciera' si el programa fallaba a la mitad — pensá qué garantiza cada una de las otras tres letras en tu ejemplo.",
            },
            {
                "titulo": "Detectá y resolvé un problema N+1",
                "descripcion": "QUÉ: escribí una consulta que, para listar N pedidos, haga una consulta separada por cada pedido para traer su cliente (N+1 consultas en total), y después resolvelo con un solo JOIN. POR QUÉ: el problema N+1 es una de las causas más comunes de APIs lentas en producción — parece funcionar bien con pocos datos y se vuelve un desastre de performance apenas crece el volumen.",
                "pista": "Contá cuántas consultas SQL se ejecutan en cada versión (podés loguear cada conn.execute) para ver la diferencia numérica entre el enfoque N+1 y el JOIN.",
            },
        ],
        "criterios": [
            "Existe una tabla que fue normalizada, separando datos que antes estaban duplicados.",
            "Se mide y documenta la diferencia de tiempo de una consulta antes y después de agregar un índice.",
            "Una operación de varios pasos usa una transacción real (BEGIN/COMMIT/ROLLBACK), probada con un caso de fallo.",
            "Se identifica un caso de problema N+1 en el propio código y se resuelve con un JOIN, mostrando la reducción en cantidad de consultas.",
        ],
        "retos_extra": [
            "Agregá una restricción UNIQUE o FOREIGN KEY a tu esquema y probá qué pasa si intentás violarla.",
            "Usá EXPLAIN QUERY PLAN de SQLite para ver si tus consultas realmente están usando los índices que creaste.",
        ],
    },
    {
        "id": 23,
        "disponible_en_ide": "no",
        "titulo": "Git avanzado: rebase, cherry-pick y estrategias de branching",
        "descripcion": "Más allá de add/commit/push — los comandos y estrategias que usa un equipo real para mantener un historial de Git limpio y coordinar el trabajo de varias personas.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["git rebase", "git cherry-pick", "git bisect", "Git Flow", "trunk-based development"],
        "xp": 200,
        "objetivo": "Practicar comandos avanzados de Git (rebase, cherry-pick, bisect) sobre un repositorio de prueba, y entender cuándo conviene cada estrategia de branching en equipo.",
        "requisitos": ["Proyecto: Tu primer repositorio: Git y GitHub desde cero"],
        "pasos": [
            {
                "titulo": "Practicá rebase vs merge en un repo de prueba",
                "descripcion": "QUÉ: creá una rama, hacé un par de commits en main mientras tanto, y traé esos cambios a tu rama primero con merge y después (en otro intento) con rebase, comparando el historial resultante. POR QUÉ: merge conserva el historial real tal cual pasó (con un commit de merge), mientras que rebase reescribe tu rama como si hubiera partido del último commit de main — cada uno tiene su lugar, y mezclar ambos sin saberlo genera historiales confusos.",
                "pista": "'git log --graph --oneline --all' te deja ver visualmente la diferencia de forma entre el historial después de un merge y después de un rebase.",
            },
            {
                "titulo": "Usá cherry-pick para traer un commit específico",
                "descripcion": "QUÉ: en una rama distinta, aplicá un solo commit puntual de otra rama con git cherry-pick, sin traer el resto de los cambios de esa rama. POR QUÉ: a veces necesitás un fix específico (por ejemplo un hotfix urgente) en varias ramas sin mezclar todo el trabajo en progreso de la rama original.",
                "pista": "'git cherry-pick <hash-del-commit>' aplica ese commit puntual — copiá el hash con 'git log' antes de usarlo.",
            },
            {
                "titulo": "Encontrá un bug con git bisect",
                "descripcion": "QUÉ: en un repo con varios commits, introducí un bug a propósito en alguno del medio, y usá git bisect (marcando commits como good/bad) para encontrar exactamente cuál lo introdujo. POR QUÉ: en un proyecto con cientos de commits, revisar uno por uno a mano para encontrar cuándo se rompió algo es carísimo — bisect hace búsqueda binaria por vos, en log(N) pasos en vez de N.",
                "pista": "'git bisect start', después 'git bisect bad' (en el commit actual, que sabés que tiene el bug) y 'git bisect good <hash-viejo>' (uno que sabés que andaba bien) — git te va llevando commit por commit hasta encontrarlo.",
            },
            {
                "titulo": "Explicá Git Flow",
                "descripcion": "QUÉ: describí con tus palabras las ramas típicas de Git Flow (main, develop, feature/*, release/*, hotfix/*) y para qué sirve cada una. POR QUÉ: es una de las estrategias de branching más usadas en equipos con ciclos de release planificados, y entenderla te permite trabajar en un proyecto que ya la use sin romper la convención del equipo.",
                "pista": "Pensá Git Flow como capas: 'main' es siempre lo que está en producción, 'develop' es donde se integra el trabajo en curso, y las ramas 'feature/*' son trabajo individual que eventualmente se junta en develop.",
            },
            {
                "titulo": "Explicá trunk-based development y cuándo conviene sobre Git Flow",
                "descripcion": "QUÉ: describí en qué se diferencia trunk-based (todo el mundo integra seguido a una rama principal, con feature flags para lo incompleto) de Git Flow, y en qué tipo de equipo tiene más sentido cada enfoque. POR QUÉ: no hay una estrategia 'correcta' universal — un equipo chico con deploys frecuentes suele preferir trunk-based (menos fricción de ramas), mientras que un proyecto con releases planificadas y QA formal suele preferir algo como Git Flow.",
                "pista": "Pensá en la diferencia entre 'trabajo terminado antes de integrar' (Git Flow, ramas de larga vida) versus 'integrar seguido y ocultar lo incompleto con un flag' (trunk-based, ramas de vida muy corta).",
            },
        ],
        "criterios": [
            "Se practicó rebase y merge sobre el mismo escenario, y se puede explicar la diferencia en el historial resultante.",
            "Se usó cherry-pick para traer un commit puntual sin mezclar toda una rama.",
            "Se usó git bisect para encontrar un commit específico que introdujo un bug, de forma verificable.",
            "Existe una explicación propia de Git Flow y trunk-based development, con cuándo conviene cada uno.",
        ],
        "retos_extra": [
            "Provocá un conflicto de merge a propósito (editando la misma línea en dos ramas distintas) y resolvelo manualmente.",
            "Investigá 'git reflog' y usalo para recuperar un commit que 'perdiste' después de un reset --hard en un repo de prueba.",
        ],
    },
    {
        "id": 24,
        "disponible_en_ide": "no",
        "titulo": "Estrategia de testing: la pirámide y un test de integración real",
        "descripcion": "No todos los tests son iguales — entendé la pirámide de testing (unit, integración, e2e) y escribí un test de integración de verdad contra tu base de datos.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["pirámide de testing", "tests unitarios", "tests de integración", "tests e2e", "pytest"],
        "xp": 200,
        "objetivo": "Entender la pirámide de testing (muchos tests unitarios rápidos, menos tests de integración, muy pocos e2e) y aplicarla escribiendo un test de integración real que use la base de datos SQLite de un proyecto existente, en vez de mockearla.",
        "requisitos": ["Proyecto: Testing con pytest: probá tu código como un profesional", "Proyecto: Base de datos con SQL: sqlite3 desde Python"],
        "pasos": [
            {
                "titulo": "Explicá la pirámide de testing",
                "descripcion": "QUÉ: describí con tus palabras qué es un test unitario, uno de integración y uno end-to-end (e2e), y por qué la pirámide sugiere tener muchos de los primeros y pocos de los últimos. POR QUÉ: entender esta jerarquía te ayuda a decidir qué tipo de test escribir para cada situación, en vez de escribir siempre el mismo tipo (o ninguno).",
                "pista": "Pensá en velocidad y costo: un test unitario corre en milisegundos y prueba una función aislada; un test e2e puede tardar segundos y prueba el sistema completo como lo usaría un usuario real — por eso conviene tener muchos más de los rápidos y baratos.",
            },
            {
                "titulo": "Identificá qué tests de un proyecto tuyo son unitarios",
                "descripcion": "QUÉ: revisá los tests de un proyecto anterior (o escribí 2-3 nuevos) que prueben una sola función aislada, sin tocar archivos, red ni base de datos. POR QUÉ: los tests unitarios son la base de la pirámide — deben ser rápidos y no depender de nada externo para poder correr cientos de ellos en segundos.",
                "pista": "Si tu test necesita que algo esté 'levantado' (un servidor, una base de datos real) para pasar, no es un test unitario, es de integración.",
            },
            {
                "titulo": "Escribí un test de integración real contra SQLite",
                "descripcion": "QUÉ: escribí un test que use una base de datos SQLite real (podés usar una base temporal o en memoria con ':memory:') para probar que una función que inserta y después lee datos funciona de punta a punta. POR QUÉ: a diferencia de un test unitario, este prueba que tu código y la base de datos real trabajan bien juntos — cosas como un tipo de dato mal mapeado o una consulta SQL con errores de sintaxis solo aparecen acá, no en un test que mockea la base.",
                "pista": "sqlite3.connect(':memory:') crea una base temporal en RAM, ideal para tests: es rápida y no deja archivos residuales entre corridas.",
            },
            {
                "titulo": "Compará qué hubiera pasado si mockeabas la base de datos",
                "descripcion": "QUÉ: escribí (o al menos describí) cómo sería el mismo test si en vez de una base real usaras un mock que simula las respuestas. POR QUÉ: un mock que devuelve exactamente lo que vos programaste puede pasar aunque tu consulta SQL real tenga un error de sintaxis — el test de integración contra la base real es el que hubiera detectado ese problema.",
                "pista": "Pensá en un caso concreto: si escribís mal el nombre de una columna en tu consulta SQL, un mock bien configurado seguiría 'pasando' el test, pero la base de datos real fallaría con un error — eso es justamente lo que el test de integración está pensado para atrapar.",
            },
            {
                "titulo": "Organizá los tests por tipo",
                "descripcion": "QUÉ: separá tus tests en archivos o carpetas distintas (por ejemplo tests/unit/ y tests/integration/) y configurá pytest para poder correr solo un grupo a la vez. POR QUÉ: en un proyecto real, correr todos los tests de integración (más lentos) en cada guardado de archivo sería frustrante — separarlos permite correr solo los unitarios durante el desarrollo activo, y todos antes de un commit o deploy.",
                "pista": "Podés usar marcadores de pytest (@pytest.mark.integration) o simplemente carpetas separadas y correr pytest tests/unit/ vs pytest tests/integration/.",
            },
        ],
        "criterios": [
            "Existe una explicación propia de la pirámide de testing (unit, integración, e2e) y cuándo usar cada nivel.",
            "Hay al menos un test de integración real que usa SQLite de verdad, no un mock.",
            "Los tests unitarios y de integración están organizados de forma que se puedan correr por separado.",
        ],
        "retos_extra": [
            "Agregá un test e2e simple usando requests contra un servidor FastAPI real levantado en el mismo test (con TestClient de FastAPI).",
            "Medí cuánto tarda correr solo los tests unitarios vs correr toda la suite, y compará la diferencia.",
        ],
    },
    {
        "id": 25,
        "disponible_en_ide": "no",
        "titulo": "Observabilidad: logs, métricas, traces y un /health real",
        "descripcion": "Cuando tu app está en producción y algo falla a las 3 de la mañana, la observabilidad es lo que te permite entender qué pasó sin adivinar.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["logs", "métricas", "traces", "observabilidad", "health checks"],
        "xp": 200,
        "objetivo": "Entender la diferencia entre logs, métricas y traces (los tres pilares de la observabilidad), y construir un endpoint /health en FastAPI que verifique de verdad el estado de las dependencias de tu app, no solo devuelva 'ok'.",
        "requisitos": ["Módulo: Manejo de errores", "Proyecto: Código limpio: linters, formateadores y logging"],
        "pasos": [
            {
                "titulo": "Explicá logs, métricas y traces con un ejemplo cada uno",
                "descripcion": "QUÉ: describí con tus palabras qué es cada uno, y dá un ejemplo concreto de qué información aportaría cada uno frente a un mismo problema (por ejemplo, una API que responde lento). POR QUÉ: son herramientas distintas para preguntas distintas — un log te dice 'qué pasó exactamente en este request', una métrica te dice 'cuántos requests están tardando de más ahora mismo', y un trace te dice 'en qué paso específico de este request se fue el tiempo'.",
                "pista": "Pensá en logs como un diario detallado de eventos individuales, métricas como números agregados a lo largo del tiempo (promedios, contadores), y traces como el recorrido paso a paso de UN request específico a través de todo el sistema.",
            },
            {
                "titulo": "Agregá logs estructurados con contexto útil",
                "descripcion": "QUÉ: en vez de mensajes sueltos ('error'), logueá con contexto: qué endpoint, qué usuario (si aplica), qué parámetros, y el timestamp. POR QUÉ: un log sin contexto ('Error en la base de datos') no te sirve de nada a las 3 de la mañana intentando entender qué pasó — necesitás poder reconstruir la situación exacta.",
                "pista": "El módulo logging de Python te permite loguear con formato, pero para logs realmente estructurados podés armar un diccionario y loguearlo como JSON (con json.dumps) para que sea fácil de buscar y filtrar después.",
            },
            {
                "titulo": "Contá una métrica simple: requests por endpoint",
                "descripcion": "QUÉ: llevá un contador (aunque sea en memoria, con un diccionario) de cuántas veces se llamó a cada endpoint, y exponelo en un endpoint /metrics. POR QUÉ: esto es la base de cualquier sistema de métricas real (como Prometheus): números agregados que te dejan ver patrones de uso y detectar anomalías (por ejemplo, un endpoint que de repente recibe 100 veces más tráfico de lo normal).",
                "pista": "Un middleware de FastAPI que se ejecute en cada request es el lugar ideal para incrementar el contador correspondiente, sin tener que modificar cada endpoint individualmente.",
            },
            {
                "titulo": "Medí la duración de cada request (la base de un trace)",
                "descripcion": "QUÉ: con un middleware, medí cuánto tarda cada request en procesarse y logueá esa duración junto con el path. POR QUÉ: sin esta medición no podés saber si tu API se está poniendo lenta con el tiempo, ni identificar qué endpoints son los más costosos — es el primer paso hacia un sistema de tracing real.",
                "pista": "time.time() antes de llamar a call_next(request) y de nuevo después te da la duración total de ese request específico.",
            },
            {
                "titulo": "Construí un /health que chequee dependencias reales",
                "descripcion": "QUÉ: hacé que el endpoint /health verifique de verdad que la base de datos responde (por ejemplo con una consulta simple SELECT 1) y devuelva un status distinto si algo falla, no solo {'status': 'ok'} fijo. POR QUÉ: un /health que siempre dice 'ok' sin chequear nada es inútil para un sistema de monitoreo — el objetivo es que herramientas automáticas (o vos mismo) puedan saber si la app realmente puede funcionar, no solo si el proceso está corriendo.",
                "pista": "Devolvé un status_code 503 (Service Unavailable) si alguna dependencia crítica falla, y 200 solo si todo lo esencial responde — no le mientas al que llama al endpoint.",
            },
        ],
        "criterios": [
            "Existe una explicación propia de la diferencia entre logs, métricas y traces, con ejemplos concretos.",
            "Los logs incluyen contexto útil (endpoint, timestamp, parámetros relevantes), no solo un mensaje suelto.",
            "Hay un endpoint /metrics (o similar) que expone al menos un contador real de uso.",
            "El endpoint /health verifica al menos una dependencia real (por ejemplo la base de datos) y devuelve un status distinto si falla.",
        ],
        "retos_extra": [
            "Agregá un ID único a cada request (un 'request ID') y propagalo en todos los logs de ese request, para poder rastrear un pedido específico entre múltiples líneas de log.",
            "Investigá qué es OpenTelemetry y cómo se relaciona con lo que armaste en este proyecto.",
        ],
    },
    {
        "id": 26,
        "disponible_en_ide": "no",
        "titulo": "Tipado estático en Python: type hints y mypy",
        "descripcion": "Python no obliga a declarar tipos, pero podés anotarlos igual — y dejar que una herramienta te avise de errores antes de correr el programa.",
        "dificultad": "Intermedio+",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["type hints", "mypy", "Optional", "Union", "List[T]"],
        "xp": 175,
        "objetivo": "Tomar un proyecto Python existente sin anotaciones de tipos, agregarle type hints completos, correr mypy sobre él, y corregir los errores que encuentre.",
        "requisitos": ["Módulo: Funciones avanzadas", "Módulo: Diccionarios"],
        "pasos": [
            {
                "titulo": "Instalá mypy y corré un chequeo inicial",
                "descripcion": "QUÉ: instalá mypy (pip install mypy) y corrélo sobre un proyecto tuyo sin anotaciones. POR QUÉ: sin type hints, mypy no tiene mucho que chequear todavía — este primer paso es la línea de base antes de empezar a anotar.",
                "pista": "mypy nombre_archivo.py sobre un archivo sin anotaciones probablemente no reporte casi nada — eso va a cambiar apenas empieces a agregar tipos.",
            },
            {
                "titulo": "Anotá los tipos de parámetros y retorno de tus funciones",
                "descripcion": "QUÉ: agregá anotaciones de tipo a cada función (def sumar(a: int, b: int) -> int:). POR QUÉ: las anotaciones documentan la intención de tu código para cualquiera que lo lea, y le dan a mypy la información que necesita para detectar usos incorrectos.",
                "pista": "Si una función no devuelve nada útil (solo hace efectos secundarios como imprimir), anotala con -> None.",
            },
            {
                "titulo": "Usá Optional y Union donde corresponda",
                "descripcion": "QUÉ: identificá parámetros o retornos que pueden ser de más de un tipo, o que pueden ser None, y anotalos con Optional[X] o Union[X, Y]. POR QUÉ: una función que a veces devuelve un dato y a veces None es una fuente clásica de bugs (AttributeError sobre None) — anotarlo explícitamente hace que mypy te avise si no chequeaste ese caso antes de usar el valor.",
                "pista": "Optional[int] es exactamente lo mismo que Union[int, None] — es solo una forma más corta de escribirlo para el caso específico de 'esto o None'.",
            },
            {
                "titulo": "Anotá estructuras de datos con List, Dict y tipos genéricos",
                "descripcion": "QUÉ: en vez de anotar solo 'list' o 'dict', especificá qué contienen: List[str], Dict[str, int]. POR QUÉ: saber que una lista es de strings (no de cualquier cosa) le permite a mypy (y a vos) detectar si en algún lugar estás metiendo un tipo incorrecto adentro.",
                "pista": "En Python 3.9+ podés usar list[str] y dict[str, int] directamente, sin necesidad de importar List y Dict desde typing.",
            },
            {
                "titulo": "Corré mypy de nuevo y corregí todos los errores",
                "descripcion": "QUÉ: ejecutá mypy sobre el proyecto ya anotado, y arreglá cada error que reporte (no lo ignores con # type: ignore salvo casos justificados). POR QUÉ: el punto de anotar tipos es justamente que la herramienta te avise de inconsistencias reales antes de que se conviertan en un bug en producción — ignorar los errores sin entenderlos anula el beneficio completo del ejercicio.",
                "pista": "Si mypy se queja de algo que estás seguro que es correcto, es más probable que tu anotación esté mal (demasiado estricta o demasiado floja) que que mypy esté equivocado — revisala de nuevo antes de silenciar el error.",
            },
        ],
        "criterios": [
            "Todas las funciones del proyecto anotado tienen tipos en sus parámetros y su retorno.",
            "Se usa Optional o Union en al menos un caso donde realmente corresponde (un valor que puede faltar o ser de más de un tipo).",
            "mypy corre sobre el proyecto sin errores (o con errores justificados y documentados, no ignorados sin razón).",
        ],
        "retos_extra": [
            "Configurá mypy en modo estricto (--strict) y ajustá tu código para que pase igual.",
            "Investigá qué es un Protocol en typing y en qué se diferencia de heredar de una clase abstracta.",
        ],
    },
    {
        "id": 27,
        "disponible_en_ide": "no",
        "titulo": "Documentación de código y APIs: docstrings con criterio",
        "descripcion": "Documentar todo es tan malo como no documentar nada — aprendé a elegir qué merece una explicación, y aprovechá que FastAPI ya te regala documentación automática.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1 hora",
        "conceptos": ["docstrings", "README", "OpenAPI/Swagger", "documentación técnica"],
        "xp": 150,
        "objetivo": "Aplicar criterio real sobre qué documentar (y qué no) en un proyecto Python: docstrings útiles en vez de redundantes, un README profesional, y aprovechar la documentación automática que FastAPI genera para mejorarla con descripciones claras.",
        "requisitos": ["Módulo: Funciones avanzadas", "Módulo: Mini API con FastAPI"],
        "pasos": [
            {
                "titulo": "Identificá qué NO necesita docstring",
                "descripcion": "QUÉ: revisá un proyecto tuyo y marcá funciones cuyo nombre y firma ya explican todo lo necesario (por ejemplo def sumar(a: int, b: int) -> int). POR QUÉ: un docstring que solo repite lo que el nombre de la función ya dice ('Suma a y b') no aporta nada y solo agrega ruido que hay que mantener actualizado.",
                "pista": "Si podés borrar el docstring y el código sigue siendo igual de entendible, probablemente no hacía falta.",
            },
            {
                "titulo": "Escribí docstrings donde realmente aportan",
                "descripcion": "QUÉ: agregá docstrings a funciones donde el nombre NO explica todo: comportamiento no obvio, casos borde, o por qué se hace algo de una forma particular (no qué hace). POR QUÉ: el valor real de un docstring está en explicar lo que el código por sí solo no puede mostrar — el razonamiento detrás, no la traducción línea por línea de lo que ya es legible.",
                "pista": "Si estás por escribir 'Esta función recorre la lista y suma los elementos', pará — eso ya lo dice el código. Si en cambio necesitás explicar 'por qué se ignoran los valores negativos acá', eso sí vale la pena.",
            },
            {
                "titulo": "Escribí un README profesional",
                "descripcion": "QUÉ: armá un README.md con: qué hace el proyecto, cómo instalarlo, cómo correrlo, y un ejemplo de uso. POR QUÉ: un README es lo primero (a veces lo único) que alguien lee antes de decidir si usar, contribuir, o incluso seguir mirando tu proyecto — sin uno, hasta un proyecto excelente parece abandonado.",
                "pista": "Probá seguir tu propio README desde cero, como si fueras alguien que nunca vio el proyecto — si algún paso te genera dudas, a otra persona también se las va a generar.",
            },
            {
                "titulo": "Mejorá la documentación automática de FastAPI",
                "descripcion": "QUÉ: en tus endpoints de FastAPI, agregá descripciones a los parámetros y al endpoint en sí (usando el parámetro description, o el docstring de la función, que FastAPI toma automáticamente para el Swagger). POR QUÉ: FastAPI ya te genera documentación interactiva en /docs sin que hagas nada — pero sin descripciones, esa documentación es solo una lista de endpoints sin contexto de qué esperan o para qué sirven.",
                "pista": "El docstring de una función de ruta en FastAPI aparece automáticamente como la descripción de ese endpoint en /docs — probá agregar uno y recargar la página de Swagger para ver el cambio en vivo.",
            },
            {
                "titulo": "Revisá /docs y compará antes/después",
                "descripcion": "QUÉ: abrí /docs de tu API antes y después de agregar las descripciones, y compará qué tan clara es para alguien que nunca vio tu código. POR QUÉ: esto demuestra en la práctica que documentar bien un endpoint no es trabajo extra desperdiciado — FastAPI lo convierte automáticamente en documentación real que cualquiera puede usar para entender tu API sin leer el código fuente.",
                "pista": "Fijate especialmente en los ejemplos de request/response que Swagger genera automáticamente a partir de tus modelos Pydantic — son gratis si tus modelos están bien tipados.",
            },
        ],
        "criterios": [
            "El proyecto distingue entre funciones que necesitan docstring y las que no, con criterio explicado.",
            "Existe un README.md con instalación, uso, y al menos un ejemplo concreto.",
            "Al menos 3 endpoints de FastAPI tienen descripciones visibles en /docs que antes no tenían.",
        ],
        "retos_extra": [
            "Agregá ejemplos de request/response custom en tus modelos Pydantic usando Config.json_schema_extra.",
            "Generá documentación de tu código Python (no la API) con una herramienta como pdoc o Sphinx.",
        ],
    },
    {
        "id": 28,
        "disponible_en_ide": "no",
        "titulo": "Publicá tu propio paquete en PyPI",
        "descripcion": "De un script suelto a algo instalable con pip install — estructura de paquete, versionado semántico y publicación real (o simulada) en TestPyPI.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["pyproject.toml", "estructura de paquetes", "versionado semántico", "PyPI", "TestPyPI"],
        "xp": 200,
        "objetivo": "Convertir un módulo de utilidades propio en un paquete Python instalable, con la estructura, el pyproject.toml y el versionado correctos, y publicarlo (real o simuladamente) en TestPyPI.",
        "requisitos": ["Proyecto: Entorno profesional: venv, pip y estructura de proyecto"],
        "pasos": [
            {
                "titulo": "Elegí (o armá) un módulo simple para empaquetar",
                "descripcion": "QUÉ: tomá algunas funciones de utilidad propias (por ejemplo, un conjunto de validadores, o el cache del proyecto de Diseño de sistemas) y organizalas en una carpeta con la estructura de un paquete instalable. POR QUÉ: necesitás algo real y chico para practicar todo el proceso de empaquetado sin distraerte con la complejidad del contenido en sí.",
                "pista": "La estructura típica es una carpeta con el nombre de tu paquete, adentro un __init__.py, y afuera de esa carpeta el pyproject.toml y el README.",
            },
            {
                "titulo": "Escribí el pyproject.toml",
                "descripcion": "QUÉ: creá el archivo pyproject.toml con el nombre del paquete, versión, descripción, autor, y dependencias (si tiene alguna). POR QUÉ: este archivo es el que le dice a pip (y a PyPI) todo lo que necesita saber para instalar y describir tu paquete — sin él, no hay paquete que publicar.",
                "pista": "El campo 'name' en pyproject.toml tiene que ser único en todo PyPI si pensás publicarlo de verdad — probá con un nombre bien específico o un sufijo random para evitar colisiones.",
            },
            {
                "titulo": "Aplicá versionado semántico",
                "descripcion": "QUÉ: elegí una versión inicial (por ejemplo 0.1.0) siguiendo el formato MAYOR.MENOR.PARCHE, y explicá qué cambiaría cada número. POR QUÉ: el versionado semántico le comunica a quien usa tu paquete qué tan seguro es actualizar: un cambio de PARCHE no debería romper nada, uno de MENOR agrega funcionalidad compatible, uno de MAYOR puede romper compatibilidad.",
                "pista": "Pensá en un ejemplo concreto: si arreglás un bug sin cambiar cómo se usa tu paquete, subís el PARCHE (0.1.0 a 0.1.1); si agregás una función nueva sin tocar las existentes, subís el MENOR (0.1.1 a 0.2.0); si cambiás la firma de una función existente, subís el MAYOR (0.2.0 a 1.0.0).",
            },
            {
                "titulo": "Construí el paquete",
                "descripcion": "QUÉ: usá 'python -m build' (o el comando equivalente) para generar los archivos de distribución (.whl y .tar.gz) a partir de tu pyproject.toml. POR QUÉ: estos son los archivos concretos que se suben a PyPI y que pip descarga cuando alguien instala tu paquete — es el paso que convierte tu código fuente en algo distribuible.",
                "pista": "Si el build falla, casi siempre es porque falta algo en el pyproject.toml (como la sección [build-system]) — copiá la estructura mínima de la documentación oficial de packaging.python.org si te trabás.",
            },
            {
                "titulo": "Publicá (o simulá publicar) en TestPyPI",
                "descripcion": "QUÉ: creá una cuenta en test.pypi.org (el entorno de pruebas separado del PyPI real) y subí tu paquete con twine, o si preferís no crear cuentas, documentá paso a paso cómo se haría. POR QUÉ: TestPyPI existe exactamente para esto: practicar el proceso de publicación real sin arriesgarte a romper o ensuciar el índice público de paquetes de verdad.",
                "pista": "'twine upload --repository testpypi dist/*' es el comando típico — necesitás un token de API de tu cuenta de TestPyPI, nunca tu contraseña directa.",
            },
        ],
        "criterios": [
            "El proyecto tiene la estructura de un paquete instalable con pyproject.toml completo.",
            "La versión sigue el formato semántico MAYOR.MENOR.PARCHE con una explicación de qué significaría subir cada número.",
            "El paquete se construyó exitosamente generando archivos .whl y/o .tar.gz.",
            "Se completó (o se documentó paso a paso) la publicación en TestPyPI.",
        ],
        "retos_extra": [
            "Instalá tu propio paquete desde TestPyPI en un entorno virtual limpio para confirmar que funciona como un usuario real lo experimentaría.",
            "Agregá una GitHub Action que construya y publique el paquete automáticamente cuando se cree un nuevo tag de versión.",
        ],
    },
    {
        "id": 29,
        "disponible_en_ide": "no",
        "titulo": "El patrón Middleware: cómo funciona por dentro",
        "descripcion": "Cada vez que usás CORS o autenticación en FastAPI, hay un middleware trabajando — armá los tuyos propios y entendé exactamente qué hacen.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["middleware", "FastAPI", "patrón de diseño", "interceptores"],
        "xp": 200,
        "objetivo": "Entender cómo funciona un middleware por dentro implementando 2-3 middlewares propios en FastAPI: uno de logging de requests, uno que mida tiempos de respuesta, y uno de autenticación simple como middleware (no como dependencia).",
        "requisitos": ["Módulo: Mini API con FastAPI", "Módulo: Funciones avanzadas"],
        "pasos": [
            {
                "titulo": "Explicá qué es un middleware con tus palabras",
                "descripcion": "QUÉ: describí el patrón middleware: código que se ejecuta ANTES y/o DESPUÉS de cada request, envolviendo a los endpoints reales. POR QUÉ: entender esta idea de 'capas que envuelven' es la base para poder razonar sobre en qué orden se ejecutan varios middlewares juntos, y por qué el orden importa.",
                "pista": "Pensá en un middleware como una cebolla: cada capa envuelve a la siguiente, el request atraviesa las capas de afuera hacia adentro, y la respuesta las atraviesa de adentro hacia afuera de vuelta.",
            },
            {
                "titulo": "Implementá un middleware de logging",
                "descripcion": "QUÉ: escribí un middleware con @app.middleware('http') que loguee el método y el path de cada request que llega. POR QUÉ: esto te deja ver en la práctica que el middleware se ejecuta para TODOS los endpoints automáticamente, sin tener que agregar código repetido en cada uno.",
                "pista": "La función de middleware recibe (request, call_next) — llamá a 'await call_next(request)' para que el request siga su curso hacia el endpoint real, y guardá lo que devuelve como la respuesta.",
            },
            {
                "titulo": "Implementá un middleware que mida tiempos de respuesta",
                "descripcion": "QUÉ: medí cuánto tarda call_next(request) en resolver, y agregá esa duración como un header en la respuesta (por ejemplo X-Process-Time). POR QUÉ: esto es exactamente el mismo patrón que usan las herramientas de monitoreo reales para medir performance sin modificar cada endpoint individualmente — y conecta con lo que viste en el proyecto de Observabilidad.",
                "pista": "Podés modificar response.headers directamente antes de devolver la respuesta, ya que la tenés disponible después del await call_next(request).",
            },
            {
                "titulo": "Implementá autenticación simple como middleware",
                "descripcion": "QUÉ: escribí un middleware que revise un header (por ejemplo X-API-Key) y rechace el request con 401 si no está o es incorrecto, ANTES de que llegue al endpoint. POR QUÉ: esto muestra la diferencia práctica entre resolver algo como middleware (se aplica a todo automáticamente) versus como dependencia de FastAPI (hay que agregarla explícitamente a cada endpoint que la necesite) — cada enfoque tiene su lugar según si la regla aplica a TODA la API o solo a algunos endpoints.",
                "pista": "Si el middleware detecta que falta o es inválida la key, podés devolver directamente una respuesta (por ejemplo con JSONResponse) sin llamar a call_next — así el request nunca llega al endpoint real.",
            },
            {
                "titulo": "Ordená varios middlewares y observá el orden de ejecución",
                "descripcion": "QUÉ: agregá los 2-3 middlewares juntos y logueá en qué orden se ejecuta cada uno (antes y después del endpoint). POR QUÉ: en FastAPI, el orden en que agregás los middlewares determina el orden real de ejecución — entender esto evita bugs sutiles, como un middleware de autenticación que se ejecuta DESPUÉS de uno que ya hizo trabajo costoso que no hacía falta hacer si el request iba a ser rechazado igual.",
                "pista": "Los middlewares agregados más tarde envuelven a los agregados antes — logueá un mensaje al principio y al final de cada uno para ver el orden real con tus propios ojos en la consola.",
            },
        ],
        "criterios": [
            "Existe una explicación propia de qué es un middleware y cómo envuelve a los endpoints.",
            "Hay al menos 2 middlewares propios funcionando: logging y medición de tiempos, como mínimo.",
            "Un middleware de autenticación simple rechaza requests sin la credencial correcta antes de llegar al endpoint.",
            "Se observó y se explica el orden real de ejecución cuando hay varios middlewares juntos.",
        ],
        "retos_extra": [
            "Compará el mismo chequeo de autenticación implementado como middleware vs como dependencia (Depends) de FastAPI, y explicá cuándo usarías cada enfoque.",
            "Agregá un middleware que capture cualquier excepción no manejada y devuelva una respuesta de error consistente en vez de que FastAPI muestre el error crudo.",
        ],
    },
    {
        "id": 30,
        "disponible_en_ide": "no",
        "titulo": "Arquitectura basada en eventos: colas de mensajes con Redis pub/sub",
        "descripcion": "Desacoplá tus servicios con mensajes en vez de llamadas directas — publicá eventos con Redis y dejá que otros procesos reaccionen sin que vos sepas quién los escucha.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["arquitectura basada en eventos", "Redis", "pub/sub", "desacoplamiento"],
        "xp": 200,
        "objetivo": "Entender el patrón de arquitectura basada en eventos implementando un publicador y un suscriptor con Redis pub/sub, para desacoplar dos procesos que hoy se llaman directamente.",
        "requisitos": ["Módulo: Concurrencia real: threading y multiprocessing", "Módulo: Manejo de errores"],
        "pasos": [
            {
                "titulo": "Instalá Redis (o corré un contenedor)",
                "descripcion": "QUÉ: instalá Redis localmente, o levantá un contenedor con 'docker run -p 6379:6379 redis'. POR QUÉ: pub/sub es una funcionalidad nativa de Redis — necesitás una instancia corriendo antes de poder publicar o suscribirte a nada.",
                "pista": "Si no querés instalar nada en tu sistema, 'docker run -d -p 6379:6379 redis' es la forma más rápida de tener Redis corriendo en un minuto.",
            },
            {
                "titulo": "Escribí un suscriptor que escuche un canal",
                "descripcion": "QUÉ: con la librería redis de Python, conectate y suscribite a un canal (por ejemplo 'notificaciones'), y quedate escuchando mensajes que lleguen. POR QUÉ: un suscriptor no sabe (ni le importa) quién le va a mandar mensajes — solo escucha el canal, que es la esencia del desacoplamiento en este patrón.",
                "pista": "pubsub = r.pubsub(); pubsub.subscribe('notificaciones'); for mensaje in pubsub.listen(): ... es el patrón básico de un suscriptor bloqueante.",
            },
            {
                "titulo": "Escribí un publicador que emita eventos",
                "descripcion": "QUÉ: en otro script (o proceso), publicá mensajes al mismo canal con r.publish('notificaciones', mensaje). POR QUÉ: el publicador tampoco sabe quién (ni cuántos) está escuchando — solo emite el evento y sigue con lo suyo, sin esperar respuesta.",
                "pista": "Corré el publicador y el suscriptor en dos terminales distintas al mismo tiempo para ver el mensaje llegar en tiempo real.",
            },
            {
                "titulo": "Desacoplá dos partes de un proyecto anterior con este patrón",
                "descripcion": "QUÉ: tomá dos partes de un proyecto tuyo que hoy se llaman directamente (por ejemplo, 'crear tarea' que directamente envía un email), y separalas: una publica un evento 'tarea_creada', la otra se suscribe y reacciona. POR QUÉ: esto demuestra el beneficio real del patrón — podés agregar un tercer suscriptor (por ejemplo, un log de auditoría) sin tocar el código que crea la tarea.",
                "pista": "Pensá qué pasaría si mañana agregás una función nueva que también necesita reaccionar a 'tarea_creada' — con llamadas directas tendrías que modificar el código original, con eventos solo agregás otro suscriptor.",
            },
            {
                "titulo": "Explicá los trade-offs de este enfoque",
                "descripcion": "QUÉ: describí con tus palabras qué ganás (desacoplamiento, poder agregar suscriptores sin tocar el publicador) y qué perdés (es más difícil rastrear el flujo completo, y con pub/sub simple los mensajes se pierden si nadie está escuchando en ese momento). POR QUÉ: ninguna arquitectura es gratis — entender los costos reales de este patrón es lo que te permite decidir cuándo vale la pena usarlo y cuándo un llamado directo es más simple y suficiente.",
                "pista": "Investigá la diferencia entre pub/sub simple (lo que hiciste acá, sin persistencia) y una cola de mensajes real con persistencia (como Redis Streams o RabbitMQ) — esa diferencia es clave para saber cuándo cada uno alcanza.",
            },
        ],
        "criterios": [
            "Redis está corriendo y accesible desde el código Python.",
            "El suscriptor recibe en tiempo real mensajes publicados por un proceso separado.",
            "Al menos dos partes de un proyecto anterior quedaron desacopladas usando este patrón.",
            "Existe una explicación propia de los trade-offs de arquitectura basada en eventos frente a llamadas directas.",
        ],
        "retos_extra": [
            "Agregá un segundo suscriptor al mismo canal y verificá que ambos reciben el mismo mensaje.",
            "Investigá Redis Streams y en qué se diferencia de pub/sub simple para casos donde no podés permitirte perder mensajes.",
        ],
    },
]


# ═══════════════════════════════════ JAVASCRIPT ═══════════════════════════════════
PROYECTOS_JAVASCRIPT = [
    {
        "id": 1,
        "disponible_en_ide": "si",
        "titulo": "Cajero automático (ATM) simulado",
        "descripcion": "Simulá un cajero en consola con Node.js: consultar saldo, depositar y retirar, protegido con PIN.",
        "dificultad": "Principiante+",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["POO", "encapsulamiento", "menús por consola con Node.js"],
        "xp": 175,
        "objetivo": "Simular un cajero automático en la terminal usando Node.js: consultar saldo, depositar y retirar dinero, protegido por un PIN de acceso.",
        "requisitos": ["Módulo: Variables: let y const", "Módulo: Arrow functions", "Módulo: Bucles"],
        "pasos": [
            {
                "titulo": "Diseñá la clase CuentaBancaria",
                "descripcion": "QUÉ: usá class con campos privados (con #) para saldo y pin, y métodos para consultar, depositar y retirar. POR QUÉ: encapsular el saldo evita que se modifique directamente desde afuera de la clase, como en un cajero real.",
                "pista": "Los campos privados de JS se declaran con #saldo dentro de la clase, y solo son accesibles desde sus propios métodos.",
            },
            {
                "titulo": "Validá el PIN antes de cualquier operación",
                "descripcion": "QUÉ: un método verificarPin(intento) que compare contra el PIN privado. POR QUÉ: es la barrera de seguridad mínima de cualquier sistema bancario.",
                "pista": "El método puede devolver un booleano, y las demás operaciones pueden chequearlo antes de ejecutarse.",
            },
            {
                "titulo": "Implementá depositar y retirar con reglas",
                "descripcion": "QUÉ: retirar() debe rechazar montos mayores al saldo disponible; ambos métodos deben rechazar montos negativos o iguales a cero. POR QUÉ: sin estas validaciones el 'banco' podría terminar en números negativos, algo que no pasa en la vida real.",
                "pista": "Podés hacer que los métodos devuelvan true/false según si la operación se pudo realizar, para poder mostrar el resultado en el menú.",
            },
            {
                "titulo": "Armá un menú interactivo con readline",
                "descripcion": "QUÉ: usá el módulo readline de Node para leer opciones del usuario en un loop (consultar/depositar/retirar/salir). POR QUÉ: es la forma estándar de leer input interactivo en un script de Node.js, similar a cin en C++ o input() en Python.",
                "pista": "require('readline').createInterface({ input: process.stdin, output: process.stdout }) te da un objeto con .question() para pedir datos.",
            },
            {
                "titulo": "Mostrá mensajes claros en cada operación",
                "descripcion": "QUÉ: después de cada acción, mostrá el resultado (éxito, error, nuevo saldo). POR QUÉ: un cajero sin feedback claro genera desconfianza en el usuario real.",
                "pista": "console.log con template literals (`Saldo actual: $${saldo}`) hace los mensajes más legibles.",
            },
        ],
        "criterios": [
            "El PIN incorrecto bloquea el acceso a las operaciones.",
            "No se puede retirar más saldo del disponible.",
            "El menú funciona en loop hasta que el usuario elige salir.",
        ],
        "retos_extra": [
            "Agregá un límite de 3 intentos de PIN antes de bloquear la sesión.",
            "Agregá un historial de transacciones.",
            "Soportá múltiples cuentas simultáneas.",
        ],
    },
    {
        "id": 2,
        "disponible_en_ide": "si",
        "titulo": "Sistema de gestión de estudiantes (CRUD)",
        "descripcion": "Programa en Node.js para crear, leer, actualizar y eliminar estudiantes guardados en memoria.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "2 horas",
        "conceptos": ["clases", "arrays", "colecciones (Map)"],
        "xp": 200,
        "objetivo": "Construir un sistema CRUD (crear, leer, actualizar, eliminar) para gestionar estudiantes guardados en memoria.",
        "requisitos": ["Módulo: Arrays: map, filter, reduce", "Módulo: Arrow functions"],
        "pasos": [
            {
                "titulo": "Diseñá la clase Estudiante",
                "descripcion": "QUÉ: definí sus atributos: id, nombre, materias (array), promedio. POR QUÉ: necesitás una forma consistente de representar cada estudiante antes de poder gestionarlos.",
                "pista": "El constructor puede generar el id automáticamente en vez de pedirlo como parámetro.",
            },
            {
                "titulo": "Elegí dónde guardarlos",
                "descripcion": "QUÉ: decidí entre un array de objetos o un Map indexado por id. POR QUÉ: un Map te da búsqueda por id en tiempo constante, útil cuando el CRUD crece; un array es más simple para empezar.",
                "pista": "Un Map se recorre igual que un array con for...of, pero accede por clave con .get(id) en vez de buscar linealmente.",
            },
            {
                "titulo": "Implementá Create y Read",
                "descripcion": "QUÉ: funciones para agregar un estudiante nuevo y para listar todos o buscar uno por id. POR QUÉ: son las operaciones más básicas de cualquier sistema CRUD.",
                "pista": "La función de listar puede usar .map() para transformar los datos antes de mostrarlos, por ejemplo formateando el promedio.",
            },
            {
                "titulo": "Implementá Update",
                "descripcion": "QUÉ: una función que reciba un id y los campos a modificar, y actualice solo esos campos. POR QUÉ: actualizar parcialmente (no reemplazar todo el objeto) es el comportamiento esperado en un sistema real.",
                "pista": "El spread operator te sirve para fusionar los campos nuevos sobre el objeto existente: { ...estudiante, ...cambios }.",
            },
            {
                "titulo": "Implementá Delete y un poco de reporting",
                "descripcion": "QUÉ: eliminar un estudiante por id, y una función que calcule el promedio general con reduce(). POR QUÉ: completa el ciclo CRUD y te da la oportunidad de aplicar los métodos funcionales de arrays que ya conocés.",
                "pista": "reduce((acc, e) => acc + e.promedio, 0) / total te da el promedio general de todos los estudiantes.",
            },
        ],
        "criterios": [
            "Las 4 operaciones (crear, leer, actualizar, eliminar) funcionan correctamente sobre los datos en memoria.",
            "Actualizar un estudiante no rompe ni duplica a los demás.",
            "Eliminar un id inexistente no crashea el programa.",
        ],
        "retos_extra": [
            "Exponé el CRUD como una mini API con Express.",
            "Agregá validación de datos (nombre no vacío, promedio entre 0 y 10).",
            "Persistí los datos en un archivo JSON entre ejecuciones.",
        ],
    },
    {
        "id": 3,
        "disponible_en_ide": "no",
        "titulo": "Juego del ahorcado con interfaz web (DOM)",
        "descripcion": "Ahorcado jugable en el navegador: se elige una palabra al azar y se adivina letra por letra con un teclado en pantalla.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["DOM", "manejo de eventos", "arreglos"],
        "xp": 200,
        "objetivo": "Construir el juego del ahorcado jugable en el navegador, donde el jugador adivina una palabra secreta haciendo clic en letras de un teclado en pantalla.",
        "requisitos": ["Módulo: DOM y eventos"],
        "pasos": [
            {
                "titulo": "Armá el HTML base",
                "descripcion": "QUÉ: un contenedor para la palabra oculta (guiones bajos), un contenedor para el teclado y un contador de intentos. POR QUÉ: necesitás la estructura visual antes de conectarle la lógica de JavaScript.",
                "pista": "Podés usar divs vacíos con id, que vas a ir llenando dinámicamente desde JS.",
            },
            {
                "titulo": "Elegí una palabra al azar y ocultala",
                "descripcion": "QUÉ: armá un array de palabras posibles, elegí una al azar y mostrá tantos guiones bajos como letras tiene. POR QUÉ: es el estado inicial del juego.",
                "pista": "Math.floor(Math.random() * array.length) te da un índice al azar dentro del array.",
            },
            {
                "titulo": "Generá el teclado dinámicamente",
                "descripcion": "QUÉ: creá un botón por cada letra del abecedario con createElement(), agregándolos al contenedor del teclado. POR QUÉ: escribir 27 botones a mano en el HTML sería repetitivo y difícil de mantener; generarlos con JS es mucho más flexible.",
                "pista": "Podés recorrer un string 'abcdefghijklmnopqrstuvwxyz' con un for...of para crear cada botón.",
            },
            {
                "titulo": "Manejá el clic en cada letra",
                "descripcion": "QUÉ: con addEventListener, si la letra está en la palabra revelala en su posición correspondiente; si no está, restá un intento y deshabilitá el botón. POR QUÉ: es la mecánica central del juego.",
                "pista": "includes() te dice si un carácter está en la palabra secreta. Deshabilitá el botón con boton.disabled = true para que no se pueda usar de nuevo.",
            },
            {
                "titulo": "Detectá victoria o derrota",
                "descripcion": "QUÉ: después de cada clic, revisá si ya no quedan guiones sin revelar (ganó) o si los intentos llegaron a cero (perdió), y mostrá el mensaje correspondiente. POR QUÉ: sin esta lógica el juego nunca comunica su resultado final al jugador.",
                "pista": "Podés comparar la palabra oculta actual contra la palabra secreta completa para saber si ya se reveló entera.",
            },
        ],
        "criterios": [
            "El teclado se genera dinámicamente con JavaScript, no está escrito letra por letra en el HTML.",
            "El juego detecta correctamente cuándo se ganó o se perdió.",
            "Las letras ya usadas quedan deshabilitadas para no poder repetirlas.",
        ],
        "retos_extra": [
            "Agregá un dibujo del ahorcado que se vaya completando con cada error (con CSS o SVG).",
            "Agregá categorías de palabras seleccionables.",
            "Guardá el puntaje en localStorage.",
        ],
    },
    {
        "id": 4,
        "disponible_en_ide": "no",
        "titulo": "Agenda de contactos con persistencia",
        "descripcion": "Agenda de contactos que guarda los datos entre sesiones usando localStorage.",
        "dificultad": "Intermedio+",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["serialización JSON", "localStorage", "objetos/Map"],
        "xp": 250,
        "objetivo": "Construir una agenda de contactos (nombre, teléfono, email) que persista los datos entre sesiones usando localStorage.",
        "requisitos": ["Módulo: Arrays: map, filter, reduce", "Módulo: DOM y eventos"],
        "pasos": [
            {
                "titulo": "Diseñá el modelo de contacto",
                "descripcion": "QUÉ: un objeto con id, nombre, telefono y email. POR QUÉ: necesitás una forma consistente antes de empezar a guardar nada.",
                "pista": "Date.now() es una forma simple y rápida de generar un id único para cada contacto nuevo.",
            },
            {
                "titulo": "Guardá y recuperá con localStorage",
                "descripcion": "QUÉ: usá localStorage.setItem() con JSON.stringify() para guardar el array de contactos, y JSON.parse() con getItem() para recuperarlo al cargar la página. POR QUÉ: localStorage solo guarda strings, por eso necesitás serializar y deserializar el array.",
                "pista": "Al iniciar la página, verificá si ya existe algo guardado; si no, empezá con un array vacío.",
            },
            {
                "titulo": "Implementá agregar contacto",
                "descripcion": "QUÉ: una función que valide los campos (nombre no vacío, email con formato básico) antes de agregarlo y volver a guardar. POR QUÉ: validar antes de persistir evita ensuciar tu 'base de datos' con datos incompletos.",
                "pista": "Un chequeo simple de email puede ser: email.includes('@') && email.includes('.').",
            },
            {
                "titulo": "Implementá buscar y eliminar",
                "descripcion": "QUÉ: una función de búsqueda por nombre (parcial, sin distinguir mayúsculas) y otra de eliminar por id. POR QUÉ: una agenda sin búsqueda deja de ser útil apenas tenés más de 10 contactos.",
                "pista": "filter() con toLowerCase().includes(texto) te da una búsqueda simple e insensible a mayúsculas.",
            },
            {
                "titulo": "Renderizá la lista actualizada",
                "descripcion": "QUÉ: cada vez que cambien los datos, volvé a dibujar la lista completa de contactos en el DOM. POR QUÉ: mantener la interfaz sincronizada con los datos es un patrón central en cualquier app interactiva.",
                "pista": "Una función renderizar() que limpie el contenedor y vuelva a crear un elemento por cada contacto simplifica mucho mantener todo sincronizado.",
            },
        ],
        "criterios": [
            "Los contactos siguen ahí después de recargar la página.",
            "Agregar valida los campos mínimos antes de guardar.",
            "Buscar y eliminar funcionan correctamente sobre los datos persistidos.",
        ],
        "retos_extra": [
            "Agregá edición de contactos existentes.",
            "Agregá favoritos marcables con una estrella.",
            "Exportá la agenda a un archivo JSON descargable.",
        ],
    },
    {
        "id": 5,
        "disponible_en_ide": "no",
        "titulo": "Chat cliente-servidor con WebSockets",
        "descripcion": "Chat en tiempo real donde varios clientes conectados a un servidor Node.js se envían mensajes entre sí.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "3-4 horas",
        "conceptos": ["WebSockets", "Node.js", "concurrencia con el event loop"],
        "xp": 300,
        "objetivo": "Construir un chat en tiempo real donde varios clientes conectados a un servidor Node.js puedan enviarse mensajes entre sí.",
        "requisitos": ["Módulo: Promesas y async/await", "Módulo: DOM y eventos"],
        "pasos": [
            {
                "titulo": "Investigá cómo funciona un WebSocket",
                "descripcion": "QUÉ: entendé la diferencia entre una petición HTTP normal (pedido/respuesta) y una conexión WebSocket (bidireccional y persistente). POR QUÉ: un chat en tiempo real necesita que el servidor pueda enviar mensajes al cliente sin que este los pida explícitamente, algo que HTTP normal no hace bien.",
                "pista": "Pensalo como una llamada telefónica (WebSocket, conexión abierta) contra enviar cartas (HTTP, un pedido a la vez).",
            },
            {
                "titulo": "Armá un servidor WebSocket básico",
                "descripcion": "QUÉ: usando una librería como ws, creá un servidor que acepte conexiones y loguee cuando un cliente se conecta. POR QUÉ: es la base sobre la que vas a construir toda la lógica de mensajería.",
                "pista": "npm install ws. El servidor emite un evento 'connection' cada vez que un cliente nuevo se conecta.",
            },
            {
                "titulo": "Enviá mensajes del cliente al servidor",
                "descripcion": "QUÉ: desde una página HTML simple, conectate al servidor y enviá un mensaje cuando el usuario lo escriba. POR QUÉ: necesitás el camino cliente → servidor antes de poder retransmitir nada.",
                "pista": "En el navegador: new WebSocket('ws://localhost:PUERTO') te da un objeto con .send() para mandar mensajes.",
            },
            {
                "titulo": "Retransmití el mensaje a todos los clientes conectados",
                "descripcion": "QUÉ: en el servidor, cuando llega un mensaje de un cliente, reenvialo a todos los demás clientes conectados (broadcast). POR QUÉ: es lo que convierte una simple conexión en un chat grupal real.",
                "pista": "Guardá todas las conexiones activas en un array o Set, y recorrelo para reenviar cada mensaje entrante.",
            },
            {
                "titulo": "Mostrá los mensajes entrantes en la interfaz",
                "descripcion": "QUÉ: en el cliente, escuchá el evento de mensaje entrante y agregalo a la lista de mensajes en el DOM. POR QUÉ: sin esto los mensajes llegan al navegador pero el usuario nunca los ve.",
                "pista": "socket.addEventListener('message', (evento) => { ... }) te da el contenido en evento.data.",
            },
        ],
        "criterios": [
            "Dos o más pestañas/clientes conectados pueden verse los mensajes entre sí en tiempo real.",
            "El servidor no se cae si un cliente se desconecta abruptamente.",
            "Los mensajes se muestran en el orden en que llegaron.",
        ],
        "retos_extra": [
            "Agregá nombres de usuario a los mensajes.",
            "Agregá salas de chat separadas.",
            "Agregá un indicador de 'usuario escribiendo...'.",
        ],
    },
    {
        "id": 6,
        "disponible_en_ide": "no",
        "titulo": "Tu primer repositorio: Git y GitHub para proyectos JS",
        "descripcion": "Versioná un proyecto de JavaScript con Git, trabajá con ramas y subilo a GitHub.",
        "dificultad": "Principiante+",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["control de versiones", "git", "ramas", "github"],
        "xp": 175,
        "objetivo": "Aprender a usar Git de verdad sobre un proyecto de JavaScript: guardar el historial en commits, trabajar con ramas, y publicar el resultado en GitHub sin subir basura como node_modules.",
        "requisitos": ["Cualquier proyecto propio en una carpeta (podés usar la Agenda de contactos con persistencia)"],
        "pasos": [
            {
                "titulo": "Inicializá el repositorio",
                "descripcion": "QUÉ: parado en la carpeta de tu proyecto, corré git init. POR QUÉ: eso crea la carpeta oculta .git donde Git guarda todo el historial de cambios, separado de tu código.",
                "pista": "git status te muestra en todo momento qué archivos están sin trackear, modificados, o listos para commitear.",
            },
            {
                "titulo": "Creá un .gitignore ANTES del primer commit",
                "descripcion": "QUÉ: un archivo .gitignore que excluya node_modules/, .env y archivos de build. POR QUÉ: node_modules puede pesar cientos de MB y se regenera con npm install — versionarlo es un error muy común en proyectos JS.",
                "pista": "Mínimo para JS: node_modules/, .env, dist/, .DS_Store — hacé esto ANTES de tu primer git add, si no node_modules ya quedó en el historial.",
            },
            {
                "titulo": "Configurá tu identidad y hacé el primer commit",
                "descripcion": "QUÉ: git config para tu nombre/email, git add para el staging area, git commit -m con un mensaje claro. POR QUÉ: cada commit es un punto al que podés volver si algo se rompe más adelante.",
                "pista": "git config --global user.name \"Tu Nombre\" — mensajes de commit en imperativo y cortos: \"Agrega validación de email\", no \"agregué cosas\".",
            },
            {
                "titulo": "Trabajá con ramas (branches)",
                "descripcion": "QUÉ: creá una rama con git switch -c, hacé cambios ahí, y mergeala de vuelta a main. POR QUÉ: te deja experimentar con una funcionalidad nueva sin arriesgar el código que ya funciona.",
                "pista": "git switch -c agregar-busqueda — después de terminar: git switch main && git merge agregar-busqueda",
            },
            {
                "titulo": "Subilo a GitHub",
                "descripcion": "QUÉ: creá un repo vacío en GitHub, conectalo con git remote add origin y subí con git push. POR QUÉ: tu código queda respaldado en la nube y disponible como portfolio.",
                "pista": "git remote add origin <url> — git push -u origin main. Agregá un package.json con 'npm init -y' si todavía no lo tenés, y un README.md explicando cómo correr el proyecto.",
            },
        ],
        "criterios": [
            "node_modules nunca aparece en el historial de Git (verificalo con git log --all --full-history -- node_modules).",
            "El proyecto tiene al menos 4 commits con mensajes descriptivos.",
            "Se usó al menos una rama separada que después se mergeó a main.",
            "El código está publicado en GitHub con un README que explica cómo instalarlo y correrlo.",
        ],
        "retos_extra": [
            "Provocá un conflicto de merge a propósito y resolvelo a mano.",
            "Agregá un GitHub Action que corra tus tests automáticamente en cada push.",
            "Escribí los commits siguiendo Conventional Commits (feat:, fix:, docs:).",
        ],
    },
    {
        "id": 7,
        "disponible_en_ide": "no",
        "titulo": "Debugging en el navegador: Chrome DevTools",
        "descripcion": "Dejá el console.log everywhere y aprendé a debuggear JS con las herramientas reales del navegador.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1 hora",
        "conceptos": ["devtools", "breakpoints", "call stack", "scope"],
        "xp": 175,
        "objetivo": "Aprender a pausar la ejecución de JavaScript en el navegador, inspeccionar variables en cada punto y navegar la pila de llamadas usando el panel Sources de Chrome DevTools.",
        "requisitos": ["Módulo: DOM y eventos"],
        "pasos": [
            {
                "titulo": "Reproducí un bug real en una página",
                "descripcion": "QUÉ: tomá tu Agenda de contactos (u otro proyecto con DOM) y provocá un comportamiento incorrecto, por ejemplo un contador que no se actualiza bien. POR QUÉ: necesitás un caso real para practicar, no alcanza con leer la teoría.",
                "pista": "Un bug clásico: usar == en vez de === y que una comparación de tipos distintos dé un resultado inesperado, o un event listener agregado dos veces por error.",
            },
            {
                "titulo": "Abrí el panel Sources y poné un breakpoint",
                "descripcion": "QUÉ: en DevTools (F12), andá a la pestaña Sources, buscá tu archivo .js y hacé click a la izquierda del número de línea donde sospechás el problema. POR QUÉ: eso pausa la ejecución exactamente ahí, cada vez que el navegador llega a esa línea.",
                "pista": "También podés escribir la palabra clave 'debugger;' directamente en tu código JS — tiene el mismo efecto que un breakpoint puesto a mano.",
            },
            {
                "titulo": "Inspeccioná el panel Scope y Call Stack",
                "descripcion": "QUÉ: con la ejecución pausada, mirá el panel Scope (variables locales, closures, globales) y el panel Call Stack (qué funciones llamaron a qué otras funciones para llegar hasta acá). POR QUÉ: ver el valor REAL de las variables en ese instante es mucho más confiable que suponer basándote en console.log de antes.",
                "pista": "Podés hacer hover sobre cualquier variable en el código para ver su valor actual sin ni siquiera abrir el panel Scope.",
            },
            {
                "titulo": "Navegá paso a paso con los controles de ejecución",
                "descripcion": "QUÉ: usá los botones (o atajos) Step over, Step into y Step out para avanzar de a una línea, entrar en funciones, o salir de la actual. POR QUÉ: te deja seguir el flujo exacto de ejecución en vez de adivinar qué código corrió.",
                "pista": "F10 es step over (ejecuta la línea sin entrar a funciones que llama), F11 es step into (entra a la función), Shift+F11 es step out (termina la función actual y vuelve a quien la llamó).",
            },
            {
                "titulo": "Usá la consola avanzada",
                "descripcion": "QUÉ: probá console.table() para mostrar arrays/objetos como tabla, console.trace() para ver la pila de llamadas sin pausar, y la pestaña Network para ver requests fetch/XHR reales. POR QUÉ: son herramientas que superan ampliamente a un console.log suelto para entender qué está pasando en tu app.",
                "pista": "console.table(misObjetos) es especialmente útil con arrays de objetos — te arma una tabla legible en vez de un montón de texto anidado.",
            },
        ],
        "criterios": [
            "Lograste pausar el código en un punto específico usando un breakpoint o la palabra debugger.",
            "Usaste el panel Scope para ver el valor real de una variable en el momento del bug.",
            "Navegaste con step over/into/out para seguir el flujo de ejecución.",
            "Identificaste la causa raíz del bug y lo corregiste, verificando el resultado.",
        ],
        "retos_extra": [
            "Configurá un breakpoint condicional (click derecho sobre la línea) que solo pare cuando una variable tiene cierto valor.",
            "Usá la pestaña Network para inspeccionar una petición fetch real: headers, respuesta, tiempo.",
            "Probá un breakpoint de tipo 'DOM breakpoint' que pause cuando un elemento específico del HTML cambia.",
        ],
    },
    {
        "id": 8,
        "disponible_en_ide": "no",
        "titulo": "Testing en JS con Jest",
        "descripcion": "Escribí tests automatizados para tu código JavaScript en vez de probarlo a mano cada vez.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["jest", "tests unitarios", "mocks", "coverage"],
        "xp": 200,
        "objetivo": "Aprender a escribir tests automatizados con Jest para funciones ya existentes, detectando si un cambio futuro rompe algo sin tener que probar todo a mano en la consola.",
        "requisitos": ["Módulo: Arrow functions", "Módulo: Sistema de inventario"],
        "pasos": [
            {
                "titulo": "Instalá Jest y escribí tu primer test",
                "descripcion": "QUÉ: instalá Jest como dependencia de desarrollo, creá un archivo suma.test.js con un test que use expect(). POR QUÉ: Jest detecta automáticamente cualquier archivo que termine en .test.js y corre las funciones test() que encuentre adentro.",
                "pista": "npm install --save-dev jest — un test mínimo: test('suma 2+2', () => { expect(2+2).toBe(4); }); — corré con: npx jest",
            },
            {
                "titulo": "Testeá una función real con múltiples casos",
                "descripcion": "QUÉ: elegí una función de tu Sistema de inventario (por ejemplo agregarProducto o calcularTotal) y escribí varios tests con el caso normal Y los límite (inventario vacío, cantidad negativa). POR QUÉ: los bugs se esconden en los casos límite, no en el camino feliz.",
                "pista": "describe('agregarProducto', () => { test('agrega un producto nuevo', () => {...}); test('rechaza cantidad negativa', () => {...}); }); — describe agrupa tests relacionados.",
            },
            {
                "titulo": "Usá mocks para aislar dependencias",
                "descripcion": "QUÉ: si tu función depende de otra (por ejemplo una que consulta una API), reemplazala con jest.fn() para controlar qué devuelve durante el test. POR QUÉ: un test unitario debe probar UNA función, no depender de que internet funcione o de que una API externa esté disponible.",
                "pista": "const fetchMock = jest.fn(() => Promise.resolve({ precio: 100 })); — así controlás exactamente qué devuelve sin llamar a la API real.",
            },
            {
                "titulo": "Probá casos asíncronos",
                "descripcion": "QUÉ: escribí un test para una función async, usando async/await dentro del test mismo. POR QUÉ: mucho código JS real es asíncrono (fetch, timers), y Jest necesita saber cuándo esperar a que termine antes de evaluar el resultado.",
                "pista": "test('trae los datos', async () => { const datos = await obtenerDatos(); expect(datos).toBeDefined(); });",
            },
            {
                "titulo": "Medí cobertura de código",
                "descripcion": "QUÉ: corré npx jest --coverage para ver qué porcentaje de tu código pasa por algún test. POR QUÉ: la cobertura te muestra puntos ciegos: funciones o ramas de código (if/else) que nunca se ejecutan durante los tests.",
                "pista": "El reporte te muestra % Stmts, % Branch, % Funcs y % Lines por archivo — apuntá primero a las funciones con 0% de cobertura.",
            },
        ],
        "criterios": [
            "Existen al menos 8 tests que cubren casos normales y casos límite.",
            "Se usó al menos un mock para aislar una dependencia externa.",
            "Hay al menos un test de una función asíncrona con async/await.",
            "npx jest --coverage muestra una cobertura razonable (apuntá a más del 70%).",
        ],
        "retos_extra": [
            "Agregá un test que verifique que una función lanza un error esperado con expect(...).toThrow().",
            "Configurá que los tests corran automáticamente antes de cada commit con un git hook.",
            "Agregá un script 'test:watch' en package.json que corra Jest en modo watch mientras programás.",
        ],
    },
    {
        "id": 9,
        "disponible_en_ide": "no",
        "titulo": "Bases de datos con SQL: SQLite desde Node.js",
        "descripcion": "Reemplazá localStorage o un JSON por una base de datos SQL real, sin instalar un servidor aparte.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "2 horas",
        "conceptos": ["SQL", "SQLite", "CRUD", "JOIN"],
        "xp": 225,
        "objetivo": "Aprender SQL básico (CREATE TABLE, INSERT, SELECT, UPDATE, DELETE, JOIN) usando SQLite desde Node.js, migrando tu Agenda de contactos de localStorage a una base de datos real.",
        "requisitos": ["Módulo: JSON: stringify y parse", "Módulo: Agenda de contactos con persistencia"],
        "pasos": [
            {
                "titulo": "Instalá el driver de SQLite y creá una tabla",
                "descripcion": "QUÉ: instalá better-sqlite3 (o usá el módulo node:sqlite si tu versión de Node lo trae), y definí una tabla contactos con CREATE TABLE. POR QUÉ: a diferencia de localStorage, SQL te obliga a definir de antemano qué columnas y tipos son válidos, evitando datos corruptos.",
                "pista": "npm install better-sqlite3 — const db = new Database('contactos.db'); db.exec('CREATE TABLE IF NOT EXISTS contactos (id INTEGER PRIMARY KEY, nombre TEXT, telefono TEXT)');",
            },
            {
                "titulo": "Insertá y consultá datos",
                "descripcion": "QUÉ: usá INSERT INTO para agregar contactos y SELECT * FROM para listarlos. POR QUÉ: son las operaciones más básicas de cualquier base de datos: guardar y recuperar.",
                "pista": "SIEMPRE usá parámetros (?) en vez de template literals para insertar valores: db.prepare('INSERT INTO contactos (nombre, telefono) VALUES (?, ?)').run(nombre, telefono) — esto previene inyección SQL.",
            },
            {
                "titulo": "Actualizá y eliminá con condiciones",
                "descripcion": "QUÉ: usá UPDATE ... WHERE y DELETE FROM ... WHERE para modificar o borrar un contacto específico. POR QUÉ: sin el WHERE, esas operaciones afectan a TODAS las filas de la tabla.",
                "pista": "db.prepare('UPDATE contactos SET telefono = ? WHERE id = ?').run(nuevoTelefono, id);",
            },
            {
                "titulo": "Relacioná dos tablas con JOIN",
                "descripcion": "QUÉ: creá una tabla grupos, vinculá cada contacto a un grupo con grupo_id, y usá SELECT ... JOIN para traer contactos junto con el nombre de su grupo. POR QUÉ: separar datos relacionados en tablas distintas es la base del diseño de bases de datos relacionales.",
                "pista": "SELECT contactos.nombre, grupos.nombre AS grupo FROM contactos JOIN grupos ON contactos.grupo_id = grupos.id",
            },
            {
                "titulo": "Migrá tu Agenda de contactos completa a SQLite",
                "descripcion": "QUÉ: reemplazá las funciones que leían/escribían en localStorage por funciones que usen la base de datos SQLite. POR QUÉ: es el mismo patrón de persistencia que ya conocés, solo cambia el motor de almacenamiento por dentro.",
                "pista": "El resto de tu código (agregar, buscar, eliminar contacto) no debería cambiar su interfaz pública — solo CÓMO se guardan y leen los datos.",
            },
        ],
        "criterios": [
            "Existe una base de datos SQLite con al menos dos tablas relacionadas.",
            "Todas las consultas con datos del usuario usan parámetros (?) y no template literals o concatenación.",
            "El CRUD completo funciona sobre la base de datos real.",
            "Al menos una consulta usa JOIN para combinar datos de ambas tablas.",
        ],
        "retos_extra": [
            "Agregá una tabla de historial que registre cada vez que se edita un contacto.",
            "Usá GROUP BY para contar cuántos contactos hay por grupo.",
            "Explorá el archivo .db con DB Browser for SQLite para ver los datos sin código.",
        ],
    },
    {
        "id": 10,
        "disponible_en_ide": "no",
        "titulo": "Node.js y npm: gestores de paquetes en JS",
        "descripcion": "Entendé package.json de una vez por todas y organizá las dependencias de tu proyecto como corresponde.",
        "dificultad": "Principiante+",
        "tiempo_estimado": "1 hora",
        "conceptos": ["npm", "package.json", "dependencias", "scripts"],
        "xp": 150,
        "objetivo": "Entender qué hace npm por debajo, para qué sirve package.json, la diferencia entre dependencies y devDependencies, y cómo usar scripts de npm para automatizar tareas del proyecto.",
        "requisitos": ["Módulo: Objetos: propiedades y métodos"],
        "pasos": [
            {
                "titulo": "Inicializá un proyecto con npm init",
                "descripcion": "QUÉ: corré npm init -y en una carpeta nueva y mirá el package.json que se genera. POR QUÉ: package.json es el 'documento de identidad' de cualquier proyecto Node — nombre, versión, dependencias y cómo correrlo, todo en un solo archivo.",
                "pista": "npm init -y salta las preguntas interactivas y usa valores por defecto — perfecto para empezar rápido y ajustar después a mano.",
            },
            {
                "titulo": "Instalá dependencias y observá qué cambia",
                "descripcion": "QUÉ: instalá una librería (por ejemplo, una de fecha o de validación) y mirá cómo se actualiza package.json y aparece package-lock.json. POR QUÉ: package.json guarda QUÉ necesitás en términos generales; package-lock.json fija las versiones EXACTAS de todo el árbol de dependencias, para builds reproducibles.",
                "pista": "npm install nombre-paquete la agrega a 'dependencies'. Nunca edites package-lock.json a mano — se regenera solo.",
            },
            {
                "titulo": "Diferenciá dependencies de devDependencies",
                "descripcion": "QUÉ: instalá algo que solo se usa durante desarrollo (como nodemon o eslint) con la flag --save-dev. POR QUÉ: en producción no necesitás herramientas de desarrollo — separarlas mantiene el deploy final más liviano y claro sobre qué es esencial para que la app funcione.",
                "pista": "npm install --save-dev nodemon la agrega a 'devDependencies' en vez de 'dependencies'.",
            },
            {
                "titulo": "Definí scripts en package.json",
                "descripcion": "QUÉ: agregá scripts personalizados en la sección 'scripts' (por ejemplo 'start', 'dev', 'test') para no tener que recordar comandos largos. POR QUÉ: cualquiera que clone tu proyecto puede correr npm run dev sin necesidad de saber qué comando exacto hay detrás.",
                "pista": "\"scripts\": { \"start\": \"node index.js\", \"dev\": \"nodemon index.js\" } — después corré con npm run dev (o npm start, que es un caso especial sin 'run').",
            },
            {
                "titulo": "Usá npx para ejecutar paquetes sin instalarlos globalmente",
                "descripcion": "QUÉ: corré una herramienta con npx nombre-paquete en vez de instalarla globalmente. POR QUÉ: evita ensuciar tu sistema con instalaciones globales y siempre usa la versión que corresponde a ese proyecto específico.",
                "pista": "npx create-react-app o npx cowsay 'hola' son ejemplos típicos — npx descarga y ejecuta sin dejar el paquete instalado permanentemente.",
            },
        ],
        "criterios": [
            "El proyecto tiene un package.json válido con nombre, versión y al menos una dependencia real.",
            "Las herramientas de desarrollo están en devDependencies, no mezcladas con dependencies de producción.",
            "Existen al menos 2 scripts personalizados en package.json que simplifican comandos usados seguido.",
            "package-lock.json existe y no fue editado a mano.",
        ],
        "retos_extra": [
            "Investigá qué son los rangos de versiones semver (^1.2.3 vs ~1.2.3 vs 1.2.3 exacto) y por qué importan.",
            "Agregá un script 'postinstall' que corra automáticamente después de npm install.",
            "Probá npm audit para detectar vulnerabilidades conocidas en tus dependencias.",
        ],
    },
    {
        "id": 11,
        "disponible_en_ide": "no",
        "titulo": "Código limpio: ESLint, Prettier y logging profesional",
        "descripcion": "Dejá que las herramientas encuentren tus errores de estilo, y reemplazá los console.log por un logging con criterio.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["eslint", "prettier", "logging", "clean code"],
        "xp": 175,
        "objetivo": "Incorporar ESLint y Prettier para detectar problemas y mantener un estilo consistente, y reemplazar los console.log desordenados por un logging con niveles de severidad reales.",
        "requisitos": ["Módulo: Sistema de inventario"],
        "pasos": [
            {
                "titulo": "Configurá ESLint en tu proyecto",
                "descripcion": "QUÉ: instalá ESLint, inicializalo con npx eslint --init, y corré npx eslint . sobre tu código. POR QUÉ: ESLint detecta automáticamente problemas reales (variables no usadas, comparaciones con == en vez de ===, código inalcanzable) que a simple vista se pasan por alto.",
                "pista": "npm install --save-dev eslint — npx eslint --init te hace preguntas para configurar las reglas — después: npx eslint .",
            },
            {
                "titulo": "Formateá automáticamente con Prettier",
                "descripcion": "QUÉ: instalá Prettier y corré npx prettier --write . para reformatear tu código con un estilo consistente. POR QUÉ: discutir sobre espacios, comillas o punto y coma en un equipo es tiempo perdido — Prettier elimina esa discusión aplicando un único estilo automáticamente.",
                "pista": "npm install --save-dev prettier — npx prettier --write . reformatea TODOS los archivos del proyecto (revisá el diff antes de commitear).",
            },
            {
                "titulo": "Reemplazá console.log por niveles de logging",
                "descripcion": "QUÉ: usá una librería simple (o funciones propias) para loguear con niveles: debug, info, warn, error. POR QUÉ: con niveles podés filtrar qué mostrar según el ambiente (todo en desarrollo, solo errores en producción), algo que console.log suelto no te permite.",
                "pista": "Podés armar algo simple vos mismo: const log = { info: (...a) => console.log('[INFO]', ...a), error: (...a) => console.error('[ERROR]', ...a) }; o usar una librería como pino o winston.",
            },
            {
                "titulo": "Agregá timestamp y contexto a cada log",
                "descripcion": "QUÉ: hacé que cada mensaje de log incluya la fecha/hora y de qué parte del código viene. POR QUÉ: un log sin contexto ('Error') es casi inútil para debuggear después — necesitás saber CUÁNDO pasó y EN QUÉ función.",
                "pista": "new Date().toISOString() te da un timestamp estándar. Podés armar un wrapper: const log = (nivel, origen, msg) => console.log(`[${new Date().toISOString()}] [${nivel}] [${origen}] ${msg}`);",
            },
            {
                "titulo": "Configurá ESLint y Prettier para que no choquen entre sí",
                "descripcion": "QUÉ: instalá eslint-config-prettier para desactivar las reglas de formato de ESLint que pisan a Prettier. POR QUÉ: sin esto, ESLint y Prettier pueden 'pelearse' proponiendo formatos distintos para la misma línea.",
                "pista": "npm install --save-dev eslint-config-prettier — agregalo al final del array 'extends' en tu configuración de ESLint para que tenga la última palabra sobre reglas de formato.",
            },
        ],
        "criterios": [
            "npx eslint . corre sobre el proyecto sin errores graves (solo, como mucho, warnings menores).",
            "El código está formateado consistentemente con Prettier.",
            "No quedan console.log sueltos de debugging — todos los logs pasan por un sistema con niveles.",
            "Cada log incluye al menos timestamp y nivel de severidad.",
        ],
        "retos_extra": [
            "Configurá ESLint y Prettier para que corran automáticamente antes de cada commit con husky + lint-staged.",
            "Agregá una regla custom de ESLint que prohíba el uso de console.log directo en el código (para forzar el uso de tu logger).",
            "Investigá niveles de log configurables por variable de entorno (LOG_LEVEL=debug vs LOG_LEVEL=error).",
        ],
    },
    {
        "id": 12,
        "disponible_en_ide": "no",
        "titulo": "Deploy básico: subí tu app JS a internet",
        "descripcion": "Llevá tu app de Node de 'funciona en mi máquina' a una URL pública y accesible desde cualquier lado.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["variables de entorno en producción", "Docker (noción)", "deploy", "CI/CD básico"],
        "xp": 200,
        "objetivo": "Preparar una aplicación Node/JS para producción y publicarla en un servicio de hosting gratuito, entendiendo qué cambia entre correr algo localmente y tenerlo disponible públicamente.",
        "requisitos": ["Módulo: Promesas y async/await"],
        "pasos": [
            {
                "titulo": "Preparé la app para producción",
                "descripcion": "QUÉ: revisá que ningún secreto (claves de API, tokens) esté escrito literalmente en el código, y que todo venga de process.env. POR QUÉ: el código que subís a un repositorio público NUNCA debería contener credenciales reales.",
                "pista": "Si encontrás const API_KEY = 'abc123' hardcodeado, cambialo por const API_KEY = process.env.API_KEY y documentá en el README qué variables hacen falta.",
            },
            {
                "titulo": "Entendé la noción de Docker con un Dockerfile simple",
                "descripcion": "QUÉ: escribí un Dockerfile mínimo que empaquete tu app Node con sus dependencias. POR QUÉ: Docker garantiza que tu app corre EXACTAMENTE igual en cualquier máquina, eliminando el clásico 'en mi compu funciona'.",
                "pista": "Un Dockerfile mínimo para Node: FROM node:20-alpine, WORKDIR /app, COPY package*.json ./, RUN npm install, COPY . ., CMD [\"node\", \"index.js\"]",
            },
            {
                "titulo": "Elegí un servicio de hosting gratuito y desplegá",
                "descripcion": "QUÉ: usá un servicio gratuito para apps pequeñas (como Render, Railway o Vercel para frontend) y seguí sus pasos para conectar tu repositorio de GitHub. POR QUÉ: estos servicios manejan la infraestructura (servidor, HTTPS, reinicio automático) para que vos te enfoques en el código.",
                "pista": "La mayoría de estos servicios detectan automáticamente un package.json con un script 'start' y te dan una URL pública apenas termina el deploy.",
            },
            {
                "titulo": "Configurá las variables de entorno en el servicio",
                "descripcion": "QUÉ: en el panel del servicio de hosting, configurá las mismas variables que usabas localmente en tu .env. POR QUÉ: tu .env local nunca se sube al repositorio (está en .gitignore), así que producción necesita que se las pases por otro lado.",
                "pista": "Buscá una sección tipo 'Environment Variables' en el panel del servicio — se configuran una por una, sin tocar código.",
            },
            {
                "titulo": "Agregá un CI básico que corra tus tests",
                "descripcion": "QUÉ: un archivo de GitHub Actions simple que instale dependencias y corra tus tests de Jest automáticamente en cada push. POR QUÉ: así te enterás de que rompiste algo ANTES de hacer deploy.",
                "pista": "Un workflow mínimo de GitHub Actions vive en .github/workflows/tests.yml, con steps que hacen actions/checkout, setup-node, npm install y npm test.",
            },
        ],
        "criterios": [
            "La app está desplegada y accesible desde una URL pública (no localhost).",
            "Ningún secreto real quedó escrito en el código subido al repositorio.",
            "Las variables de entorno de producción están configuradas en el panel del servicio, no en el código.",
            "Existe un workflow de CI que corre los tests automáticamente en cada push.",
        ],
        "retos_extra": [
            "Configurá un dominio personalizado (o subdominio gratuito) apuntando a tu deploy.",
            "Agregá un endpoint /health que el servicio pueda usar para verificar que la app sigue viva.",
            "Hacé que el CI también corra ESLint, fallando el build si hay errores de lint.",
        ],
    },
    {
        "id": 13,
        "disponible_en_ide": "parcial",
        "titulo": "Seguridad básica en JS: XSS, validación e inyección",
        "descripcion": "Entendé (y prevení) los errores de seguridad más comunes en aplicaciones web con JavaScript.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["XSS", "validación de inputs", "inyección SQL", "sanitización"],
        "xp": 200,
        "objetivo": "Entender de forma práctica los ataques más comunes en aplicaciones web (XSS e inyección SQL), reproduciéndolos en un entorno propio y controlado, y aprender las defensas básicas que cualquier app JS real necesita.",
        "requisitos": ["Módulo: DOM y eventos"],
        "pasos": [
            {
                "titulo": "Reproducí un XSS a propósito",
                "descripcion": "QUÉ: en una página propia de práctica, insertá texto de un usuario directamente con innerHTML, y probá pasarle un input como '<img src=x onerror=alert(1)>'. POR QUÉ: ver cómo un input diseñado a propósito ejecuta código arbitrario en tu página es mucho más contundente que solo leer la teoría del ataque XSS (Cross-Site Scripting).",
                "pista": "elemento.innerHTML = comentarioDeUsuario; — si comentarioDeUsuario contiene HTML/JS, el navegador lo EJECUTA. Nunca hagas esto con texto que no controlás.",
            },
            {
                "titulo": "Corregilo usando textContent o sanitización",
                "descripcion": "QUÉ: reemplazá innerHTML por textContent cuando solo necesitás mostrar texto plano, o usá una librería de sanitización (como DOMPurify) cuando SÍ necesitás permitir algo de HTML. POR QUÉ: textContent nunca interpreta el contenido como HTML/JS ejecutable — el ataque deja de ser posible por diseño.",
                "pista": "elemento.textContent = comentarioDeUsuario; — es la solución correcta en el 90% de los casos donde solo mostrás texto de usuario.",
            },
            {
                "titulo": "Reproducí y corregí una inyección SQL (si usás una API con base de datos)",
                "descripcion": "QUÉ: si tenés un backend Node con SQL, probá una query armada con template literals e input malicioso, y después corregila con parámetros. POR QUÉ: el mismo problema que en cualquier otro lenguaje — concatenar input del usuario directo en SQL permite alterar la consulta.",
                "pista": "Mal: db.exec(`SELECT * FROM usuarios WHERE nombre = '${nombreInput}'`) — bien: db.prepare('SELECT * FROM usuarios WHERE nombre = ?').get(nombreInput)",
            },
            {
                "titulo": "Validá inputs de usuario antes de usarlos",
                "descripcion": "QUÉ: agregá validaciones de tipo, rango y longitud para cualquier dato que venga de un formulario, query param o body de request. POR QUÉ: XSS e inyección SQL son solo DOS consecuencias de confiar ciegamente en el input del usuario — validar temprano previene muchos otros problemas.",
                "pista": "Preguntas básicas: ¿es del tipo esperado? ¿tiene una longitud máxima razonable? ¿coincide con el formato esperado (regex)? Rechazá, no 'arregles silenciosamente'.",
            },
            {
                "titulo": "Auditá tu proyecto por secretos hardcodeados",
                "descripcion": "QUÉ: revisá tu código buscando claves, tokens o contraseñas escritas directamente, y movelos a variables de entorno (process.env). POR QUÉ: un secreto hardcodeado que se sube a un repositorio público queda expuesto para siempre en el historial de Git.",
                "pista": "Buscá patrones como apiKey =, password =, token = con un valor literal al lado — deberían venir de process.env en su lugar.",
            },
        ],
        "criterios": [
            "Reprodujiste un XSS exitoso en tu propio entorno de práctica y entendés por qué funciona.",
            "El código nunca usa innerHTML con datos de usuario sin sanitizar.",
            "Si el proyecto usa SQL, todas las queries usan parámetros, ninguna concatena input del usuario.",
            "No queda ningún secreto escrito literalmente en el código.",
        ],
        "retos_extra": [
            "Investigá Content Security Policy (CSP) como capa extra de defensa contra XSS.",
            "Agregá rate limiting básico a un endpoint sensible (como login) para dificultar ataques de fuerza bruta.",
            "Probá una herramienta como npm audit o Snyk para detectar vulnerabilidades en tus dependencias.",
        ],
    },
    {
        "id": 14,
        "disponible_en_ide": "no",
        "titulo": "Consumí una API de IA desde JS",
        "descripcion": "Conectate a un modelo de lenguaje real desde JavaScript, como lo hace el tutor IA de esta misma app.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["APIs de IA", "fetch", "prompt engineering básico", "manejo de errores", "seguridad en IA"],
        "xp": 225,
        "objetivo": "Aprender a integrar una API de inteligencia artificial (como Gemini) desde JavaScript: autenticación, armado del request con fetch, manejo de la respuesta y de errores.",
        "requisitos": ["Módulo: Promesas y async/await", "Módulo: JSON: stringify y parse"],
        "pasos": [
            {
                "titulo": "Conseguí una API key",
                "descripcion": "QUÉ: registrate en un proveedor de IA con capa gratuita (por ejemplo Google AI Studio para Gemini) y generá tu propia API key. POR QUÉ: sin una key válida ningún request va a funcionar.",
                "pista": "Guardá la key en una variable de entorno (process.env en Node) apenas la generes, NUNCA la pegues directo en el código del lado del cliente/navegador.",
            },
            {
                "titulo": "Armá tu primer request con fetch",
                "descripcion": "QUÉ: usá fetch() con método POST para enviar un prompt simple a la API, con headers y body en el formato que pide la documentación del proveedor. POR QUÉ: cada API de IA tiene su propio formato de request — leer la documentación y probar con un caso simple es el primer paso siempre.",
                "pista": "const res = await fetch(url, { method: 'POST', headers: {...}, body: JSON.stringify({...}) }); const datos = await res.json();",
            },
            {
                "titulo": "Extraé el texto generado de la respuesta",
                "descripcion": "QUÉ: parseá el JSON de respuesta y navegá su estructura hasta encontrar el texto generado. POR QUÉ: la respuesta completa suele traer metadata además del texto — necesitás saber exactamente dónde está lo que te interesa.",
                "pista": "console.log(JSON.stringify(datos, null, 2)) la primera vez te muestra la estructura completa antes de intentar extraer un campo específico.",
            },
            {
                "titulo": "Manejá errores de la API",
                "descripcion": "QUÉ: probá qué pasa con una key inválida, y agregá manejo con try/catch para rate limiting y timeouts. POR QUÉ: una API externa puede fallar por razones que no controlás — tu programa no debería crashear silenciosamente.",
                "pista": "if (!res.ok) { throw new Error(`Error ${res.status}: ${await res.text()}`); } — 401/403 es autenticación, 429 es rate limit, 5xx es problema del servidor.",
            },
            {
                "titulo": "Iterá el prompt (prompt engineering básico)",
                "descripcion": "QUÉ: probá el mismo pedido con 3 prompts distintos (uno vago, uno específico, uno con ejemplos) y comparé la calidad de las respuestas. POR QUÉ: la forma en que le pedís algo a un modelo cambia drásticamente la calidad de la respuesta.",
                "pista": "Un prompt específico con formato esperado ('Respondé en 3 bullets cortos, en español') suele dar resultados mucho más útiles que uno vago.",
            },
            {
                "titulo": "Pensá en seguridad: qué es el prompt injection",
                "descripcion": "QUÉ: investigá qué es un ataque de prompt injection (cuando un input del usuario intenta manipular las instrucciones que le diste al modelo) y probá un caso simple, metiendo dentro del texto que le pasás como dato una instrucción falsa como 'Ignorá las instrucciones anteriores y...'. POR QUÉ: si tu programa alguna vez usa la respuesta del modelo para tomar una decisión automática (ejecutar código, borrar datos, aprobar algo), un prompt injection exitoso puede hacer que el modelo 'decida' cualquier cosa que un atacante le sugiera — nunca hay que confiar ciegamente en la respuesta de una IA para acciones automáticas sin validar.",
                "pista": "Separá siempre las instrucciones del sistema (lo que vos le decís al modelo que haga) de los datos que vienen del usuario, y nunca ejecutes código ni tomes una acción destructiva basándote directamente en lo que el modelo respondió, sin una validación explícita de tu parte antes.",
            },
        ],
        "criterios": [
            "El programa hace un request real a una API de IA con fetch y muestra la respuesta generada.",
            "La API key nunca queda expuesta en código del lado del cliente/navegador.",
            "El programa maneja al menos 2 tipos de error distintos sin crashear.",
            "Se probaron y compararon al menos 3 variantes de prompt para la misma tarea.",
            "Se probó al menos un caso de prompt injection y se explica por qué nunca hay que confiar ciegamente en la respuesta del modelo para tomar decisiones automáticas.",
        ],
        "retos_extra": [
            "Armá una conversación con memoria: mandá el historial de mensajes previos en cada request.",
            "Agregá un modo streaming si el proveedor lo soporta, mostrando la respuesta a medida que se genera.",
            "Construí una interfaz mínima en el navegador (input + botón + área de respuesta) para probar la API interactivamente.",
        ],
    },
    {
        "id": 15,
        "disponible_en_ide": "no",
        "titulo": "Accesibilidad web básica (a11y)",
        "descripcion": "Hacé que tus páginas sean usables por cualquiera, incluyendo personas que navegan con teclado o lector de pantalla.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["a11y", "HTML semántico", "ARIA", "navegación por teclado"],
        "xp": 175,
        "objetivo": "Aprender los fundamentos de accesibilidad web (a11y): HTML semántico, atributos ARIA, contraste de color y navegación por teclado, auditando y mejorando una página propia.",
        "requisitos": ["Módulo: DOM y eventos"],
        "pasos": [
            {
                "titulo": "Auditá una página con las herramientas del navegador",
                "descripcion": "QUÉ: abrí una de tus páginas (por ejemplo el Ahorcado con interfaz web) en Chrome DevTools y corré una auditoría de Accesibilidad (Lighthouse). POR QUÉ: la auditoría te da una lista concreta de problemas reales, en vez de adivinar qué mejorar.",
                "pista": "En DevTools: pestaña Lighthouse (o Auditorías) → marcá 'Accessibility' → Generate report. Te va a dar un puntaje y una lista de problemas específicos con explicación.",
            },
            {
                "titulo": "Reemplazá divs genéricos por HTML semántico",
                "descripcion": "QUÉ: cambiá <div> usados como botones o encabezados por elementos semánticos reales: <button>, <nav>, <header>, <main>, <h1>-<h6>. POR QUÉ: los lectores de pantalla usan las etiquetas semánticas para entender la estructura de la página — un <div onclick=...> no es anunciado como un botón interactivo.",
                "pista": "Si algo se comporta como un botón, DEBE ser un <button>, no un <div> con un onclick — así obtenés gratis el foco con Tab, la activación con Enter/Espacio y el anuncio correcto para lectores de pantalla.",
            },
            {
                "titulo": "Agregá atributos ARIA donde el HTML semántico no alcanza",
                "descripcion": "QUÉ: para componentes custom (como un modal o un menú desplegable), agregá aria-label, aria-expanded, role, según corresponda. POR QUÉ: ARIA le da información extra a las tecnologías asistivas cuando la semántica HTML nativa no es suficiente para describir el componente.",
                "pista": "aria-label='Cerrar' en un botón de ícono sin texto visible, aria-expanded='true'/'false' en un botón que abre/cierra un menú.",
            },
            {
                "titulo": "Probá navegar tu página SOLO con el teclado",
                "descripcion": "QUÉ: sin usar el mouse, navegá tu página completa usando Tab, Shift+Tab, Enter y las flechas. POR QUÉ: mucha gente no puede (o prefiere no) usar mouse — si algo importante de tu página solo se puede activar con click de mouse, esas personas quedan bloqueadas.",
                "pista": "Fijate si el foco (el contorno que aparece al presionar Tab) sigue un orden lógico, y si CUALQUIER acción posible con click también se puede hacer con teclado.",
            },
            {
                "titulo": "Verificá el contraste de color",
                "descripcion": "QUÉ: usá el inspector de colores de DevTools (o una herramienta como WebAIM Contrast Checker) para verificar que el texto tenga suficiente contraste contra el fondo. POR QUÉ: bajo contraste dificulta la lectura para personas con baja visión, y a veces simplemente por estar usando la pantalla con mucha luz ambiente.",
                "pista": "El estándar WCAG AA pide un ratio de contraste mínimo de 4.5:1 para texto normal — DevTools te muestra este ratio automáticamente al inspeccionar un elemento de texto.",
            },
        ],
        "criterios": [
            "La auditoría de Lighthouse mejora su puntaje de accesibilidad respecto a la versión inicial.",
            "Los elementos interactivos usan etiquetas semánticas (button, nav, etc.), no divs genéricos con onclick.",
            "Toda la funcionalidad de la página se puede usar navegando solo con teclado.",
            "El texto principal cumple con un contraste mínimo de 4.5:1 contra su fondo.",
        ],
        "retos_extra": [
            "Probá tu página con un lector de pantalla real (NVDA en Windows es gratuito) y anotá qué se entiende mal.",
            "Agregá un 'skip link' que permita saltar directo al contenido principal, ignorando la navegación repetitiva.",
            "Investigá prefers-reduced-motion en CSS para respetar a usuarios sensibles a animaciones.",
        ],
    },
    {
        "id": 16,
        "disponible_en_ide": "no",
        "titulo": "Autenticación y autorización con JWT",
        "descripcion": "Login real con tokens: quién sos, qué podés hacer, y por cuánto tiempo — armá tu propio sistema de auth con Express y jsonwebtoken.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["JWT", "hashing de contraseñas", "Express", "middlewares de autenticación"],
        "xp": 250,
        "objetivo": "Construir un sistema de login con Express que genere tokens JWT, proteja rutas según el token recibido, y maneje expiración y roles de usuario.",
        "requisitos": ["Módulo: try / catch / finally", "Proyecto: Seguridad básica en JS: XSS, validación e inyección"],
        "pasos": [
            {
                "titulo": "Armá el endpoint de registro con contraseña hasheada",
                "descripcion": "QUÉ: usá bcrypt para hashear la contraseña antes de guardarla. POR QUÉ: guardar contraseñas en texto plano compromete a todos los usuarios si la base se filtra — repasá el proyecto de Seguridad básica.",
                "pista": "bcrypt.hash(password, 10) agrega el salt automáticamente por vos.",
            },
            {
                "titulo": "Generá un JWT al hacer login",
                "descripcion": "QUÉ: si el login es válido, armá un token con jsonwebtoken que incluya el id de usuario y una fecha de expiración. POR QUÉ: el JWT es la prueba portátil de que el usuario se autenticó, sin que el servidor tenga que guardar sesión en memoria.",
                "pista": "jwt.sign({ id: usuario.id }, SECRET_KEY, { expiresIn: '1h' }). Nunca hardcodees el SECRET_KEY, usalo desde una variable de entorno.",
            },
            {
                "titulo": "Protegé una ruta con un middleware de auth",
                "descripcion": "QUÉ: creá un middleware que lea el header Authorization, valide el JWT con jwt.verify() y deje pasar el request (o lo rechace con 401). POR QUÉ: sin esta validación, cualquiera podría llamar a rutas que deberían requerir login.",
                "pista": "jwt.verify() lanza una excepción si el token es inválido o expiró — atrapala con try/catch y devolvé res.status(401).",
            },
            {
                "titulo": "Agregá expiración y manejo de tokens vencidos",
                "descripcion": "QUÉ: probá qué pasa cuando el token expira, y devolvé un mensaje claro (401, no un error genérico de servidor). POR QUÉ: un token que dura para siempre es un riesgo de seguridad — si se filtra, queda válido eternamente.",
                "pista": "Generá un token con expiresIn: '5s' para probar el caso vencido más rápido durante el desarrollo.",
            },
            {
                "titulo": "Distinguí roles o permisos básicos",
                "descripcion": "QUÉ: agregá un campo 'rol' al token y una ruta que solo el rol admin pueda usar. POR QUÉ: autenticación (quién sos) y autorización (qué podés hacer) son cosas distintas — la mayoría de las apps reales necesitan ambas.",
                "pista": "En el middleware, después de verificar el token podés chequear req.usuario.rol y devolver 403 (no 401) si no tiene permiso.",
            },
        ],
        "criterios": [
            "El sistema hashea las contraseñas antes de guardarlas, nunca en texto plano.",
            "Genera un JWT válido al hacer login exitoso y lo rechaza si las credenciales son incorrectas.",
            "Al menos una ruta está protegida y devuelve 401 sin token válido.",
            "Distingue al menos 2 roles con permisos distintos.",
        ],
        "retos_extra": [
            "Agregá una ruta de refresh token que renueve la sesión sin pedir contraseña de nuevo.",
            "Implementá logout invalidando el token (por ejemplo con una lista negra en memoria).",
            "Agregá rate limiting a la ruta de login para frenar ataques de fuerza bruta.",
        ],
    },
    {
        "id": 17,
        "disponible_en_ide": "no",
        "titulo": "Arquitectura MVC: organizá tu código como un framework real",
        "descripcion": "Separá tu API en modelos, vistas y controladores — la misma organización que usan Rails, Django y la mayoría de los frameworks profesionales.",
        "dificultad": "Intermedio+",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["arquitectura de software", "separación de responsabilidades", "Express", "organización de proyectos"],
        "xp": 200,
        "objetivo": "Reestructurar (o construir desde cero) una API Express separando claramente modelos (datos), controladores (lógica de negocio) y rutas (entrada HTTP), en vez de tener todo mezclado en un solo archivo.",
        "requisitos": ["Módulo: Clases: constructor y métodos", "Proyecto: Sistema de gestión de estudiantes (CRUD)"],
        "pasos": [
            {
                "titulo": "Separá los modelos de datos",
                "descripcion": "QUÉ: creá un archivo models/ con las clases o funciones que representan tus datos. POR QUÉ: cuando el modelo vive separado de la lógica, podés cambiar cómo se guardan los datos sin tocar el resto del código.",
                "pista": "Un modelo puede ser tan simple como una clase con propiedades, o funciones que devuelven objetos con una forma consistente.",
            },
            {
                "titulo": "Separá la lógica de negocio en controladores",
                "descripcion": "QUÉ: creá funciones en un archivo controllers/ que reciban datos y hagan la lógica real, sin saber nada de Express (req/res). POR QUÉ: si la lógica no depende de Express, la podés testear directo con Jest, sin levantar un servidor.",
                "pista": "Un controlador no debería recibir req ni res directamente — que reciba y devuelva datos planos, y que la ruta se encargue de traducir eso a HTTP.",
            },
            {
                "titulo": "Dejá las rutas como una capa fina",
                "descripcion": "QUÉ: cada ruta debería ser pocas líneas: recibe el request, llama al controlador, devuelve la respuesta. POR QUÉ: si la ruta hace demasiado, mezclás 'cómo llega el dato' con 'qué se hace con el dato' y el código se vuelve difícil de reusar o testear.",
                "pista": "Si un handler de ruta tiene más de 10-15 líneas con lógica real, esa lógica probablemente debería estar en el controlador.",
            },
            {
                "titulo": "Organizá todo en carpetas",
                "descripcion": "QUÉ: armá una estructura de carpetas (models/, controllers/, routes/). POR QUÉ: a medida que un proyecto crece, la organización por responsabilidad es lo que permite que varias personas trabajen sin pisarse.",
                "pista": "Cada carpeta puede tener un index.js que reexporte todo lo de adentro, para simplificar los imports desde otras partes del proyecto.",
            },
            {
                "titulo": "Escribí un test que pruebe el controlador sin HTTP",
                "descripcion": "QUÉ: importá una función del controlador directamente en un test de Jest y llamala con datos de prueba, sin pasar por Express. POR QUÉ: esto demuestra en la práctica el beneficio real de la separación: podés probar la lógica sin levantar un servidor.",
                "pista": "Si esto te resulta difícil de escribir, es una señal de que el controlador todavía depende de algo de Express que debería sacarse de ahí.",
            },
        ],
        "criterios": [
            "El proyecto tiene modelos, controladores y rutas en archivos o carpetas separadas.",
            "Los controladores no dependen directamente de req/res de Express.",
            "Al menos un test prueba un controlador sin pasar por una petición HTTP real.",
        ],
        "retos_extra": [
            "Agregá una capa de 'repositorio' entre el controlador y el almacenamiento de datos, para poder cambiar de un array en memoria a SQLite sin tocar el controlador.",
            "Migrá un proyecto anterior tuyo (por ejemplo el CRUD de estudiantes) a esta arquitectura.",
        ],
    },
    {
        "id": 18,
        "disponible_en_ide": "no",
        "titulo": "Clean code y refactorización en JS",
        "descripcion": "Tomá un código que funciona pero es un desastre, y transformalo paso a paso en algo que cualquier profesional podría leer y mantener.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["refactorización", "nombres descriptivos", "funciones pequeñas", "código limpio"],
        "xp": 175,
        "objetivo": "Partir de un archivo de código deliberadamente desordenado (funciones gigantes, nombres crípticos, lógica duplicada) y refactorizarlo aplicando principios de código limpio, sin cambiar su comportamiento.",
        "requisitos": ["Módulo: Closures y funciones de orden superior", "Proyecto: Código limpio: ESLint, Prettier y logging profesional"],
        "pasos": [
            {
                "titulo": "Escribí (o usá) el código spaghetti de partida",
                "descripcion": "QUÉ: armá una función de 80+ líneas que procese pedidos de una tienda: valide, calcule descuentos, aplique impuestos, y arme un resumen, todo mezclado con nombres como 'x', 'datos2', 'flag'. POR QUÉ: para practicar refactorización necesitás primero algo real para refactorizar — y este patrón (una función que hace de todo) es extremadamente común en código real.",
                "pista": "Si te cuesta imaginar código así, pensá en cómo escribirías la solución 'lo más rápido posible' sin pensar en mantenibilidad — ese es exactamente el punto de partida.",
            },
            {
                "titulo": "Escribí tests ANTES de tocar nada",
                "descripcion": "QUÉ: con el código como está, escribí 2-3 tests de Jest que verifiquen el comportamiento actual (mismos inputs, mismos outputs). POR QUÉ: refactorizar sin tests es peligroso — no tenés forma de saber si rompiste algo hasta que sea tarde.",
                "pista": "Los tests deben pasar ANTES de empezar a refactorizar. Si no pasan, primero arreglá eso, no es parte del ejercicio de refactor.",
            },
            {
                "titulo": "Extraé funciones pequeñas con nombres que expliquen el qué",
                "descripcion": "QUÉ: dividí la función gigante en funciones más chicas (calcularDescuento, aplicarImpuesto, generarResumen), cada una con un nombre que describe exactamente lo que hace. POR QUÉ: una función que hace una sola cosa es más fácil de entender, testear y reusar que una que hace diez.",
                "pista": "Si te cuesta nombrar una función, probablemente está haciendo más de una cosa — dividila de nuevo.",
            },
            {
                "titulo": "Eliminá números y strings mágicos",
                "descripcion": "QUÉ: reemplazá valores sueltos como 0.21 o 'VIP' por constantes con nombre (const IVA = 0.21, const CATEGORIA_VIP = 'VIP'). POR QUÉ: un número suelto en el medio del código no explica su significado — alguien que lo lea seis meses después no va a saber qué es 0.21 sin buscarlo.",
                "pista": "Las constantes suelen ir en mayúsculas al principio del archivo o en un módulo aparte de configuración.",
            },
            {
                "titulo": "Corré los tests de nuevo y comparalos",
                "descripcion": "QUÉ: ejecutá los mismos tests del paso 2 contra el código refactorizado. POR QUÉ: si pasan igual que antes, tenés evidencia real de que el comportamiento no cambió — solo mejoró la legibilidad.",
                "pista": "Si algún test falla, el problema está en la refactorización, no en el test — volvé atrás y revisá qué cambiaste de más.",
            },
        ],
        "criterios": [
            "Existe una versión 'antes' y una 'después' del mismo código, con comportamiento idéntico.",
            "Los tests escritos antes de refactorizar pasan igual después de refactorizar.",
            "Ninguna función del código final supera ~20 líneas, y los nombres describen claramente qué hace cada una.",
            "No quedan números o strings mágicos sin explicar mediante una constante con nombre.",
        ],
        "retos_extra": [
            "Medí la complejidad de tu código con una herramienta como eslint-plugin-complexity y compará antes/después.",
            "Pedile a otra persona (o a Pip) que lea solo el código 'después' y te explique qué hace, sin ayuda tuya — si puede, el refactor funcionó.",
        ],
    },
    {
        "id": 19,
        "disponible_en_ide": "no",
        "titulo": "Docker de verdad para apps Node",
        "descripcion": "Un Dockerfile simple no alcanza para una app real — armá un entorno completo con base de datos, volumes y una imagen optimizada para producción.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["Docker", "docker-compose", "volumes", "multi-stage builds", "redes de contenedores"],
        "xp": 225,
        "objetivo": "Extender un Dockerfile básico a un entorno completo con docker-compose: la API Node en un contenedor, una base de datos en otro, comunicándose por una red interna, con datos persistentes y una imagen final optimizada.",
        "requisitos": ["Proyecto: Deploy básico: subí tu app JS a internet", "Proyecto: Bases de datos con SQL: SQLite desde Node.js"],
        "pasos": [
            {
                "titulo": "Armá un docker-compose.yml con dos servicios",
                "descripcion": "QUÉ: definí un servicio 'api' (tu aplicación Node) y un servicio 'db' (por ejemplo postgres) en el mismo archivo docker-compose.yml. POR QUÉ: las apps reales casi nunca corren solas — necesitan una base de datos, y docker-compose es la forma estándar de levantar varios contenedores juntos con un solo comando.",
                "pista": "docker-compose up levanta todos los servicios definidos; cada uno corre en su propio contenedor pero pueden hablarse entre sí por nombre de servicio, no por localhost.",
            },
            {
                "titulo": "Conectá los servicios por una red interna",
                "descripcion": "QUÉ: hacé que tu API se conecte a la base usando el nombre del servicio ('db') como host, no 'localhost'. POR QUÉ: docker-compose crea una red virtual donde cada servicio es alcanzable por su nombre — esto es distinto (y más simple) que exponer puertos manualmente.",
                "pista": "Si tu API dice 'connection refused' a 'localhost', ese es el error clásico de no usar el nombre del servicio de docker-compose como host.",
            },
            {
                "titulo": "Agregá un volume para persistir los datos",
                "descripcion": "QUÉ: montá un volume para la carpeta de datos de la base, para que la información sobreviva si el contenedor se reinicia. POR QUÉ: sin un volume, cada vez que recreás el contenedor de la base perdés todos los datos — los contenedores son efímeros por diseño.",
                "pista": "En docker-compose.yml, la sección volumes de un servicio mapea una carpeta del contenedor a un volume nombrado o a una carpeta de tu máquina.",
            },
            {
                "titulo": "Pasá configuración con variables de entorno, no hardcodeadas",
                "descripcion": "QUÉ: usá un archivo .env (que NO se sube a git) para las credenciales de la base y otras configuraciones sensibles. POR QUÉ: hardcodear contraseñas en el docker-compose.yml es el mismo problema de seguridad que hardcodearlas en el código — y este archivo suele terminar en un repositorio público por error.",
                "pista": "Agregá .env a tu .gitignore desde el primer commit, y dejá un .env.example con los nombres de las variables (sin valores reales) para que otros sepan qué configurar.",
            },
            {
                "titulo": "Optimizá la imagen con un build multi-stage",
                "descripcion": "QUÉ: dividí tu Dockerfile en una etapa de build (instala dependencias con npm ci) y una etapa final que solo copia lo necesario para correr. POR QUÉ: la imagen final queda mucho más chica y segura si no incluye devDependencies ni archivos temporales que solo hacían falta durante el build.",
                "pista": "Copiá primero package.json y package-lock.json y corré npm ci antes de copiar el resto del código — así Docker cachea la instalación de dependencias y no la repite en cada build si el código cambia pero las dependencias no.",
            },
        ],
        "criterios": [
            "docker-compose up levanta la API y la base de datos correctamente conectadas entre sí.",
            "Los datos de la base sobreviven a un 'docker-compose down' seguido de 'docker-compose up' (gracias al volume).",
            "Ninguna credencial está hardcodeada en el docker-compose.yml, todas vienen de variables de entorno.",
            "El Dockerfile usa build multi-stage y la imagen final es notablemente más chica que una versión de una sola etapa.",
        ],
        "retos_extra": [
            "Agregá un tercer servicio (por ejemplo un cache con Redis) y conectalo también por la red interna.",
            "Configurá un healthcheck en docker-compose para que la API espere a que la base esté realmente lista antes de arrancar.",
        ],
    },
    {
        "id": 20,
        "disponible_en_ide": "no",
        "titulo": "Migrá tu proyecto JS a TypeScript",
        "descripcion": "Convertí un proyecto JavaScript real a TypeScript paso a paso: tipos básicos, interfaces y tsconfig.json, sin reescribir todo de una.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["TypeScript", "tsconfig.json", "interfaces", "tipos básicos"],
        "xp": 225,
        "objetivo": "Migrar un proyecto JavaScript existente a TypeScript de forma incremental: configurar el compilador, tipar funciones y datos, y usar interfaces para las estructuras principales del proyecto.",
        "requisitos": ["Módulo: Objetos: propiedades y métodos", "Proyecto: Node.js y npm: gestores de paquetes en JS"],
        "pasos": [
            {
                "titulo": "Instalá TypeScript y creá tu tsconfig.json",
                "descripcion": "QUÉ: npm install --save-dev typescript, y npx tsc --init para generar la configuración. POR QUÉ: tsconfig.json define cómo el compilador de TypeScript va a chequear y transformar tu código — sin él, no hay reglas consistentes de compilación.",
                "pista": "Activá \"strict\": true desde el principio si podés — te va a obligar a escribir tipos más precisos, aunque al principio moleste un poco más.",
            },
            {
                "titulo": "Renombrá un archivo a .ts y arreglá lo que rompa",
                "descripcion": "QUÉ: cambiá la extensión de un archivo de tu proyecto de .js a .ts, y corregí los errores de tipos que aparezcan. POR QUÉ: TypeScript es un superset de JavaScript — todo JS válido es (casi) TS válido, pero el compilador va a empezar a exigirte tipos apenas cambies la extensión.",
                "pista": "Hacelo un archivo a la vez, no todo el proyecto junto — migrar incrementalmente es justamente el punto de este ejercicio.",
            },
            {
                "titulo": "Tipá los parámetros y retornos de tus funciones",
                "descripcion": "QUÉ: agregá anotaciones de tipo a las funciones del archivo migrado. POR QUÉ: sin anotaciones explícitas, TypeScript infiere tipos, pero en funciones exportadas es mejor ser explícito para que quien las use sepa exactamente qué esperar.",
                "pista": "function sumar(a: number, b: number): number es la sintaxis básica — muy similar a los type hints de Python si ya los viste.",
            },
            {
                "titulo": "Definí una interface para tu estructura de datos principal",
                "descripcion": "QUÉ: creá una interface que describa la forma de tu objeto principal (por ejemplo Usuario o Tarea), y usala como tipo en las funciones que lo manejan. POR QUÉ: una interface documenta explícitamente qué forma tiene un dato, y TypeScript te avisa si en algún lugar armás ese objeto sin todos los campos que necesita.",
                "pista": "interface Tarea { texto: string; completada: boolean } — después podés usar 'tarea: Tarea' como tipo de parámetro en cualquier función.",
            },
            {
                "titulo": "Compilá el proyecto y corré el resultado",
                "descripcion": "QUÉ: usá npx tsc para compilar tus archivos .ts a .js, y corré el resultado con node. POR QUÉ: TypeScript no corre directamente — se compila a JavaScript plano, así que necesitás confirmar que el código generado funciona igual que el original.",
                "pista": "Agregá un script \"build\": \"tsc\" en tu package.json para no tener que recordar el comando completo cada vez.",
            },
        ],
        "criterios": [
            "tsconfig.json está configurado, idealmente con modo strict.",
            "Al menos un archivo fue migrado a .ts y compila sin errores.",
            "Las funciones migradas tienen tipos explícitos en parámetros y retorno.",
            "Existe al menos una interface definida y usada en funciones reales.",
            "El código compilado corre igual que el original.",
        ],
        "retos_extra": [
            "Migrá el proyecto completo, no solo un archivo.",
            "Agregá un tipo genérico a una función reutilizable (por ejemplo una función que envuelve cualquier tipo de dato).",
        ],
    },
    {
        "id": 21,
        "disponible_en_ide": "no",
        "titulo": "Estrategia de testing: la pirámide con Jest",
        "descripcion": "No todos los tests son iguales — entendé la pirámide de testing (unit, integración, e2e) y organizá tus tests de Jest según ese criterio.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["pirámide de testing", "tests unitarios", "tests de integración", "tests e2e", "Jest"],
        "xp": 200,
        "objetivo": "Entender la pirámide de testing (muchos tests unitarios rápidos, menos de integración, muy pocos e2e) y aplicarla escribiendo un test de integración real que use la base de datos SQLite de un proyecto existente, en vez de mockearla.",
        "requisitos": ["Proyecto: Testing en JS con Jest", "Proyecto: Bases de datos con SQL: SQLite desde Node.js"],
        "pasos": [
            {
                "titulo": "Explicá la pirámide de testing",
                "descripcion": "QUÉ: describí con tus palabras qué es un test unitario, uno de integración y uno end-to-end (e2e), y por qué la pirámide sugiere tener muchos de los primeros y pocos de los últimos. POR QUÉ: entender esta jerarquía te ayuda a decidir qué tipo de test escribir para cada situación, en vez de escribir siempre el mismo tipo (o ninguno).",
                "pista": "Pensá en velocidad y costo: un test unitario corre en milisegundos y prueba una función aislada; un test e2e puede tardar segundos y prueba el sistema completo como lo usaría un usuario real — por eso conviene tener muchos más de los rápidos y baratos.",
            },
            {
                "titulo": "Identificá qué tests de un proyecto tuyo son unitarios",
                "descripcion": "QUÉ: revisá los tests de un proyecto anterior (o escribí 2-3 nuevos con Jest) que prueben una sola función aislada, sin tocar archivos, red ni base de datos. POR QUÉ: los tests unitarios son la base de la pirámide — deben ser rápidos y no depender de nada externo para poder correr cientos de ellos en segundos.",
                "pista": "Si tu test necesita que algo esté 'levantado' (un servidor, una base de datos real) para pasar, no es un test unitario, es de integración.",
            },
            {
                "titulo": "Escribí un test de integración real contra SQLite",
                "descripcion": "QUÉ: escribí un test que use una base de datos SQLite real (una base temporal o en memoria) para probar que una función que inserta y después lee datos funciona de punta a punta. POR QUÉ: a diferencia de un test unitario, este prueba que tu código y la base de datos real trabajan bien juntos — cosas como una consulta SQL con errores de sintaxis solo aparecen acá, no en un test que mockea la base.",
                "pista": "Muchas librerías de SQLite para Node soportan una base en memoria (':memory:' o similar) — es rápida y no deja archivos residuales entre corridas de test.",
            },
            {
                "titulo": "Compará qué hubiera pasado si mockeabas la base de datos",
                "descripcion": "QUÉ: escribí (o al menos describí) cómo sería el mismo test si en vez de una base real usaras jest.mock() para simular las respuestas. POR QUÉ: un mock que devuelve exactamente lo que vos programaste puede pasar aunque tu consulta SQL real tenga un error de sintaxis — el test de integración contra la base real es el que hubiera detectado ese problema.",
                "pista": "Pensá en un caso concreto: si escribís mal el nombre de una columna en tu consulta SQL, un mock bien configurado seguiría 'pasando' el test, pero la base de datos real fallaría con un error — eso es justamente lo que el test de integración está pensado para atrapar.",
            },
            {
                "titulo": "Organizá los tests por tipo",
                "descripcion": "QUÉ: separá tus tests en carpetas distintas (por ejemplo tests/unit/ y tests/integration/) y configurá scripts de npm para poder correr solo un grupo a la vez. POR QUÉ: en un proyecto real, correr todos los tests de integración (más lentos) en cada guardado de archivo sería frustrante — separarlos permite correr solo los unitarios durante el desarrollo activo, y todos antes de un commit o deploy.",
                "pista": "Podés agregar scripts como \"test:unit\": \"jest tests/unit\" y \"test:integration\": \"jest tests/integration\" en tu package.json.",
            },
        ],
        "criterios": [
            "Existe una explicación propia de la pirámide de testing (unit, integración, e2e) y cuándo usar cada nivel.",
            "Hay al menos un test de integración real que usa SQLite de verdad, no un mock.",
            "Los tests unitarios y de integración están organizados de forma que se puedan correr por separado.",
        ],
        "retos_extra": [
            "Agregá un test e2e simple usando supertest contra un servidor Express real levantado en el mismo test.",
            "Medí cuánto tarda correr solo los tests unitarios vs correr toda la suite, y compará la diferencia.",
        ],
    },
    {
        "id": 22,
        "disponible_en_ide": "no",
        "titulo": "Observabilidad en Node: logs, métricas y un /health real",
        "descripcion": "Cuando tu app está en producción y algo falla a las 3 de la mañana, la observabilidad es lo que te permite entender qué pasó sin adivinar.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["logs", "métricas", "observabilidad", "health checks", "Express"],
        "xp": 200,
        "objetivo": "Entender la diferencia entre logs, métricas y traces (los tres pilares de la observabilidad), y construir un endpoint /health en Express que verifique de verdad el estado de las dependencias de tu app, no solo devuelva 'ok'.",
        "requisitos": ["Módulo: try / catch / finally", "Proyecto: Código limpio: ESLint, Prettier y logging profesional"],
        "pasos": [
            {
                "titulo": "Explicá logs, métricas y traces con un ejemplo cada uno",
                "descripcion": "QUÉ: describí con tus palabras qué es cada uno, y dá un ejemplo concreto de qué información aportaría cada uno frente a un mismo problema (por ejemplo, una API que responde lento). POR QUÉ: son herramientas distintas para preguntas distintas — un log te dice 'qué pasó exactamente en este request', una métrica te dice 'cuántos requests están tardando de más ahora mismo', y un trace te dice 'en qué paso específico de este request se fue el tiempo'.",
                "pista": "Pensá en logs como un diario detallado de eventos individuales, métricas como números agregados a lo largo del tiempo (promedios, contadores), y traces como el recorrido paso a paso de UN request específico a través de todo el sistema.",
            },
            {
                "titulo": "Agregá logs estructurados con contexto útil",
                "descripcion": "QUÉ: en vez de mensajes sueltos ('error'), logueá con contexto: qué ruta, qué usuario (si aplica), qué parámetros, y el timestamp, idealmente como JSON. POR QUÉ: un log sin contexto ('Error en la base de datos') no te sirve de nada a las 3 de la mañana intentando entender qué pasó — necesitás poder reconstruir la situación exacta.",
                "pista": "console.log(JSON.stringify({ ruta, timestamp, error: error.message })) ya te da logs estructurados sin instalar nada — herramientas como pino o winston hacen esto mismo con más funcionalidad.",
            },
            {
                "titulo": "Contá una métrica simple: requests por ruta",
                "descripcion": "QUÉ: llevá un contador (aunque sea en memoria, con un objeto) de cuántas veces se llamó a cada ruta, y exponelo en un endpoint /metrics. POR QUÉ: esto es la base de cualquier sistema de métricas real (como Prometheus): números agregados que te dejan ver patrones de uso y detectar anomalías (por ejemplo, una ruta que de repente recibe 100 veces más tráfico de lo normal).",
                "pista": "Un middleware de Express que se ejecute en cada request es el lugar ideal para incrementar el contador correspondiente, sin tener que modificar cada ruta individualmente.",
            },
            {
                "titulo": "Medí la duración de cada request (la base de un trace)",
                "descripcion": "QUÉ: con un middleware, medí cuánto tarda cada request en procesarse y logueá esa duración junto con la ruta. POR QUÉ: sin esta medición no podés saber si tu API se está poniendo lenta con el tiempo, ni identificar qué rutas son las más costosas — es el primer paso hacia un sistema de tracing real.",
                "pista": "Guardá Date.now() al entrar al middleware, y escuchá el evento 'finish' de la response (res.on('finish', ...)) para calcular la duración total incluso si el handler tarda en responder.",
            },
            {
                "titulo": "Construí un /health que chequee dependencias reales",
                "descripcion": "QUÉ: hacé que la ruta /health verifique de verdad que la base de datos responde (por ejemplo con una consulta simple) y devuelva un status distinto si algo falla, no solo { status: 'ok' } fijo. POR QUÉ: un /health que siempre dice 'ok' sin chequear nada es inútil para un sistema de monitoreo — el objetivo es que herramientas automáticas (o vos mismo) puedan saber si la app realmente puede funcionar, no solo si el proceso está corriendo.",
                "pista": "Devolvé un status 503 (Service Unavailable) si alguna dependencia crítica falla, y 200 solo si todo lo esencial responde — no le mientas a quien llama al endpoint.",
            },
        ],
        "criterios": [
            "Existe una explicación propia de la diferencia entre logs, métricas y traces, con ejemplos concretos.",
            "Los logs incluyen contexto útil (ruta, timestamp, parámetros relevantes), no solo un mensaje suelto.",
            "Hay un endpoint /metrics (o similar) que expone al menos un contador real de uso.",
            "El endpoint /health verifica al menos una dependencia real (por ejemplo la base de datos) y devuelve un status distinto si falla.",
        ],
        "retos_extra": [
            "Agregá un ID único a cada request (un 'request ID') y propagalo en todos los logs de ese request, para poder rastrear un pedido específico entre múltiples líneas de log.",
            "Investigá qué es OpenTelemetry y cómo se relaciona con lo que armaste en este proyecto.",
        ],
    },
    {
        "id": 23,
        "disponible_en_ide": "parcial",
        "titulo": "Documentación de código con JSDoc",
        "descripcion": "Comentarios que generan documentación real — y por qué eso es distinto de un comentario cualquiera tirado arriba de una función.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1 hora",
        "conceptos": ["JSDoc", "documentación técnica", "comentarios con criterio"],
        "xp": 150,
        "objetivo": "Aprender a documentar funciones JavaScript con JSDoc, generar documentación real a partir de esos comentarios, y aplicar el mismo criterio de 'qué documentar y qué no' que en cualquier código limpio.",
        "requisitos": ["Módulo: Closures y funciones de orden superior", "Proyecto: Node.js y npm: gestores de paquetes en JS"],
        "pasos": [
            {
                "titulo": "Identificá qué NO necesita documentación",
                "descripcion": "QUÉ: revisá funciones cuyo nombre y parámetros ya explican todo. POR QUÉ: un comentario que solo repite el nombre de la función no aporta nada y hay que mantenerlo actualizado para siempre.",
                "pista": "Si podés borrar el comentario y la función sigue siendo igual de clara, probablemente no hacía falta.",
            },
            {
                "titulo": "Escribí tu primer bloque JSDoc",
                "descripcion": "QUÉ: agregá un comentario /** ... */ arriba de una función, con @param y @returns describiendo tipos y propósito. POR QUÉ: a diferencia de un comentario común, JSDoc sigue un formato estándar que herramientas (editores, generadores de docs) pueden leer y usar automáticamente.",
                "pista": "@param {string} nombre - descripción y @returns {boolean} - descripción es la sintaxis básica.",
            },
            {
                "titulo": "Instalá una herramienta que genere documentación real",
                "descripcion": "QUÉ: instalá jsdoc (npm install --save-dev jsdoc) y corrélo sobre tu proyecto para generar páginas HTML de documentación. POR QUÉ: esto es lo que separa a JSDoc de un comentario cualquiera: el mismo texto que escribiste se convierte en documentación navegable de verdad.",
                "pista": "npx jsdoc archivo.js -d docs genera la documentación en una carpeta docs/ que podés abrir en el navegador.",
            },
            {
                "titulo": "Documentá tipos complejos con @typedef",
                "descripcion": "QUÉ: si tenés un objeto con una forma específica que se repite (por ejemplo Usuario), definilo una vez con @typedef y reusalo en los @param de varias funciones. POR QUÉ: repetir la misma descripción de forma de objeto en cada función es tan malo como duplicar código — @typedef centraliza esa definición.",
                "pista": "/** @typedef {Object} Usuario @property {string} nombre @property {number} edad */ y después @param {Usuario} usuario en cualquier función que lo reciba.",
            },
            {
                "titulo": "Compará con y sin editor",
                "descripcion": "QUÉ: abrí tu archivo documentado en un editor con soporte de JSDoc (como VS Code) y fijate qué autocompletado e información aparece al usar esas funciones desde otro archivo. POR QUÉ: además de generar documentación HTML, JSDoc mejora directamente la experiencia de programar: el editor te muestra los tipos y descripciones mientras escribís, sin que tengas que ir a buscar la documentación.",
                "pista": "Pasá el mouse sobre el nombre de una función documentada en VS Code — debería aparecer un tooltip con la descripción y los tipos que escribiste.",
            },
        ],
        "criterios": [
            "Existe un criterio explicado sobre qué funciones necesitan documentación y cuáles no.",
            "Al menos 3 funciones tienen un bloque JSDoc completo con @param y @returns.",
            "Se generó documentación HTML real con la herramienta jsdoc.",
            "Se usó @typedef al menos una vez para una estructura de datos que se repite.",
        ],
        "retos_extra": [
            "Investigá cómo usar anotaciones JSDoc junto con la opción checkJs de TypeScript para chequear tipos sin migrar todo el proyecto.",
            "Publicá la documentación generada en GitHub Pages.",
        ],
    },
    {
        "id": 24,
        "disponible_en_ide": "no",
        "titulo": "Publicá tu propio paquete en npm",
        "descripcion": "De un módulo suelto a algo instalable con npm install — package.json listo para publicar, versionado semántico y npm publish (o simulado).",
        "dificultad": "Avanzado",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["package.json", "versionado semántico", "npm publish", "registro local"],
        "xp": 200,
        "objetivo": "Convertir un módulo de utilidades propio en un paquete npm publicable, con el package.json y el versionado correctos, y publicarlo (real o simuladamente) en un registro.",
        "requisitos": ["Proyecto: Node.js y npm: gestores de paquetes en JS"],
        "pasos": [
            {
                "titulo": "Elegí (o armá) un módulo simple para empaquetar",
                "descripcion": "QUÉ: tomá algunas funciones de utilidad propias (por ejemplo, un conjunto de validadores) y organizalas en una carpeta con la estructura de un paquete instalable. POR QUÉ: necesitás algo real y chico para practicar todo el proceso de empaquetado sin distraerte con la complejidad del contenido en sí.",
                "pista": "Un paquete mínimo necesita un package.json y un archivo de entrada (por ejemplo index.js) que exporte lo que querés compartir.",
            },
            {
                "titulo": "Completá el package.json para publicación",
                "descripcion": "QUÉ: agregá name, version, description, main, author, license, y el campo 'files' que define qué se publica. POR QUÉ: npm usa exactamente estos campos para saber qué instalar y cómo describir tu paquete en el registro.",
                "pista": "El campo 'name' tiene que ser único en todo npm si pensás publicarlo de verdad — probá con un scope propio (@tu-usuario/nombre) para evitar colisiones sin tener que buscar un nombre libre.",
            },
            {
                "titulo": "Aplicá versionado semántico",
                "descripcion": "QUÉ: elegí una versión inicial (por ejemplo 0.1.0) siguiendo el formato MAYOR.MENOR.PARCHE, y explicá qué cambiaría cada número. POR QUÉ: el versionado semántico le comunica a quien usa tu paquete qué tan seguro es actualizar: un cambio de PARCHE no debería romper nada, uno de MENOR agrega funcionalidad compatible, uno de MAYOR puede romper compatibilidad.",
                "pista": "Los comandos npm version patch, npm version minor y npm version major actualizan automáticamente el número en package.json y crean un tag de git.",
            },
            {
                "titulo": "Probá el paquete localmente antes de publicar",
                "descripcion": "QUÉ: usá npm link o npm pack para instalar tu paquete en otro proyecto local, como si viniera del registro real. POR QUÉ: esto te deja detectar problemas (archivos faltantes, imports rotos) antes de publicar algo roto públicamente.",
                "pista": "npm pack genera un archivo .tgz igual al que se subiría a npm — podés instalarlo en otro proyecto con npm install ../ruta/paquete.tgz.",
            },
            {
                "titulo": "Publicá (o simulá publicar) en un registro",
                "descripcion": "QUÉ: creá una cuenta en npmjs.com y publicá con npm publish, o si preferís no crear cuentas, usá un registro local como Verdaccio, o documentá paso a paso cómo se haría. POR QUÉ: practicar el proceso completo de publicación es lo que te prepara para hacerlo de verdad cuando tengas un paquete que valga la pena compartir.",
                "pista": "npm publish --access public es necesario para paquetes con scope (@usuario/nombre), si no van a quedar privados por defecto (y privados requiere una cuenta paga).",
            },
        ],
        "criterios": [
            "El package.json está completo con todos los campos necesarios para publicar.",
            "La versión sigue el formato semántico MAYOR.MENOR.PARCHE con una explicación de qué significaría subir cada número.",
            "El paquete se probó localmente (npm link o npm pack) antes de intentar publicarlo.",
            "Se completó (o se documentó paso a paso) la publicación en un registro.",
        ],
        "retos_extra": [
            "Agregá un README.md y una licencia al paquete.",
            "Configurá una GitHub Action que publique el paquete automáticamente en cada release.",
        ],
    },
    {
        "id": 25,
        "disponible_en_ide": "no",
        "titulo": "El patrón Middleware en Express",
        "descripcion": "Cada vez que usás CORS, autenticación o logging en Express, hay un middleware trabajando — armá los tuyos propios y entendé el orden de ejecución.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["middleware", "Express", "app.use()", "interceptores"],
        "xp": 200,
        "objetivo": "Entender cómo funciona un middleware por dentro implementando 2-3 middlewares propios en Express: uno de logging de requests, uno que mida tiempos de respuesta, y uno de autenticación simple.",
        "requisitos": ["Módulo: Closures y funciones de orden superior", "Módulo: try / catch / finally"],
        "pasos": [
            {
                "titulo": "Explicá qué es un middleware con tus palabras",
                "descripcion": "QUÉ: describí el patrón middleware: código que se ejecuta ANTES de que el request llegue a la ruta final, y que decide si dejarlo pasar (con next()) o cortarlo ahí. POR QUÉ: entender esta idea de 'capas que envuelven' es la base para poder razonar sobre en qué orden se ejecutan varios middlewares juntos, y por qué el orden importa.",
                "pista": "Pensá en un middleware como un control de acceso en fila: cada uno revisa el request y decide si lo deja pasar al siguiente (next()) o lo corta ahí con una respuesta propia.",
            },
            {
                "titulo": "Implementá un middleware de logging",
                "descripcion": "QUÉ: escribí un middleware con app.use((req, res, next) => {...}) que loguee el método y la ruta de cada request que llega. POR QUÉ: esto te deja ver en la práctica que el middleware se ejecuta para TODAS las rutas automáticamente, sin tener que agregar código repetido en cada una.",
                "pista": "No te olvides de llamar a next() al final, o el request se queda colgado sin respuesta — es el error más común al escribir tu primer middleware.",
            },
            {
                "titulo": "Implementá un middleware que mida tiempos de respuesta",
                "descripcion": "QUÉ: medí cuánto tarda en procesarse cada request, y agregá esa duración como un header en la respuesta (por ejemplo X-Response-Time). POR QUÉ: esto es exactamente el mismo patrón que usan las herramientas de monitoreo reales para medir performance sin modificar cada ruta individualmente — y conecta con lo que viste en el proyecto de Observabilidad.",
                "pista": "Guardá Date.now() al entrar al middleware, y usá res.on('finish', ...) para calcular la duración total una vez que la respuesta ya se envió.",
            },
            {
                "titulo": "Implementá autenticación simple como middleware",
                "descripcion": "QUÉ: escribí un middleware que revise un header (por ejemplo X-API-Key) y rechace el request con 401 si no está o es incorrecto, ANTES de que llegue a la ruta. POR QUÉ: esto muestra la diferencia práctica entre resolver algo como middleware global (se aplica a todo automáticamente) versus agregarlo ruta por ruta — cada enfoque tiene su lugar según si la regla aplica a TODA la API o solo a algunas rutas.",
                "pista": "Si el middleware detecta que falta o es inválida la key, devolvé la respuesta con res.status(401).json(...) y NO llames a next() — así el request nunca llega a la ruta real.",
            },
            {
                "titulo": "Ordená varios middlewares y observá el orden de ejecución",
                "descripcion": "QUÉ: agregá los 2-3 middlewares juntos y logueá en qué orden se ejecuta cada uno. POR QUÉ: en Express, el orden en que llamás a app.use() determina el orden real de ejecución — entender esto evita bugs sutiles, como un middleware de autenticación que se ejecuta DESPUÉS de uno que ya hizo trabajo costoso que no hacía falta hacer si el request iba a ser rechazado igual.",
                "pista": "Los middlewares se ejecutan en el orden exacto en que los agregaste con app.use() — logueá un mensaje al principio de cada uno para ver el orden real con tus propios ojos en la consola.",
            },
        ],
        "criterios": [
            "Existe una explicación propia de qué es un middleware y cómo decide dejar pasar o cortar un request.",
            "Hay al menos 2 middlewares propios funcionando: logging y medición de tiempos, como mínimo.",
            "Un middleware de autenticación simple rechaza requests sin la credencial correcta antes de llegar a la ruta.",
            "Se observó y se explica el orden real de ejecución cuando hay varios middlewares juntos.",
        ],
        "retos_extra": [
            "Compará el mismo chequeo de autenticación implementado como middleware global vs aplicado solo a rutas específicas, y explicá cuándo usarías cada enfoque.",
            "Agregá un middleware de manejo de errores (con 4 parámetros: err, req, res, next) que capture cualquier excepción no manejada y devuelva una respuesta de error consistente.",
        ],
    },
    {
        "id": 26,
        "disponible_en_ide": "no",
        "titulo": "CORS y same-origin policy: por qué tu fetch() falla",
        "descripcion": "Ese error rojo en la consola que dice 'blocked by CORS policy' — entendé qué es lo que realmente está pasando y cómo configurarlo bien del lado del servidor.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1 hora",
        "conceptos": ["CORS", "same-origin policy", "fetch", "Express"],
        "xp": 150,
        "objetivo": "Entender por qué el navegador bloquea ciertos requests entre orígenes distintos (same-origin policy), reproducir el error de CORS a propósito, y configurarlo correctamente del lado del servidor con Express.",
        "requisitos": ["Módulo: Promesas y async/await", "Módulo: DOM y eventos"],
        "pasos": [
            {
                "titulo": "Reproducí un error de CORS a propósito",
                "descripcion": "QUÉ: levantá un servidor Express simple en un puerto (por ejemplo 3001) sin configurar CORS, y desde una página HTML servida en otro puerto (por ejemplo 5500) hacé un fetch() hacia el primero. POR QUÉ: ver el error real en la consola del navegador ('blocked by CORS policy') es la mejor forma de entender qué problema estás resolviendo antes de arreglarlo.",
                "pista": "El error de CORS aparece en la consola del navegador, no en el servidor — el servidor en realidad respondió bien, es el navegador el que bloquea que JavaScript lea esa respuesta.",
            },
            {
                "titulo": "Explicá qué es la same-origin policy",
                "descripcion": "QUÉ: describí con tus palabras qué hace que dos URLs sean del 'mismo origen' (protocolo + dominio + puerto tienen que coincidir los tres), y por qué el navegador restringe requests entre orígenes distintos por defecto. POR QUÉ: CORS no es un capricho del servidor — es una relajación controlada de una protección de seguridad del navegador que existe para proteger al usuario, no a vos como developer.",
                "pista": "http://localhost:3000 y http://localhost:3001 son orígenes DISTINTOS porque el puerto no coincide, aunque el dominio (localhost) sea el mismo — es un error común pensar que solo importa el dominio.",
            },
            {
                "titulo": "Agregá el middleware CORS a tu servidor",
                "descripcion": "QUÉ: instalá el paquete cors (npm install cors) y agregalo con app.use(cors()) o configurándolo con opciones específicas. POR QUÉ: este middleware agrega los headers (Access-Control-Allow-Origin, entre otros) que le dicen al navegador que ESE origen específico tiene permiso para leer la respuesta.",
                "pista": "app.use(cors()) sin opciones permite CUALQUIER origen — andá directamente al paso siguiente para restringirlo, no lo dejes así en un proyecto real.",
            },
            {
                "titulo": "Restringí CORS a orígenes específicos",
                "descripcion": "QUÉ: configurá el middleware para permitir solo el origen real de tu frontend, no todos. POR QUÉ: permitir cualquier origen ('*') significa que cualquier sitio web podría hacer requests a tu API en nombre de un usuario que la tenga abierta — un riesgo real si tu API maneja datos sensibles o requiere sesión.",
                "pista": "cors({ origin: 'http://localhost:5500' }) o una lista de orígenes permitidos es la forma correcta — nunca '*' si tu API requiere autenticación.",
            },
            {
                "titulo": "Probá con y sin credentials",
                "descripcion": "QUÉ: si tu API usa cookies de sesión, probá agregar credentials: 'include' en el fetch() del cliente y credentials: true en la configuración de CORS del servidor, y observá qué pasa si falta alguno de los dos. POR QUÉ: para requests con credenciales (cookies, headers de auth), el navegador exige que AMBOS lados (cliente y servidor) declaren explícitamente que aceptan compartir esas credenciales entre orígenes — es una capa extra de protección para datos de sesión.",
                "pista": "Si configurás credentials: true en el servidor pero el origin sigue siendo '*', el navegador va a bloquear igual el request — con credenciales, CORS exige un origen explícito, no comodín.",
            },
        ],
        "criterios": [
            "Se reprodujo y se explica el error real de CORS visto en la consola del navegador.",
            "Existe una explicación propia de la same-origin policy.",
            "El middleware CORS está configurado con un origen explícito, no con '*'.",
            "Se probó el caso de requests con credenciales (cookies) y CORS configurado para aceptarlas.",
        ],
        "retos_extra": [
            "Investigá qué es un preflight request (OPTIONS) y cuándo el navegador lo dispara automáticamente antes de tu request real.",
            "Configurá CORS para permitir solo ciertos métodos HTTP (GET, POST) y no otros.",
        ],
    },
    {
        "id": 27,
        "disponible_en_ide": "no",
        "titulo": "GraphQL como alternativa a REST",
        "descripcion": "Un solo endpoint, el cliente pide exactamente los datos que necesita — armá un mini servidor GraphQL y compará el enfoque con REST.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["GraphQL", "schemas", "resolvers", "queries", "REST vs GraphQL"],
        "xp": 225,
        "objetivo": "Construir un mini endpoint GraphQL con Express (usando express-graphql o apollo-server) que exponga los mismos datos que una API REST existente, y comparar ambos enfoques en la práctica.",
        "requisitos": ["Proyecto: Sistema de gestión de estudiantes (CRUD)", "Módulo: Objetos: propiedades y métodos"],
        "pasos": [
            {
                "titulo": "Definí tu schema de GraphQL",
                "descripcion": "QUÉ: escribí el schema (tipos y queries) que describe qué datos existen y cómo se pueden pedir, usando el lenguaje de definición de tipos de GraphQL. POR QUÉ: a diferencia de REST (donde cada endpoint define su propia forma de respuesta), en GraphQL el schema es un contrato único y explícito de TODO lo que el cliente puede pedir.",
                "pista": "type Estudiante { id: ID, nombre: String, notas: [Int] } y type Query { estudiantes: [Estudiante] } es la sintaxis básica de un schema mínimo.",
            },
            {
                "titulo": "Escribí los resolvers",
                "descripcion": "QUÉ: implementá las funciones (resolvers) que efectivamente van a buscar y devolver los datos para cada campo del schema. POR QUÉ: el schema solo describe la forma de los datos — los resolvers son el código real que sabe cómo conseguirlos (de un array en memoria, una base de datos, etc.).",
                "pista": "Un resolver para 'estudiantes' es simplemente una función que devuelve tu array de estudiantes — podés reusar los mismos datos que ya tenías en tu API REST.",
            },
            {
                "titulo": "Montá el endpoint único de GraphQL",
                "descripcion": "QUÉ: usá express-graphql (o apollo-server-express) para exponer un solo endpoint (típicamente /graphql) que reciba las queries. POR QUÉ: a diferencia de REST donde cada recurso tiene su propia URL, GraphQL expone UN SOLO endpoint — toda la flexibilidad está en qué le pedís en el body del request, no en la URL.",
                "pista": "La mayoría de las herramientas de GraphQL te dan también una interfaz interactiva (como GraphiQL) en el navegador para probar queries sin escribir código cliente todavía.",
            },
            {
                "titulo": "Pedí exactamente los campos que necesitás",
                "descripcion": "QUÉ: hacé dos queries distintas: una pidiendo solo el nombre de los estudiantes, y otra pidiendo nombre y notas. POR QUÉ: esto demuestra la ventaja central de GraphQL sobre REST: el cliente decide exactamente qué datos quiere en cada pedido, sin recibir de más (over-fetching) ni tener que hacer múltiples requests para juntar lo que necesita (under-fetching).",
                "pista": "{ estudiantes { nombre } } devuelve SOLO el nombre de cada estudiante, aunque el resolver internamente tenga acceso a todos los demás campos.",
            },
            {
                "titulo": "Comparé con tu API REST equivalente",
                "descripcion": "QUÉ: escribí una comparación concreta: cuántos requests necesitarías en REST para conseguir lo mismo que una sola query de GraphQL, y en qué casos REST sigue siendo más simple. POR QUÉ: GraphQL no es 'mejor' que REST en abstracto — resuelve problemas específicos (over/under-fetching, múltiples requests para datos relacionados) a costa de más complejidad en el servidor, y elegir uno u otro depende del caso real.",
                "pista": "Pensá en un caso concreto de tu proyecto: si necesitás mostrar un estudiante junto con sus notas Y sus datos de contacto, ¿cuántos endpoints REST distintos tendrías que llamar versus una sola query GraphQL?",
            },
        ],
        "criterios": [
            "El schema define al menos un tipo y una query.",
            "Los resolvers devuelven datos reales, no valores fijos hardcodeados.",
            "El endpoint único /graphql funciona y responde a queries reales.",
            "Se probaron al menos 2 queries pidiendo campos distintos del mismo tipo.",
            "Existe una comparación explícita con el enfoque REST equivalente.",
        ],
        "retos_extra": [
            "Agregá una mutation para crear un estudiante nuevo vía GraphQL.",
            "Agregá un resolver anidado (por ejemplo estudiante -> curso -> profesor) y observá cómo GraphQL resuelve relaciones sin joins manuales de tu parte.",
        ],
    },
    {
        "id": 28,
        "disponible_en_ide": "no",
        "titulo": "Performance web: lazy loading, bundling y minificación",
        "descripcion": "Por qué tu página tarda en cargar, y qué podés hacer al respecto — cargá menos, más tarde, y más chico.",
        "dificultad": "Intermedio+",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["lazy loading", "bundling", "minificación", "performance web"],
        "xp": 175,
        "objetivo": "Mejorar el tiempo de carga de un proyecto web propio aplicando lazy loading de imágenes, empaquetado (bundling) de múltiples archivos JS en uno, y minificación, midiendo el impacto real de cada técnica.",
        "requisitos": ["Módulo: DOM y eventos", "Proyecto: Node.js y npm: gestores de paquetes en JS"],
        "pasos": [
            {
                "titulo": "Medí el estado actual con las DevTools",
                "descripcion": "QUÉ: abrí la pestaña Network de Chrome DevTools en un proyecto tuyo, recargá la página, y anotá cuántos requests se hacen y cuánto tarda en cargar todo. POR QUÉ: no podés medir una mejora si no tenés un número de partida — esta es tu línea de base antes de optimizar cualquier cosa.",
                "pista": "Fijate especialmente en el tamaño total transferido y el tiempo hasta que la página se vuelve interactiva, no solo cuándo termina de cargar todo.",
            },
            {
                "titulo": "Aplicá lazy loading a las imágenes",
                "descripcion": "QUÉ: agregá el atributo loading='lazy' a las etiquetas <img> que no son visibles inmediatamente al cargar la página (las que están más abajo, fuera de la pantalla inicial). POR QUÉ: cargar imágenes que el usuario todavía no va a ver desperdicia ancho de banda y retrasa la carga de lo que sí es visible de entrada.",
                "pista": "loading='lazy' es un atributo nativo del navegador, no necesitás ninguna librería — pero no lo pongas en imágenes que SÍ son visibles al cargar (como el logo o el hero), ahí lo ideal es que carguen inmediato.",
            },
            {
                "titulo": "Empaquetá tus archivos JS en un bundle",
                "descripcion": "QUÉ: si tu proyecto tiene varios archivos <script> separados, usá una herramienta de bundling (como esbuild o Vite) para combinarlos en uno solo. POR QUÉ: cada archivo separado es un request HTTP distinto — combinar varios en uno reduce la cantidad de idas y vueltas entre el navegador y el servidor, que suelen pesar más que el tamaño de los archivos en sí.",
                "pista": "npx esbuild entrada.js --bundle --outfile=bundle.js es un comando mínimo para empezar a experimentar con bundling sin configuración compleja.",
            },
            {
                "titulo": "Minificá el resultado",
                "descripcion": "QUÉ: generá una versión minificada de tu bundle (sin espacios, saltos de línea ni nombres de variables largos). POR QUÉ: un archivo minificado pesa menos bytes para transferir, aunque el código siga haciendo exactamente lo mismo — es pura reducción de tamaño, sin cambiar comportamiento.",
                "pista": "La mayoría de las herramientas de bundling (esbuild, Vite, webpack) tienen un flag de minificación (--minify en esbuild) que hace esto automáticamente.",
            },
            {
                "titulo": "Medí de nuevo y comparé",
                "descripcion": "QUÉ: repetí la medición del paso 1 con los cambios aplicados, y comparé cantidad de requests, tamaño transferido y tiempo de carga contra el número de partida. POR QUÉ: esto es lo que convierte esto de 'hice cosas que suenan bien' a una optimización real y verificada — sin medir el antes y el después, no sabés si realmente mejoraste algo.",
                "pista": "Anotá los tres números (requests, tamaño transferido, tiempo de carga) en una tabla simple de antes/después para que la comparación sea concreta, no una impresión general.",
            },
        ],
        "criterios": [
            "Existe una medición de línea de base documentada con DevTools (requests, tamaño, tiempo).",
            "Al menos una imagen usa lazy loading correctamente.",
            "Los archivos JS del proyecto están empaquetados en un bundle.",
            "El bundle final está minificado.",
            "Existe una medición final comparada explícitamente contra la línea de base, con números concretos.",
        ],
        "retos_extra": [
            "Investigá code splitting: cargar un bundle separado solo para una sección de la página que no todos los usuarios visitan.",
            "Agregá compresión gzip o brotli del lado del servidor y medí el impacto adicional sobre el tamaño transferido.",
        ],
    },
]


# ═══════════════════════════════════ C++ ═══════════════════════════════════
PROYECTOS_CPP = [
    {
        "id": 1,
        "disponible_en_ide": "si",
        "titulo": "Calculadora de consola",
        "descripcion": "Programa que lee dos números y una operación, muestra el resultado y repite hasta que el usuario decida salir.",
        "dificultad": "Principiante",
        "tiempo_estimado": "30-45 min",
        "conceptos": ["funciones", "switch", "operadores", "entrada/salida"],
        "xp": 150,
        "objetivo": "Construir una calculadora de consola que lea dos números y una operación, muestre el resultado, y permita repetir el cálculo sin reiniciar el programa.",
        "requisitos": ["Módulo: cin: entrada del usuario", "Módulo: Funciones en C++", "Módulo: if/else y switch"],
        "pasos": [
            {
                "titulo": "Leé dos números y un operador",
                "descripcion": "QUÉ: usá cin para leer dos double y un char que represente la operación (+, -, *, /). POR QUÉ: necesitás los tres datos antes de poder calcular nada.",
                "pista": "cin >> a >> op >> b; permite leer los tres valores en una sola línea separados por espacios.",
            },
            {
                "titulo": "Escribí una función por operación",
                "descripcion": "QUÉ: funciones sumar, restar, multiplicar, dividir que reciban dos double y devuelvan double. POR QUÉ: separar cada operación en su propia función hace el código más legible que un solo bloque gigante.",
                "pista": "Cada función es de una sola línea: return a + b; por ejemplo.",
            },
            {
                "titulo": "Elegí la operación con switch",
                "descripcion": "QUÉ: según el char leído, llamá a la función correspondiente. POR QUÉ: switch es la herramienta natural cuando comparás una variable contra varios valores fijos.",
                "pista": "case '+': resultado = sumar(a, b); break; — repetí el patrón para cada operador.",
            },
            {
                "titulo": "Manejá la división por cero",
                "descripcion": "QUÉ: antes de dividir, verificá que el divisor no sea 0 y mostrá un mensaje de error si lo es. POR QUÉ: dividir por cero con floats en C++ da inf o nan, es mejor prevenirlo explícitamente.",
                "pista": "if (b == 0) { cout << \"Error: no se puede dividir por cero\" << endl; } antes de llamar a dividir().",
            },
            {
                "titulo": "Repetí con un bucle hasta que el usuario salga",
                "descripcion": "QUÉ: envolvé todo en un while que pregunte si querés hacer otra operación. POR QUÉ: una calculadora de un solo uso no es muy útil en la práctica.",
                "pista": "Podés usar un char de respuesta ('s'/'n') o un do-while que siempre ejecute al menos una vez.",
            },
        ],
        "criterios": [
            "La calculadora hace las 4 operaciones básicas correctamente.",
            "No crashea ni da resultados inválidos al dividir por cero.",
            "Permite hacer varias operaciones seguidas sin reiniciar el programa.",
        ],
        "retos_extra": [
            "Agregá potencia y raíz cuadrada.",
            "Agregá un historial de operaciones realizadas en la sesión.",
            "Validá que el operador ingresado sea válido y volvé a pedirlo si no lo es.",
        ],
    },
    {
        "id": 2,
        "disponible_en_ide": "si",
        "titulo": "Tres en raya (Tic-Tac-Toe)",
        "descripcion": "Juego de tres en raya para dos jugadores en la misma consola, con tablero visual en texto.",
        "dificultad": "Principiante+",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["arreglos 2D", "lógica de juego", "bucles"],
        "xp": 175,
        "objetivo": "Construir el clásico juego de tres en raya para dos jugadores, jugado por turnos en la misma consola con un tablero visual en texto.",
        "requisitos": ["Módulo: Bucles en C++", "Módulo: Arrays y vectores STL"],
        "pasos": [
            {
                "titulo": "Representá el tablero",
                "descripcion": "QUÉ: usá una matriz 3x3 (array 2D o vector de vectores) inicializada con espacios vacíos. POR QUÉ: necesitás una estructura donde guardar el estado del juego en todo momento.",
                "pista": "char tablero[3][3]; inicializado con ' ' en cada celda es suficiente para empezar.",
            },
            {
                "titulo": "Mostrá el tablero en pantalla",
                "descripcion": "QUÉ: escribí una función que imprima la matriz con separadores tipo | y -. POR QUÉ: sin ver el tablero los jugadores no pueden decidir su siguiente jugada.",
                "pista": "Un doble bucle for (filas y columnas) recorre la matriz e imprime cada celda con su separador.",
            },
            {
                "titulo": "Pedí la jugada y validala",
                "descripcion": "QUÉ: pedí fila y columna al jugador actual, verificá que estén dentro del rango y que la celda esté vacía. POR QUÉ: sin validación, un jugador podría sobrescribir una jugada ya hecha o salirse del tablero.",
                "pista": "Repetí el pedido dentro de un bucle hasta recibir una jugada válida, en vez de aceptar cualquier entrada.",
            },
            {
                "titulo": "Alterná turnos entre X y O",
                "descripcion": "QUÉ: llevá una variable que indique de quién es el turno y cambiala después de cada jugada válida. POR QUÉ: es la regla central del juego, sin esto no hay competencia entre dos jugadores.",
                "pista": "Un char turno = 'X'; que se actualice con turno = (turno == 'X') ? 'O' : 'X'; después de cada jugada.",
            },
            {
                "titulo": "Detectá el ganador o el empate",
                "descripcion": "QUÉ: después de cada jugada, revisá filas, columnas y diagonales para ver si alguien ganó, o si el tablero se llenó sin ganador. POR QUÉ: sin esta lógica el juego nunca termina formalmente.",
                "pista": "Una función separada que revise las 8 combinaciones ganadoras posibles mantiene el código de main() más ordenado.",
            },
        ],
        "criterios": [
            "El tablero se muestra correctamente después de cada jugada.",
            "El juego no permite jugadas inválidas (fuera de rango o sobre una celda ocupada).",
            "Detecta correctamente la victoria en fila, columna o diagonal, y también el empate.",
        ],
        "retos_extra": [
            "Agregá un modo contra la computadora con jugadas aleatorias válidas.",
            "Agregá un contador de partidas ganadas por jugador.",
            "Permití tableros de tamaño configurable (4x4, 5x5).",
        ],
    },
    {
        "id": 3,
        "disponible_en_ide": "si",
        "titulo": "Sistema de gestión de biblioteca (POO)",
        "descripcion": "Sistema en consola para gestionar libros de una biblioteca: agregar, buscar, prestar y devolver.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["clases", "herencia", "vectores", "encapsulamiento"],
        "xp": 225,
        "objetivo": "Construir un sistema de gestión de biblioteca en consola: agregar libros al catálogo, buscarlos, prestarlos y devolverlos.",
        "requisitos": ["Módulo: Structs y clases", "Módulo: Arrays y vectores STL"],
        "pasos": [
            {
                "titulo": "Diseñá la clase Libro",
                "descripcion": "QUÉ: atributos privados título, autor, ISBN, disponible; getters y un método mostrar(). POR QUÉ: encapsular los datos evita que se modifiquen desde fuera sin control.",
                "pista": "Marcá los atributos como private y exponé solo lo necesario a través de métodos públicos.",
            },
            {
                "titulo": "Guardá los libros en un vector",
                "descripcion": "QUÉ: una clase Biblioteca con un vector<Libro> como catálogo. POR QUÉ: necesitás una colección dinámica ya que no sabés cuántos libros vas a tener de antemano.",
                "pista": "vector<Libro> catalogo; se puede ir llenando con push_back() a medida que agregás libros.",
            },
            {
                "titulo": "Implementá agregar y listar",
                "descripcion": "QUÉ: métodos para sumar un libro nuevo al catálogo y mostrar todos. POR QUÉ: es la operación más básica antes de sumar lógica de préstamos.",
                "pista": "Para listar, un range-based for (const Libro& l : catalogo) recorre todo el vector sin copiar cada elemento.",
            },
            {
                "titulo": "Implementá buscar por título o autor",
                "descripcion": "QUÉ: recorré el vector comparando el texto buscado (podés usar find_if de <algorithm>). POR QUÉ: en una biblioteca real, buscar es una operación más frecuente que listar todo el catálogo.",
                "pista": "find_if(catalogo.begin(), catalogo.end(), [&](const Libro& l) { return l.getTitulo() == buscado; });",
            },
            {
                "titulo": "Implementá prestar y devolver",
                "descripcion": "QUÉ: métodos que cambien el atributo disponible del libro correspondiente, validando su estado actual. POR QUÉ: es la funcionalidad central de gestión de una biblioteca real.",
                "pista": "Antes de prestar, verificá que el libro esté disponible; antes de devolver, que esté efectivamente prestado.",
            },
        ],
        "criterios": [
            "Se pueden agregar, buscar, prestar y devolver libros sin errores.",
            "Un libro prestado no se puede volver a prestar hasta que se devuelva.",
            "Los atributos de Libro están correctamente encapsulados (privados, accesibles vía métodos).",
        ],
        "retos_extra": [
            "Agregá una clase Socio y llevá registro de quién tiene prestado cada libro.",
            "Agregá fecha límite de devolución y detectá atrasos.",
            "Persistí el catálogo en un archivo de texto entre ejecuciones.",
        ],
    },
    {
        "id": 4,
        "disponible_en_ide": "no",
        "titulo": "Juego de la serpiente (Snake) en consola",
        "descripcion": "Versión simplificada de Snake que corre en la consola, con movimiento en tiempo real y detección de colisiones.",
        "dificultad": "Intermedio+",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["estructuras", "punteros", "lógica en tiempo real"],
        "xp": 250,
        "objetivo": "Construir una versión simplificada del juego Snake que corra en la consola, moviendo la serpiente con el teclado en tiempo real.",
        "requisitos": ["Módulo: Structs y clases", "Módulo: Arrays y vectores STL", "Módulo: Bucles en C++"],
        "pasos": [
            {
                "titulo": "Representá la serpiente y el tablero",
                "descripcion": "QUÉ: usá una estructura para cada segmento (posición x, y) y un vector o lista para toda la serpiente. POR QUÉ: la serpiente crece dinámicamente, necesitás una colección que soporte eso.",
                "pista": "struct Punto { int x, y; }; y vector<Punto> serpiente; como punto de partida.",
            },
            {
                "titulo": "Dibujá el estado del juego",
                "descripcion": "QUÉ: una función que imprima el tablero completo (bordes, serpiente, comida) en cada vuelta del loop principal. POR QUÉ: en un juego en tiempo real necesitás refrescar la pantalla constantemente para mostrar el estado actual.",
                "pista": "system(\"cls\") en Windows limpia la consola antes de redibujar el tablero en cada vuelta.",
            },
            {
                "titulo": "Leé el input sin bloquear el juego",
                "descripcion": "QUÉ: investigá cómo leer una tecla sin que el programa se detenga a esperar (por ejemplo _kbhit()/_getch() en Windows). POR QUÉ: con cin normal el juego se pausaría esperando Enter, rompiendo la sensación de tiempo real.",
                "pista": "La librería conio.h en Windows tiene _kbhit() para saber si hay una tecla presionada y _getch() para leerla sin bloquear.",
            },
            {
                "titulo": "Mové la serpiente y detectá colisiones",
                "descripcion": "QUÉ: en cada vuelta, actualizá la posición de la cabeza según la dirección actual, y verificá colisión contra los bordes o contra su propio cuerpo. POR QUÉ: es lo que determina si el juego termina.",
                "pista": "La cabeza nueva se agrega al frente del vector y, si no comió, se elimina el último segmento para simular movimiento.",
            },
            {
                "titulo": "Hacé que coma y crezca",
                "descripcion": "QUÉ: cuando la cabeza llega a la posición de la comida, agregá un segmento nuevo y generá comida en una posición nueva al azar. POR QUÉ: es la mecánica central que hace que el juego se vuelva progresivamente más difícil.",
                "pista": "Si la cabeza coincide con la comida, simplemente no elimines el último segmento en esa vuelta: así la serpiente crece un lugar.",
            },
        ],
        "criterios": [
            "La serpiente se mueve fluidamente según el input del jugador.",
            "El juego detecta correctamente cuándo choca contra el borde o contra sí misma.",
            "La serpiente crece cada vez que come.",
        ],
        "retos_extra": [
            "Agregá un marcador de puntaje en pantalla.",
            "Agregá niveles de velocidad creciente a medida que crece la serpiente.",
            "Guardá el mejor puntaje entre partidas en un archivo.",
        ],
    },
    {
        "id": 5,
        "disponible_en_ide": "si",
        "titulo": "Evaluador de expresiones matemáticas",
        "descripcion": "Programa que recibe una expresión matemática como texto y calcula su resultado respetando la precedencia de operadores.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "3-4 horas",
        "conceptos": ["pilas", "parsing", "precedencia de operadores"],
        "xp": 300,
        "objetivo": "Construir un programa que reciba una expresión matemática como texto (por ejemplo '3 + 4 * 2') y calcule su resultado respetando la precedencia de operadores.",
        "requisitos": ["Módulo: Stack y Queue con STL", "Módulo: Funciones en C++"],
        "pasos": [
            {
                "titulo": "Investigá el algoritmo shunting-yard o notación postfija",
                "descripcion": "QUÉ: entendé conceptualmente cómo convertir una expresión infija (la normal) a postfija (RPN) usando una pila auxiliar. POR QUÉ: evaluar directamente una expresión infija con paréntesis y precedencia es complejo; convertirla primero simplifica mucho el problema.",
                "pista": "Buscá 'shunting-yard algorithm' y prestá atención especialmente a cómo se maneja la precedencia y los paréntesis.",
            },
            {
                "titulo": "Tokenizá la expresión",
                "descripcion": "QUÉ: separá el string de entrada en números, operadores y paréntesis individuales. POR QUÉ: no podés procesar la expresión como un solo bloque de texto, necesitás trabajar con sus piezas por separado.",
                "pista": "Podés recorrer el string carácter por carácter, acumulando dígitos consecutivos para formar números de más de una cifra.",
            },
            {
                "titulo": "Convertí a notación postfija",
                "descripcion": "QUÉ: usando una pila auxiliar, aplicá las reglas de precedencia (* y / antes que + y -) para reordenar los tokens. POR QUÉ: es el paso central del algoritmo que resuelve el problema de la precedencia.",
                "pista": "Los números van directo a la salida; los operadores se comparan contra el tope de la pila antes de apilarse.",
            },
            {
                "titulo": "Evaluá la expresión postfija",
                "descripcion": "QUÉ: recorré los tokens postfijos usando una pila: los números se apilan, y los operadores toman los dos últimos valores apilados para apilar el resultado. POR QUÉ: la notación postfija se evalúa de forma mecánica, sin necesidad de reglas de precedencia adicionales.",
                "pista": "Al final del recorrido, el único valor que queda en la pila es el resultado de la expresión completa.",
            },
            {
                "titulo": "Manejá errores de expresión",
                "descripcion": "QUÉ: detectá paréntesis desbalanceados, operadores sin suficientes operandos, o división por cero. POR QUÉ: un evaluador real tiene que fallar con gracia ante entradas inválidas, no crashear.",
                "pista": "Verificá el tamaño de la pila antes de hacer pop(): si tiene menos elementos de los que necesitás, la expresión es inválida.",
            },
        ],
        "criterios": [
            "El programa evalúa correctamente expresiones con +, -, *, /, y paréntesis, respetando la precedencia.",
            "Maneja errores de sintaxis sin crashear.",
            "Da el mismo resultado que una calculadora estándar para al menos 5 expresiones de prueba distintas.",
        ],
        "retos_extra": [
            "Agregá soporte para potencia (^) y números decimales.",
            "Agregá funciones como sqrt() o funciones trigonométricas.",
            "Construí un modo interactivo que permita ingresar expresiones repetidamente.",
        ],
    },
    {
        "id": 6,
        "disponible_en_ide": "no",
        "titulo": "Git para proyectos C++",
        "descripcion": "Versioná un proyecto C++ con Git sin ensuciar el repositorio con binarios compilados.",
        "dificultad": "Principiante+",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["control de versiones", "git", "ramas", "github"],
        "xp": 175,
        "objetivo": "Aprender a usar Git sobre un proyecto C++: guardar el historial en commits, trabajar con ramas, y publicarlo en GitHub sin versionar ejecutables ni archivos objeto que se regeneran en cada compilación.",
        "requisitos": ["Cualquier proyecto propio en una carpeta (podés usar el Sistema de gestión de biblioteca)"],
        "pasos": [
            {
                "titulo": "Inicializá el repositorio",
                "descripcion": "QUÉ: parado en la carpeta de tu proyecto, corré git init. POR QUÉ: eso crea la carpeta oculta .git donde se guarda todo el historial de cambios.",
                "pista": "git status te muestra en todo momento qué archivos están sin trackear, modificados o listos para commitear.",
            },
            {
                "titulo": "Creá un .gitignore para binarios ANTES del primer commit",
                "descripcion": "QUÉ: un .gitignore que excluya los archivos que genera el compilador: *.exe, *.o, *.obj, y la carpeta build/. POR QUÉ: esos archivos se regeneran cada vez que compilás — versionarlos infla el repositorio y genera conflictos sin sentido entre distintas máquinas.",
                "pista": "Mínimo para C++: *.exe, *.o, *.obj, *.out, build/, *.exe.stackdump — hacé esto ANTES de tu primer git add.",
            },
            {
                "titulo": "Configurá tu identidad y hacé el primer commit",
                "descripcion": "QUÉ: git config para nombre/email, git add para el staging area, git commit -m con mensaje claro. POR QUÉ: cada commit es un punto al que podés volver si algo se rompe.",
                "pista": "git config --global user.name \"Tu Nombre\" — commiteá solo el código fuente (.cpp, .h) y el .gitignore, nunca el ejecutable compilado.",
            },
            {
                "titulo": "Trabajá con ramas (branches)",
                "descripcion": "QUÉ: creá una rama con git switch -c, agregá una función nueva ahí, y mergeala a main cuando funcione. POR QUÉ: te deja probar cambios riesgosos (como cambiar una estructura de datos) sin romper la versión que ya andaba.",
                "pista": "git switch -c agregar-revista — al terminar: git switch main && git merge agregar-revista",
            },
            {
                "titulo": "Subilo a GitHub",
                "descripcion": "QUÉ: creá un repo vacío en GitHub, conectalo con git remote add origin y subí con git push. POR QUÉ: tu código queda respaldado y disponible como portfolio, con instrucciones de compilación para cualquiera que lo quiera probar.",
                "pista": "git remote add origin <url> — git push -u origin main. En el README.md incluí el comando exacto de compilación: g++ -o programa main.cpp -std=c++17",
            },
        ],
        "criterios": [
            "Ningún archivo .exe, .o u .obj aparece en el historial de Git.",
            "El proyecto tiene al menos 4 commits con mensajes descriptivos.",
            "Se usó al menos una rama separada que después se mergeó a main.",
            "El repositorio en GitHub tiene un README con las instrucciones de compilación.",
        ],
        "retos_extra": [
            "Provocá un conflicto de merge a propósito y resolvelo a mano.",
            "Agregá un GitHub Action que compile tu proyecto automáticamente en cada push (verificando que no rompiste el build).",
            "Escribí los commits siguiendo Conventional Commits (feat:, fix:, docs:).",
        ],
    },
    {
        "id": 7,
        "disponible_en_ide": "no",
        "titulo": "Debugging con GDB: encontrá bugs como un profesional",
        "descripcion": "Usá el debugger de línea de comandos de C++ para encontrar segfaults y otros bugs reales.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["gdb", "breakpoints", "segmentation fault", "backtrace"],
        "xp": 200,
        "objetivo": "Aprender a usar GDB para pausar un programa C++ en cualquier línea, inspeccionar variables y memoria, y diagnosticar la causa exacta de un segmentation fault en vez de adivinar.",
        "requisitos": ["Módulo: Punteros y referencias", "Módulo: Manejo de excepciones"],
        "pasos": [
            {
                "titulo": "Compilá con información de debug",
                "descripcion": "QUÉ: compilá tu programa con la flag -g, que agrega información de debug (nombres de variables, líneas) al ejecutable. POR QUÉ: sin -g, GDB solo ve direcciones de memoria crudas, sin poder mostrarte nombres de variables ni líneas de código.",
                "pista": "g++ -g -o programa main.cpp -std=c++17 — el ejecutable pesa un poco más, pero es indispensable para debuggear.",
            },
            {
                "titulo": "Provocá y capturá un segmentation fault",
                "descripcion": "QUÉ: escribí (o usá) un programa con un bug real de memoria, por ejemplo acceder a un puntero después de un delete, o desreferenciar un puntero nulo. POR QUÉ: los segfaults son de los errores más frustrantes de C++ porque el programa crashea sin decirte directamente cuál línea falló.",
                "pista": "Un bug clásico: int* p = nullptr; cout << *p; — o un vector.at(indice) con un índice fuera de rango (aunque ese lanza una excepción, no un segfault directo).",
            },
            {
                "titulo": "Iniciá GDB y usá breakpoints",
                "descripcion": "QUÉ: corré gdb ./programa, poné un breakpoint en la función sospechosa con break nombreFuncion, y ejecutá con run. POR QUÉ: pausar antes de la línea problemática te deja inspeccionar el estado exacto de las variables justo antes de que todo explote.",
                "pista": "gdb ./programa — dentro de gdb: break main — run — next (avanza línea por línea) — print variable (muestra su valor)",
            },
            {
                "titulo": "Usá backtrace después de un crash",
                "descripcion": "QUÉ: dejá que el programa crashee dentro de GDB (sin breakpoints, solo run) y después corré bt (backtrace). POR QUÉ: backtrace te muestra la pila COMPLETA de llamadas que llevó al crash, señalando la línea exacta donde ocurrió.",
                "pista": "bt te lista las funciones de la más reciente (donde crasheó) a la más antigua. frame N te mueve a inspeccionar las variables de un nivel específico de esa pila.",
            },
            {
                "titulo": "Corregí el bug y verificá con GDB",
                "descripcion": "QUÉ: una vez identificada la causa exacta, arreglá el código, recompilá con -g y volvé a correr en GDB para confirmar que ya no crashea. POR QUÉ: cerrar el ciclo verificando en la misma herramienta te da certeza real, no solo la esperanza de que 'ahora sí debería andar'.",
                "pista": "Si el programa corre hasta el final sin crashear, GDB te devuelve el control normalmente y podés ver el mensaje '[Inferior 1 (process ...) exited normally]'.",
            },
        ],
        "criterios": [
            "Compilaste con -g y pudiste ver nombres de variables reales dentro de GDB (no solo direcciones de memoria).",
            "Usaste breakpoints y next/step para inspeccionar el programa antes del crash.",
            "Usaste backtrace para identificar la línea exacta del segmentation fault.",
            "Corregiste el bug y verificaste con GDB que el programa ya no crashea.",
        ],
        "retos_extra": [
            "Investigá watch variable para pausar automáticamente cuando una variable específica cambia de valor.",
            "Probá compilar con -fsanitize=address, una herramienta que detecta errores de memoria con mensajes mucho más claros que un segfault crudo.",
            "Usá GDB para inspeccionar el contenido de un vector o struct completo con print *puntero o print miVector",
        ],
    },
    {
        "id": 8,
        "disponible_en_ide": "si",
        "titulo": "Testing en C++ con asserts y un mini framework",
        "descripcion": "Armá tu propio sistema de tests para verificar que tu código C++ funciona, sin depender de librerías externas.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["assert", "testing", "TDD básico"],
        "xp": 200,
        "objetivo": "Aprender los fundamentos del testing automatizado en C++ usando <cassert>, y después construir un mini framework casero que agrupe tests y reporte cuántos pasaron y cuántos fallaron.",
        "requisitos": ["Módulo: Recursividad", "Módulo: Manejo de excepciones"],
        "pasos": [
            {
                "titulo": "Escribí tus primeros tests con assert",
                "descripcion": "QUÉ: usá <cassert> para verificar que una función (por ejemplo tu factorial o mcd recursivos) devuelve el valor esperado. POR QUÉ: assert(condicion) detiene el programa inmediatamente si la condición es falsa, mostrando la línea exacta — es la forma más simple de verificar que tu código hace lo que pensás.",
                "pista": "#include <cassert> — assert(factorial(5) == 120); — si compilás con NDEBUG definido, los asserts se desactivan, así que usalos solo para desarrollo/testing, no como validación en producción.",
            },
            {
                "titulo": "Agrupá varios asserts en funciones de test",
                "descripcion": "QUÉ: creá funciones como void test_factorial() { assert(...); assert(...); } y llamalas todas desde main(). POR QUÉ: agrupar los asserts por función que estás probando hace mucho más fácil ver qué se rompió cuando algo falla.",
                "pista": "void test_factorial() { assert(factorial(0) == 1); assert(factorial(1) == 1); assert(factorial(5) == 120); cout << \"test_factorial: OK\" << endl; }",
            },
            {
                "titulo": "Armá un mini framework que cuente pass/fail",
                "descripcion": "QUÉ: en vez de que un assert fallido crashee todo el programa, escribí una función CHECK(condicion, nombreTest) que imprima PASS o FAIL y siga corriendo el resto de los tests. POR QUÉ: un framework de testing real nunca se detiene en el primer fallo — corre TODOS los tests y te da un resumen completo al final.",
                "pista": "int pasados = 0, fallados = 0; void CHECK(bool condicion, string nombre) { if (condicion) { cout << \"PASS: \" << nombre << endl; pasados++; } else { cout << \"FAIL: \" << nombre << endl; fallados++; } }",
            },
            {
                "titulo": "Testeá casos límite, no solo el camino feliz",
                "descripcion": "QUÉ: agregá tests para entradas raras: números negativos, cero, listas vacías, valores muy grandes. POR QUÉ: la mayoría de los bugs reales aparecen en los bordes del comportamiento esperado, no en el caso obvio que probás primero.",
                "pista": "Para tu BST del sendero: ¿qué pasa si buscás en un árbol vacío? ¿Qué pasa si insertás el mismo valor dos veces? Esos son los tests que realmente atrapan bugs.",
            },
            {
                "titulo": "Mostrá un resumen final",
                "descripcion": "QUÉ: al final de main(), imprimí cuántos tests pasaron y cuántos fallaron en total, y devolvé un código de salida distinto de 0 si hubo fallos. POR QUÉ: un código de salida distinto de 0 es lo que le permite a herramientas externas (como CI/CD) saber automáticamente si los tests pasaron o no.",
                "pista": "cout << pasados << \" pasaron, \" << fallados << \" fallaron\" << endl; return fallados > 0 ? 1 : 0;",
            },
        ],
        "criterios": [
            "Existen al menos 10 checks/asserts distribuidos en varias funciones de test.",
            "El framework casero sigue corriendo todos los tests aunque alguno falle (no se detiene en el primero).",
            "Hay tests específicos para casos límite (vacío, cero, negativo, duplicado), no solo el caso normal.",
            "El programa termina con un resumen claro de pasados/fallados y un código de salida acorde.",
        ],
        "retos_extra": [
            "Investigá Catch2, una librería de testing header-only muy popular en C++, e instalala para reescribir tus tests con ella.",
            "Agregá medición de tiempo a cada test para detectar si alguno es sospechosamente lento.",
            "Integrá tus tests a un GitHub Action que los corra automáticamente en cada push.",
        ],
    },
    {
        "id": 9,
        "disponible_en_ide": "no",
        "titulo": "Compilación real: Makefiles y CMake básico",
        "descripcion": "Dejá de compilar a mano con g++ cada vez: automatizá el build de un proyecto con varios archivos.",
        "dificultad": "Intermedio",
        "tiempo_estimado": "1-2 horas",
        "conceptos": ["make", "makefile", "cmake", "build systems"],
        "xp": 200,
        "objetivo": "Aprender a automatizar la compilación de un proyecto C++ con varios archivos fuente usando Make y, después, CMake — las herramientas de build que vas a encontrar en cualquier proyecto C++ real.",
        "requisitos": ["Módulo: Templates genéricos"],
        "pasos": [
            {
                "titulo": "Separá tu proyecto en varios archivos",
                "descripcion": "QUÉ: tomá un proyecto que tenías en un solo .cpp (como tu Sistema de gestión de biblioteca) y separalo en headers (.h) e implementaciones (.cpp) por clase. POR QUÉ: proyectos reales de C++ casi nunca son un solo archivo — organizar en múltiples archivos es indispensable para que el código sea mantenible.",
                "pista": "Cada clase suele ir en su propio par: Libro.h (declaración) y Libro.cpp (implementación) — usá include guards (#ifndef LIBRO_H / #define LIBRO_H / #endif) en cada header.",
            },
            {
                "titulo": "Compilá manualmente todos los archivos para entender el problema",
                "descripcion": "QUÉ: compilá tu proyecto multi-archivo con un solo comando largo de g++ que liste todos los .cpp. POR QUÉ: necesitás sentir el dolor de escribir (y recordar) ese comando cada vez, para apreciar por qué existe una herramienta que lo automatice.",
                "pista": "g++ -o programa main.cpp Libro.cpp Biblioteca.cpp -std=c++17 — a medida que agregás archivos, este comando se vuelve inmanejable.",
            },
            {
                "titulo": "Escribí un Makefile básico",
                "descripcion": "QUÉ: creá un Makefile con una regla que compile tu proyecto, y corré make en vez del comando largo de g++. POR QUÉ: Make además solo recompila los archivos que CAMBIARON desde la última vez, ahorrando tiempo en proyectos grandes.",
                "pista": "Un Makefile mínimo:\\nprograma: main.cpp Libro.cpp Biblioteca.cpp\\n\\tg++ -o programa main.cpp Libro.cpp Biblioteca.cpp -std=c++17\\n(la línea de comando DEBE empezar con un TAB, no espacios)",
            },
            {
                "titulo": "Agregá reglas de conveniencia al Makefile",
                "descripcion": "QUÉ: agregá reglas 'clean' (borra los archivos generados) y 'run' (compila y ejecuta) a tu Makefile. POR QUÉ: centralizar las tareas comunes del proyecto en el Makefile significa que cualquiera puede compilar, limpiar o correr sin memorizar comandos.",
                "pista": "clean:\\n\\trm -f programa *.o\\n\\nrun: programa\\n\\t./programa\\n\\nDespués corré con: make, make clean, o make run",
            },
            {
                "titulo": "Migrá a CMake",
                "descripcion": "QUÉ: creá un CMakeLists.txt equivalente a tu Makefile, y generá el build con cmake y make. POR QUÉ: CMake es multiplataforma (Windows/Mac/Linux) y es el estándar de facto en proyectos C++ modernos — Make puro se vuelve difícil de mantener en proyectos grandes o multiplataforma.",
                "pista": "CMakeLists.txt mínimo:\\ncmake_minimum_required(VERSION 3.10)\\nproject(MiBiblioteca)\\nset(CMAKE_CXX_STANDARD 17)\\nadd_executable(programa main.cpp Libro.cpp Biblioteca.cpp)\\n\\nCompilar: mkdir build && cd build && cmake .. && make",
            },
        ],
        "criterios": [
            "El proyecto está separado en múltiples archivos .h/.cpp organizados por clase.",
            "make (o make run) compila el proyecto completo con un solo comando.",
            "make clean elimina los archivos generados por la compilación.",
            "Existe un CMakeLists.txt funcional que genera el mismo ejecutable.",
        ],
        "retos_extra": [
            "Agregá una regla de Makefile que compile con flags de debug (-g) por separado de una de release optimizada (-O2).",
            "Investigá cómo CMake maneja dependencias externas con find_package o FetchContent.",
            "Configurá tu CMakeLists.txt para generar también un archivo compile_commands.json (útil para autocompletado en editores).",
        ],
    },
    {
        "id": 10,
        "disponible_en_ide": "no",
        "titulo": "Consumí una API de IA desde C++ con libcurl",
        "descripcion": "Hacé requests HTTP reales desde C++ y conectate a un modelo de lenguaje, sin salir del lenguaje.",
        "dificultad": "Avanzado",
        "tiempo_estimado": "2-3 horas",
        "conceptos": ["libcurl", "HTTP en C++", "parseo de JSON", "APIs de IA"],
        "xp": 250,
        "objetivo": "Aprender a hacer requests HTTP desde C++ usando libcurl, y usar esa base para conectarte a una API de inteligencia artificial real, parseando su respuesta JSON.",
        "requisitos": ["Módulo: Manejo de excepciones", "Proyecto: Compilación real: Makefiles y CMake básico"],
        "pasos": [
            {
                "titulo": "Instalá libcurl y compilá un ejemplo mínimo",
                "descripcion": "QUÉ: instalá la librería libcurl para tu sistema, y compilá un programa mínimo que haga un GET a una URL de prueba. POR QUÉ: C++ no trae un cliente HTTP en su librería estándar — libcurl es la opción más usada para esto, y hay que enlazarla explícitamente al compilar.",
                "pista": "En Windows con MSYS2: pacman -S mingw-w64-x86_64-curl — compilar enlazando la librería: g++ -o programa main.cpp -lcurl",
            },
            {
                "titulo": "Hacé tu primer request GET",
                "descripcion": "QUÉ: usá la API de libcurl (curl_easy_init, curl_easy_setopt, curl_easy_perform) para traer el contenido de una URL simple y mostrarlo en pantalla. POR QUÉ: entender el flujo básico de libcurl (init → configurar opciones → ejecutar → limpiar) es la base para cualquier request más complejo.",
                "pista": "Necesitás una función callback para recibir los datos de a pedazos: curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, funcionCallback); — buscá el ejemplo 'simple.c' de la documentación oficial de libcurl como referencia.",
            },
            {
                "titulo": "Armá un request POST con headers y body JSON",
                "descripcion": "QUÉ: configurá un request POST con el header Content-Type: application/json y un body JSON armado a mano (o con una librería como nlohmann/json). POR QUÉ: las APIs de IA esperan requests POST con el prompt dentro de un body JSON estructurado según su documentación.",
                "pista": "curl_slist* headers = curl_slist_append(nullptr, \"Content-Type: application/json\"); curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers); curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonBody.c_str());",
            },
            {
                "titulo": "Parseá la respuesta JSON",
                "descripcion": "QUÉ: instalá una librería de JSON para C++ (nlohmann/json es la más popular y fácil de usar) y parseá la respuesta de la API para extraer el texto generado. POR QUÉ: a diferencia de Python o JS, C++ no tiene parseo de JSON nativo — sin una librería, tendrías que parsear el string a mano, un desperdicio de tiempo y fuente de bugs.",
                "pista": "#include <nlohmann/json.hpp> — auto j = nlohmann::json::parse(respuestaString); std::string texto = j[\"campo\"][\"anidado\"];",
            },
            {
                "titulo": "Manejá errores de red y de la API",
                "descripcion": "QUÉ: verificá el código de retorno de curl_easy_perform() y el código de status HTTP de la respuesta, mostrando un mensaje claro si algo falla. POR QUÉ: un request de red puede fallar por mil razones (sin internet, key inválida, timeout) — tu programa no debería crashear ni mostrar un mensaje críptico.",
                "pista": "CURLcode res = curl_easy_perform(curl); if (res != CURLE_OK) { std::cerr << \"Error: \" << curl_easy_strerror(res) << std::endl; }",
            },
        ],
        "criterios": [
            "El programa compila enlazando libcurl correctamente (-lcurl).",
            "Hace un request POST real a una API de IA con headers y body JSON armados desde C++.",
            "Parsea la respuesta JSON con una librería (no con manipulación manual de strings) y extrae el texto generado.",
            "Maneja al menos un caso de error de red y uno de error de la API sin crashear.",
        ],
        "retos_extra": [
            "Envolvé la lógica de request en una clase ClienteIA reutilizable, con manejo de errores mediante excepciones.",
            "Agregá un CMakeLists.txt que enlace automáticamente libcurl y nlohmann/json usando find_package.",
            "Medí con chrono cuánto tarda el request completo, y agregá un timeout configurable con CURLOPT_TIMEOUT.",
        ],
    },
]


PROYECTOS_POR_LENGUAJE = {
    "python": PROYECTOS_PYTHON,
    "javascript": PROYECTOS_JAVASCRIPT,
    "cpp": PROYECTOS_CPP,
}


@router.get("/proyectos/{lenguaje}")
def get_proyectos(lenguaje: str):
    lenguaje = lenguaje.lower()
    if lenguaje not in PROYECTOS_POR_LENGUAJE:
        raise HTTPException(status_code=404, detail="Lenguaje inválido")
    return PROYECTOS_POR_LENGUAJE[lenguaje]


class PasoRequest(BaseModel):
    lenguaje: str
    proyecto_id: int
    paso_index: int
    completado: bool = True


@router.post("/proyectos/paso")
def marcar_paso(req: PasoRequest):
    lenguaje = req.lenguaje.lower()
    if lenguaje not in PROYECTOS_POR_LENGUAJE:
        raise HTTPException(status_code=400, detail="Lenguaje inválido")

    progreso = _cargar_progreso()
    clave = f"{lenguaje}_{req.proyecto_id}"
    pasos_completados = progreso.setdefault("proyectos_pasos", {})
    completados = set(pasos_completados.get(clave, []))

    if req.completado:
        completados.add(req.paso_index)
    else:
        completados.discard(req.paso_index)

    pasos_completados[clave] = sorted(completados)
    _guardar_progreso(progreso)

    return {"pasos_completados": pasos_completados[clave]}


class CompletarProyectoRequest(BaseModel):
    lenguaje: str
    proyecto_id: int


@router.post("/proyectos/completar")
def completar_proyecto(req: CompletarProyectoRequest):
    lenguaje = req.lenguaje.lower()
    if lenguaje not in PROYECTOS_POR_LENGUAJE:
        raise HTTPException(status_code=400, detail="Lenguaje inválido")

    proyecto = next((p for p in PROYECTOS_POR_LENGUAJE[lenguaje] if p["id"] == req.proyecto_id), None)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    progreso = _cargar_progreso()
    proyectos_lang = progreso.setdefault("proyectos", {}).setdefault(lenguaje, [])

    if req.proyecto_id in proyectos_lang:
        return {
            "message": "Ya completado anteriormente",
            "ya_estaba": True,
            "xp_ganado": 0,
            "xp_bonus_racha": 0,
            "xp_total_ganado": 0,
            "xp_total": progreso["xp"],
            "nivel_info": _calcular_nivel(progreso["xp"]),
            "completados": proyectos_lang,
            "racha": progreso.get("racha", 0),
            "mejor_racha": progreso.get("mejor_racha", 0),
            "es_nueva_racha": False,
        }

    racha, mejor_racha, today, es_nueva_racha = _calcular_racha(progreso)
    xp_ganado = proyecto["xp"]
    xp_bonus = _bonus_racha(racha, xp_ganado)
    xp_total_ganado = xp_ganado + xp_bonus

    proyectos_lang.append(req.proyecto_id)
    progreso["xp"] = progreso.get("xp", 0) + xp_total_ganado
    progreso["racha"] = racha
    progreso["mejor_racha"] = mejor_racha
    progreso["ultima_actividad"] = today

    nivel_info = _calcular_nivel(progreso["xp"])
    progreso["nivel"] = nivel_info["nivel"]

    _guardar_progreso(progreso)

    return {
        "message": "¡Proyecto completado!",
        "ya_estaba": False,
        "xp_ganado": xp_ganado,
        "xp_bonus_racha": xp_bonus,
        "xp_total_ganado": xp_total_ganado,
        "xp_total": progreso["xp"],
        "nivel_info": nivel_info,
        "completados": proyectos_lang,
        "racha": racha,
        "mejor_racha": mejor_racha,
        "es_nueva_racha": es_nueva_racha,
    }
