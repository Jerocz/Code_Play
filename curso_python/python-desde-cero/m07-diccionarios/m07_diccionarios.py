# =============================================================
# MÓDULO 07 — Diccionarios: datos con nombre
# =============================================================
# Un diccionario guarda pares clave→valor.
# Perfectos para representar objetos del mundo real.
# Son la base de JSON — el formato de datos más usado en la web.
# =============================================================

# ─────────────────────────────────────────────────────────────
# 1. Crear diccionarios
# ─────────────────────────────────────────────────────────────

# Diccionario vacío
vacio = {}

# Persona
persona = {
    "nombre": "Ana García",
    "edad":   25,
    "ciudad": "Buenos Aires",
    "activo": True
}

# Producto
producto = {
    "id":        1,
    "nombre":    "Notebook",
    "precio":    150000,
    "stock":     5,
    "categoria": "tecnología"
}

print(persona)
print(producto)

# ─────────────────────────────────────────────────────────────
# 2. Acceder a valores
# ─────────────────────────────────────────────────────────────

print(persona["nombre"])   # Ana García
print(persona["edad"])     # 25

# .get() — más seguro (no lanza error si la clave no existe)
print(persona.get("ciudad"))          # Buenos Aires
print(persona.get("telefono"))        # None (no existe, no da error)
print(persona.get("telefono", "N/A")) # N/A (valor por defecto)

# La diferencia:
# persona["telefono"]    → KeyError (error si no existe)
# persona.get("telefono")→ None    (no da error)

# ─────────────────────────────────────────────────────────────
# 3. Modificar diccionarios
# ─────────────────────────────────────────────────────────────

persona = {"nombre": "Ana", "edad": 25}

# Agregar nueva clave
persona["email"] = "ana@test.com"
print(persona)

# Modificar valor existente
persona["edad"] = 26
print(persona)

# Agregar/modificar múltiples a la vez
persona.update({"ciudad": "Córdoba", "edad": 27})
print(persona)

# Eliminar
del persona["email"]
print(persona)

valor = persona.pop("ciudad")    # elimina y retorna
print(f"Eliminé: {valor}")
print(persona)

# ─────────────────────────────────────────────────────────────
# 4. Iterar sobre diccionarios
# ─────────────────────────────────────────────────────────────

persona = {
    "nombre": "Ana",
    "edad":   25,
    "ciudad": "Buenos Aires",
    "email":  "ana@test.com"
}

# Solo las claves
print("Claves:")
for clave in persona:
    print(f"  {clave}")

# Solo los valores
print("Valores:")
for valor in persona.values():
    print(f"  {valor}")

# Clave y valor juntos (lo más común)
print("Todo:")
for clave, valor in persona.items():
    print(f"  {clave}: {valor}")

# ─────────────────────────────────────────────────────────────
# 5. Verificar si existe una clave
# ─────────────────────────────────────────────────────────────

usuario = {"nombre": "Luis", "rol": "admin"}

if "rol" in usuario:
    print(f"Rol: {usuario['rol']}")

if "email" not in usuario:
    print("No tiene email registrado")

# ─────────────────────────────────────────────────────────────
# 6. Dict comprehensions
# ─────────────────────────────────────────────────────────────

# {clave: valor for elemento in secuencia}

# Cuadrados del 1 al 5
cuadrados = {x: x**2 for x in range(1, 6)}
print(cuadrados)    # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Longitud de cada palabra
palabras = ["python", "es", "genial", "y", "poderoso"]
longitudes = {p: len(p) for p in palabras}
print(longitudes)

# Invertir un diccionario (clave→valor a valor→clave)
original = {"a": 1, "b": 2, "c": 3}
invertido = {v: k for k, v in original.items()}
print(invertido)    # {1: 'a', 2: 'b', 3: 'c'}

# Filtrar
precios = {"manzana": 50, "banana": 30, "kiwi": 120, "uva": 80}
caros = {k: v for k, v in precios.items() if v > 50}
print(caros)    # {'kiwi': 120, 'uva': 80}

# ─────────────────────────────────────────────────────────────
# 7. Diccionarios anidados
# ─────────────────────────────────────────────────────────────

# Los valores pueden ser cualquier cosa, incluyendo otros dicts

empresa = {
    "nombre": "TechCorp",
    "empleados": {
        "E001": {
            "nombre": "Ana García",
            "cargo":  "Developer",
            "salario": 80000,
            "habilidades": ["Python", "SQL", "Git"]
        },
        "E002": {
            "nombre": "Luis Pérez",
            "cargo":  "Designer",
            "salario": 70000,
            "habilidades": ["Figma", "CSS", "Illustrator"]
        }
    },
    "sede": {
        "ciudad": "Buenos Aires",
        "pais":   "Argentina"
    }
}

# Acceder a niveles anidados
print(empresa["nombre"])
print(empresa["sede"]["ciudad"])
print(empresa["empleados"]["E001"]["nombre"])
print(empresa["empleados"]["E001"]["habilidades"][0])

