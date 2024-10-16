class Registro:
    def __init__(self, carnet, nombre, carrera, color):
        self.carnet = carnet
        self.nombre = nombre
        self.carrera = carrera
        self.color = color

    def __repr__(self):
        return f'Carnet: {self.carnet}, Nombre: {self.nombre}, Carrera: {self.carrera}, Color: {self.color}'

class SistemaRegistros:
    def __init__(self):
        self.registros = []

    def carnet_existe(self, carnet):
        """Verifica si el carnet ya está registrado."""
        for registro in self.registros:
            if registro.carnet == carnet:
                return True
        return False

    def agregar_registro(self):
        while True:
            carnet = input("Ingrese el carnet: ")
            if self.carnet_existe(carnet):
                print(f"El carnet {carnet} ya existe. Ingrese un número de carnet diferente.")
            else:
                break
        nombre = input("Ingrese el nombre: ")
        carrera = input("Ingrese la carrera: ")
        color = input("Ingrese el color favorito: ")
        registro = Registro(carnet, nombre, carrera, color)
        self.registros.append(registro)
        print("Registro agregado con éxito.")

    def buscar_registro(self):
        carnet = input("Ingrese el carnet a buscar: ")
        for registro in self.registros:
            if registro.carnet == carnet:
                print("Registro encontrado:")
                print(registro)
                return
        print("Registro no encontrado.")

    def ordenar_registros(self):
        print("Ordenar por: 1) Carnet 2) Nombre 3) Carrera 4) Color")
        opcion = input("Seleccione una opción (1-4): ")
        if opcion == '1':
            self.registros.sort(key=lambda x: x.carnet)
        elif opcion == '2':
            self.registros.sort(key=lambda x: x.nombre)
        elif opcion == '3':
            self.registros.sort(key=lambda x: x.carrera)
        elif opcion == '4':
            self.registros.sort(key=lambda x: x.color)
        else:
            print("Opción inválida.")
            return
        print("Registros ordenados:")
        for registro in self.registros:
            print(registro)

    def guardar_registros(self):
        with open("registros.txt", "w") as archivo:
            for registro in self.registros:
                archivo.write(f'{registro.carnet}, {registro.nombre}, {registro.carrera}, {registro.color}\n')
        print("Registros guardados en 'registros.txt'.")

    def menu(self):
        while True:
            print("\n--- Sistema de Registros ---")
            print(f"Total de registros: {len(self.registros)} (mínimo 15 registros)")
            print("1) Ingresar nuevo registro")
            print("2) Buscar registro por carnet")
            print("3) Ordenar registros")
            print("4) Guardar registros en archivo")
            if len(self.registros) >= 15:
                print("5) Salir")
            opcion = input("Seleccione una opción (1-5): " if len(self.registros) >= 15 else "Seleccione una opción (1-4): ")
            
            if opcion == '1':
                self.agregar_registro()
            elif opcion == '2':
                self.buscar_registro()
            elif opcion == '3':
                self.ordenar_registros()
            elif opcion == '4':
                self.guardar_registros()
            elif opcion == '5' and len(self.registros) >= 15:
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida." if len(self.registros) >= 15 else "Debe ingresar al menos 15 registros antes de salir.")

# Ejecución del programa
sistema = SistemaRegistros()
sistema.menu()
    