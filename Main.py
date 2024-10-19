import os
import struct

# Ubicación de los archivos
CARRERAS_FILE = "carreras.dat"
ESTUDIANTES_FILE = "estudiantes.dat"

# Función para verificar si el carnet ya existe
def carnet_existe(carnet):
    if os.path.exists(ESTUDIANTES_FILE):
        file = os.open(ESTUDIANTES_FILE, os.O_RDONLY)  # Abrir archivo en solo lectura
        while True:
            data = os.read(file, 65)  # Leer el tamaño completo del registro de estudiante
            if not data:
                break
            registro_carnet = struct.unpack('10s30s15s10s', data)[0].decode().strip()
            if registro_carnet == carnet:
                os.close(file)
                return True
        os.close(file)
    return False

# Función para obtener todas las carreras disponibles
def obtener_carreras():
    carreras = {}
    if os.path.exists(CARRERAS_FILE):
        file = os.open(CARRERAS_FILE, os.O_RDONLY)  # Abrir archivo en solo lectura
        while True:
            data = os.read(file, 40)
            if not data:
                break
            codigo, nombre = struct.unpack('10s30s', data)
            carreras[codigo.decode().strip()] = nombre.decode().strip()
        os.close(file)  # Cerrar archivo
    return carreras

# Función para agregar una carrera
def agregar_carrera():
    codigo = input("Ingrese el código de la carrera: ").ljust(10)  #
    nombre = input("Ingrese el nombre de la carrera: ").ljust(30)  

    file = os.open(CARRERAS_FILE, os.O_RDWR | os.O_CREAT | os.O_APPEND)  # Abrir archivo
    os.write(file, struct.pack('10s30s', codigo.encode(), nombre.encode()))  # Escribir datos
    os.close(file)  # Cerrar el archivo manualmente
    print("Carrera agregada exitosamente.\n")

# Función para agregar un estudiante con validación de carnet y carrera
def agregar_estudiante():
    while True:
        carnet = input("Ingrese el carnet del estudiante: ").ljust(10)
        if carnet_existe(carnet.strip()):
            print("El número de carnet ya existe. Ingrese un nuevo número.")
        else:
            break

    nombre = input("Ingrese el nombre del estudiante: ").ljust(30) 
    color = input("Ingrese el color favorito del estudiante: ").ljust(15) 
    
    carreras = obtener_carreras()
    
    # Mostrar las carreras disponibles
    print("\nCarreras disponibles:")
    for codigo, nombre_carrera in carreras.items():
        print(f"Código: {codigo}, Nombre: {nombre_carrera}")
    
    # Validar el código de carrera
    while True:
        codigo_carrera = input("Ingrese el código de la carrera del estudiante: ").ljust(10)
        if codigo_carrera.strip() in carreras:
            break
        else:
            print("Código de carrera no válido. Ingrese un código de carrera existente.")
    
    file = os.open(ESTUDIANTES_FILE, os.O_RDWR | os.O_CREAT | os.O_APPEND)  # Abrir archivo
    os.write(file, struct.pack('10s30s15s10s', carnet.encode(), nombre.encode(), color.encode(), codigo_carrera.encode()))  # Escribir datos
    os.close(file)  # Cerrar archivo
    print("Estudiante agregado exitosamente.\n")


def mostrar_carreras():
    if os.path.exists(CARRERAS_FILE):
        file = os.open(CARRERAS_FILE, os.O_RDONLY)  # Abrir archivo
        print("\nCarreras actuales:")
        while True:
            data = os.read(file, 40)
            if not data:
                break
            codigo, nombre = struct.unpack('10s30s', data)
            print(f"Codigo: {codigo.decode().strip()}, Nombre: {nombre.decode().strip()}")
        os.close(file)  # Cerrar archivo
    else:
        print("No hay carreras registradas.\n")


def mostrar_estudiantes():
    carreras = obtener_carreras()

    # Leer estudiantes y mostrar información con el nombre de la carrera
    if os.path.exists(ESTUDIANTES_FILE):
        file = os.open(ESTUDIANTES_FILE, os.O_RDONLY)  # Abrir archivo en solo lectura
        print("\nEstudiantes registrados:")
        while True:
            data = os.read(file, 65)
            if not data:
                break
            carnet, nombre, color, codigo_carrera = struct.unpack('10s30s15s10s', data)
            codigo_carrera = codigo_carrera.decode().strip()
            nombre_carrera = carreras.get(codigo_carrera, "Carrera desconocida")
            print(f"Carnet: {carnet.decode().strip()}, Nombre: {nombre.decode().strip()}, Color: {color.decode().strip()}, Carrera: {nombre_carrera}")
        os.close(file)  # Cerrar archivo
    else:
        print("No hay estudiantes registrados.\n")

# Menú principal
def menu():
    while True:
        print("\n--- Sistema Gestor de Estudiantes ---")
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
