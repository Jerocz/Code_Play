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
]


# ═══════════════════════════════════ JAVASCRIPT ═══════════════════════════════════
PROYECTOS_JAVASCRIPT = [
    {
        "id": 1,
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
]


# ═══════════════════════════════════ C++ ═══════════════════════════════════
PROYECTOS_CPP = [
    {
        "id": 1,
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
