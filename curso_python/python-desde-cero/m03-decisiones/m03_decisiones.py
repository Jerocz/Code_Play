# =============================================================
# MÓDULO 03 — Tomar decisiones: if, elif, else
# =============================================================
# Los programas no siempre hacen lo mismo.
# Dependiendo de los datos, toman caminos distintos.
# =============================================================

# ─────────────────────────────────────────────────────────────
# 1. if — hacer algo solo si se cumple una condición
# ─────────────────────────────────────────────────────────────

# Estructura básica:
#   if condicion:
#       codigo que se ejecuta si la condicion es True

edad = 20

if edad >= 18:
    print("Sos mayor de edad")

# Si la condición es False, simplemente no hace nada
edad_menor = 15
if edad_menor >= 18:
    print("Esto NO se imprime porque 15 < 18")

print("Esto sí se imprime siempre")

# ─────────────────────────────────────────────────────────────
# 2. else — qué hacer cuando la condición NO se cumple
# ─────────────────────────────────────────────────────────────

edad = 16

if edad >= 18:
    print("Podés entrar al boliche")
else:
    print("No podés entrar, sos menor de edad")

# ─────────────────────────────────────────────────────────────
# 3. elif — múltiples condiciones
# ─────────────────────────────────────────────────────────────

# elif = "else if" = si lo anterior no se cumplió, probá esto

nota = 75

if nota >= 90:
    print("Sobresaliente")
elif nota >= 80:
    print("Muy bueno")
elif nota >= 70:
    print("Bueno")
elif nota >= 60:
    print("Aprobado")
else:
    print("Desaprobado")

# Solo se ejecuta el PRIMER bloque cuya condición sea True
# Los demás se saltean

# ─────────────────────────────────────────────────────────────
# 4. Operadores de comparación — las condiciones
# ─────────────────────────────────────────────────────────────

a, b = 10, 20

print(a == b)   # False — ¿son iguales?    (== no confundir con =)
print(a != b)   # True  — ¿son distintos?
print(a < b)    # True  — ¿a es menor que b?
print(a > b)    # False — ¿a es mayor que b?
print(a <= b)   # True  — ¿a es menor o igual a b?
print(a >= b)   # False — ¿a es mayor o igual a b?

# Con strings
print("ana" == "ana")   # True
print("Ana" == "ana")   # False (mayúsculas importan)
print("b" > "a")        # True (orden alfabético)

# ─────────────────────────────────────────────────────────────
# 5. Operadores lógicos — combinar condiciones
# ─────────────────────────────────────────────────────────────

# and — las DOS condiciones deben ser True
edad = 25
tiene_dni = True

if edad >= 18 and tiene_dni:
    print("Puede votar")

# or — AL MENOS UNA condición debe ser True
tiene_efectivo = False
tiene_tarjeta  = True

if tiene_efectivo or tiene_tarjeta:
    print("Puede pagar")

# not — invierte True/False
esta_lloviendo = False

if not esta_lloviendo:
    print("Podemos salir sin paraguas")

# Combinaciones
temperatura = 22
humedad = 60

if temperatura >= 20 and temperatura <= 30 and humedad < 70:
    print("Día agradable para salir")

# Forma más pytónica de verificar rangos
if 20 <= temperatura <= 30:
    print("Temperatura agradable")

# ─────────────────────────────────────────────────────────────
# 6. Valores "truthy" y "falsy"
# ─────────────────────────────────────────────────────────────

# En Python, no solo True/False actúan como booleanos
# Estos valores se comportan como False:
#   False, 0, 0.0, "", [], {}, None

# Estos se comportan como True:
#   Cualquier otro valor

nombre = ""
if nombre:
    print("El nombre no está vacío")
else:
    print("El nombre está vacío")    # esto se ejecuta

saldo = 0
if saldo:
    print("Tenés saldo")
else:
    print("Sin saldo")               # esto se ejecuta

lista = [1, 2, 3]
if lista:
    print("La lista tiene elementos")  # esto se ejecuta

