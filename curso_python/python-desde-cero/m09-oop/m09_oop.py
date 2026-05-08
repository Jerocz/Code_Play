# =============================================================
# MÓDULO 09 — Clases y Objetos (OOP) desde cero
# =============================================================
# Hasta ahora usamos funciones para organizar código.
# Las clases nos dejan agrupar datos Y comportamiento juntos.
# =============================================================

# ─────────────────────────────────────────────────────────────
# 1. ¿Por qué clases? El problema que resuelven
# ─────────────────────────────────────────────────────────────

# Sin clases — representar una persona con dict y funciones separadas
def calcular_edad_en_anios(anio_nacimiento):
    return 2024 - anio_nacimiento

persona1 = {"nombre": "Ana", "anio_nac": 1999, "saldo": 1000}
persona2 = {"nombre": "Luis", "anio_nac": 1990, "saldo": 5000}

print(calcular_edad_en_anios(persona1["anio_nac"]))

# El problema: los datos y las funciones están separados.
# Cualquiera puede modificar el saldo directamente.
# No hay forma de garantizar que los datos sean válidos.

# Con clases — los datos y el comportamiento van juntos
class Persona:
    def __init__(self, nombre, anio_nac):
        self.nombre   = nombre
        self.anio_nac = anio_nac

    def calcular_edad(self):
        return 2024 - self.anio_nac

    def saludar(self):
        return f"Hola, soy {self.nombre} y tengo {self.calcular_edad()} años"

ana  = Persona("Ana", 1999)
luis = Persona("Luis", 1990)

print(ana.saludar())
print(luis.saludar())

# ─────────────────────────────────────────────────────────────
# 2. Anatomía de una clase
# ─────────────────────────────────────────────────────────────

class CuentaBancaria:
    # ── Atributo de clase (compartido por TODAS las instancias)
    tasa_interes = 0.03   # 3% anual

    # ── Constructor — se llama automáticamente al crear el objeto
    def __init__(self, titular, saldo_inicial=0):
        # Atributos de instancia — únicos para cada objeto
        self.titular = titular
        self._saldo  = saldo_inicial   # _ = convención "no tocar directamente"
        self._historial = []

    # ── Métodos de instancia — operan sobre self
    def depositar(self, monto):
        if monto <= 0:
            print("El monto debe ser positivo")
            return
        self._saldo += monto
        self._historial.append(f"+ ${monto:,.0f}")
        print(f"Depósito exitoso. Nuevo saldo: ${self._saldo:,.0f}")

    def retirar(self, monto):
        if monto <= 0:
            print("El monto debe ser positivo")
            return
        if monto > self._saldo:
            print(f"Saldo insuficiente. Tenés ${self._saldo:,.0f}")
            return
        self._saldo -= monto
        self._historial.append(f"- ${monto:,.0f}")
        print(f"Retiro exitoso. Nuevo saldo: ${self._saldo:,.0f}")

    def ver_saldo(self):
        return self._saldo

    def ver_historial(self):
        if not self._historial:
            print("Sin movimientos")
            return
        print(f"\nHistorial de {self.titular}:")
        for mov in self._historial:
            print(f"  {mov}")

    def aplicar_interes(self):
        interes = self._saldo * self.tasa_interes
        self._saldo += interes
        self._historial.append(f"+ ${interes:,.0f} (interés)")
        print(f"Interés aplicado: ${interes:,.0f}")

    # ── Representación string del objeto
    def __repr__(self):
        return f"CuentaBancaria('{self.titular}', ${self._saldo:,.0f})"

    def __str__(self):
        return f"Cuenta de {self.titular}: ${self._saldo:,.0f}"

# Crear objetos (instancias)
cuenta_ana  = CuentaBancaria("Ana García", 10000)
cuenta_luis = CuentaBancaria("Luis Pérez", 5000)

cuenta_ana.depositar(3000)
cuenta_ana.retirar(1500)
cuenta_ana.aplicar_interes()
cuenta_ana.ver_historial()

print(cuenta_ana)       # usa __str__
print(repr(cuenta_ana)) # usa __repr__

# Atributo de clase accesible desde la clase o la instancia
print(f"\nTasa de interés: {CuentaBancaria.tasa_interes:.0%}")
print(f"Tasa desde objeto: {cuenta_ana.tasa_interes:.0%}")

# ─────────────────────────────────────────────────────────────
# 3. Herencia — reutilizar y extender
# ─────────────────────────────────────────────────────────────

# La clase hijo hereda TODO de la clase padre y puede agregar más

