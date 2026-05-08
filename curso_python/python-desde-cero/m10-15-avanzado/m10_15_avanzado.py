# =============================================================
# MÓDULOS 10-15 — Temas avanzados: errores, módulos,
# algoritmos, estructuras, web y datos
# =============================================================

# ─────────────────────────────────────────────────────────────
# MÓDULO 10 — Manejo de errores profesional
# ─────────────────────────────────────────────────────────────

print("=" * 50)
print("MÓDULO 10 — Manejo de errores")
print("=" * 50)

# Jerarquía de excepciones:
# BaseException
#   └── Exception
#         ├── ValueError     — valor incorrecto
#         ├── TypeError      — tipo incorrecto
#         ├── KeyError       — clave no existe en dict
#         ├── IndexError     — índice fuera de rango
#         ├── AttributeError — atributo no existe
#         ├── FileNotFoundError — archivo no existe
#         ├── ZeroDivisionError — dividir por cero
#         └── ...

# Capturar múltiples tipos
def dividir_seguro(a, b):
    try:
        resultado = a / b
        return resultado
    except ZeroDivisionError:
        print("Error: no se puede dividir por cero")
        return None
    except TypeError:
        print(f"Error: tipos inválidos ({type(a).__name__} / {type(b).__name__})")
        return None
    else:
        pass                # se ejecuta si NO hubo excepción
    finally:
        pass                # se ejecuta SIEMPRE (limpiar recursos)

print(dividir_seguro(10, 2))    # 5.0
print(dividir_seguro(10, 0))    # None
print(dividir_seguro("5", 2))   # None

# Excepciones propias — para errores específicos de tu dominio
class ValidacionError(Exception):
    """Error de validación de datos de usuario."""
    def __init__(self, campo, mensaje):
        self.campo   = campo
        self.mensaje = mensaje
        super().__init__(f"[{campo}] {mensaje}")

class EdadInvalidaError(ValidacionError):
    pass

class EmailInvalidoError(ValidacionError):
    pass

def crear_usuario(nombre, edad, email):
    if not nombre or len(nombre) < 2:
        raise ValidacionError("nombre", "Debe tener al menos 2 caracteres")
    if not isinstance(edad, int) or edad < 0 or edad > 150:
        raise EdadInvalidaError("edad", f"Edad inválida: {edad}")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise EmailInvalidoError("email", f"Email inválido: {email}")
    return {"nombre": nombre, "edad": edad, "email": email}

# Capturar excepciones propias
casos = [
    ("Ana", 25, "ana@test.com"),
    ("", 25, "ana@test.com"),
    ("Luis", -5, "luis@test.com"),
    ("Sara", 30, "sara-sin-arroba"),
]

for nombre, edad, email in casos:
    try:
        u = crear_usuario(nombre, edad, email)
        print(f"✓ Usuario creado: {u['nombre']}")
    except ValidacionError as e:
        print(f"✗ Error en campo '{e.campo}': {e.mensaje}")

# Context manager propio — protocolo with
class ConexionSimulada:
    def __init__(self, host):
        self.host = host

    def __enter__(self):
        print(f"  Conectando a {self.host}...")
        return self

    def consultar(self, query):
        return f"Resultado de: {query}"

    def __exit__(self, tipo_exc, valor_exc, traceback):
        print(f"  Desconectando de {self.host}")
        # Si retorna True, suprime la excepción
        return False

with ConexionSimulada("db.localhost:5432") as conn:
    resultado = conn.consultar("SELECT * FROM users")
    print(f"  {resultado}")

# ─────────────────────────────────────────────────────────────
# MÓDULO 11 — Módulos y el ecosistema Python
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("MÓDULO 11 — Módulos y librerías")
print("=" * 50)

# Módulos de la librería estándar (ya vienen con Python)
import math
import random
import datetime
import collections
import itertools
import functools
import re
import os
import sys

# math — operaciones matemáticas
print(f"π = {math.pi:.4f}")
print(f"e = {math.e:.4f}")
print(f"sqrt(144) = {math.sqrt(144)}")
print(f"ceil(3.2) = {math.ceil(3.2)}")    # redondear hacia arriba
print(f"floor(3.8) = {math.floor(3.8)}")  # redondear hacia abajo
print(f"sin(π/2) = {math.sin(math.pi/2):.1f}")

