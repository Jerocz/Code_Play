# 🐍 Python desde cero — Curso completo

> Desde tu primer `print("Hola mundo")` hasta estructuras de datos,
> algoritmos y consumo de APIs. Todo en Python, todo con ejemplos reales.

---

## ▶️ Cómo correr cualquier archivo

```bash
# Desde la terminal, en la carpeta del módulo:
python m01_primeros_pasos.py

# Para ver todos los módulos:
ls
```

---

## 📚 Módulos del curso

| # | Módulo | Temas | Archivo |
|---|--------|-------|---------|
| 01 | Primeros pasos | Variables, tipos, print, input, operadores, f-strings | `m01-primeros-pasos/m01_primeros_pasos.py` |
| 02 | Strings | Métodos, slicing, índices, split, join, f-strings avanzados | `m02-datos/m02_strings.py` |
| 03 | Decisiones | if/elif/else, operadores lógicos, ternario, guard clauses | `m03-decisiones/m03_decisiones.py` |
| 04 | Loops | while, for, range, break, continue, enumerate, zip, comprehensions | `m04-loops/m04_loops.py` |
| 05 | Funciones | def, return, *args, **kwargs, lambda, recursión, decoradores | `m05-funciones/m05_funciones.py` |
| 06 | Listas | CRUD, slicing, sort, comprehensions, tuplas, sets | `m06-listas/m06_listas.py` |
| 07 | Diccionarios | CRUD, iteración, anidados, Counter, defaultdict, casos reales | `m07-diccionarios/m07_diccionarios.py` |
| 08 | Archivos | Leer/escribir texto, JSON, CSV, persistencia de datos | `m08-archivos/m08_archivos.py` |
| 09 | OOP | Clases, herencia, polimorfismo, @property, dunder methods | `m09-oop/m09_oop.py` |
| 10-15 | Avanzado | Errores, módulos, algoritmos, estructuras, web, datos | `m10-15-avanzado/m10_15_avanzado.py` |

---

## 🗺️ Camino de aprendizaje

```
SEMANA 1    → Módulos 01, 02, 03
             Ejercicio: Calculadora con menú interactivo

SEMANA 2    → Módulos 04, 05
             Ejercicio: Juego de adivinar el número

SEMANA 3    → Módulos 06, 07
             Ejercicio: Sistema de inventario

SEMANA 4    → Módulo 08
             Ejercicio: Agenda de contactos con persistencia

SEMANA 5-6  → Módulo 09
             Proyecto: Juego de rol básico

SEMANA 7+   → Módulos 10-15
             Proyectos: los de la lista al final del módulo 15
```

---

## 💡 Cómo usar estos archivos

Cada archivo tiene:

1. **Teoría explicada con comentarios** — lée antes de copiar
2. **Código ejecutable** — correlo y fijate el output
3. **Variaciones y casos reales** — no solo lo básico
4. **Ejercicios al final** — no los saltees

**El proceso para cada módulo:**
```
1. Leer el archivo de arriba a abajo sin ejecutar
2. Ejecutar: python nombre_modulo.py
3. Modificar el código — cambiar valores, sacar partes
4. Resolver los ejercicios del final SIN mirar el código del módulo
5. Recién cuando terminaste → siguiente módulo
```

---

## 🔥 Errores más comunes

```python
# 1. IndentationError — Python usa indentación para estructura
if True:
print("mal")    # IndentationError: falta indentación
if True:
    print("bien")   # ✓

# 2. NameError — usar variable antes de definirla
print(nombre)    # NameError: name 'nombre' is not defined
nombre = "Ana"
print(nombre)    # ✓

# 3. TypeError — operación entre tipos incompatibles
"5" + 3          # TypeError: can only concatenate str (not "int") to str
int("5") + 3     # ✓ → 8
"5" + str(3)     # ✓ → "53"

# 4. IndexError — índice fuera de rango
lista = [1, 2, 3]
lista[5]         # IndexError: list index out of range
lista[-1]        # ✓ → 3 (último elemento)

# 5. KeyError — clave que no existe en dict
d = {"a": 1}
d["b"]           # KeyError: 'b'
d.get("b", 0)    # ✓ → 0 (valor por defecto)
```

---

## 📖 Cómo leer un error (lo más importante)

Cuando algo falla, Python te dice exactamente qué pasó:

```
Traceback (most recent call last):       ← empezar a leer de abajo
  File "mi_script.py", line 15, in calcular   ← en qué función
    resultado = 100 / numero             ← la línea exacta
ZeroDivisionError: division by zero      ← el tipo y mensaje del error
```

**Siempre leé el error de abajo para arriba.** El nombre del error y el mensaje están abajo. El archivo y la línea también.

---

## ✅ Checklist de cada módulo

Antes de pasar al siguiente, asegurate de poder:

**M01:** Crear variables, imprimir, pedir input, hacer operaciones matemáticas
**M02:** Manipular strings con métodos, hacer slicing, usar f-strings
**M03:** Escribir condiciones complejas, usar elif, entender truthy/falsy
**M04:** Escribir loops while y for, usar enumerate y zip, hacer comprehensions
**M05:** Crear funciones con parámetros y return, usar *args y **kwargs
**M06:** Manipular listas, ordenarlas, hacer slicing, usar sets y tuplas
**M07:** Crear y manipular diccionarios, iterar con .items(), usar Counter
**M08:** Leer y escribir archivos, trabajar con JSON
**M09:** Crear clases con herencia, usar @property, implementar __str__
**M10-15:** Manejar errores, usar la librería estándar, implementar estructuras básicas

---

*Programar es un oficio. Se aprende haciendo, no leyendo.*
