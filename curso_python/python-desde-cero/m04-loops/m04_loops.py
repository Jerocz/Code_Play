# =============================================================
# MÓDULO 04 — Loops: repetir cosas
# =============================================================
# Los loops son lo que hace que los programas sean poderosos.
# Sin loops, para procesar 1000 datos necesitarías 1000 líneas.
# Con loops, lo hacés en 3.
# =============================================================

# ─────────────────────────────────────────────────────────────
# 1. while — repetir MIENTRAS se cumpla una condición
# ─────────────────────────────────────────────────────────────

# Estructura:
#   while condicion:
#       codigo que se repite

contador = 1
while contador <= 5:
    print(f"Vuelta número {contador}")
    contador += 1     # MUY IMPORTANTE: si olvidás esto, loop infinito

print("Terminó el while")

# Caso real: seguir preguntando hasta que el usuario responda bien
# (descomentá para probar)
# respuesta = ""
# while respuesta != "si" and respuesta != "no":
#     respuesta = input("¿Querés continuar? (si/no): ").lower()
# print(f"Respondiste: {respuesta}")

# ─────────────────────────────────────────────────────────────
# 2. for — recorrer una secuencia
# ─────────────────────────────────────────────────────────────

# for es más común que while.
# Recorre cada elemento de una secuencia (lista, string, range...)

# Recorrer un string (letra por letra)
for letra in "Python":
    print(letra)

print()

# Recorrer una lista de cosas
frutas = ["manzana", "banana", "naranja", "uva"]
for fruta in frutas:
    print(f"Fruta: {fruta}")

print()

# ─────────────────────────────────────────────────────────────
# 3. range() — generar secuencias de números
# ─────────────────────────────────────────────────────────────

# range(n)         → 0, 1, 2, ..., n-1
# range(a, b)      → a, a+1, ..., b-1
# range(a, b, paso)→ de a hasta b con saltos de "paso"

print("range(5):")
for i in range(5):
    print(i, end=" ")    # end=" " para imprimir en la misma línea
print()

print("range(1, 6):")
for i in range(1, 6):
    print(i, end=" ")
print()

print("range(0, 20, 5):")
for i in range(0, 20, 5):
    print(i, end=" ")
print()

print("range(10, 0, -1)  — cuenta regresiva:")
for i in range(10, 0, -1):
    print(i, end=" ")
print()

# Suma de los primeros 100 números
total = 0
for i in range(1, 101):
    total += i
print(f"Suma del 1 al 100: {total}")   # 5050

# ─────────────────────────────────────────────────────────────
# 4. break y continue — controlar el loop
# ─────────────────────────────────────────────────────────────

# break — SALIR del loop antes de que termine
print("\nbreak — buscar el primer número mayor a 7:")
numeros = [2, 5, 3, 9, 1, 4, 8]
for n in numeros:
    if n > 7:
        print(f"Encontré: {n}")
        break   # salimos del loop, no seguimos buscando
    print(f"  {n} no es mayor a 7")

# continue — SALTEAR esta vuelta y seguir con la siguiente
print("\ncontinue — imprimir solo números pares:")
for i in range(1, 11):
    if i % 2 != 0:    # si es impar
        continue      # saltear, no ejecutar el print
    print(i, end=" ")
print()

# ─────────────────────────────────────────────────────────────
# 5. enumerate() — recorrer con índice y valor
# ─────────────────────────────────────────────────────────────

# A veces necesitás saber en qué posición estás

frutas = ["manzana", "banana", "naranja"]

# Sin enumerate — funciona pero es feo
for i in range(len(frutas)):
    print(f"{i}: {frutas[i]}")

print()

# Con enumerate — limpio y pythónico
for indice, fruta in enumerate(frutas):
    print(f"{indice}: {fruta}")

print()

# enumerate empieza en 0, pero podés cambiarlo
for numero, fruta in enumerate(frutas, start=1):
    print(f"{numero}. {fruta}")

# ─────────────────────────────────────────────────────────────
# 6. zip() — recorrer dos listas a la vez
# ─────────────────────────────────────────────────────────────

nombres  = ["Ana", "Luis", "Sara"]
edades   = [25, 30, 22]
ciudades = ["Buenos Aires", "Córdoba", "Rosario"]

for nombre, edad, ciudad in zip(nombres, edades, ciudades):
    print(f"{nombre} tiene {edad} años y vive en {ciudad}")

# ─────────────────────────────────────────────────────────────
# 7. List comprehensions — loops en una línea
# ─────────────────────────────────────────────────────────────

# [expresión for elemento in secuencia if condición]

# Forma larga:
cuadrados = []
for x in range(1, 6):
    cuadrados.append(x ** 2)
print(cuadrados)    # [1, 4, 9, 16, 25]

# Con comprehension — mismo resultado, una línea:
cuadrados = [x ** 2 for x in range(1, 6)]
print(cuadrados)    # [1, 4, 9, 16, 25]