# random — números aleatorios
print(f"\nrandom: {random.random():.4f}")         # float entre 0 y 1
print(f"randint: {random.randint(1, 100)}")       # entero entre 1 y 100
lista = [1, 2, 3, 4, 5]
print(f"choice: {random.choice(lista)}")          # elemento aleatorio
random.shuffle(lista)
print(f"shuffle: {lista}")
print(f"sample: {random.sample(range(100), 5)}")  # 5 sin repetir

# datetime — fechas y horas
ahora = datetime.datetime.now()
print(f"\nAhora: {ahora.strftime('%d/%m/%Y %H:%M:%S')}")
print(f"Año: {ahora.year}, Mes: {ahora.month}, Día: {ahora.day}")

mañana = ahora + datetime.timedelta(days=1)
print(f"Mañana: {mañana.strftime('%d/%m/%Y')}")

fecha1 = datetime.date(2024, 1, 1)
fecha2 = datetime.date(2024, 12, 31)
diferencia = fecha2 - fecha1
print(f"Días en 2024: {diferencia.days}")

# collections — estructuras especiales
from collections import Counter, defaultdict, deque, OrderedDict, namedtuple

# Counter — contar elementos
votos = ["Ana", "Luis", "Ana", "Sara", "Ana", "Luis", "Ana"]
conteo = Counter(votos)
print(f"\nVotos: {dict(conteo)}")
print(f"Ganador: {conteo.most_common(1)[0][0]}")

# namedtuple — tuple con nombres
Punto = namedtuple("Punto", ["x", "y"])
p = Punto(3, 4)
print(f"Punto: {p}, x={p.x}, y={p.y}")
print(f"Magnitud: {(p.x**2 + p.y**2)**0.5}")

# deque — cola eficiente (O(1) en ambos extremos)
cola = deque(maxlen=5)     # máximo 5 elementos
for i in range(8):
    cola.append(i)
print(f"Deque (maxlen=5): {cola}")  # solo los últimos 5

# itertools — herramientas para iterar
from itertools import chain, combinations, permutations, product

letras = ["a", "b", "c"]
print(f"Combinaciones de 2: {list(combinations(letras, 2))}")
print(f"Permutaciones de 2: {list(permutations(letras, 2))}")
print(f"Producto cartesiano: {list(product([0,1], repeat=3))}")

# functools — herramientas para funciones
from functools import reduce, lru_cache, partial

# lru_cache — memoización automática
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"Fibonacci(30) = {fibonacci(30)}")

# partial — función con argumentos pre-fijados
def potencia(base, exponente):
    return base ** exponente

cuadrado = partial(potencia, exponente=2)
cubo     = partial(potencia, exponente=3)
print(f"cuadrado(5) = {cuadrado(5)}")
print(f"cubo(3) = {cubo(3)}")

