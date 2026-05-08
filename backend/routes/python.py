from fastapi import APIRouter

router = APIRouter(prefix="/python", tags=["Python"])

modulos = [

    # ══════════════════════════════════════════
    # BLOQUE 1 — FUNDAMENTOS ABSOLUTOS
    # ══════════════════════════════════════════
    {
        "id": 1, "bloque": "Fundamentos", "titulo": "Hola Mundo",
        "descripcion": "Tu primer programa — mostrá texto en pantalla con print()",
        "xp": 20,
        "teoria": "print() es la función más básica de Python. Muestra cualquier cosa en la pantalla. Es como decirle a Python: 'mostrá esto'.",
        "ejemplo": "print('Hola mundo')\nprint('Esto es Python')\nprint(42)\nprint(3.14)",
        "ejercicio": "Escribí un programa que imprima en 3 líneas separadas: tu nombre, tu edad y tu ciudad favorita.",
        "pista": "Necesitás 3 líneas, cada una con print(). El texto va entre comillas, los números no."
    },
    {
        "id": 2, "bloque": "Fundamentos", "titulo": "Comentarios",
        "descripcion": "Líneas que Python ignora — para explicar tu código",
        "xp": 20,
        "teoria": "Un comentario empieza con #. Python lo ignora completamente. Sirven para explicar qué hace tu código. Cuando volvés a leer código de hace semanas, los comentarios te salvan.",
        "ejemplo": "# Este es un comentario\nprint('Hola')  # También puede ir al final\n# print('Esto NO se ejecuta')\nprint('Esto sí se ejecuta')",
        "ejercicio": "Tomá el programa del módulo anterior y agregá un comentario arriba de cada print() explicando qué hace.",
        "pista": "Poné # antes del texto del comentario. Ejemplo: # Imprimo mi nombre"
    },
    {
        "id": 3, "bloque": "Fundamentos", "titulo": "Variables",
        "descripcion": "Guardá datos con nombres para usarlos después",
        "xp": 30,
        "teoria": "Una variable es como una caja con nombre. Guardás algo adentro y lo podés usar después. El = no significa 'igual' matemático, significa 'guardá esto acá'.",
        "ejemplo": "nombre = 'Ana'\nedad = 25\naltura = 1.65\nactivo = True\n\nprint(nombre)\nprint(edad)\nprint(f'Me llamo {nombre} y tengo {edad} años')",
        "ejercicio": "Creá variables para tu nombre, edad y ciudad. Usá las 3 en un print() que diga: 'Me llamo [nombre], tengo [edad] años y vivo en [ciudad].'",
        "pista": "Creá 3 variables primero. Después usá f-strings: print(f'Me llamo {nombre}...')"
    },
    {
        "id": 4, "bloque": "Fundamentos", "titulo": "Tipos de datos",
        "descripcion": "int, float, str, bool — los 4 tipos básicos",
        "xp": 30,
        "teoria": "Python tiene tipos distintos para distintos datos. int son números enteros (5, -3, 100). float son decimales (3.14, -0.5). str es texto ('hola'). bool es True o False. type() te dice qué tipo es algo.",
        "ejemplo": "edad = 25          # int\nprecio = 19.99     # float\nnombre = 'Ana'     # str\nactivo = True      # bool\n\nprint(type(edad))    # <class 'int'>\nprint(type(precio))  # <class 'float'>\nprint(type(nombre))  # <class 'str'>\nprint(type(activo))  # <class 'bool'>",
        "ejercicio": "Creá una variable de cada tipo. Imprimí el valor y el tipo de cada una usando type(). Luego intentá sumar el int con el float y mostrá el resultado.",
        "pista": "Para cada variable hacé print(valor) y print(type(valor)). Para la suma: resultado = entero + decimal"
    },
    {
        "id": 5, "bloque": "Fundamentos", "titulo": "Operadores matemáticos",
        "descripcion": "Suma, resta, multiplicación, división y más",
        "xp": 30,
        "teoria": "Python puede hacer matemáticas: + suma, - resta, * multiplica, / divide (siempre da decimal), // divide sin decimales, % da el resto de la división, ** es potencia.",
        "ejemplo": "a, b = 10, 3\nprint(a + b)   # 13\nprint(a - b)   # 7\nprint(a * b)   # 30\nprint(a / b)   # 3.333...\nprint(a // b)  # 3\nprint(a % b)   # 1 (resto)\nprint(a ** b)  # 1000 (10³)",
        "ejercicio": "Una remera cuesta $1500 y tiene 30% de descuento. Calculá el precio final usando variables y operadores. Mostrá el precio original, el descuento en pesos y el precio final.",
        "pista": "descuento = precio * 0.30 y precio_final = precio - descuento. Usá f-strings para mostrar los resultados."
    },
    {
        "id": 6, "bloque": "Fundamentos", "titulo": "Input del usuario",
        "descripcion": "Pedile datos al usuario con input()",
        "xp": 40,
        "teoria": "input() pausa el programa y espera que el usuario escriba algo. SIEMPRE retorna texto (str), aunque el usuario escriba un número. Si necesitás operar con él, convertilo: int(input()) o float(input()).",
        "ejemplo": "nombre = input('¿Cómo te llamás? ')\nprint(f'Hola, {nombre}!')\n\nedad = int(input('¿Cuántos años tenés? '))\nprint(f'El año que viene tenés {edad + 1} años')",
        "ejercicio": "Pedí al usuario su nombre y año de nacimiento. Calculá su edad (2024 - año_nacimiento) y mostrá: 'Hola [nombre], tenés [edad] años.'",
        "pista": "El año de nacimiento hay que convertirlo a int. La edad se calcula restando al año actual."
    },

    # ══════════════════════════════════════════
    # BLOQUE 2 — STRINGS Y TEXTO
    # ══════════════════════════════════════════
    {
        "id": 7, "bloque": "Strings", "titulo": "Strings en profundidad",
        "descripcion": "Texto, métodos, slicing y f-strings",
        "xp": 50,
        "teoria": "Los strings tienen métodos útiles: .upper() mayúsculas, .lower() minúsculas, .strip() quita espacios, .replace() reemplaza, .split() divide en lista, len() cuenta caracteres. Con [0] accedés al primer caracter.",
        "ejemplo": "s = '  Hola Mundo  '\nprint(s.strip())        # 'Hola Mundo'\nprint(s.upper())        # '  HOLA MUNDO  '\nprint(s.replace('Hola', 'Chau'))\nprint(len(s))           # 14\nprint(s[2])             # 'H'\nprint(s[-1])            # ' '\n\npalabras = 'Python es genial'\nprint(palabras.split()) # ['Python', 'es', 'genial']",
        "ejercicio": "Pedí el nombre completo del usuario. Mostrá: en mayúsculas, en minúsculas, cuántas letras tiene (sin espacios), y la primera y última letra.",
        "pista": "Para quitar espacios del conteo: nombre.replace(' ', ''). Para primera letra: nombre[0]. Para última: nombre[-1]."
    },
    {
        "id": 8, "bloque": "Strings", "titulo": "f-strings avanzados",
        "descripcion": "Formatear números, alinear texto y expresiones",
        "xp": 40,
        "teoria": "Los f-strings permiten formatear valores dentro de {}. :.2f muestra 2 decimales. :, agrega separador de miles. :.1% convierte a porcentaje. Podés poner expresiones directamente: {precio * 0.9}.",
        "ejemplo": "precio = 1234567.89\npct = 0.1567\n\nprint(f'Precio: ${precio:,.2f}')   # $1,234,567.89\nprint(f'Porcentaje: {pct:.1%}')     # 15.7%\nprint(f'Redondeado: {precio:.0f}') # 1234568\n\nnombre = 'Ana'\nprint(f'{'izquierda':<20}|')\nprint(f'{'derecha':>20}|')",
        "ejercicio": "Mostrá una factura simple: precio unitario $1500, cantidad 3 unidades, 21% de IVA. Mostrá subtotal, IVA en pesos y total, todo con formato de precio (2 decimales y separador de miles).",
        "pista": "subtotal = precio * cantidad. iva = subtotal * 0.21. total = subtotal + iva. Usá :,.2f para el formato."
    },

    # ══════════════════════════════════════════
    # BLOQUE 3 — DECISIONES
    # ══════════════════════════════════════════
    {
        "id": 9, "bloque": "Decisiones", "titulo": "if / elif / else",
        "descripcion": "Tomá decisiones según condiciones",
        "xp": 60,
        "teoria": "if ejecuta código solo si la condición es True. elif (else if) prueba otra condición si la anterior falló. else ejecuta si ninguna condición fue True. Solo se ejecuta UNO de los bloques.",
        "ejemplo": "nota = 75\n\nif nota >= 90:\n    print('Sobresaliente')\nelif nota >= 80:\n    print('Muy bueno')\nelif nota >= 60:\n    print('Aprobado')\nelse:\n    print('Desaprobado')",
        "ejercicio": "Pedí la temperatura actual. Según el valor decí qué ropa usar: menos de 10° → 'Campera gruesa', 10-20° → 'Rompevientos', 20-30° → 'Remera', más de 30° → 'Lo menos posible'.",
        "pista": "Pedí la temperatura con float(input()). Usá if/elif/else comparando con los rangos. El orden importa."
    },
    {
        "id": 10, "bloque": "Decisiones", "titulo": "Operadores lógicos",
        "descripcion": "and, or, not — combinar condiciones",
        "xp": 50,
        "teoria": "and: las DOS condiciones deben ser True. or: AL MENOS UNA debe ser True. not: invierte True/False. Podés encadenar comparaciones: 18 <= edad <= 65 es válido en Python.",
        "ejemplo": "edad = 25\ntiene_dni = True\n\nif edad >= 18 and tiene_dni:\n    print('Puede votar')\n\nif edad < 18 or edad > 65:\n    print('Tarifa especial')\n\nif not tiene_dni:\n    print('Falta el DNI')\n\n# Rango elegante\nif 20 <= edad <= 30:\n    print('Joven adulto')",
        "ejercicio": "Sistema de descuentos: precio base $5000. Si es socio: 10% off. Si el día es lunes o martes: 15% off adicional. Si la compra supera $3000: 5% off adicional. Mostrá el precio final.",
        "pista": "Pedí is_socio (True/False) y dia con input. Calculá cada descuento por separado y sumalos. precio_final = precio * (1 - descuento_total)."
    },

    # ══════════════════════════════════════════
    # BLOQUE 4 — LOOPS
    # ══════════════════════════════════════════
    {
        "id": 11, "bloque": "Loops", "titulo": "Loop for",
        "descripcion": "Repetí acciones recorriendo secuencias",
        "xp": 60,
        "teoria": "for recorre cada elemento de una secuencia. range(n) genera números del 0 al n-1. range(a,b) del a al b-1. enumerate() da índice y valor. zip() recorre dos listas a la vez.",
        "ejemplo": "# Recorrer lista\nfrutas = ['manzana', 'banana', 'naranja']\nfor fruta in frutas:\n    print(fruta)\n\n# range\nfor i in range(1, 6):\n    print(i)  # 1 2 3 4 5\n\n# enumerate\nfor i, fruta in enumerate(frutas, 1):\n    print(f'{i}. {fruta}')",
        "ejercicio": "Tabla de multiplicar del número que elija el usuario. Mostrá: '3 x 1 = 3', '3 x 2 = 6', etc. hasta el 10.",
        "pista": "Pedí el número con input(). Usá for i in range(1, 11). Dentro: print(f'{num} x {i} = {num*i}')"
    },
    {
        "id": 12, "bloque": "Loops", "titulo": "Loop while",
        "descripcion": "Repetí mientras se cumpla una condición",
        "xp": 60,
        "teoria": "while repite mientras la condición sea True. Si la condición nunca cambia, loop infinito. break sale del loop. continue salta al siguiente ciclo. Patrón común: while True con break para menús.",
        "ejemplo": "# Contar\ncontador = 1\nwhile contador <= 5:\n    print(contador)\n    contador += 1\n\n# Menú con while True\nwhile True:\n    opcion = input('1-Ver, 2-Salir: ')\n    if opcion == '2':\n        break\n    print('Mostrando...')",
        "ejercicio": "Adivinar el número: el programa elige un número del 1 al 100 (usá random.randint). El usuario tiene 7 intentos. Después de cada intento decí 'muy alto', 'muy bajo' o '¡correcto!'.",
        "pista": "import random al inicio. numero = random.randint(1, 100). Usá while intentos < 7. Pedí el intento con int(input())."
    },
    {
        "id": 13, "bloque": "Loops", "titulo": "List comprehensions",
        "descripcion": "Crear listas en una línea — forma pythónica",
        "xp": 50,
        "teoria": "[expresión for elemento in secuencia if condición]. Es más corto y más rápido que un for con append. No abuses — si es muy complejo, mejor un for normal.",
        "ejemplo": "# Forma larga\ncuadrados = []\nfor x in range(1, 6):\n    cuadrados.append(x**2)\n\n# Con comprehension\ncuadrados = [x**2 for x in range(1, 6)]\n# [1, 4, 9, 16, 25]\n\n# Con condición\npares = [x for x in range(20) if x % 2 == 0]\n\n# Transformar strings\nnombres = ['ana', 'luis', 'SARA']\nlimpios = [n.strip().title() for n in nombres]",
        "ejercicio": "Tenés esta lista de notas: [45, 78, 92, 55, 88, 33, 71, 95, 60, 48]. Usando comprehensions creá: lista de aprobados (>=60), lista de los cuadrados de los aprobados, y un diccionario {nota: 'aprobado'/'desaprobado'}.",
        "pista": "aprobados = [n for n in notas if n >= 60]. Para el diccionario: {n: 'aprobado' if n>=60 else 'desaprobado' for n in notas}."
    },

    # ══════════════════════════════════════════
    # BLOQUE 5 — ESTRUCTURAS DE DATOS
    # ══════════════════════════════════════════
    {
        "id": 14, "bloque": "Estructuras de datos", "titulo": "Listas",
        "descripcion": "Colecciones ordenadas — la estructura más usada",
        "xp": 70,
        "teoria": "Las listas guardan elementos en orden. Se modifican (son mutables). append() agrega al final, pop() saca el último, insert() agrega en posición, remove() elimina por valor, sort() ordena. len() da la longitud.",
        "ejemplo": "frutas = ['manzana', 'banana', 'naranja']\nfrutas.append('uva')\nfrutas.insert(1, 'kiwi')\nprint(frutas[0])   # manzana\nprint(frutas[-1])  # uva\nfrutas.sort()\nfrutas.remove('banana')\nsacado = frutas.pop()  # saca el último",
        "ejercicio": "Sistema de lista de compras: el usuario puede agregar ítems, ver la lista numerada, eliminar por número y ver cuántos ítems hay. Usá un menú con while.",
        "pista": "Usá una lista vacía. Para eliminar por número: lista.pop(numero - 1). Mostrá la lista con enumerate()."
    },
    {
        "id": 15, "bloque": "Estructuras de datos", "titulo": "Diccionarios",
        "descripcion": "Pares clave-valor — como un objeto del mundo real",
        "xp": 70,
        "teoria": "Los diccionarios guardan datos con nombre. persona['nombre'] accede al valor. .get() no da error si la clave no existe. .items() permite iterar clave y valor juntos. Son perfectos para representar objetos.",
        "ejemplo": "persona = {\n    'nombre': 'Ana',\n    'edad': 25,\n    'ciudad': 'Buenos Aires'\n}\n\nprint(persona['nombre'])          # Ana\nprint(persona.get('email', 'N/A'))  # N/A\n\npersona['email'] = 'ana@test.com'\n\nfor clave, valor in persona.items():\n    print(f'{clave}: {valor}')",
        "ejercicio": "Agenda de contactos: diccionario donde la clave es el nombre y el valor es el teléfono. Menú para: agregar contacto, buscar por nombre, ver todos, eliminar.",
        "pista": "agenda = {}. Para agregar: agenda[nombre] = telefono. Para buscar: agenda.get(nombre, 'No encontrado')."
    },

    # ══════════════════════════════════════════
    # BLOQUE 6 — FUNCIONES
    # ══════════════════════════════════════════
    {
        "id": 16, "bloque": "Funciones", "titulo": "Funciones básicas",
        "descripcion": "Organizá código reutilizable con def",
        "xp": 80,
        "teoria": "Una función es un bloque de código con nombre. def la define, return devuelve un valor. Los parámetros son los datos que recibe. Si no tiene return, devuelve None. Los valores por defecto se ponen con =.",
        "ejemplo": "def saludar(nombre, saludo='Hola'):\n    return f'{saludo}, {nombre}!'\n\nprint(saludar('Ana'))          # Hola, Ana!\nprint(saludar('Luis', 'Buenas'))  # Buenas, Luis!\n\ndef calcular_imc(peso, altura):\n    imc = peso / (altura ** 2)\n    return round(imc, 1)\n\nresultado = calcular_imc(70, 1.75)\nprint(f'IMC: {resultado}')",
        "ejercicio": "Creá estas 3 funciones: es_primo(n) que retorna True/False, celsius_a_fahrenheit(c) que convierte temperatura, y validar_email(email) que retorna True si tiene @ y un punto después del @.",
        "pista": "Para es_primo: probá si n es divisible por algún número del 2 al n-1. Para email: '@' in email and '.' in email.split('@')[1]."
    },
    {
        "id": 17, "bloque": "Funciones", "titulo": "Funciones avanzadas",
        "descripcion": "*args, **kwargs, lambda y decoradores",
        "xp": 80,
        "teoria": "*args acepta cantidad variable de argumentos (llegan como tupla). **kwargs acepta argumentos nombrados variables (llegan como dict). lambda crea funciones en una línea. Los decoradores modifican funciones con @.",
        "ejemplo": "def sumar(*numeros):\n    return sum(numeros)\n\nprint(sumar(1, 2, 3, 4, 5))  # 15\n\ndef mostrar(**datos):\n    for k, v in datos.items():\n        print(f'{k}: {v}')\n\nmostrar(nombre='Ana', edad=25)\n\n# Lambda\ndoble = lambda x: x * 2\nnombres = ['Sara', 'Ana', 'Luis']\nordenados = sorted(nombres, key=lambda n: len(n))",
        "ejercicio": "Creá un decorador medir_tiempo que imprima cuánto tardó en ejecutarse cualquier función. Aplicalo a una función que calcule el factorial de 1000.",
        "pista": "import time. El decorador recibe la función, define wrapper() que llama start=time.time(), ejecuta la función, imprime time.time()-start."
    },

    # ══════════════════════════════════════════
    # BLOQUE 7 — ARCHIVOS Y ERRORES
    # ══════════════════════════════════════════
    {
        "id": 18, "bloque": "Archivos y errores", "titulo": "Archivos y JSON",
        "descripcion": "Guardá datos que persisten entre ejecuciones",
        "xp": 80,
        "teoria": "open() abre archivos. Siempre usá with para que se cierren solos. 'r' lee, 'w' escribe (sobreescribe), 'a' agrega al final. json.dump() guarda un dict en JSON. json.load() lo carga de vuelta.",
        "ejemplo": "import json\nimport os\n\n# Guardar\ndatos = {'nombre': 'Ana', 'puntos': 1500}\nwith open('datos.json', 'w') as f:\n    json.dump(datos, f, indent=2)\n\n# Cargar\nif os.path.exists('datos.json'):\n    with open('datos.json', 'r') as f:\n        cargado = json.load(f)\n    print(cargado['nombre'])",
        "ejercicio": "Diario personal: el usuario puede escribir entradas (con fecha automática), ver todas las entradas y borrar la última. Todo se guarda en un archivo JSON y persiste entre ejecuciones.",
        "pista": "Usá datetime.now().strftime('%Y-%m-%d') para la fecha. Guardá una lista de {'fecha': ..., 'texto': ...}. Cargá al inicio con json.load si el archivo existe."
    },
    {
        "id": 19, "bloque": "Archivos y errores", "titulo": "Manejo de errores",
        "descripcion": "try, except, finally — código que no se rompe",
        "xp": 70,
        "teoria": "try ejecuta código que puede fallar. except captura el error. finally siempre se ejecuta. Podés crear excepciones propias con class MiError(Exception). Mejor capturar errores específicos que Exception genérico.",
        "ejemplo": "def dividir(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return 'Error: no se puede dividir por cero'\n    except TypeError:\n        return 'Error: los valores deben ser números'\n\nclass EdadInvalidaError(Exception):\n    pass\n\ndef validar_edad(edad):\n    if not 0 <= edad <= 150:\n        raise EdadInvalidaError(f'Edad inválida: {edad}')",
        "ejercicio": "Calculadora que nunca se rompe: pedí dos números y una operación (+,-,*,/). Manejá: división por cero, texto en lugar de número, operación inválida. Repetí hasta que el usuario escriba 'salir'.",
        "pista": "Usá try/except ValueError para capturar cuando el usuario escribe texto en vez de número. ZeroDivisionError para la división."
    },

    # ══════════════════════════════════════════
    # BLOQUE 8 — OOP
    # ══════════════════════════════════════════
    {
        "id": 20, "bloque": "OOP", "titulo": "Clases y objetos",
        "descripcion": "Agrupá datos y comportamiento en una clase",
        "xp": 100,
        "teoria": "Una clase es una plantilla. Un objeto es una instancia de esa plantilla. __init__ es el constructor. self se refiere al objeto actual. Los métodos son funciones que pertenecen a la clase. __str__ define cómo se muestra el objeto.",
        "ejemplo": "class CuentaBancaria:\n    def __init__(self, titular, saldo=0):\n        self.titular = titular\n        self._saldo = saldo\n\n    def depositar(self, monto):\n        if monto > 0:\n            self._saldo += monto\n            print(f'+${monto} depositado')\n\n    def ver_saldo(self):\n        return self._saldo\n\n    def __str__(self):\n        return f'Cuenta de {self.titular}: ${self._saldo}'\n\ncuenta = CuentaBancaria('Ana', 1000)\ncuenta.depositar(500)\nprint(cuenta)",
        "ejercicio": "Clase Producto para un e-commerce: tiene nombre, precio y stock. Métodos: vender(cantidad) que reduce el stock, aplicar_descuento(porcentaje), y esta_disponible() que retorna True si hay stock.",
        "pista": "En vender(), verificá que haya suficiente stock antes de reducirlo. Si no hay: raise ValueError('Stock insuficiente')."
    },
    {
        "id": 21, "bloque": "OOP", "titulo": "Herencia y polimorfismo",
        "descripcion": "Reutilizá y extendé clases existentes",
        "xp": 100,
        "teoria": "La herencia permite que una clase hijo tenga todo lo de la clase padre más sus propias cosas. super().__init__() llama al constructor del padre. El polimorfismo permite que distintos objetos respondan distinto al mismo método.",
        "ejemplo": "class Animal:\n    def __init__(self, nombre):\n        self.nombre = nombre\n\n    def sonido(self):\n        raise NotImplementedError\n\nclass Perro(Animal):\n    def sonido(self):\n        return 'Guau!'\n\nclass Gato(Animal):\n    def sonido(self):\n        return 'Miau!'\n\nanimales = [Perro('Rex'), Gato('Mimi')]\nfor a in animales:\n    print(f'{a.nombre}: {a.sonido()}')",
        "ejercicio": "Sistema de empleados: clase base Empleado con nombre y salario_base. Subclases EmpleadoFull (con bono anual del 20%) y Contratista (tarifa por hora). Ambas tienen calcular_salario_mensual() pero calculan diferente.",
        "pista": "EmpleadoFull: salario_mensual = salario_base + (salario_base * 0.20 / 12). Contratista: salario_mensual = tarifa_hora * horas_mes."
    },

    # ══════════════════════════════════════════
    # BLOQUE 9 — CASOS REALES
    # ══════════════════════════════════════════
    {
        "id": 22, "bloque": "Casos reales", "titulo": "Caso real: Gestor de tareas",
        "descripcion": "App completa con persistencia — como un Todoist básico",
        "xp": 150,
        "teoria": "Este proyecto combina todo: listas, diccionarios, funciones, archivos JSON y manejo de errores. Es el tipo de proyecto que ponés en tu portfolio.",
        "ejemplo": "# Estructura de una tarea\ntarea = {\n    'id': 1,\n    'texto': 'Aprender Python',\n    'completada': False,\n    'fecha': '2024-01-15',\n    'prioridad': 'alta'\n}",
        "ejercicio": "Construí un gestor de tareas completo: agregar tarea (con prioridad: alta/media/baja), listar todas, marcar como completada, filtrar por prioridad, eliminar completadas. Todo persiste en JSON.",
        "pista": "Empezá con las funciones: cargar_tareas(), guardar_tareas(), agregar_tarea(), listar_tareas(). Después el menú principal con while True."
    },
    {
        "id": 23, "bloque": "Casos reales", "titulo": "Caso real: Analizador de datos",
        "descripcion": "Procesá datos reales como un analista — sin pandas",
        "xp": 150,
        "teoria": "Antes de usar pandas, es importante entender cómo procesar datos con Python puro. Esto te da base para entender qué hace pandas por debajo.",
        "ejemplo": "ventas = [\n    {'mes': 'Enero', 'total': 45000, 'region': 'Norte'},\n    {'mes': 'Febrero', 'total': 52000, 'region': 'Sur'},\n]\n\n# Estadísticas\ntotales = [v['total'] for v in ventas]\npromedio = sum(totales) / len(totales)\nmejor = max(ventas, key=lambda v: v['total'])",
        "ejercicio": "Analizá estos datos de ventas mensuales que te damos. Calculá: total anual, promedio mensual, mejor y peor mes, comparación norte vs sur, y un gráfico de barras ASCII.",
        "pista": "Para el gráfico ASCII: calculá el porcentaje de cada mes respecto al máximo. Multiplicá por 30 para tener la longitud de la barra. Usá '█' * longitud."
    },
    {
        "id": 24, "bloque": "Casos reales", "titulo": "Caso real: API con FastAPI",
        "descripcion": "Tu primer backend real — endpoints, validación, base de datos",
        "xp": 200,
        "teoria": "FastAPI es el framework más moderno para hacer APIs en Python. Con muy poco código tenés una API con documentación automática, validación de datos y manejo de errores.",
        "ejemplo": "from fastapi import FastAPI\nfrom pydantic import BaseModel\n\napp = FastAPI()\n\nclass Tarea(BaseModel):\n    titulo: str\n    completada: bool = False\n\ntareas = []\n\n@app.get('/tareas')\ndef listar():\n    return tareas\n\n@app.post('/tareas')\ndef crear(tarea: Tarea):\n    tareas.append(tarea)\n    return tarea",
        "ejercicio": "Construí una API REST para la agenda de contactos: GET /contactos (listar todos), POST /contactos (crear), GET /contactos/{nombre} (buscar), DELETE /contactos/{nombre} (eliminar). Usá una lista en memoria.",
        "pista": "Creá una clase Contacto con BaseModel. Usá una lista global contactos = []. Para buscar: next((c for c in contactos if c.nombre == nombre), None)."
    },
    {
        "id": 25, "bloque": "Casos reales", "titulo": "Caso real: Estructuras de datos",
        "descripcion": "Stack, Queue y LRU Cache — lo que se pregunta en entrevistas",
        "xp": 200,
        "teoria": "Stack (LIFO) y Queue (FIFO) son las estructuras de datos más básicas. Un LRU Cache combina un diccionario (O(1) búsqueda) con una cola ordenada para saber cuál elemento usar menos recientemente.",
        "ejemplo": "# Stack — historial del navegador\nhistorial = []\nhistorial.append('google.com')    # push\nhistorial.append('youtube.com')\nhistorial.pop()  # vuelve a google.com\n\n# Queue — cola de tickets\nfrom collections import deque\ntickets = deque()\ntickets.append('ticket-1')  # enqueue\ntickets.popleft()           # dequeue",
        "ejercicio": "Implementá desde cero: (1) un Stack con push, pop y peek, (2) una Queue con enqueue y dequeue, (3) un sistema de historial del navegador que soporte ir atrás y adelante (necesitás DOS stacks).",
        "pista": "Para el historial con adelante/atrás necesitás: stack_atras y stack_adelante. Cuando navegás: push al stack_atras, limpiar adelante. Cuando vas atrás: pop de atras, push a adelante."
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

@router.get("/bloques")
def obtener_bloques():
    bloques = {}
    for m in modulos:
        b = m["bloque"]
        if b not in bloques:
            bloques[b] = []
        bloques[b].append({"id": m["id"], "titulo": m["titulo"], "xp": m["xp"]})
    return bloques
