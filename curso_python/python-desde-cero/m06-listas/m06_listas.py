# =============================================================
# MÓDULO 06 — Listas: colecciones ordenadas
# =============================================================
# Las listas son el tipo de dato más usado en Python.
# Guardan múltiples valores en un orden específico.
# =============================================================

# ─────────────────────────────────────────────────────────────
# 1. Crear listas
# ─────────────────────────────────────────────────────────────

# Lista vacía
vacia = []

# Lista de números
numeros = [1, 2, 3, 4, 5]

# Lista de strings
frutas = ["manzana", "banana", "naranja"]

# Lista mixta (puede tener cualquier tipo)
mezclada = [1, "hola", True, 3.14, None]

# Lista de listas (matriz)
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

print(numeros)
print(frutas)
print(f"Longitud: {len(frutas)}")

# ─────────────────────────────────────────────────────────────
# 2. Acceder a elementos
# ─────────────────────────────────────────────────────────────

frutas = ["manzana", "banana", "naranja", "uva", "kiwi"]
#           0           1         2         3      4
#          -5          -4        -3        -2     -1

print(frutas[0])    # manzana  (primero)
print(frutas[2])    # naranja
print(frutas[-1])   # kiwi     (último)
print(frutas[-2])   # uva      (penúltimo)

# Slicing — extraer partes
print(frutas[1:3])   # ['banana', 'naranja']
print(frutas[:2])    # ['manzana', 'banana']
print(frutas[2:])    # ['naranja', 'uva', 'kiwi']
print(frutas[::2])   # ['manzana', 'naranja', 'kiwi'] (de a 2)
print(frutas[::-1])  # invertida

# Matriz
print(matriz[0])        # [1, 2, 3]
print(matriz[1][2])     # 6 (fila 1, columna 2)

# ─────────────────────────────────────────────────────────────
# 3. Modificar listas
# ─────────────────────────────────────────────────────────────

frutas = ["manzana", "banana", "naranja"]

# Cambiar un elemento
frutas[1] = "frutilla"
print(frutas)    # ['manzana', 'frutilla', 'naranja']

# Agregar elementos
frutas.append("uva")              # agrega al FINAL
print(frutas)

frutas.insert(1, "kiwi")          # inserta en posición 1
print(frutas)

frutas.extend(["mango", "pera"])  # agrega una lista al final
print(frutas)

# Eliminar elementos
frutas.remove("kiwi")    # elimina por valor (primera ocurrencia)
print(frutas)

ultimo = frutas.pop()    # elimina y retorna el último
print(f"Saqué: {ultimo}")
print(frutas)

segundo = frutas.pop(1)  # elimina y retorna el de posición 1
print(f"Saqué: {segundo}")
print(frutas)

del frutas[0]            # elimina por índice (no retorna)
print(frutas)

# ─────────────────────────────────────────────────────────────
# 4. Buscar en listas
# ─────────────────────────────────────────────────────────────

numeros = [5, 3, 8, 1, 9, 3, 7, 3]

print(3 in numeros)          # True
print(100 in numeros)        # False
print(numeros.index(9))      # 4 (posición del 9)
print(numeros.count(3))      # 3 (cuántas veces aparece el 3)

# ─────────────────────────────────────────────────────────────
# 5. Ordenar listas
# ─────────────────────────────────────────────────────────────

numeros = [5, 3, 8, 1, 9, 2, 7]

# sort() — modifica la lista original
numeros.sort()
print(numeros)    # [1, 2, 3, 5, 7, 8, 9]

numeros.sort(reverse=True)
print(numeros)    # [9, 8, 7, 5, 3, 2, 1]

# sorted() — retorna una nueva lista, no modifica la original
original = [5, 3, 8, 1, 9]
ordenada = sorted(original)
print(f"Original: {original}")   # no cambió
print(f"Ordenada: {ordenada}")