# re — expresiones regulares
import re
texto = "Mi email es usuario@ejemplo.com y también uso otro@mail.org"
emails = re.findall(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', texto)
print(f"\nEmails encontrados: {emails}")

# ─────────────────────────────────────────────────────────────
# MÓDULO 12 — Algoritmos: resolver problemas eficientemente
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("MÓDULO 12 — Algoritmos")
print("=" * 50)

# ── Búsqueda binaria ─────────────────────────────────────────
def busqueda_binaria(arr, target):
    """O(log n) — requiere array ordenado"""
    izq, der = 0, len(arr) - 1
    pasos = 0
    while izq <= der:
        pasos += 1
        mid = (izq + der) // 2
        if arr[mid] == target:
            return mid, pasos
        elif arr[mid] < target:
            izq = mid + 1
        else:
            der = mid - 1
    return -1, pasos

arr = list(range(0, 1000, 2))   # [0, 2, 4, ..., 998]
idx, pasos = busqueda_binaria(arr, 642)
print(f"Búsqueda binaria: encontrado en índice {idx}, {pasos} pasos (de {len(arr)} elementos)")

# ── Two pointers ─────────────────────────────────────────────
def dos_suma_sorted(arr, target):
    """Encontrar dos números que sumen target en array ordenado — O(n)"""
    izq, der = 0, len(arr) - 1
    while izq < der:
        suma = arr[izq] + arr[der]
        if suma == target:
            return izq, der, arr[izq], arr[der]
        elif suma < target:
            izq += 1
        else:
            der -= 1
    return None

resultado = dos_suma_sorted([1, 3, 5, 7, 9, 11, 13], 16)
if resultado:
    i, j, a, b = resultado
    print(f"Dos suma: {a} + {b} = 16 (índices {i} y {j})")

# ── Sliding window ───────────────────────────────────────────
def max_suma_subarray(arr, k):
    """Suma máxima de k elementos consecutivos — O(n)"""
    if len(arr) < k:
        return None
    suma_actual = sum(arr[:k])
    max_suma = suma_actual
    inicio_max = 0

    for i in range(k, len(arr)):
        suma_actual += arr[i] - arr[i - k]
        if suma_actual > max_suma:
            max_suma = suma_actual
            inicio_max = i - k + 1

    return max_suma, arr[inicio_max:inicio_max + k]

arr = [2, 1, 5, 1, 3, 2, 6, 4, 1, 3]
suma, subarray = max_suma_subarray(arr, 3)
print(f"Suma máxima de 3 consecutivos: {suma} → {subarray}")

# ── Dynamic Programming ──────────────────────────────────────
def mochila(pesos, valores, capacidad):
    """
    Problema de la mochila — DP clásico.
    ¿Qué objetos llevar para maximizar el valor sin superar la capacidad?
    O(n * capacidad)
    """
    n = len(pesos)
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacidad + 1):
            # No llevar el objeto i
            dp[i][w] = dp[i-1][w]
            # Llevar el objeto i (si entra)
            if pesos[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - pesos[i-1]] + valores[i-1])

    return dp[n][capacidad]

pesos   = [2, 3, 4, 5]
valores = [3, 4, 5, 6]
capacidad = 8
resultado = mochila(pesos, valores, capacidad)
print(f"Mochila (cap={capacidad}): valor máximo = {resultado}")

