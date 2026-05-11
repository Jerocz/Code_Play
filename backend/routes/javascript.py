from fastapi import APIRouter

router = APIRouter(prefix="/javascript", tags=["JavaScript"])

modulos = [
    {
        "id": 1, "bloque": "Fundamentos", "titulo": "Hola Mundo",
        "descripcion": "Tu primer programa — console.log()",
        "xp": 20,
        "teoria": "console.log() muestra texto en la consola del navegador. Abrís las DevTools con F12 → Console para verlo. Es el print() de JavaScript.",
        "ejemplo": 'console.log("Hola mundo");\nconsole.log("Esto es JavaScript");\nconsole.log(42);\nconsole.log(3.14);',
        "ejercicio": "Abrí la consola del navegador (F12 → Console) y escribí 3 console.log(): tu nombre, tu edad y tu ciudad favorita.",
        "pista": "Cada console.log() va en su propia línea. El texto va entre comillas, los números no."
    },
    {
        "id": 2, "bloque": "Fundamentos", "titulo": "Variables",
        "descripcion": "let, const y var — guardar datos",
        "xp": 30,
        "teoria": "JavaScript tiene 3 formas de declarar variables. const es para valores que no cambian. let es para valores que pueden cambiar. var es la forma vieja (evitarla). Siempre preferí const, usá let cuando necesitás reasignar.",
        "ejemplo": 'const nombre = "Ana";     // no cambia\nlet edad = 25;            // puede cambiar\nlet contador = 0;\ncontador = contador + 1;  // reasignar\n\nconsole.log(nombre);\nconsole.log(`Tengo ${edad} años`); // template literal',
        "ejercicio": "Creá variables con const para tu nombre y ciudad (no van a cambiar). Usá let para tu edad. Mostrá todo con console.log usando template literals.",
        "pista": "Los template literals van entre backticks ` ` y las variables van dentro de ${}."
    },
    {
        "id": 3, "bloque": "Fundamentos", "titulo": "Tipos de datos",
        "descripcion": "number, string, boolean, null, undefined",
        "xp": 30,
        "teoria": "JavaScript tiene tipos dinámicos: number (todos los números, enteros y decimales), string (texto), boolean (true/false), null (vacío intencional), undefined (sin valor asignado). typeof te dice el tipo.",
        "ejemplo": 'const edad = 25;           // number\nconst precio = 19.99;      // number\nconst nombre = "Ana";      // string\nconst activo = true;       // boolean\nconst vacio = null;        // null\nlet sinValor;              // undefined\n\nconsole.log(typeof edad);    // "number"\nconsole.log(typeof nombre);  // "string"',
        "ejercicio": "Creá una variable de cada tipo. Mostrá el valor y el tipo con typeof para cada una.",
        "pista": "typeof devuelve un string con el nombre del tipo. Usá console.log(typeof variable)."
    },
    {
        "id": 4, "bloque": "Fundamentos", "titulo": "Operadores",
        "descripcion": "Matemáticos, comparación y lógicos",
        "xp": 30,
        "teoria": "Operadores matemáticos: + - * / % **. Comparación: == (igual valor), === (igual valor Y tipo — siempre usá este), !=, !==, <, >. Lógicos: && (and), || (or), ! (not).",
        "ejemplo": 'console.log(10 + 3);    // 13\nconsole.log(10 % 3);    // 1\nconsole.log(2 ** 8);    // 256\n\nconsole.log(5 === 5);   // true\nconsole.log(5 === "5"); // false (distinto tipo)\nconsole.log(5 == "5");  // true (evitar)\n\nconst mayor = 20 > 18 && true;\nconsole.log(mayor);     // true',
        "ejercicio": "Calculá el precio final de un producto con 21% de IVA. Verificá si el total supera $1000 con ===. Mostrá si es una compra grande (true/false).",
        "pista": "const total = precio * 1.21. Después: const esGrande = total > 1000."
    },
    {
        "id": 5, "bloque": "Decisiones", "titulo": "if / else",
        "descripcion": "Tomá decisiones con condiciones",
        "xp": 50,
        "teoria": "if ejecuta código si la condición es true. else if prueba otra condición. else es el caso por defecto. El operador ternario condition ? valorSiTrue : valorSiFalse es la forma corta.",
        "ejemplo": 'const nota = 75;\n\nif (nota >= 90) {\n    console.log("Sobresaliente");\n} else if (nota >= 60) {\n    console.log("Aprobado");\n} else {\n    console.log("Desaprobado");\n}\n\n// Ternario\nconst estado = nota >= 60 ? "Aprobado" : "Desaprobado";\nconsole.log(estado);',
        "ejercicio": "Escribí una función clasificarEdad(edad) que retorne: 'niño' (<13), 'adolescente' (13-17), 'adulto' (18-64), 'adulto mayor' (65+).",
        "pista": "Usá if/else if/else con las condiciones de rango. Recordá que el orden importa."
    },
    {
        "id": 6, "bloque": "Loops", "titulo": "Loops for y while",
        "descripcion": "Repetir acciones con for, while y forEach",
        "xp": 60,
        "teoria": "for clásico: for(let i=0; i<n; i++). for...of recorre arrays. forEach es un método de arrays. while repite mientras sea true. En JS moderno se prefiere forEach y for...of sobre el for clásico.",
        "ejemplo": 'const frutas = ["manzana", "banana", "naranja"];\n\n// for clásico\nfor (let i = 0; i < frutas.length; i++) {\n    console.log(frutas[i]);\n}\n\n// for...of (más limpio)\nfor (const fruta of frutas) {\n    console.log(fruta);\n}\n\n// forEach\nfrutas.forEach((fruta, i) => {\n    console.log(`${i+1}. ${fruta}`);\n});',
        "ejercicio": "Creá un array con los números del 1 al 10. Usando forEach mostrá cada número y si es par o impar.",
        "pista": "Usá Array.from({length:10}, (_,i) => i+1) para crear el array. En forEach: n % 2 === 0 ? 'par' : 'impar'."
    },
    {
        "id": 7, "bloque": "Funciones", "titulo": "Funciones y Arrow functions",
        "descripcion": "function, arrow functions y callbacks",
        "xp": 70,
        "teoria": "Hay dos formas principales: function nombre() {} y arrow functions: const nombre = () => {}. Las arrow functions son más cortas y son las preferidas en JS moderno. Si solo retornan una expresión, podés omitir las llaves y el return.",
        "ejemplo": '// Función clásica\nfunction saludar(nombre) {\n    return `Hola, ${nombre}!`;\n}\n\n// Arrow function\nconst saludar2 = (nombre) => `Hola, ${nombre}!`;\n\n// Con lógica\nconst calcularIVA = (precio, tasa = 0.21) => {\n    const iva = precio * tasa;\n    return { precio, iva, total: precio + iva };\n};\n\nconsole.log(calcularIVA(1000));',
        "ejercicio": "Creá estas arrow functions: esPrimo(n), celsiusAFahrenheit(c) y validarEmail(email). Probá cada una con distintos valores.",
        "pista": "Para esPrimo: iterá del 2 a Math.sqrt(n). Para email: email.includes('@') && email.includes('.')."
    },
    {
        "id": 8, "bloque": "Arrays", "titulo": "Arrays y métodos modernos",
        "descripcion": "map, filter, reduce, find — el poder de los arrays",
        "xp": 80,
        "teoria": "Los arrays en JS tienen métodos poderosos: map() transforma cada elemento, filter() filtra según condición, reduce() acumula en un valor, find() busca el primero que cumple, some() verifica si alguno cumple, every() verifica si todos cumplen.",
        "ejemplo": 'const numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];\n\nconst dobles = numeros.map(n => n * 2);\nconst pares = numeros.filter(n => n % 2 === 0);\nconst suma = numeros.reduce((acc, n) => acc + n, 0);\nconst primerMayor5 = numeros.find(n => n > 5);\n\nconsole.log(dobles);       // [2,4,6,8...]\nconsole.log(pares);        // [2,4,6,8,10]\nconsole.log(suma);         // 55\nconsole.log(primerMayor5); // 6',
        "ejercicio": "Tenés este array de productos: [{nombre:'Laptop',precio:1200},{nombre:'Mouse',precio:25},{nombre:'Monitor',precio:350}]. Usá filter para los que cuestan más de $100, map para mostrar solo los nombres, y reduce para el total.",
        "pista": "productos.filter(p => p.precio > 100). Después .map(p => p.nombre). Para reduce: (acc, p) => acc + p.precio, 0."
    },
    {
        "id": 9, "bloque": "Async", "titulo": "Promesas y async/await",
        "descripcion": "Código asíncrono — fetch y APIs",
        "xp": 100,
        "teoria": "JavaScript es asíncrono — puede hacer cosas mientras espera. fetch() hace requests HTTP. Retorna una Promise. async/await hace que el código asíncrono se lea como sincrónico. Siempre manejá errores con try/catch.",
        "ejemplo": 'async function obtenerUsuario(id) {\n    try {\n        const response = await fetch(\n            `https://jsonplaceholder.typicode.com/users/${id}`\n        );\n        \n        if (!response.ok) {\n            throw new Error(`Error: ${response.status}`);\n        }\n        \n        const usuario = await response.json();\n        console.log(usuario.name);\n        return usuario;\n    } catch (error) {\n        console.error("Falló:", error.message);\n    }\n}\n\nobtenerUsuario(1);',
        "ejercicio": "Usá fetch para traer datos de https://jsonplaceholder.typicode.com/posts. Mostrá los títulos de los primeros 5 posts. Manejá el error si la request falla.",
        "pista": "const posts = await response.json(). Después posts.slice(0,5).forEach(p => console.log(p.title))."
    },
    {
        "id": 10, "bloque": "Casos reales", "titulo": "Caso real: DOM y eventos",
        "descripcion": "Manipulá la página web — getElementById, addEventListener",
        "xp": 120,
        "teoria": "El DOM (Document Object Model) es la representación de la página en JavaScript. getElementById() busca un elemento. innerHTML cambia el contenido. addEventListener() escucha eventos como clicks.",
        "ejemplo": '// HTML necesario:\n// <button id="btn">Click</button>\n// <div id="resultado"></div>\n\nconst btn = document.getElementById("btn");\nconst resultado = document.getElementById("resultado");\nlet contador = 0;\n\nbtn.addEventListener("click", () => {\n    contador++;\n    resultado.innerHTML = `Clickeaste ${contador} veces`;\n    \n    if (contador >= 10) {\n        resultado.style.color = "red";\n    }\n});',
        "ejercicio": "Creá una página HTML con un input de texto, un botón y un div. Al hacer click, tomá el texto del input y agregalo a una lista visible en el div. Agregá un botón para limpiar la lista.",
        "pista": "document.getElementById('input').value para leer el input. Para agregar a la lista: div.innerHTML += '<p>' + texto + '</p>'."
    },
]

@router.get("/modulos")
def obtener_modulos():
    return modulos

@router.get("/modulos/{modulo_id}")
def obtener_modulo(modulo_id: int):
    modulo = next((m for m in modulos if m["id"] == modulo_id), None)
    if not modulo:
        return {"error": "Módulo no encontrado"}
    return modulo
