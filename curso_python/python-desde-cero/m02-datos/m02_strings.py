# =============================================================
# MÓDULO 02 — Strings (texto) en profundidad
# =============================================================
# Los strings son el tipo de dato que más vas a usar.
# Aprendelos bien — vale la pena.
# =============================================================

# ─────────────────────────────────────────────────────────────
# 1. Crear strings
# ─────────────────────────────────────────────────────────────

s1 = "comillas dobles"
s2 = 'comillas simples'    # igual que las dobles
s3 = "texto con 'comillas' adentro"
s4 = 'texto con "comillas" adentro'

# String multilínea — tres comillas
poema = """
Este es un texto
que ocupa varias líneas
sin problema.
"""
print(poema)

# ─────────────────────────────────────────────────────────────
# 2. Operaciones básicas con strings
# ─────────────────────────────────────────────────────────────

nombre = "Python"

# Longitud — cuántos caracteres tiene
print(len(nombre))      # 6

# Concatenar — unir strings con +
saludo = "Hola " + nombre
print(saludo)           # Hola Python

# Repetir — multiplicar un string por un número
print("=" * 30)         # ==============================
print("ha" * 3)         # hahaha

# ─────────────────────────────────────────────────────────────
# 3. Acceder a caracteres — índices
# ─────────────────────────────────────────────────────────────

# Los strings son como una fila de caracteres, cada uno con su posición.
# La posición empieza en 0, no en 1.

# P  y  t  h  o  n
# 0  1  2  3  4  5    ← índices positivos
#-6 -5 -4 -3 -2 -1    ← índices negativos (desde el final)

palabra = "Python"

print(palabra[0])    # P — primer caracter
print(palabra[1])    # y — segundo caracter
print(palabra[5])    # n — último caracter
print(palabra[-1])   # n — último caracter (forma más elegante)
print(palabra[-2])   # o — penúltimo caracter

# ─────────────────────────────────────────────────────────────
# 4. Slicing — obtener partes de un string
# ─────────────────────────────────────────────────────────────

# string[inicio:fin]  → desde inicio hasta fin (sin incluir fin)
# string[inicio:]     → desde inicio hasta el final
# string[:fin]        → desde el principio hasta fin
# string[::paso]      → de a cuántos saltar

texto = "Hola Mundo Python"
#        0123456789...

print(texto[0:4])    # Hola   (posiciones 0,1,2,3)
print(texto[5:10])   # Mundo
print(texto[11:])    # Python (desde 11 hasta el final)
print(texto[:4])     # Hola   (desde el inicio hasta 4)
print(texto[-6:])    # Python (últimos 6 caracteres)
print(texto[::2])    # HlMnoPto (cada 2 caracteres)
print(texto[::-1])   # nohtyP odnuM aloH (invertido)

# ─────────────────────────────────────────────────────────────
# 5. Métodos de string — las herramientas
# ─────────────────────────────────────────────────────────────

frase = "  Hola Mundo desde Python  "

# Mayúsculas y minúsculas
print(frase.upper())      # TODO EN MAYÚSCULAS
print(frase.lower())      # todo en minúsculas
print(frase.capitalize()) # Solo primera letra en mayúscula
print(frase.title())      # Cada Palabra Con Mayúscula

# Quitar espacios
print(frase.strip())      # quita espacios al inicio y al final
print(frase.lstrip())     # solo al inicio (left)
print(frase.rstrip())     # solo al final (right)

# Buscar y reemplazar
frase2 = "me gusta el café con leche"
print(frase2.replace("café", "mate"))   # me gusta el mate con leche
print(frase2.replace("e", "3"))         # reemplaza TODOS los e

# Buscar
print(frase2.find("café"))       # 14 (posición donde empieza)
print(frase2.find("pizza"))      # -1 (no encontrado)
print(frase2.count("e"))         # 4 (cuántas veces aparece)
print("café" in frase2)          # True (está en la frase)
print("pizza" in frase2)         # False

# Verificar contenido
print("123".isdigit())           # True (solo dígitos)
print("abc".isalpha())           # True (solo letras)
print("abc123".isalnum())        # True (letras y números)
print("  ".isspace())            # True (solo espacios)

# Empieza y termina con
url = "https://www.python.org"
print(url.startswith("https"))   # True
print(url.endswith(".org"))      # True

# ─────────────────────────────────────────────────────────────
# 6. Split y Join — dividir y unir
# ─────────────────────────────────────────────────────────────

