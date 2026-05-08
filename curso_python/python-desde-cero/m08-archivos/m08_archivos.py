# =============================================================
# MÓDULO 08 — Archivos y JSON: guardar datos
# =============================================================
# Los programas guardan datos en archivos para que persistan
# cuando el programa se cierra. Vamos de texto plano a JSON.
# =============================================================

import json
import os
import csv
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# 1. Leer archivos de texto
# ─────────────────────────────────────────────────────────────

# Primero creamos un archivo de ejemplo para trabajar
with open("ejemplo.txt", "w", encoding="utf-8") as f:
    f.write("Línea 1: Hola mundo\n")
    f.write("Línea 2: Python es genial\n")
    f.write("Línea 3: Aprendiendo archivos\n")

# Leer todo el contenido de una vez
with open("ejemplo.txt", "r", encoding="utf-8") as f:
    contenido = f.read()
    print("=== Contenido completo ===")
    print(contenido)

# Leer línea por línea (eficiente para archivos grandes)
with open("ejemplo.txt", "r", encoding="utf-8") as f:
    print("=== Línea por línea ===")
    for linea in f:
        print(f"  |{linea}", end="")  # linea ya incluye \n
    print()

# Leer todas las líneas en una lista
with open("ejemplo.txt", "r", encoding="utf-8") as f:
    lineas = f.readlines()
    print(f"Total de líneas: {len(lineas)}")
    print(f"Primera línea: {lineas[0].strip()}")

# ─────────────────────────────────────────────────────────────
# 2. Escribir archivos
# ─────────────────────────────────────────────────────────────

# "w" — escribir (sobreescribe si existe)
with open("nuevo.txt", "w", encoding="utf-8") as f:
    f.write("Primera línea\n")
    f.write("Segunda línea\n")

# "a" — append (agrega al final, no sobreescribe)
with open("nuevo.txt", "a", encoding="utf-8") as f:
    f.write("Esta línea se agrega al final\n")

# Escribir múltiples líneas
lineas = ["Python\n", "es\n", "genial\n"]
with open("nuevo.txt", "a") as f:
    f.writelines(lineas)

# ─────────────────────────────────────────────────────────────
# 3. El bloque with — por qué es importante
# ─────────────────────────────────────────────────────────────

# with garantiza que el archivo se cierra aunque haya un error.
# Es siempre la forma correcta de trabajar con archivos.

# ❌ Sin with — podría quedar abierto si hay un error
# f = open("archivo.txt", "r")
# contenido = f.read()
# f.close()    # podría no ejecutarse si hay un error antes

# ✓ Con with — siempre se cierra
# with open("archivo.txt", "r") as f:
#     contenido = f.read()
# El archivo se cierra automáticamente al salir del with

# ─────────────────────────────────────────────────────────────
# 4. JSON — guardar datos estructurados
# ─────────────────────────────────────────────────────────────

# JSON es el formato más usado para guardar y transmitir datos
# Es como un diccionario de Python, pero universal

# Python → JSON (serializar)
usuario = {
    "nombre": "Ana García",
    "edad":   25,
    "activo": True,
    "hobbies": ["leer", "programar", "cocinar"],
    "direccion": {
        "ciudad": "Buenos Aires",
        "pais":   "Argentina"
    }
}

# Guardar en archivo JSON
with open("usuario.json", "w", encoding="utf-8") as f:
    json.dump(usuario, f, indent=2, ensure_ascii=False)

print("Archivo JSON guardado")

# JSON → Python (deserializar)
with open("usuario.json", "r", encoding="utf-8") as f:
    usuario_cargado = json.load(f)

print(f"Cargado: {usuario_cargado['nombre']}")
print(f"Ciudad: {usuario_cargado['direccion']['ciudad']}")
print(f"Hobbies: {', '.join(usuario_cargado['hobbies'])}")

# Convertir a string JSON
json_string = json.dumps(usuario, indent=2, ensure_ascii=False)
print("\nJSON como string:")
print(json_string[:100] + "...")

# String JSON a Python
datos_recuperados = json.loads(json_string)
print(f"Nombre: {datos_recuperados['nombre']}")

# ─────────────────────────────────────────────────────────────
# 5. Verificar si un archivo existe
# ─────────────────────────────────────────────────────────────

archivo = "usuario.json"

if os.path.exists(archivo):
    print(f"\n'{archivo}' existe")
    tamaño = os.path.getsize(archivo)
    print(f"Tamaño: {tamaño} bytes")
else:
    print(f"'{archivo}' no existe")

# ─────────────────────────────────────────────────────────────
# 6. CSV — datos en tabla
# ─────────────────────────────────────────────────────────────

# CSV = Comma Separated Values — como Excel pero en texto plano