# Ordenar por criterio personalizado
personas = [
    {"nombre": "Luis", "edad": 30},
    {"nombre": "Ana",  "edad": 25},
    {"nombre": "Sara", "edad": 28},
]

por_edad   = sorted(personas, key=lambda p: p["edad"])
por_nombre = sorted(personas, key=lambda p: p["nombre"])

for p in por_edad:
    print(f"{p['nombre']}: {p['edad']}")

# ─────────────────────────────────────────────────────────────
# 6. Operaciones comunes
# ─────────────────────────────────────────────────────────────

numeros = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

print(sum(numeros))    # 39  — suma
print(min(numeros))    # 1   — mínimo
print(max(numeros))    # 9   — máximo
print(len(numeros))    # 10  — cantidad

# Promedio
promedio = sum(numeros) / len(numeros)
print(f"Promedio: {promedio:.1f}")

# Invertir
numeros.reverse()         # in-place
al_reves = numeros[::-1]  # nueva lista

# Copiar (¡importante!)
original = [1, 2, 3]
copia    = original.copy()    # copia real
copia.append(4)
print(f"Original: {original}")  # [1, 2, 3] — no cambió
print(f"Copia:    {copia}")     # [1, 2, 3, 4]

# Sin copy — son el MISMO objeto
referencia = original
referencia.append(99)
print(f"Original: {original}")  # [1, 2, 3, 99] — ¡cambió!

# Vaciar
original.clear()
print(original)   # []

# ─────────────────────────────────────────────────────────────
# 7. List comprehensions avanzadas
# ─────────────────────────────────────────────────────────────

# Aplanar una lista de listas
lista_de_listas = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
plana = [n for sublista in lista_de_listas for n in sublista]
print(plana)   # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Matriz de ceros
filas, cols = 3, 4
matriz = [[0 for _ in range(cols)] for _ in range(filas)]
print(matriz)  # [[0,0,0,0],[0,0,0,0],[0,0,0,0]]

# Filtrar y transformar
datos = ["  Ana  ", "LUIS", " sara ", "PEDRO  "]
limpios = [d.strip().title() for d in datos]
print(limpios)   # ['Ana', 'Luis', 'Sara', 'Pedro']

# ─────────────────────────────────────────────────────────────
# 8. Zip y enumerate — patrones comunes
# ─────────────────────────────────────────────────────────────

nombres = ["Ana", "Luis", "Sara"]
notas   = [85, 92, 78]
ciudades = ["Buenos Aires", "Córdoba", "Rosario"]

# Combinar con zip
for i, (nombre, nota, ciudad) in enumerate(zip(nombres, notas, ciudades), 1):
    estado = "✓" if nota >= 80 else "✗"
    print(f"{i}. {nombre} ({ciudad}): {nota} {estado}")

# ─────────────────────────────────────────────────────────────
# 9. Tuplas — listas inmutables
# ─────────────────────────────────────────────────────────────

# Una tupla es como una lista pero NO se puede modificar
# Se usa para datos que no deben cambiar

coordenadas = (40.7128, -74.0060)   # latitud, longitud de NYC
rgb_rojo    = (255, 0, 0)
dias_semana = ("lunes", "martes", "miércoles", "jueves",
               "viernes", "sábado", "domingo")

# Acceder igual que lista
print(coordenadas[0])    # 40.7128
print(dias_semana[-1])   # domingo

# NO podés modificar
# coordenadas[0] = 0    # TypeError: 'tuple' object does not support item assignment

# Desempaquetar (muy común)
x, y = coordenadas
print(f"Lat: {x}, Lon: {y}")

primer, *resto = dias_semana
print(f"Primer día: {primer}")
print(f"Resto: {resto}")

# Función que retorna tupla
def obtener_dimensiones(texto):
    lineas   = texto.count("\n") + 1
    max_ancho = max(len(l) for l in texto.split("\n"))
    return lineas, max_ancho

lineas, ancho = obtener_dimensiones("Hola\nMundo\nPython")
print(f"Líneas: {lineas}, Ancho máximo: {ancho}")