# ── Merge Sort — divide y conquista ──────────────────────────
def merge_sort(arr):
    """O(n log n) — más eficiente que bubble sort"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    izq = merge_sort(arr[:mid])
    der = merge_sort(arr[mid:])

    return merge(izq, der)

def merge(izq, der):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

desordenado = [38, 27, 43, 3, 9, 82, 10]
ordenado    = merge_sort(desordenado)
print(f"Merge sort: {desordenado} → {ordenado}")

# ─────────────────────────────────────────────────────────────
# MÓDULO 13 — Estructuras de datos implementadas
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("MÓDULO 13 — Estructuras de datos")
print("=" * 50)

# ── Stack con clase ──────────────────────────────────────────
class Stack:
    def __init__(self):
        self._data = []

    def push(self, item): self._data.append(item)
    def pop(self):
        if self.is_empty(): raise IndexError("Stack vacío")
        return self._data.pop()
    def peek(self):
        if self.is_empty(): raise IndexError("Stack vacío")
        return self._data[-1]
    def is_empty(self): return len(self._data) == 0
    def size(self): return len(self._data)
    def __repr__(self): return f"Stack({self._data})"

# Uso real: evaluar expresiones con paréntesis
def parentesis_balanceados(texto):
    pila = Stack()
    pares = {")": "(", "]": "[", "}": "{"}
    for c in texto:
        if c in "([{":
            pila.push(c)
        elif c in ")]}":
            if pila.is_empty() or pila.peek() != pares[c]:
                return False
            pila.pop()
    return pila.is_empty()

casos = ["(())", "({[]})", "((())", "([)]", ""]
for c in casos:
    resultado = parentesis_balanceados(c)
    print(f"  '{c}': {'✓' if resultado else '✗'}")

# ── Queue con deque ──────────────────────────────────────────
from collections import deque as Deque

class Queue:
    def __init__(self, maxsize=None):
        self._data = Deque()
        self._maxsize = maxsize

    def enqueue(self, item):
        if self._maxsize and len(self._data) >= self._maxsize:
            raise OverflowError("Queue llena")
        self._data.append(item)

    def dequeue(self):
        if self.is_empty(): raise IndexError("Queue vacía")
        return self._data.popleft()

    def front(self): return self._data[0]
    def is_empty(self): return len(self._data) == 0
    def size(self): return len(self._data)
    def __repr__(self): return f"Queue({list(self._data)})"

# Uso real: BFS (explorar árbol nivel por nivel)
def bfs(grafo, inicio):
    """Explorar todos los nodos de un grafo en orden de distancia."""
    visitados = set()
    cola = Queue()
    cola.enqueue((inicio, 0))
    visitados.add(inicio)
    orden = []

    while not cola.is_empty():
        nodo, nivel = cola.dequeue()
        orden.append((nodo, nivel))
        for vecino in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.enqueue((vecino, nivel + 1))

    return orden

grafo = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [], "E": [], "F": []
}

recorrido = bfs(grafo, "A")
print(f"\nBFS desde A:")
for nodo, nivel in recorrido:
    print(f"  {'  ' * nivel}{nodo} (nivel {nivel})")

# ── Linked List simple ───────────────────────────────────────
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self._tamaño = 0

    def agregar_al_final(self, dato):
        nuevo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._tamaño += 1

    def agregar_al_inicio(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self._tamaño += 1

    def eliminar(self, dato):
        if not self.cabeza: return False
        if self.cabeza.dato == dato:
            self.cabeza = self.cabeza.siguiente
            self._tamaño -= 1
            return True
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self._tamaño -= 1
                return True
            actual = actual.siguiente
        return False

    def invertir(self):
        anterior = None
        actual   = self.cabeza
        while actual:
            siguiente    = actual.siguiente
            actual.siguiente = anterior
            anterior     = actual
            actual       = siguiente
        self.cabeza = anterior

    def a_lista(self):
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def __repr__(self):
        return " → ".join(str(x) for x in self.a_lista()) + " → None"

ll = ListaEnlazada()
for v in [1, 2, 3, 4, 5]:
    ll.agregar_al_final(v)

print(f"\nLista: {ll}")
ll.agregar_al_inicio(0)
print(f"Con 0 al inicio: {ll}")
ll.eliminar(3)
print(f"Sin el 3: {ll}")
ll.invertir()
print(f"Invertida: {ll}")

# ─────────────────────────────────────────────────────────────
# MÓDULO 14 — Web: hacer requests a APIs reales
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("MÓDULO 14 — Web y APIs")
print("=" * 50)

# Para instalar: pip install requests
# import requests

# Ejemplo de cómo se usa (descomentá si tenés conexión):
# def obtener_chiste():
#     url = "https://official-joke-api.appspot.com/random_joke"
#     respuesta = requests.get(url)
#
#     if respuesta.status_code == 200:
#         datos = respuesta.json()
#         return f"{datos['setup']}\n→ {datos['punchline']}"
#     else:
#         return f"Error {respuesta.status_code}"
#
# print(obtener_chiste())
#
# # POST request
# def crear_post(titulo, cuerpo, usuario_id):
#     url = "https://jsonplaceholder.typicode.com/posts"
#     datos = {"title": titulo, "body": cuerpo, "userId": usuario_id}
#     respuesta = requests.post(url, json=datos)
#     return respuesta.json()
#
# nuevo_post = crear_post("Mi primer post", "Hola mundo desde Python", 1)
# print(nuevo_post)

# Simular una respuesta de API para el ejemplo
import json

respuesta_simulada = """{
    "id": 1,
    "title": "Python es genial",
    "body": "Aprendiendo a hacer APIs con Python",
    "userId": 1
}"""

datos = json.loads(respuesta_simulada)
print(f"Post simulado: {datos['title']}")
print(f"Autor ID: {datos['userId']}")

# ─────────────────────────────────────────────────────────────
# MÓDULO 15 — Trabajar con datos
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("MÓDULO 15 — Análisis de datos con Python puro")
print("=" * 50)

# Sin pandas — entender los fundamentos
ventas = [
    {"mes": "Enero",      "ventas": 45000, "gastos": 30000, "region": "Norte"},
    {"mes": "Febrero",    "ventas": 52000, "gastos": 33000, "region": "Norte"},
    {"mes": "Marzo",      "ventas": 48000, "gastos": 31000, "region": "Sur"},
    {"mes": "Abril",      "ventas": 61000, "gastos": 35000, "region": "Norte"},
    {"mes": "Mayo",       "ventas": 55000, "gastos": 34000, "region": "Sur"},
    {"mes": "Junio",      "ventas": 70000, "gastos": 40000, "region": "Norte"},
    {"mes": "Julio",      "ventas": 65000, "gastos": 38000, "region": "Sur"},
    {"mes": "Agosto",     "ventas": 72000, "gastos": 41000, "region": "Norte"},
    {"mes": "Septiembre", "ventas": 68000, "gastos": 39000, "region": "Sur"},
    {"mes": "Octubre",    "ventas": 75000, "gastos": 42000, "region": "Norte"},
    {"mes": "Noviembre",  "ventas": 90000, "gastos": 50000, "region": "Norte"},
    {"mes": "Diciembre",  "ventas": 110000,"gastos": 55000, "region": "Sur"},
]

# Métricas básicas
total_ventas  = sum(v["ventas"] for v in ventas)
total_gastos  = sum(v["gastos"] for v in ventas)
ganancia_neta = total_ventas - total_gastos
mejor_mes     = max(ventas, key=lambda v: v["ventas"])
peor_mes      = min(ventas, key=lambda v: v["ventas"])

print(f"Total ventas:  ${total_ventas:>12,.0f}")
print(f"Total gastos:  ${total_gastos:>12,.0f}")
print(f"Ganancia neta: ${ganancia_neta:>12,.0f}")
print(f"Margen:        {ganancia_neta/total_ventas:.1%}")
print(f"Mejor mes:     {mejor_mes['mes']} (${mejor_mes['ventas']:,.0f})")
print(f"Peor mes:      {peor_mes['mes']} (${peor_mes['ventas']:,.0f})")

# Agrupar por región
from collections import defaultdict
por_region = defaultdict(list)
for v in ventas:
    por_region[v["region"]].append(v)

print("\nPor región:")
for region, datos_region in sorted(por_region.items()):
    total = sum(d["ventas"] for d in datos_region)
    meses = len(datos_region)
    promedio = total / meses
    print(f"  {region}: ${total:,.0f} total, ${promedio:,.0f} promedio/mes ({meses} meses)")

# Gráfico ASCII simple
print("\nVentas mensuales (barras ASCII):")
max_ventas = max(v["ventas"] for v in ventas)
for v in ventas:
    barra = "█" * int(v["ventas"] / max_ventas * 30)
    print(f"  {v['mes'][:3]:>3} | {barra:<30} ${v['ventas']:>7,.0f}")

# Crecimiento mensual
print("\nCrecimiento mensual:")
for i in range(1, len(ventas)):
    anterior = ventas[i-1]["ventas"]
    actual   = ventas[i]["ventas"]
    cambio   = (actual - anterior) / anterior
    flecha   = "↑" if cambio > 0 else "↓"
    print(f"  {ventas[i]['mes'][:3]}: {flecha} {abs(cambio):.1%}")

# =============================================================
# EJERCICIOS FINALES — proyectos de integración
# =============================================================
print("\n" + "=" * 50)
print("PROYECTOS SUGERIDOS")
print("=" * 50)

proyectos = [
    ("🎮 Juego de ahorcado",
     "Palabras en un archivo JSON, intentos limitados, mostrar progreso"),
    ("📊 Analizador de gastos",
     "Agregar gastos por categoría, ver totales, gráficos ASCII, guardar en JSON"),
    ("🎯 Quiz interactivo",
     "Preguntas con opciones múltiples, puntaje, cargar preguntas de archivo"),
    ("🌡️ Conversor universal",
     "Temperatura, distancia, peso, moneda. Menú interactivo."),
    ("📝 Gestor de tareas",
     "CRUD completo, prioridades, fechas, filtrar por estado, persistencia JSON"),
    ("🔐 Gestor de contraseñas",
     "Guardar, buscar y generar contraseñas seguras. Cifrado básico."),
    ("📈 Simulador de inversiones",
     "Calcular rendimiento, interés compuesto, comparar escenarios"),
    ("🌐 Scraper básico",
     "Usar requests + json para consumir una API pública real"),
]

for i, (nombre, descripcion) in enumerate(proyectos, 1):
    print(f"\n{i}. {nombre}")
    print(f"   {descripcion}")

print("\n✓ Curso completo. ¡A programar!")