# Escribir CSV
empleados = [
    ["Nombre", "Cargo", "Salario", "Ciudad"],  # encabezados
    ["Ana García", "Developer", 80000, "Buenos Aires"],
    ["Luis Pérez", "Designer", 70000, "Córdoba"],
    ["Sara López", "Manager", 95000, "Rosario"],
]

with open("empleados.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(empleados)

print("CSV guardado")

# Leer CSV
with open("empleados.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print("\nEmpleados:")
    for fila in reader:
        print(f"  {fila['Nombre']} — {fila['Cargo']} (${int(fila['Salario']):,})")

# ─────────────────────────────────────────────────────────────
# 7. Proyecto completo — sistema de notas con persistencia
# ─────────────────────────────────────────────────────────────

ARCHIVO_NOTAS = "notas.json"

def cargar_notas():
    """Carga las notas desde el archivo JSON."""
    if os.path.exists(ARCHIVO_NOTAS):
        with open(ARCHIVO_NOTAS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_notas(notas):
    """Guarda las notas en el archivo JSON."""
    with open(ARCHIVO_NOTAS, "w", encoding="utf-8") as f:
        json.dump(notas, f, indent=2, ensure_ascii=False)

def agregar_nota(titulo, contenido):
    notas = cargar_notas()
    id_nota = str(len(notas) + 1)
    notas[id_nota] = {
        "titulo":    titulo,
        "contenido": contenido,
        "fecha":     datetime.now().strftime("%Y-%m-%d %H:%M"),
        "editada":   False
    }
    guardar_notas(notas)
    print(f"✓ Nota #{id_nota} guardada: '{titulo}'")
    return id_nota

def editar_nota(id_nota, nuevo_contenido):
    notas = cargar_notas()
    if id_nota not in notas:
        print(f"✗ Nota #{id_nota} no encontrada")
        return False
    notas[id_nota]["contenido"] = nuevo_contenido
    notas[id_nota]["editada"]   = True
    notas[id_nota]["ultima_edicion"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    guardar_notas(notas)
    print(f"✓ Nota #{id_nota} actualizada")
    return True

def listar_notas():
    notas = cargar_notas()
    if not notas:
        print("No hay notas guardadas")
        return
    print(f"\n{'ID':>3} {'Título':<25} {'Fecha':<17} {'Estado'}")
    print("-" * 60)
    for id_n, nota in notas.items():
        estado = "✏️ editada" if nota.get("editada") else "nueva"
        print(f"{id_n:>3} {nota['titulo']:<25} {nota['fecha']:<17} {estado}")

def ver_nota(id_nota):
    notas = cargar_notas()
    if id_nota not in notas:
        print(f"Nota #{id_nota} no encontrada")
        return
    nota = notas[id_nota]
    print(f"\n{'='*40}")
    print(f"#{id_nota}: {nota['titulo']}")
    print(f"Creada: {nota['fecha']}")
    if nota.get("editada"):
        print(f"Editada: {nota.get('ultima_edicion', 'desconocido')}")
    print(f"{'='*40}")
    print(nota["contenido"])

def eliminar_nota(id_nota):
    notas = cargar_notas()
    if id_nota not in notas:
        print(f"✗ Nota #{id_nota} no encontrada")
        return False
    titulo = notas[id_nota]["titulo"]
    del notas[id_nota]
    guardar_notas(notas)
    print(f"✓ Nota '{titulo}' eliminada")
    return True

# Demo del sistema
print("\n=== SISTEMA DE NOTAS ===")
agregar_nota("Aprender Python",  "Estudiar módulos 1 al 15 de CodeTutor")
agregar_nota("Lista del super",  "Leche, pan, huevos, frutas, pasta")
agregar_nota("Ideas proyecto",   "App de gestión de gastos personales")
editar_nota("2", "Leche, pan, huevos, frutas, pasta, aceite")
listar_notas()
ver_nota("1")

# Limpiar archivos de ejemplo
for archivo in ["ejemplo.txt", "nuevo.txt", "usuario.json", "empleados.csv", "notas.json"]:
    if os.path.exists(archivo):
        os.remove(archivo)

# =============================================================
# EJERCICIOS
# =============================================================
# 1. Agenda de contactos con persistencia:
#    Guardá y cargá contactos en JSON.
#    Funciones: agregar, buscar, listar, eliminar.
#    Los datos deben persistir entre ejecuciones.
#
# 2. Analizador de texto:
#    Pedí un archivo .txt por input.
#    Mostrá: total de palabras, total de líneas,
#    las 10 palabras más frecuentes, promedio de palabras por línea.
#
# 3. Log de errores:
#    Creá un decorador "log_errores" que, si una función lanza
#    una excepción, la guarde en "errores.log" con fecha/hora
#    y el mensaje del error.
#
# 4. Conversor CSV→JSON:
#    Leé un archivo CSV y guardalo como JSON.
#    Cada fila del CSV debe ser un diccionario.
# =============================================================

print("\n✓ Módulo 08 completado")