# Iterar empleados
print("\nEmpleados:")
for id_emp, datos in empresa["empleados"].items():
    habs = ", ".join(datos["habilidades"])
    print(f"  [{id_emp}] {datos['nombre']} — {datos['cargo']}")
    print(f"         Habilidades: {habs}")

# ─────────────────────────────────────────────────────────────
# 8. Contar con diccionarios — patrón muy común
# ─────────────────────────────────────────────────────────────

# Contar frecuencia de elementos
texto = "la casa es grande y la puerta de la casa es azul"
palabras = texto.split()

# Forma manual
conteo = {}
for palabra in palabras:
    if palabra in conteo:
        conteo[palabra] += 1
    else:
        conteo[palabra] = 1

# Forma con .get()
conteo2 = {}
for palabra in palabras:
    conteo2[palabra] = conteo2.get(palabra, 0) + 1

# Forma con collections.Counter (la más pythónica)
from collections import Counter
conteo3 = Counter(palabras)

print("Palabras más frecuentes:")
for palabra, cantidad in conteo3.most_common(3):
    print(f"  '{palabra}': {cantidad} veces")

# ─────────────────────────────────────────────────────────────
# 9. setdefault y defaultdict — inicialización automática
# ─────────────────────────────────────────────────────────────

# setdefault — si la clave no existe, la crea con un valor default
grupos = {}
estudiantes = [("Ana", "A"), ("Luis", "B"), ("Sara", "A"), ("Pedro", "B"), ("Marta", "A")]

for nombre, grupo in estudiantes:
    grupos.setdefault(grupo, []).append(nombre)

print(grupos)   # {'A': ['Ana', 'Sara', 'Marta'], 'B': ['Luis', 'Pedro']}

# defaultdict — diccionario que crea claves automáticamente
from collections import defaultdict

grupos2 = defaultdict(list)
for nombre, grupo in estudiantes:
    grupos2[grupo].append(nombre)

print(dict(grupos2))

# ─────────────────────────────────────────────────────────────
# 10. Casos de uso reales
# ─────────────────────────────────────────────────────────────

# Sistema de calificaciones
def analizar_notas(estudiantes_notas):
    """
    estudiantes_notas: dict de {nombre: [lista de notas]}
    """
    resultados = {}

    for nombre, notas in estudiantes_notas.items():
        promedio = sum(notas) / len(notas)
        resultados[nombre] = {
            "notas":    notas,
            "promedio": round(promedio, 1),
            "max":      max(notas),
            "min":      min(notas),
            "estado":   "Aprobado" if promedio >= 6 else "Desaprobado"
        }

    return resultados

datos = {
    "Ana":  [8, 9, 7, 10, 8],
    "Luis": [5, 4, 6, 5, 7],
    "Sara": [10, 9, 10, 8, 9],
}

resultados = analizar_notas(datos)
print("\n=== RESULTADOS ===")
for nombre, r in resultados.items():
    print(f"\n{nombre}:")
    print(f"  Promedio: {r['promedio']} — {r['estado']}")
    print(f"  Máxima: {r['max']}  Mínima: {r['min']}")

# Agenda de contactos con búsqueda
class AgendaContactos:
    def __init__(self):
        self._contactos = {}

    def agregar(self, nombre, telefono, email=None):
        self._contactos[nombre.lower()] = {
            "nombre":   nombre,
            "telefono": telefono,
            "email":    email
        }

    def buscar(self, nombre):
        return self._contactos.get(nombre.lower())

    def listar(self):
        return sorted(self._contactos.values(), key=lambda c: c["nombre"])

    def eliminar(self, nombre):
        return self._contactos.pop(nombre.lower(), None)

agenda = AgendaContactos()
agenda.agregar("Ana García", "1122334455", "ana@test.com")
agenda.agregar("Luis Pérez", "9988776655")
agenda.agregar("Sara López", "5544332211", "sara@test.com")

contacto = agenda.buscar("Ana García")
print(f"\nContacto encontrado: {contacto}")

print("\nTodos los contactos:")
for c in agenda.listar():
    email = c["email"] or "Sin email"
    print(f"  {c['nombre']}: {c['telefono']} | {email}")

# =============================================================
# EJERCICIOS
# =============================================================
# 1. Creá un diccionario que represente un auto:
#    marca, modelo, año, precio, características (lista).
#    Mostrá toda la info formateada.
#
# 2. Contador de letras:
#    Dada una frase, contá cuántas veces aparece cada letra
#    (sin espacios, sin distinguir mayúsculas).
#    Mostrá solo las 5 más frecuentes.
#
# 3. Invertir y filtrar:
#    Dado {"a":1,"b":2,"c":3,"d":4,"e":5}
#    Creá el invertido pero solo con valores pares.
#
# 4. Sistema de inventario:
#    Diccionario de productos con nombre, precio y stock.
#    Funciones: agregar_producto, actualizar_stock,
#    buscar_por_nombre, listar_disponibles, valor_total.
#
# 5. Agrupar por primera letra:
#    Dada una lista de palabras, agrupalas en un dict
#    donde la clave es la primera letra y el valor es
#    la lista de palabras que empiezan con esa letra.
# =============================================================

print("\n✓ Módulo 07 completado")
