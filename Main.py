import os
import platform

# Ubicación de los archivos
CARRERAS_FILE = "carreras.dat"
ESTUDIANTES_FILE = "estudiantes.dat"
SEPARADOR = '|'


def limpiar_consola():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Función para verificar si el carnet ya existe (bajo nivel)
def carnet_existe(carnet):
    if os.path.exists(ESTUDIANTES_FILE):
        file = os.open(ESTUDIANTES_FILE, os.O_RDONLY)  # Abrir archivo en solo lectura
        buffer = ""
        while True:
            char = os.read(file, 1).decode()  # Leer carácter por carácter
            if not char:
                break
            if char == SEPARADOR:  # Encontramos el fin del campo del carnet
                if buffer.strip() == carnet:
                    os.close(file)
                    return True
                buffer = ""
            elif char == '\n':
                buffer = ""
            else:
                buffer += char
        os.close(file)
    return False

def carrera_existe(codigo):
    carreras = obtener_carreras()  # Obtener todas las carreras
    return codigo in carreras

# Función para obtener todas las carreras
def obtener_carreras():
    carreras = {}
    if os.path.exists(CARRERAS_FILE):
        file = os.open(CARRERAS_FILE, os.O_RDONLY)
        buffer = ""
        codigo = None
        while True:
            char = os.read(file, 1).decode()  # Leer carácter por carácter
            if not char:  # Si llegamos al final del archivo, salimos del bucle
                break
            if char == SEPARADOR:
                if codigo is None:
                    codigo = buffer.strip()
                buffer = ""
            elif char == '\n':
                carreras[codigo] = buffer.strip()  # Guardar el nombre de la carrera
                codigo = None
                buffer = ""
            else:
                buffer += char
        os.close(file)
    return carreras

# Función para agregar una carrera
def agregar_carrera():
    limpiar_consola()
    while True:
        codigo = input("Ingrese el código de la carrera: ")
        if carrera_existe(codigo):
            limpiar_consola()
            print(f"El código {codigo} ya existe. Ingrese un nuevo código.")
        else:
            break

    nombre = input("Ingrese el nombre de la carrera: ")

    file = os.open(CARRERAS_FILE, os.O_RDWR | os.O_CREAT | os.O_APPEND)
    os.write(file, (codigo + SEPARADOR + nombre + '\n').encode())  # Escribir en formato de bajo nivel
    os.close(file)
    print("\nCarrera agregada exitosamente.")
    input("\nPresione Enter para volver al menú...")
    limpiar_consola()

# Función para agregar un estudiante con validación de carnet y carrera
def agregar_estudiante():
    limpiar_consola()
    while True:
        carnet = input("Ingrese el carnet del estudiante: ")
        if carnet_existe(carnet):
            limpiar_consola()
            print("El número de carnet ya existe. Ingrese un nuevo número.")
        else:
            break

    nombre = input("Ingrese el nombre del estudiante: ")
    color = input("Ingrese el color favorito del estudiante: ")
    
    carreras = obtener_carreras()
    
    # Mostrar las carreras disponibles
    if carreras:
        print("\nCarreras disponibles:")
        for codigo, nombre_carrera in carreras.items():
            print(f"Código: {codigo}, Nombre: {nombre_carrera}")
        
        # Validar el código de carrera
        while True:
            codigo_carrera = input("Ingrese el código de la carrera del estudiante: ")
            if codigo_carrera in carreras:
                break
            else:
                limpiar_consola()
                print(f"El código de carrera {codigo_carrera} no es válido. Ingrese un código existente.")
    
        file = os.open(ESTUDIANTES_FILE, os.O_RDWR | os.O_CREAT | os.O_APPEND)
        os.write(file, (carnet + SEPARADOR + nombre + SEPARADOR + color + SEPARADOR + codigo_carrera + '\n').encode())  # Escribir datos
        os.close(file)
        print("\nEstudiante agregado exitosamente.")
    else:
        print("\nError: No hay carreras disponibles. Debe agregar una carrera primero.")
    
    input("\nPresione Enter para volver al menú...")
    limpiar_consola()

# Función para mostrar carreras con mejor formato
def mostrar_carreras():
    limpiar_consola()
    carreras = obtener_carreras()

    if carreras:
        print("\nCarreras actuales:")
        print(f"{'Código':<10} {'Nombre':<30}")
        print("-" * 40)
        for codigo, nombre in carreras.items():
            print(f"{codigo:<10} {nombre:<30}")
    else:
        print("No hay carreras registradas.")

    input("\nPresione Enter para volver al menú...")


# Función para mostrar estudiantes con nombre de la carrera
def mostrar_estudiantes():
    limpiar_consola()
    carreras = obtener_carreras()

    if os.path.exists(ESTUDIANTES_FILE):
        file = os.open(ESTUDIANTES_FILE, os.O_RDONLY)
        print("\nEstudiantes registrados:")
        print(f"{'Carnet':<10} {'Nombre':<25} {'Color':<15} {'Carrera':<35}")
        print("-" * 80)
        buffer = ""
        campos = []
        while True:
            char = os.read(file, 1).decode()
            if not char:
                break
            if char == SEPARADOR:
                campos.append(buffer.strip())
                buffer = ""
            elif char == '\n':
                campos.append(buffer.strip())
                if len(campos) == 4:
                    codigo_carrera = campos[3]
                    nombre_carrera = carreras.get(codigo_carrera, "Carrera desconocida")
                    print(f"{campos[0]:<10} {campos[1]:<25} {campos[2]:<15} {nombre_carrera:<35}")
                else:
                    print(f"Registro incompleto o mal formateado: {campos}")
                campos = []
                buffer = ""
            else:
                buffer += char
        os.close(file)
    else:
        print("No hay estudiantes registrados.")

    input("\nPresione Enter para volver al menú...")

# Menú principal
def menu():
    while True:
        limpiar_consola()
        print("--- Sistema Gestor de Estudiantes ---")
        print("1. Agregar Carrera")
        print("2. Agregar Estudiante")
        print("3. Mostrar Carreras")
        print("4. Mostrar Estudiantes")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_carrera()
        elif opcion == "2":
            agregar_estudiante()
        elif opcion == "3":
            mostrar_carreras()
        elif opcion == "4":
            mostrar_estudiantes()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()