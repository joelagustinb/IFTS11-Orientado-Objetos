def crea_csv(nombre_archivo, columnas):
    file = open(nombre_archivo, "wt")
    csv_line = ",".join(columnas) + "\n"
    file.writelines([csv_line])
    file.close()


def agrega_valores_csv(nombre_archivo):
    file = open(nombre_archivo, "at")
    nombre = input("Ingrese nombre: ")
    while nombre != "":
        apellido = input("Ingrese apellido: ")
        dni = input("Ingrese DNI: ")
        numero_cliente = input("Ingrese numero cliente: ")
        vector = [nombre, apellido, dni, numero_cliente]
        fila = ",".join(vector) + "\n"
        file.writelines([fila])
        nombre = input("Ingrese nombre: ")
    file.close()

# CLASE PRESENCIAL

class Transforma(object):
    def __init__(self, atributos, tipo_registro=None):
        # limpiamos atributos
        clean = []
        i = 0
        while i < len(atributos):
            clean.append(atributos[i].strip())
            i += 1

        self.keys = clean
        self.tipo_registro = tipo_registro or Registro

    def toDict(self, values):
        if len(values) != len(self.keys):
            return None
        
        d = {}
        i = 0
        while i < len(values):
            d[self.keys[i]] = values[i].strip()
            i += 1
        return d
    
    def toObject(self, values):
        datos = {}
        i = 0

        # completar valores faltantes si vienen menos columnas
        while len(values) < len(self.keys):
            values.append("")

        while i < len(self.keys):
            valor_limpio = values[i].strip()
            clave = self.keys[i].strip()
            datos[clave] = valor_limpio
            i += 1

        obj = self.tipo_registro(**datos)
        return obj



class Registro(object):
    def __init__(self, **kwargs):
        for clave, valor in kwargs.items():
            setattr(self, clave, valor)
    
    def __str__(self):
        # convertir __dict__ a "clave: valor" usando while
        pares = []
        keys = list(self.__dict__.keys())
        i = 0
        while i < len(keys):
            k = keys[i]
            v = self.__dict__[k]
            pares.append(f"{k}: {v}")
            i += 1

        clase = self.__class__.__name__
        return f"{clase}({', '.join(pares)})"


class Turno(Registro):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def Validar(self):
        if not hasattr(self,"cliente_id"):
            return False
        if not hasattr(self,"fecha"):
            return False
        if not hasattr(self,"hora"):
            return False
        return True
    
    def fecha_hora(self):
        from datetime import datetime
        return datetime.strptime(f"{self.fecha} {self.hora}", "%Y-%m-%d %H:%M")
    
 

class Cliente(Registro):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def validar(self):
        if not hasattr(self, 'nombre') or self.nombre == "":
            return False
        
        if hasattr(self, 'dni'):
            dni = self.dni.strip()
            if len(dni) != 8:
                return False
        
        return True
    
    def nombre_completo(self):
        if hasattr(self, 'apellido'):
            return f"{self.nombre} {self.apellido}"
        return self.nombre
    
class DB(object):
    def __init__(self, filename, tipo_registro=None):
        self.filename = filename
        self.tipo_registro = tipo_registro or Registro
    
    def read(self):
        db = []
        try:
            file = open(self.filename, "rt")
        except FileNotFoundError:
            return db
        
        line = file.readline()
        if line == "":
            return db
        
        keys = line.strip().split(",")
        tran = Transforma(keys, self.tipo_registro)

        line = file.readline()
        while line != "":
            if line.strip() != "":
                values = line.strip().split(",")
                obj = tran.toObject(values)
                if obj:
                    db.append(obj)
            line = file.readline()

        file.close()
        return db

    def write(self, registros):
        if len(registros) == 0:
            return
        
        keys = list(registros[0].__dict__.keys())

        file = open(self.filename, "wt")
        header = ",".join(keys) + "\n"
        file.write(header)

        i = 0
        while i < len(registros):
            r = registros[i]
            fila = []
            j = 0
            while j < len(keys):
                val = str(r.__dict__.get(keys[j], ""))
                fila.append(val)
                j += 1

            file.write(",".join(fila) + "\n")
            i += 1
        
        file.close()

class DBTurnos(DB):
    @classmethod
    def crear_db_turnos(cls, filename):
        return cls(filename, Turno)

#MENUS
def menu_turnos(db_turnos):
    opcion = ""
    while opcion != "3":
        print("\n--- MENU TURNOS ---")
        print("1) Listar turnos")
        print("2) Agregar turno")
        print("3) Guardar y volver")
        opcion = input("Opcion: ")

        if opcion == "1":
            turnos = db_turnos.read()
            i = 0
            while i < len(turnos):
                print(turnos[i])
                i += 1

        elif opcion == "2":
            cliente_id = input("ID del cliente: ")
            fecha = input("Fecha (Dia/Mes): ")
            hora = input("Hora (Hora:Minuto): ")
            servicio = input("Servicio: ")

            nuevo = Turno(
                cliente_id=cliente_id,
                fecha=fecha,
                hora=hora,
                servicio=servicio
            )

            turnos = db_turnos.read()
            turnos.append(nuevo)
            db_turnos.write(turnos)
            print("Turno agregado")

def menu_principal():
    db_clientes = DB("clientes.csv", Cliente)
    db_turnos = DBTurnos.crear_db_turnos("turnos.csv")

    opcion = ""
    while opcion != "4":
        print("\n===== SISTEMA DE PELUQUERÍA =====")
        print("1) Registrar nuevo cliente")
        print("2) Gestionar turnos")
        print("3) Listar clientes")
        print("4) Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            registrar_cliente(db_clientes)

        elif opcion == "2":
            menu_turnos(db_turnos)

        elif opcion == "3":
            listar_clientes(db_clientes)


def registrar_cliente(db_clientes):
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    dni = input("DNI: ")
    numero_cliente = input("Numero Cliente: ")
    nuevo = Cliente(nombre=nombre, apellido=apellido, dni=dni, numero_cliente= numero_cliente)

    clientes = db_clientes.read()
    clientes.append(nuevo)
    db_clientes.write(clientes)

    print("Cliente registrado correctamente.")

def listar_clientes(db_clientes):
    clientes = db_clientes.read()
    i = 0
    while i < len(clientes):
        print(clientes[i])
        i += 1

menu_principal()