# Con condición — solo pares
pares = [x for x in range(1, 21) if x % 2 == 0]
print(pares)        # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# Transformar strings
frutas = ["manzana", "banana", "naranja"]
en_mayusculas = [f.upper() for f in frutas]
print(en_mayusculas)   # ['MANZANA', 'BANANA', 'NARANJA']

# Filtrar y transformar a la vez
notas = [45, 78, 92, 55, 88, 33, 71]
aprobados = [n for n in notas if n >= 60]
print(f"Aprobados: {aprobados}")   # [78, 92, 88, 71]

# ─────────────────────────────────────────────────────────────
# 8. Loops anidados — un loop dentro de otro
# ─────────────────────────────────────────────────────────────

# Tabla de multiplicar del 1 al 5
print("\nTabla de multiplicar:")
for i in range(1, 6):
    for j in range(1, 6):
        resultado = i * j
        print(f"{resultado:3}", end="")   # :3 = mínimo 3 espacios
    print()   # nueva línea al terminar cada fila

# ─────────────────────────────────────────────────────────────
# 9. Casos de uso reales
# ─────────────────────────────────────────────────────────────

# Menú de opciones (patrón muy común)
opciones = {
    "1": "Ver perfil",
    "2": "Cambiar contraseña",
    "3": "Ver historial",
    "0": "Salir"
}

# (descomentá para probar)
# while True:
#     print("\n=== MENÚ ===")
#     for clave, descripcion in opciones.items():
#         print(f"  {clave}. {descripcion}")
#
#     opcion = input("\nElegí una opción: ")
#
#     if opcion == "0":
#         print("Hasta luego!")
#         break
#     elif opcion in opciones:
#         print(f"\nEjecutando: {opciones[opcion]}")
#     else:
#         print("Opción inválida, intentá de nuevo")

# Estadísticas de una lista de números
def estadisticas(numeros):
    if not numeros:
        return None

    total   = sum(numeros)
    minimo  = numeros[0]
    maximo  = numeros[0]
    positivos = 0
    negativos = 0

    for n in numeros:
        if n < minimo:
            minimo = n
        if n > maximo:
            maximo = n
        if n > 0:
            positivos += 1
        elif n < 0:
            negativos += 1

    return {
        "total":     total,
        "promedio":  total / len(numeros),
        "minimo":    minimo,
        "maximo":    maximo,
        "positivos": positivos,
        "negativos": negativos,
        "cantidad":  len(numeros)
    }

datos = [5, -3, 8, 0, -1, 12, 4, -7, 9, 2]
stats = estadisticas(datos)
print(f"\nEstadísticas de {datos}:")
for clave, valor in stats.items():
    print(f"  {clave}: {valor}")

# Adivinar el número — juego básico
import random

def juego_adivinar():
    numero_secreto = random.randint(1, 100)
    intentos = 0
    max_intentos = 7

    print("\n=== ADIVINA EL NÚMERO ===")
    print(f"Pensé un número del 1 al 100. Tenés {max_intentos} intentos.")

    # (descomentá para jugar)
    # while intentos < max_intentos:
    #     intento = int(input(f"\nIntento {intentos + 1}/{max_intentos}: "))
    #     intentos += 1
    #
    #     if intento == numero_secreto:
    #         print(f"¡Correcto! Lo adivinaste en {intentos} intentos.")
    #         break
    #     elif intento < numero_secreto:
    #         print("Muy bajo, probá con un número mayor")
    #     else:
    #         print("Muy alto, probá con un número menor")
    #
    #     restantes = max_intentos - intentos
    #     if restantes > 0:
    #         print(f"Te quedan {restantes} intentos")
    # else:
    #     print(f"Se acabaron los intentos. El número era {numero_secreto}")

    print(f"(El número sería: {numero_secreto})")

juego_adivinar()

# =============================================================
# EJERCICIOS
# =============================================================
# 1. Imprimir los primeros 15 múltiplos de 7.
#
# 2. Dado [3, 1, 4, 1, 5, 9, 2, 6, 5, 3], sin usar funciones
#    built-in, encontrá: suma, promedio, máximo, mínimo.
#
# 3. Generá la tabla de multiplicar completa del 1 al 10.
#
# 4. Usando list comprehension:
#    - Lista de números del 1 al 50 divisibles por 3 o por 5
#    - Lista de cuadrados de los números pares del 1 al 20
#
# 5. Contador de letras:
#    Dada una frase, contá cuántas veces aparece cada letra
#    (ignorando espacios y mayúsculas/minúsculas).
#    Mostrá las 3 más frecuentes.
#
# 6. Pirámide de estrellas:
#    Dado n=5, imprimir:
#        *
#       ***
#      *****
#     *******
#    *********
# =============================================================

print("\n✓ Módulo 04 completado")
