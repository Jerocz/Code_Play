# =============================================================
# MÓDULO 01 — Tus primeros pasos en Python
# =============================================================
# Cómo correr este archivo:
#   Abrí la terminal, navegá hasta esta carpeta y escribí:
#   python m01_primeros_pasos.py
# =============================================================

# ─────────────────────────────────────────────────────────────
# 1. Tu primer programa — print()
# ─────────────────────────────────────────────────────────────

# print() muestra texto en la pantalla
# Es la herramienta más básica de un programador

print("Hola mundo")
print("Esto es Python")
print("Estoy aprendiendo a programar")

# Podés imprimir números también
print(42)
print(3.14)

# Podés imprimir múltiples cosas juntas
print("Tengo", 25, "años")

# ─────────────────────────────────────────────────────────────
# 2. Comentarios — líneas que Python ignora
# ─────────────────────────────────────────────────────────────

# Esto es un comentario. Python lo ignora completamente.
# Los comentarios sirven para explicar tu código.
# Empiezan con el símbolo #

print("Esto sí se ejecuta")
# print("Esto NO se ejecuta porque está comentado")

# ─────────────────────────────────────────────────────────────
# 3. Variables — guardar información
# ─────────────────────────────────────────────────────────────

# Una variable es como una caja con nombre.
# Guardás algo adentro y lo podés usar después.

nombre = "Ana"         # guardamos el texto "Ana" en la variable "nombre"
edad   = 25            # guardamos el número 25 en "edad"
altura = 1.65          # guardamos 1.65 en "altura"

# Ahora podemos usar esas variables
print(nombre)   # muestra: Ana
print(edad)     # muestra: 25
print(altura)   # muestra: 1.65

# Combinamos variables con texto
print("Me llamo", nombre)
print("Tengo", edad, "años")
print("Mido", altura, "metros")

# ─────────────────────────────────────────────────────────────
# 4. El signo = no es "igual" matemático
# ─────────────────────────────────────────────────────────────

# En Python, = significa "asignación" — guardar un valor
# No significa que los dos lados son iguales

contador = 0          # contador empieza en 0
print(contador)       # muestra: 0

contador = contador + 1   # tomamos el valor actual (0) y le sumamos 1
print(contador)            # muestra: 1

contador = contador + 1   # ahora es 1, le sumamos 1
print(contador)            # muestra: 2

# Forma corta de hacer lo mismo:
contador += 1    # equivale a: contador = contador + 1
print(contador)  # muestra: 3

contador += 5    # le sumamos 5
print(contador)  # muestra: 8

# ─────────────────────────────────────────────────────────────
# 5. Tipos de datos básicos
# ─────────────────────────────────────────────────────────────

# Python tiene distintos tipos de datos.
# Cada tipo sirve para cosas diferentes.

# int — números enteros (sin decimales)
cantidad = 10
temperatura = -5
año = 2024

# float — números con decimales
precio = 19.99
pi = 3.14159
porcentaje = 0.15

# str — texto (string = cadena de texto)
# Puede ir entre comillas simples o dobles, ambas son iguales
saludo = "Hola"
nombre = 'Python'
frase = "Me gusta programar"

# bool — verdadero o falso (solo dos valores posibles)
es_mayor_de_edad = True
tiene_descuento   = False
llueve_hoy        = True

# Podés ver el tipo de una variable con type()
print(type(cantidad))    # <class 'int'>
print(type(precio))      # <class 'float'>
print(type(saludo))      # <class 'str'>
print(type(llueve_hoy))  # <class 'bool'>

# ─────────────────────────────────────────────────────────────
# 6. Operaciones matemáticas
# ─────────────────────────────────────────────────────────────

a = 10
b = 3