class Animal:
    def __init__(self, nombre, energia=100):
        self.nombre  = nombre
        self.energia = energia

    def comer(self, alimento):
        self.energia += 10
        return f"{self.nombre} comió {alimento} (+10 energía)"

    def dormir(self):
        self.energia = min(100, self.energia + 30)
        return f"{self.nombre} durmió y recuperó energía"

    def estado(self):
        barra = "█" * (self.energia // 10)
        return f"{self.nombre}: [{barra:<10}] {self.energia}%"

    def __repr__(self):
        return f"{type(self).__name__}('{self.nombre}')"


class Perro(Animal):
    def __init__(self, nombre, raza):
        super().__init__(nombre)   # llamar al __init__ del padre
        self.raza = raza

    def ladrar(self):
        self.energia -= 5
        return f"{self.nombre}: ¡Guau! (-5 energía)"

    def fetch(self, objeto):
        self.energia -= 15
        return f"{self.nombre} trajo el {objeto} (-15 energía)"

    def __str__(self):
        return f"Perro {self.nombre} ({self.raza})"


class Gato(Animal):
    def __init__(self, nombre, es_indoor=True):
        super().__init__(nombre)
        self.es_indoor = es_indoor

    def maullar(self):
        return f"{self.nombre}: ¡Miau!"

    def ronronear(self):
        self.energia += 5
        return f"{self.nombre} ronronea feliz (+5 energía)"

    def __str__(self):
        tipo = "indoor" if self.es_indoor else "outdoor"
        return f"Gato {self.nombre} ({tipo})"


class Pajaro(Animal):
    def __init__(self, nombre, puede_volar=True):
        super().__init__(nombre)
        self.puede_volar = puede_volar

    def volar(self):
        if not self.puede_volar:
            return f"{self.nombre} no puede volar"
        self.energia -= 20
        return f"{self.nombre} está volando (-20 energía)"

    def piar(self):
        return f"{self.nombre}: ¡Pío pío!"


# Polimorfismo — mismo método, distintos comportamientos
rex    = Perro("Rex", "Labrador")
mimi   = Gato("Mimi")
tweety = Pajaro("Tweety")

print("\n=== ZOOLÓGICO ===")
print(rex)
print(mimi)
print(tweety)

animales = [rex, mimi, tweety]

print("\n--- Alimentando ---")
for animal in animales:
    print(animal.comer("comida balanceada"))

print("\n--- Estado ---")
for animal in animales:
    print(animal.estado())

# Verificar tipos
print(f"\nRex es Animal: {isinstance(rex, Animal)}")    # True
print(f"Rex es Perro:  {isinstance(rex, Perro)}")     # True
print(f"Rex es Gato:   {isinstance(rex, Gato)}")      # False

# ─────────────────────────────────────────────────────────────
# 4. @property — atributos inteligentes
# ─────────────────────────────────────────────────────────────

class Temperatura:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, valor):
        if valor < -273.15:
            raise ValueError("No existe temperatura menor al cero absoluto")
        self._celsius = valor

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @property
    def kelvin(self):
        return self._celsius + 273.15

    def __repr__(self):
        return f"{self._celsius}°C = {self.fahrenheit}°F = {self.kelvin}K"

t = Temperatura(100)
print(t)        # 100°C = 212.0°F = 373.15K

t.celsius = 0
print(t)        # 0°C = 32.0°F = 273.15K

# t.celsius = -300   # ValueError

# ─────────────────────────────────────────────────────────────
# 5. Métodos especiales (dunder methods)
# ─────────────────────────────────────────────────────────────

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, otro):          # v1 + v2
        return Vector2D(self.x + otro.x, self.y + otro.y)

    def __sub__(self, otro):          # v1 - v2
        return Vector2D(self.x - otro.x, self.y - otro.y)

    def __mul__(self, escalar):       # v * 3
        return Vector2D(self.x * escalar, self.y * escalar)

    def __eq__(self, otro):           # v1 == v2
        return self.x == otro.x and self.y == otro.y

    def __abs__(self):                # abs(v) — magnitud
        return (self.x**2 + self.y**2)**0.5

    def __len__(self):                # len(v)
        return 2

    def __iter__(self):               # for x in v
        yield self.x
        yield self.y

v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)

print(v1 + v2)     # (4, 6)
print(v1 - v2)     # (2, 2)
print(v1 * 3)      # (9, 12)
print(abs(v1))     # 5.0  (3-4-5 es un triángulo rectángulo)
print(v1 == v2)    # False

x, y = v1           # desempaquetar (usa __iter__)
print(f"x={x}, y={y}")

# ─────────────────────────────────────────────────────────────
# 6. Proyecto — juego de rol básico
# ─────────────────────────────────────────────────────────────

import random

