# =============================================================
# MÓDULO 05 — Funciones: organizar y reutilizar código
# =============================================================
# Una función es un bloque de código con nombre que podés
# llamar cuantas veces quieras desde cualquier parte.
# =============================================================

# ─────────────────────────────────────────────────────────────
# 1. Tu primera función
# ─────────────────────────────────────────────────────────────

# def nombre_funcion():
#     código de la función

def saludar():
    print("Hola!")
    print("¿Cómo estás?")

# Definir la función no la ejecuta.
# Para ejecutarla, la tenés que LLAMAR:
saludar()     # imprime "Hola!" y "¿Cómo estás?"
saludar()     # podés llamarla las veces que quieras
saludar()

# ─────────────────────────────────────────────────────────────
# 2. Parámetros — datos que recibe la función
# ─────────────────────────────────────────────────────────────

def saludar_persona(nombre):
    print(f"Hola, {nombre}!")

saludar_persona("Ana")    # Hola, Ana!
saludar_persona("Luis")   # Hola, Luis!
saludar_persona("Sara")   # Hola, Sara!

# Múltiples parámetros
def presentar(nombre, edad, ciudad):
    print(f"Me llamo {nombre}, tengo {edad} años y vivo en {ciudad}.")

presentar("Ana", 25, "Buenos Aires")
presentar("Luis", 30, "Córdoba")

# ─────────────────────────────────────────────────────────────
# 3. return — devolver un resultado
# ─────────────────────────────────────────────────────────────

# Una función puede RETORNAR un valor que podés guardar o usar

def sumar(a, b):
    resultado = a + b
    return resultado

# Guardar el resultado
total = sumar(10, 5)
print(total)          # 15

# Usar directamente
print(sumar(3, 4))    # 7
print(sumar(10, 5) * 2)  # 30

# Ejemplo real — calcular área
def area_rectangulo(base, altura):
    return base * altura

def area_circulo(radio):
    pi = 3.14159
    return pi * radio ** 2

print(f"Área rectángulo 4x5: {area_rectangulo(4, 5)}")
print(f"Área círculo r=3: {area_circulo(3):.2f}")

# ─────────────────────────────────────────────────────────────
# 4. Parámetros con valores por defecto
# ─────────────────────────────────────────────────────────────

def saludar(nombre, saludo="Hola", puntuacion="!"):
    return f"{saludo}, {nombre}{puntuacion}"

print(saludar("Ana"))                    # Hola, Ana!
print(saludar("Luis", "Buenas"))         # Buenas, Luis!
print(saludar("Sara", "Bienvenida", "."))# Bienvenida, Sara.

# Los parámetros con default van DESPUÉS de los obligatorios

def crear_usuario(nombre, email, rol="usuario", activo=True):
    return {
        "nombre": nombre,
        "email":  email,
        "rol":    rol,
        "activo": activo
    }

u1 = crear_usuario("Ana", "ana@test.com")
u2 = crear_usuario("Admin", "admin@test.com", rol="admin")
print(u1)
print(u2)

# ─────────────────────────────────────────────────────────────
# 5. Argumentos con nombre (keyword arguments)
# ─────────────────────────────────────────────────────────────

def registrar_pago(monto, moneda, descripcion, cuotas=1):
    print(f"Pago: {moneda} {monto} - {descripcion} ({cuotas} cuota/s)")

# Podés pasar los argumentos en cualquier orden si los nombrás
registrar_pago(1000, "ARS", "Suscripción mensual")
registrar_pago(monto=5000, cuotas=12, moneda="ARS", descripcion="Notebook")
registrar_pago(descripcion="Curso", monto=2500, moneda="USD")

# ─────────────────────────────────────────────────────────────
# 6. *args — cantidad variable de argumentos
# ─────────────────────────────────────────────────────────────

# A veces no sabés cuántos argumentos va a recibir la función

def sumar_todos(*numeros):
    # numeros es una tupla con todos los argumentos
    total = 0
    for n in numeros:
        total += n
    return total

print(sumar_todos(1, 2, 3))         # 6
print(sumar_todos(10, 20, 30, 40))  # 100
print(sumar_todos(5))               # 5

# Más elegante con sum()
def sumar_todos_v2(*numeros):
    return sum(numeros)

# ─────────────────────────────────────────────────────────────
# 7. **kwargs — argumentos con nombre variables
# ─────────────────────────────────────────────────────────────

def mostrar_info(**datos):
    # datos es un diccionario con los argumentos nombrados
    for clave, valor in datos.items():
        print(f"  {clave}: {valor}")

mostrar_info(nombre="Ana", edad=25, ciudad="Buenos Aires")
print()
mostrar_info(producto="Notebook", precio=150000, stock=5, categoria="tecnología")

# ─────────────────────────────────────────────────────────────
# 8. Retornar múltiples valores
# ─────────────────────────────────────────────────────────────

def min_max(numeros):
    return min(numeros), max(numeros)   # retorna una tupla

minimo, maximo = min_max([5, 3, 8, 1, 9, 2])
print(f"Mínimo: {minimo}, Máximo: {maximo}")

def dividir_con_resto(dividendo, divisor):
    cociente = dividendo // divisor
    resto    = dividendo % divisor
    return cociente, resto

q, r = dividir_con_resto(17, 5)
print(f"17 ÷ 5 = {q} con resto {r}")

# ─────────────────────────────────────────────────────────────
# 9. Scope — dónde viven las variables
# ─────────────────────────────────────────────────────────────