# ─────────────────────────────────────────────────────────────
# 7. Operador ternario — if en una línea
# ─────────────────────────────────────────────────────────────

# valor_si_true if condicion else valor_si_false

edad = 20
mensaje = "mayor" if edad >= 18 else "menor"
print(mensaje)   # mayor

# Es lo mismo que:
if edad >= 18:
    mensaje = "mayor"
else:
    mensaje = "menor"

# Útil para cosas simples, no abusar
precio = 100
descuento = 0.2 if precio > 50 else 0.1
print(f"Descuento: {descuento:.0%}")

# ─────────────────────────────────────────────────────────────
# 8. Casos de uso reales
# ─────────────────────────────────────────────────────────────

# Sistema de clasificación de IMC
peso = 70      # kg
altura = 1.75  # metros
imc = peso / (altura ** 2)

print(f"IMC: {imc:.1f}")

if imc < 18.5:
    categoria = "Bajo peso"
elif imc < 25:
    categoria = "Normal"
elif imc < 30:
    categoria = "Sobrepeso"
else:
    categoria = "Obesidad"

print(f"Categoría: {categoria}")

# ─────────────────────────────────────────────────────────────
# Calculador de descuentos
# ─────────────────────────────────────────────────────────────

def calcular_precio(precio_base, es_socio, dia_semana):
    descuento = 0

    if es_socio:
        descuento += 0.10     # 10% por ser socio

    if dia_semana in ["lunes", "martes"]:
        descuento += 0.15     # 15% los días flojos

    if precio_base > 5000:
        descuento += 0.05     # 5% extra en compras grandes

    precio_final = precio_base * (1 - descuento)
    return precio_final, descuento

precio, desc = calcular_precio(8000, True, "lunes")
print(f"Precio final: ${precio:,.0f} (descuento: {desc:.0%})")

# ─────────────────────────────────────────────────────────────
# Validador de contraseña
# ─────────────────────────────────────────────────────────────

def validar_contrasena(password):
    errores = []

    if len(password) < 8:
        errores.append("Debe tener al menos 8 caracteres")

    if not any(c.isupper() for c in password):
        errores.append("Debe tener al menos una mayúscula")

    if not any(c.isdigit() for c in password):
        errores.append("Debe tener al menos un número")

    if not any(c in "!@#$%^&*" for c in password):
        errores.append("Debe tener al menos un símbolo especial")

    if errores:
        print("Contraseña inválida:")
        for error in errores:
            print(f"  ✗ {error}")
    else:
        print("✓ Contraseña válida")

validar_contrasena("abc")
print()
validar_contrasena("Python123!")

# =============================================================
# EJERCICIOS
# =============================================================
# 1. Pedí la temperatura actual y decí qué ropa usar:
#    - < 10°: "Campera gruesa"
#    - 10-20°: "Rompevientos"
#    - 20-30°: "Remera"
#    - > 30°: "Lo menos posible"
#
# 2. Creá un sistema de notas:
#    Pedí 3 notas, calculá el promedio y mostrá:
#    - El promedio
#    - Si aprobó o desaprobó (promedio >= 6)
#    - La nota más alta y más baja
#
# 3. Calculadora de envío:
#    - Gratis si el pedido supera $5000
#    - $300 si está entre $1000 y $5000
#    - $500 si es menos de $1000
#    - Extra $200 si es zona remota
#
# 4. FizzBuzz clásico de entrevistas:
#    Para números del 1 al 20:
#    - Si es múltiplo de 3: imprimir "Fizz"
#    - Si es múltiplo de 5: imprimir "Buzz"
#    - Si es múltiplo de ambos: imprimir "FizzBuzz"
#    - Si no: imprimir el número
#
# 5. Clasificador de triángulos:
#    Pedí 3 lados. Verificá si forman un triángulo válido
#    (la suma de dos lados debe ser mayor que el tercero).
#    Si es válido, decí si es equilátero, isósceles o escaleno.
# =============================================================

print("\n✓ Módulo 03 completado")