# ─────────────────────────────────────────────────────────────
# 10. Sets — colecciones sin duplicados
# ─────────────────────────────────────────────────────────────

# Un set guarda elementos únicos, sin orden garantizado

colores = {"rojo", "azul", "verde", "rojo", "azul"}
print(colores)    # {'rojo', 'azul', 'verde'} — sin duplicados

# Crear set desde lista (eliminar duplicados)
lista_con_dups = [1, 2, 2, 3, 3, 3, 4]
sin_duplicados = list(set(lista_con_dups))
print(sin_duplicados)   # [1, 2, 3, 4]

# Operaciones de conjuntos
estudiantes_python = {"Ana", "Luis", "Sara", "Pedro"}
estudiantes_java   = {"Luis", "Pedro", "Marta", "Carlos"}

# Unión — todos
print(estudiantes_python | estudiantes_java)

# Intersección — los que están en ambos
print(estudiantes_python & estudiantes_java)   # {Luis, Pedro}

# Diferencia — solo en python
print(estudiantes_python - estudiantes_java)   # {Ana, Sara}

# Diferencia simétrica — en uno pero no en ambos
print(estudiantes_python ^ estudiantes_java)

# ─────────────────────────────────────────────────────────────
# 11. Proyecto — sistema de inventario
# ─────────────────────────────────────────────────────────────

inventario = [
    {"nombre": "Notebook",    "precio": 150000, "stock": 5,  "categoria": "tecnología"},
    {"nombre": "Mouse",       "precio": 3500,   "stock": 20, "categoria": "tecnología"},
    {"nombre": "Auriculares", "precio": 8000,   "stock": 0,  "categoria": "tecnología"},
    {"nombre": "Remera",      "precio": 2500,   "stock": 15, "categoria": "ropa"},
    {"nombre": "Zapatillas",  "precio": 25000,  "stock": 8,  "categoria": "ropa"},
    {"nombre": "Libro Python","precio": 4500,   "stock": 3,  "categoria": "libros"},
]

# Filtrar disponibles
disponibles = [p for p in inventario if p["stock"] > 0]
print(f"Disponibles: {len(disponibles)} de {len(inventario)}")

# Agrupar por categoría
categorias = set(p["categoria"] for p in inventario)
for cat in sorted(categorias):
    productos_cat = [p for p in inventario if p["categoria"] == cat]
    print(f"\n{cat.upper()}:")
    for p in sorted(productos_cat, key=lambda x: x["precio"]):
        estado = f"Stock: {p['stock']}" if p["stock"] > 0 else "SIN STOCK"
        print(f"  {p['nombre']:20} ${p['precio']:>10,.0f}  {estado}")

# Estadísticas
precios = [p["precio"] for p in inventario]
print(f"\nPrecio promedio: ${sum(precios)/len(precios):,.0f}")
print(f"Más caro:        ${max(precios):,.0f}")
print(f"Más barato:      ${min(precios):,.0f}")

# Valor total del inventario
valor_total = sum(p["precio"] * p["stock"] for p in inventario)
print(f"Valor inventario:${valor_total:,.0f}")

# =============================================================
# EJERCICIOS
# =============================================================
# 1. Dada una lista de números, sin usar sorted() ni sort():
#    implementá bubble sort manualmente.
#
# 2. Función que recibe una lista de strings y retorna:
#    - Las palabras ordenadas por longitud
#    - La más larga y más corta
#    - Las que tienen más de 5 letras
#
# 3. Eliminá duplicados de una lista pero manteniendo el orden
#    (sin usar set directamente, solo como ayuda).
#
# 4. Dada una lista de números, separalos en dos listas:
#    positivos y negativos.
#
# 5. Sistema de votación:
#    Dada una lista de votos ["Ana","Luis","Ana","Sara","Ana","Luis"]
#    Contá cuántos votos tiene cada candidato y declarar ganador.
# =============================================================

print("\n✓ Módulo 06 completado")