print(a + b)   # 13  — suma
print(a - b)   # 7   — resta
print(a * b)   # 30  — multiplicación
print(a / b)   # 3.333... — división (siempre da decimal)
print(a // b)  # 3   — división entera (solo la parte entera)
print(a % b)   # 1   — módulo (el resto de dividir 10 / 3)
print(a ** b)  # 1000 — potencia (10 elevado a la 3)

# El módulo (%) es muy útil en programación
# Sirve para saber si un número es par o impar:
print(10 % 2)  # 0 — 10 es par (el resto es 0)
print(7 % 2)   # 1 — 7 es impar (el resto es 1)

# ─────────────────────────────────────────────────────────────
# 7. f-strings — la forma moderna de combinar texto y variables
# ─────────────────────────────────────────────────────────────

# La f antes de las comillas hace que {} funcione como "hueco"
# donde Python mete el valor de la variable

nombre = "Carlos"
edad = 28
ciudad = "Buenos Aires"

print(f"Me llamo {nombre}")
print(f"Tengo {edad} años")
print(f"Vivo en {ciudad}")
print(f"Me llamo {nombre}, tengo {edad} años y vivo en {ciudad}.")

# Dentro de {} podés poner operaciones
precio = 100
descuento = 0.2
print(f"El precio con descuento es: {precio * (1 - descuento)}")
print(f"Precio: ${precio * (1 - descuento):.2f}")  # :.2f = 2 decimales

# ─────────────────────────────────────────────────────────────
# 8. Input — pedirle datos al usuario
# ─────────────────────────────────────────────────────────────

# input() pausa el programa y espera que el usuario escriba algo
# IMPORTANTE: input() siempre retorna texto (str), aunque el usuario escriba números

# Descomentá estas líneas para probarlas (sacales el #):
# nombre = input("¿Cómo te llamás? ")
# print(f"Hola, {nombre}!")

# Si querés un número, tenés que convertirlo:
# edad_texto = input("¿Cuántos años tenés? ")
# edad = int(edad_texto)    # convertir texto a número entero
# print(f"El año que viene tenés {edad + 1} años")

# Forma compacta:
# edad = int(input("¿Cuántos años tenés? "))

# ─────────────────────────────────────────────────────────────
# 9. Conversión de tipos
# ─────────────────────────────────────────────────────────────

# A veces necesitás convertir un tipo en otro

texto_numero = "42"
numero = int(texto_numero)      # str → int
print(numero + 1)               # 43 — ahora podemos operar

numero_decimal = float("3.14")  # str → float
print(numero_decimal * 2)       # 6.28

numero_a_texto = str(100)       # int → str
print("El número es: " + numero_a_texto)  # concatenar strings

# ¿Qué pasa si no convertís?
# "42" + 1   # ERROR: no podés sumar texto y número
# int("hola") # ERROR: "hola" no es un número válido

# ─────────────────────────────────────────────────────────────
# 10. Tu primer programa real — calculadora básica
# ─────────────────────────────────────────────────────────────

print("\n--- CALCULADORA ---")
# Descomentá esto para probarlo:
# numero1 = float(input("Primer número: "))
# numero2 = float(input("Segundo número: "))
# print(f"Suma:           {numero1 + numero2}")
# print(f"Resta:          {numero1 - numero2}")
# print(f"Multiplicación: {numero1 * numero2}")
# if numero2 != 0:
#     print(f"División:       {numero1 / numero2:.2f}")
# else:
#     print("División: no se puede dividir por cero")

# Versión sin input para que puedas ver el resultado ahora:
n1, n2 = 15, 4
print(f"Números: {n1} y {n2}")
print(f"Suma:           {n1 + n2}")
print(f"Resta:          {n1 - n2}")
print(f"Multiplicación: {n1 * n2}")
print(f"División:       {n1 / n2:.2f}")
print(f"División entera:{n1 // n2}")
print(f"Resto:          {n1 % n2}")
print(f"Potencia:       {n1 ** n2}")

# =============================================================
# EJERCICIOS — intentá resolverlos vos solo
# =============================================================
# 1. Creá variables con tu nombre, edad y ciudad favorita.
#    Imprimí una presentación usando f-strings.
#
# 2. Calculá cuántos segundos hay en un año.
#    Usá variables separadas para minutos, horas, días.
#    (spoiler: 31,536,000 segundos)
#
# 3. Una remera cuesta $1500. Tiene 30% de descuento.
#    Calculá el precio final y mostralo con 2 decimales.
#
# 4. Escribí un programa que pida tu nombre por input
#    y te salude con tu nombre.
#
# 5. Pedí dos números por input y mostrá todas las
#    operaciones matemáticas entre ellos.
# =============================================================

print("\n✓ Módulo 01 completado")