# Las variables dentro de una función SOLO existen dentro de ella

def mi_funcion():
    variable_local = "solo existo aquí"
    print(variable_local)   # funciona

mi_funcion()
# print(variable_local)   # ERROR: NameError — no existe fuera

# Variables globales — existen en todo el módulo
mensaje_global = "Soy global"

def usar_global():
    print(mensaje_global)   # puede leerla

usar_global()   # Soy global

# Para MODIFICAR una global desde una función (evitar si es posible)
contador = 0
def incrementar():
    global contador
    contador += 1

incrementar()
incrementar()
print(f"Contador: {contador}")   # 2

# Mejor práctica: pasar como argumento y retornar
def incrementar_v2(contador):
    return contador + 1

contador = 0
contador = incrementar_v2(contador)
contador = incrementar_v2(contador)
print(f"Contador v2: {contador}")   # 2

# ─────────────────────────────────────────────────────────────
# 10. Funciones lambda — funciones en una línea
# ─────────────────────────────────────────────────────────────

# lambda argumentos: expresion

# Función normal
def doble(x):
    return x * 2

# Lambda equivalente
doble_lambda = lambda x: x * 2

print(doble(5))        # 10
print(doble_lambda(5)) # 10

# Útil con sorted(), map(), filter()
nombres = ["Sara", "Ana", "Luis", "Pedro", "Marta"]
# Ordenar por longitud del nombre
ordenados = sorted(nombres, key=lambda n: len(n))
print(ordenados)   # ['Ana', 'Luis', 'Sara', 'Pedro', 'Marta']

# map() — aplicar función a cada elemento
numeros = [1, 2, 3, 4, 5]
cuadrados = list(map(lambda x: x**2, numeros))
print(cuadrados)   # [1, 4, 9, 16, 25]

# filter() — filtrar elementos
pares = list(filter(lambda x: x % 2 == 0, numeros))
print(pares)       # [2, 4]

# ─────────────────────────────────────────────────────────────
# 11. Recursión — función que se llama a sí misma
# ─────────────────────────────────────────────────────────────

def factorial(n):
    # Caso base — sin esto, loop infinito
    if n <= 1:
        return 1
    # Caso recursivo
    return n * factorial(n - 1)

# factorial(4) = 4 * factorial(3)
#              = 4 * 3 * factorial(2)
#              = 4 * 3 * 2 * factorial(1)
#              = 4 * 3 * 2 * 1
#              = 24

print(factorial(5))   # 120
print(factorial(10))  # 3628800

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print([fibonacci(i) for i in range(10)])
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# ─────────────────────────────────────────────────────────────
# 12. Funciones como valores — pasarlas y retornarlas
# ─────────────────────────────────────────────────────────────

# Las funciones son objetos como cualquier otro
def aplicar(funcion, valor):
    return funcion(valor)

def al_cuadrado(x): return x ** 2
def al_cubo(x):     return x ** 3

print(aplicar(al_cuadrado, 4))   # 16
print(aplicar(al_cubo, 3))       # 27

# Función que retorna otra función (closure)
def crear_multiplicador(factor):
    def multiplicar(numero):
        return numero * factor
    return multiplicar

por_dos  = crear_multiplicador(2)
por_tres = crear_multiplicador(3)
por_diez = crear_multiplicador(10)

print(por_dos(5))   # 10
print(por_tres(5))  # 15
print(por_diez(5))  # 50

# ─────────────────────────────────────────────────────────────
# 13. Decoradores — funciones que modifican funciones
# ─────────────────────────────────────────────────────────────

import time

def medir_tiempo(funcion):
    def wrapper(*args, **kwargs):
        inicio   = time.time()
        resultado = funcion(*args, **kwargs)
        fin      = time.time()
        print(f"⏱ {funcion.__name__} tardó {(fin-inicio)*1000:.2f}ms")
        return resultado
    return wrapper

@medir_tiempo
def suma_lenta(n):
    total = 0
    for i in range(n):
        total += i
    return total

resultado = suma_lenta(1_000_000)
print(f"Resultado: {resultado:,}")

# Decorador para validar tipos
def validar_positivo(funcion):
    def wrapper(*args):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Todos los argumentos deben ser positivos. Recibí: {arg}")
        return funcion(*args)
    return wrapper

@validar_positivo
def raiz_cuadrada(n):
    return n ** 0.5

print(raiz_cuadrada(16))    # 4.0
# print(raiz_cuadrada(-4))  # ValueError

# =============================================================
# EJERCICIOS
# =============================================================
# 1. Escribí una función que reciba una lista de notas y retorne:
#    el promedio, la nota más alta, la más baja y si aprobó (>= 6).
#
# 2. Función de descuento:
#    Recibe precio y porcentaje de descuento.
#    Retorna precio final y cuánto se ahorró.
#    Validá que el descuento sea entre 0 y 100.
#
# 3. Usando *args, creá una función que reciba cualquier
#    cantidad de números y retorne su suma, promedio y moda.
#
# 4. Creá un decorador "log_llamada" que imprima cada vez
#    que se llama una función, con qué argumentos y qué retornó.
#
# 5. Función recursiva:
#    Potencia sin usar **: potencia(2, 10) → 1024
#    Suma de dígitos: suma_digitos(1234) → 10
#    Palíndromo recursivo: es_palindromo("radar") → True
# =============================================================

print("\n✓ Módulo 05 completado")
