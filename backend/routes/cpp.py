from fastapi import APIRouter

router = APIRouter(prefix="/cpp", tags=["C++"])

modulos = [
    {
        "id": 1, "bloque": "Fundamentos", "titulo": "Hola Mundo",
        "descripcion": "Tu primer programa en C++ — cout y estructura básica",
        "xp": 20,
        "teoria": "Todo programa en C++ necesita #include para librerías, using namespace std para no escribir std:: todo el tiempo, int main() como punto de entrada, y return 0 al final. cout << muestra texto. endl o '\\n' hace salto de línea.",
        "ejemplo": '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hola mundo" << endl;\n    cout << "Esto es C++" << endl;\n    cout << 42 << endl;\n    cout << 3.14 << endl;\n    return 0;\n}',
        "ejercicio": "Escribí un programa que muestre en 3 líneas separadas: tu nombre, tu edad y tu ciudad favorita.",
        "pista": "Necesitás 3 cout <<. El texto va entre comillas dobles, los números van directo."
    },
    {
        "id": 2, "bloque": "Fundamentos", "titulo": "Variables y tipos",
        "descripcion": "int, double, string, bool — tipado estático",
        "xp": 30,
        "teoria": "C++ es de tipado estático — tenés que declarar el tipo de cada variable. int para enteros, double para decimales, string para texto (necesitás #include <string>), bool para true/false. Una vez declarado el tipo, no puede cambiar.",
        "ejemplo": '#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    int edad = 25;\n    double precio = 19.99;\n    string nombre = "Ana";\n    bool activo = true;\n    \n    cout << nombre << endl;\n    cout << "Tengo " << edad << " años" << endl;\n    cout << "Precio: $" << precio << endl;\n    return 0;\n}',
        "ejercicio": "Declará variables de cada tipo con tus datos. Mostrá una presentación completa usando cout con cada variable.",
        "pista": "Recordá incluir #include <string> para usar string. Concatenás con el operador <<."
    },
    {
        "id": 3, "bloque": "Fundamentos", "titulo": "Input con cin",
        "descripcion": "Pedirle datos al usuario con cin",
        "xp": 30,
        "teoria": "cin >> lee datos del usuario. El tipo de la variable determina qué acepta. Para strings con espacios usá getline(cin, variable). Siempre declará el tipo antes de usar cin.",
        "ejemplo": '#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string nombre;\n    int edad;\n    \n    cout << "¿Cómo te llamás? ";\n    getline(cin, nombre);\n    \n    cout << "¿Cuántos años tenés? ";\n    cin >> edad;\n    \n    cout << "Hola " << nombre << "!" << endl;\n    cout << "El año que viene tenés " << edad+1 << endl;\n    return 0;\n}',
        "ejercicio": "Pedí nombre y año de nacimiento al usuario. Calculá la edad (2024 - año) y mostrá: 'Hola [nombre], tenés [edad] años.'",
        "pista": "Usá getline para el nombre (puede tener espacios). Para el año usá int y cin >>."
    },
    {
        "id": 4, "bloque": "Decisiones", "titulo": "if / else",
        "descripcion": "Condiciones y decisiones en C++",
        "xp": 50,
        "teoria": "La sintaxis es igual a JavaScript: if (condición) { } else if { } else { }. Operadores: == != < > <= >=. Lógicos: && || !. A diferencia de Python, los bloques van entre llaves {}.",
        "ejemplo": '#include <iostream>\nusing namespace std;\n\nint main() {\n    int nota;\n    cout << "Ingresá tu nota: ";\n    cin >> nota;\n    \n    if (nota >= 90) {\n        cout << "Sobresaliente" << endl;\n    } else if (nota >= 60) {\n        cout << "Aprobado" << endl;\n    } else {\n        cout << "Desaprobado" << endl;\n    }\n    return 0;\n}',
        "ejercicio": "Pedí la temperatura. Mostrá qué ropa usar: <10° campera gruesa, 10-20° rompevientos, 20-30° remera, >30° lo menos posible.",
        "pista": "Usá double para la temperatura. El orden de los if/else if importa."
    },
    {
        "id": 5, "bloque": "Loops", "titulo": "Loops for y while",
        "descripcion": "Repetir con for, while y do-while",
        "xp": 60,
        "teoria": "for en C++: for(int i=0; i<n; i++). while igual que en otros lenguajes. do-while ejecuta al menos una vez. C++11 tiene range-based for: for(auto elemento : contenedor).",
        "ejemplo": '#include <iostream>\nusing namespace std;\n\nint main() {\n    // for clásico\n    for (int i = 1; i <= 5; i++) {\n        cout << i << " ";\n    }\n    cout << endl;\n    \n    // while\n    int n = 10;\n    while (n > 0) {\n        cout << n << " ";\n        n -= 3;\n    }\n    cout << endl;\n    return 0;\n}',
        "ejercicio": "Mostrá la tabla de multiplicar del número que elija el usuario. Usá for. Formato: '5 x 1 = 5'.",
        "pista": "Pedí el número con cin >>. Usá for(int i=1; i<=10; i++) y cout adentro."
    },
    {
        "id": 6, "bloque": "Funciones", "titulo": "Funciones en C++",
        "descripcion": "Declarar y usar funciones con tipos",
        "xp": 70,
        "teoria": "En C++ las funciones deben declararse antes de usarse (o usar prototipos). El tipo de retorno va antes del nombre. Si no retorna nada: void. Podés sobrecargar funciones con el mismo nombre pero distintos parámetros.",
        "ejemplo": '#include <iostream>\nusing namespace std;\n\n// Declaración\ndouble calcularIVA(double precio, double tasa = 0.21) {\n    return precio * tasa;\n}\n\nbool esPar(int n) {\n    return n % 2 == 0;\n}\n\nint main() {\n    double precio = 1000;\n    double iva = calcularIVA(precio);\n    cout << "IVA: $" << iva << endl;\n    cout << "Total: $" << precio + iva << endl;\n    \n    cout << (esPar(4) ? "par" : "impar") << endl;\n    return 0;\n}',
        "ejercicio": "Creá funciones: esPrimo(int n), potencia(double base, int exp) y celsiusAFahrenheit(double c). Probá cada una en main().",
        "pista": "Para esPrimo: iterá del 2 hasta sqrt(n). Incluí <cmath> para sqrt()."
    },
    {
        "id": 7, "bloque": "Estructuras", "titulo": "Arrays y vectores",
        "descripcion": "Arrays estáticos y vector<T> dinámico",
        "xp": 70,
        "teoria": "C++ tiene arrays estáticos (tamaño fijo: int arr[5]) y vector<T> dinámico (tamaño variable, como las listas de Python). Vector tiene push_back(), pop_back(), size(), y se puede recorrer con range-for. Incluí <vector>.",
        "ejemplo": '#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    vector<int> numeros = {3, 1, 4, 1, 5, 9};\n    numeros.push_back(2);\n    \n    cout << "Tamaño: " << numeros.size() << endl;\n    cout << "Primero: " << numeros[0] << endl;\n    cout << "Último: " << numeros.back() << endl;\n    \n    for (auto n : numeros) {\n        cout << n << " ";\n    }\n    return 0;\n}',
        "ejercicio": "Creá un vector con 5 notas. Calculá el promedio, encontrá la nota máxima y mínima, y mostrá cuántos aprobaron (>=60).",
        "pista": "Usá un for range-based para recorrer. Para max/min: mantené variables que se actualicen en cada vuelta."
    },
    {
        "id": 8, "bloque": "Estructuras", "titulo": "Structs y clases",
        "descripcion": "Agrupar datos con struct y comportamiento con class",
        "xp": 100,
        "teoria": "struct agrupa variables relacionadas. class es como struct pero con métodos y encapsulamiento (public/private). El constructor se llama igual que la clase. this-> accede a los atributos del objeto.",
        "ejemplo": '#include <iostream>\n#include <string>\nusing namespace std;\n\nclass CuentaBancaria {\nprivate:\n    string titular;\n    double saldo;\n\npublic:\n    CuentaBancaria(string t, double s) {\n        titular = t;\n        saldo = s;\n    }\n    \n    void depositar(double monto) {\n        saldo += monto;\n        cout << "+$" << monto << " depositado" << endl;\n    }\n    \n    double getSaldo() { return saldo; }\n};\n\nint main() {\n    CuentaBancaria cuenta("Ana", 1000);\n    cuenta.depositar(500);\n    cout << "Saldo: $" << cuenta.getSaldo() << endl;\n    return 0;\n}',
        "ejercicio": "Creá una clase Producto con nombre, precio y stock. Métodos: vender(int cantidad), aplicarDescuento(double pct) y estaDisponible(). Creá 2 productos y operalos.",
        "pista": "En vender() verificá que stock >= cantidad antes de reducirlo. Si no hay suficiente, mostrá un mensaje."
    },
    {
        "id": 9, "bloque": "Estructuras", "titulo": "Stack y Queue con STL",
        "descripcion": "Pilas y colas — las estructuras de datos más importantes",
        "xp": 120,
        "teoria": "La STL de C++ tiene stack<T> y queue<T> listos para usar. stack: push() agrega, pop() elimina, top() ve la cima. queue: push() agrega, pop() elimina, front() ve el frente. Son exactamente LIFO y FIFO.",
        "ejemplo": '#include <iostream>\n#include <stack>\n#include <queue>\nusing namespace std;\n\nint main() {\n    // Stack — historial del navegador\n    stack<string> historial;\n    historial.push("google.com");\n    historial.push("youtube.com");\n    historial.push("github.com");\n    cout << "Página actual: " << historial.top() << endl;\n    historial.pop(); // volver atrás\n    cout << "Volviste a: " << historial.top() << endl;\n    \n    // Queue — cola de tickets\n    queue<string> tickets;\n    tickets.push("Ana - bug crítico");\n    tickets.push("Luis - consulta");\n    cout << "Atendiendo: " << tickets.front() << endl;\n    tickets.pop();\n    return 0;\n}',
        "ejercicio": "Implementá un sistema de historial de navegador completo: podés navegar (push), ir atrás (pop del stack_atras, push al stack_adelante) e ir adelante. Mostrá siempre la página actual.",
        "pista": "Necesitás DOS stacks: uno para atrás y otro para adelante. Cuando navegás a una nueva página, limpiás el stack de adelante."
    },
    {
        "id": 10, "bloque": "Casos reales", "titulo": "Caso real: programa completo",
        "descripcion": "Sistema de gestión con todas las herramientas",
        "xp": 150,
        "teoria": "Este proyecto usa todo lo que aprendiste: clases, vectores, loops, funciones, condicionales. Es el tipo de programa que mostrás en una entrevista técnica.",
        "ejemplo": '// Sistema de biblioteca\n// - Agregar libros\n// - Buscar por título\n// - Prestar y devolver\n// - Ver disponibles',
        "ejercicio": "Construí un sistema de inventario de una tienda: Clase Producto (nombre, precio, stock). Vector de productos. Menú con: agregar producto, vender (reduce stock), ver inventario, valor total del inventario.",
        "pista": "Empezá con la clase Producto. Después el vector<Producto>. Después el menú con while y switch/if."
    },
]

@router.get("/modulos")
def obtener_modulos():
    return modulos

@router.get("/modulos/{modulo_id}")
def obtener_modulo(modulo_id: int):
    modulo = next((m for m in modulos if m["id"] == modulo_id), None)
    if not modulo:
        return {"error": "Módulo no encontrado"}
    return modulo