class Personaje:
    def __init__(self, nombre, clase, hp, ataque, defensa):
        self.nombre  = nombre
        self.clase   = clase
        self.hp_max  = hp
        self.hp      = hp
        self.ataque  = ataque
        self.defensa = defensa
        self.nivel   = 1
        self.exp     = 0

    def esta_vivo(self):
        return self.hp > 0

    def recibir_danio(self, danio):
        danio_real = max(1, danio - self.defensa)
        self.hp = max(0, self.hp - danio_real)
        return danio_real

    def atacar(self, objetivo):
        danio_base = random.randint(self.ataque - 3, self.ataque + 3)
        critico    = random.random() < 0.2   # 20% de crítico
        if critico:
            danio_base *= 2
        danio_real = objetivo.recibir_danio(danio_base)
        return danio_real, critico

    def curar(self, cantidad):
        self.hp = min(self.hp_max, self.hp + cantidad)

    def ganar_exp(self, cantidad):
        self.exp += cantidad
        if self.exp >= self.nivel * 100:
            self.nivel += 1
            self.hp_max += 10
            self.hp = self.hp_max
            self.ataque += 2
            self.defensa += 1
            print(f"  🎉 {self.nombre} subió al nivel {self.nivel}!")

    def barra_hp(self):
        porcentaje = self.hp / self.hp_max
        lleno = int(porcentaje * 10)
        if porcentaje > 0.6:
            color = "█"
        elif porcentaje > 0.3:
            color = "▓"
        else:
            color = "░"
        return f"[{color * lleno}{'·' * (10 - lleno)}] {self.hp}/{self.hp_max}"

    def __repr__(self):
        return f"{self.nombre} ({self.clase}) — HP: {self.hp}/{self.hp_max}"


class Guerrero(Personaje):
    def __init__(self, nombre):
        super().__init__(nombre, "Guerrero", hp=120, ataque=15, defensa=8)

    def golpe_poderoso(self, objetivo):
        """Ataque especial — doble daño pero -10 HP propio"""
        self.hp -= 10
        danio = self.ataque * 2
        danio_real = objetivo.recibir_danio(danio)
        return danio_real


class Mago(Personaje):
    def __init__(self, nombre):
        super().__init__(nombre, "Mago", hp=80, ataque=25, defensa=3)
        self.mana = 100

    def bola_de_fuego(self, objetivo):
        """Ataque mágico — ignora defensa pero cuesta mana"""
        if self.mana < 20:
            print("  Sin mana suficiente")
            return 0
        self.mana -= 20
        danio = random.randint(30, 50)
        objetivo.hp = max(0, objetivo.hp - danio)
        return danio


class Enemigo(Personaje):
    def __init__(self, nombre, dificultad=1):
        hp     = 60 * dificultad
        ataque = 10 * dificultad
        defensa = 3 * dificultad
        super().__init__(nombre, "Enemigo", hp, ataque, defensa)
        self.exp_recompensa = 50 * dificultad


def simular_batalla(heroe, enemigo):
    print(f"\n⚔️  {heroe.nombre} vs {enemigo.nombre}")
    print("=" * 40)
    turno = 1

    while heroe.esta_vivo() and enemigo.esta_vivo():
        print(f"\n--- Turno {turno} ---")
        print(f"  {heroe.nombre}: {heroe.barra_hp()}")
        print(f"  {enemigo.nombre}: {enemigo.barra_hp()}")

        # Héroe ataca
        danio, critico = heroe.atacar(enemigo)
        crit_txt = " ¡CRÍTICO!" if critico else ""
        print(f"  {heroe.nombre} ataca por {danio} de daño{crit_txt}")

        if not enemigo.esta_vivo():
            break

        # Enemigo ataca
        danio, _ = enemigo.atacar(heroe)
        print(f"  {enemigo.nombre} ataca por {danio} de daño")

        turno += 1

    print("\n" + "=" * 40)
    if heroe.esta_vivo():
        print(f"🏆 {heroe.nombre} ganó la batalla!")
        heroe.ganar_exp(enemigo.exp_recompensa)
    else:
        print(f"💀 {heroe.nombre} fue derrotado...")

# Demo
heroe  = Guerrero("Thor")
goblin = Enemigo("Goblin Feroz", dificultad=1)
simular_batalla(heroe, goblin)
print(f"\nEstado final: {heroe}")

# =============================================================
# EJERCICIOS
# =============================================================
# 1. Clase Rectangulo con largo y ancho.
#    Métodos: area(), perimetro(), es_cuadrado(), escalar(factor).
#    Métodos especiales: __repr__, __eq__, __lt__ (comparar por área).
#
# 2. Clase Fraccion con numerador y denominador.
#    Métodos: simplificar(), __add__, __sub__, __mul__, __str__.
#    Ej: Fraccion(1,2) + Fraccion(1,3) = "5/6"
#
# 3. Sistema de empleados:
#    Clase base Empleado con nombre, salario base, años de trabajo.
#    Subclases: EmpleadoFull (+ beneficios), Contratista (tarifa/hora).
#    Método calcular_salario() distinto en cada subclase.
#
# 4. Continuá el juego de rol:
#    - Agregar clase Arquero (ataque a distancia)
#    - Sistema de inventario (lista de ítems que dan bonos)
#    - Curar entre batallas si el HP está bajo
# =============================================================

print("\n✓ Módulo 09 completado")