# split() — divide un string en una lista de partes
frase = "Python es un lenguaje genial"
palabras = frase.split(" ")          # divide por espacio
print(palabras)    # ['Python', 'es', 'un', 'lenguaje', 'genial']
print(palabras[0]) # Python
print(len(palabras)) # 5

# split con otro separador
csv = "Ana,Luis,Sara,Pedro"
nombres = csv.split(",")
print(nombres)     # ['Ana', 'Luis', 'Sara', 'Pedro']

fecha = "2024-01-15"
partes = fecha.split("-")
anio, mes, dia = partes   # desempaquetar
print(f"Año: {anio}, Mes: {mes}, Día: {dia}")

# join() — une una lista en un string
palabras = ["Python", "es", "genial"]
frase = " ".join(palabras)
print(frase)       # Python es genial

nombres = ["Ana", "Luis", "Sara"]
print(", ".join(nombres))   # Ana, Luis, Sara
print(" | ".join(nombres))  # Ana | Luis | Sara

# ─────────────────────────────────────────────────────────────
# 7. f-strings avanzados
# ─────────────────────────────────────────────────────────────

nombre = "Ana"
saldo = 1234567.89
porcentaje = 0.1567
pi = 3.14159265

# Números decimales
print(f"{pi:.2f}")           # 3.14 (2 decimales)
print(f"{pi:.4f}")           # 3.1416 (4 decimales)
print(f"{saldo:,.2f}")       # 1,234,567.89 (con comas)
print(f"${saldo:,.2f}")      # $1,234,567.89

# Porcentajes
print(f"{porcentaje:.1%}")   # 15.7%
print(f"{porcentaje:.2%}")   # 15.67%

# Alineación
print(f"{'izquierda':<20}|")  # alinear a la izquierda en 20 chars
print(f"{'derecha':>20}|")    # alinear a la derecha
print(f"{'centro':^20}|")     # centrar
print(f"{'relleno':=^20}|")   # centrar con relleno de =

# Expresiones dentro de {}
x = 10
print(f"El doble de {x} es {x * 2}")
print(f"{'par' if x % 2 == 0 else 'impar'}")

# ─────────────────────────────────────────────────────────────
# 8. Casos de uso reales
# ─────────────────────────────────────────────────────────────

# Validar email (básico)
email = "usuario@ejemplo.com"
es_valido = "@" in email and "." in email.split("@")[-1]
print(f"¿Email válido? {es_valido}")

# Formatear un nombre (capitalizar correctamente)
nombre_sucio = "  ana GARCÍA  "
nombre_limpio = nombre_sucio.strip().title()
print(f"'{nombre_limpio}'")  # 'Ana García'

# Censurar palabras
texto = "Este producto es muy malo y pésimo"
censurado = texto.replace("malo", "****").replace("pésimo", "****")
print(censurado)

# Contar palabras
texto = "Python es un lenguaje de programación muy popular"
cantidad = len(texto.split())
print(f"El texto tiene {cantidad} palabras")

# Extraer dominio de un email
email = "usuario@gmail.com"
dominio = email.split("@")[1]
print(f"Dominio: {dominio}")    # gmail.com

# Verificar si una string es palíndromo
def es_palindromo(palabra):
    limpia = palabra.lower().replace(" ", "")
    return limpia == limpia[::-1]

print(es_palindromo("radar"))     # True
print(es_palindromo("ana"))       # True
print(es_palindromo("python"))    # False
print(es_palindromo("anita lava la tina"))  # True

# =============================================================
# EJERCICIOS
# =============================================================
# 1. Pedí un nombre por input. Mostrá:
#    - En mayúsculas
#    - En minúsculas
#    - Cuántas letras tiene
#    - La primera y última letra
#    - Si es palíndromo
#
# 2. Pedí una frase. Mostrá cuántas palabras tiene
#    y cuántas veces aparece la letra 'a'.
#
# 3. Tenés este email: "USUARIO.APELLIDO@EMPRESA.COM"
#    Ponelo en formato correcto: "usuario.apellido@empresa.com"
#    Extraé el nombre de usuario y el dominio por separado.
#
# 4. Creá un generador de tarjetas de presentación:
#    Pedí nombre, cargo y empresa.
#    Mostrá una tarjeta centrada en 40 caracteres con bordes.
#
# 5. Pedí una contraseña y verificá si:
#    - Tiene al menos 8 caracteres
#    - Tiene al menos un número
#    - Tiene al menos una mayúscula
# =============================================================

print("\n✓ Módulo 02 completado")
