# CodeTutor 🚀

Juego para aprender Python desde cero hasta casos reales.
25 módulos organizados en 9 bloques. Tutor IA con Gemini (gratis).

---

## Instalación

```
pip install -r requirements.txt
```

---

## Configurar la IA (Gemini — completamente gratis)

### Paso 1: Conseguir la API key
1. Entrá a: https://aistudio.google.com/apikey
2. Iniciá sesión con tu cuenta de Google
3. Hacé clic en "Create API key"
4. Copiá la key (empieza con "AIza...")

### Paso 2: Guardarla en Windows (una sola vez)
Abrí el CMD y escribí:
```
setx GEMINI_API_KEY "AIza...tu-key-aqui..."
```
Cerrá el CMD y volvé a abrirlo.

### Verificar que quedó guardada:
```
echo %GEMINI_API_KEY%
```
Si muestra tu key, está todo bien.

---

## Ejecutar

```
cd backend
uvicorn main:app --reload
```

Después abrí `frontend/index.html` en el navegador.

---

## Los 25 módulos

### 🧱 Fundamentos (6 módulos)
1. Hola Mundo — print()
2. Comentarios — el símbolo #
3. Variables — guardar datos
4. Tipos de datos — int, float, str, bool
5. Operadores matemáticos
6. Input del usuario

### 📝 Strings (2 módulos)
7. Strings en profundidad — métodos y slicing
8. f-strings avanzados — formato de números

### 🔀 Decisiones (2 módulos)
9. if / elif / else
10. Operadores lógicos — and, or, not

### 🔁 Loops (3 módulos)
11. Loop for
12. Loop while
13. List comprehensions

### 📦 Estructuras de datos (2 módulos)
14. Listas
15. Diccionarios

### ⚙️ Funciones (2 módulos)
16. Funciones básicas
17. Funciones avanzadas — *args, **kwargs, lambda

### 💾 Archivos y errores (2 módulos)
18. Archivos y JSON
19. Manejo de errores — try/except

### 🏗️ OOP (2 módulos)
20. Clases y objetos
21. Herencia y polimorfismo

### 🚀 Casos reales (4 módulos)
22. Gestor de tareas completo
23. Analizador de datos
24. API REST con FastAPI
25. Estructuras de datos — Stack, Queue, LRU Cache
