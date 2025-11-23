"""
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
        vector = [nombre, apellido, dni]
        fila = ",".join(vector) + "\n"
        file.writelines([fila])
        nombre = input("Ingrese nombre: ")
    file.close()

agrega_valores_csv("db.csv")
"""

# CLASE PRESENCIAL

class Transforma(object):
    def __init__(self, atributos, tipo_registro=None):
        self.keys = atributos
        self.tipo_registro = tipo_registro or Registro  # Por defecto usa Registro genérico

    def toDict(self, values):
        if len(values) != len(self.keys):
            return None
        d = {}
        i = 0
        while i < len(values):
            d[self.keys[i]] = values[i]
            i = i + 1
        return d
    
    def toObject(self, values):
        """Convierte una lista de valores en un objeto del tipo especificado"""
        if len(values) != len(self.keys):
            return None
        
        # Creamos un diccionario para usar como **kwargs
        datos = {}
        i = 0
        while i < len(values):
            # Limpiamos los valores (quitamos saltos de línea)
            valor_limpio = values[i].strip()
            datos[self.keys[i].strip()] = valor_limpio
            i = i + 1
        
        # Creamos el objeto del tipo especificado usando **kwargs
        obj = self.tipo_registro(**datos)
        
        return obj


class Registro(object):
    """Clase base que representa un registro genérico de la base de datos"""
    def __init__(self, **kwargs):
        # **kwargs nos permite recibir cualquier cantidad de argumentos con nombre
        # Los asignamos como atributos del objeto
        for clave, valor in kwargs.items():
            setattr(self, clave, valor)
    
    def __str__(self):
        """Representación en string del objeto"""
        atributos = []
        for clave, valor in self.__dict__.items():
            atributos.append(f"{clave}: {valor}")
        clase = self.__class__.__name__  # Obtiene el nombre de la clase actual
        return f"{clase}({', '.join(atributos)})"
    
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
    """Clase específica para registros de clientes"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Llama al constructor de la clase padre
    
    def validar(self):
        """Validación específica para clientes"""
        if not hasattr(self, 'nombre') or self.nombre == "":
            return False
        if hasattr(self, 'dni') and len(self.dni.strip()) != 8:
            return False
        return True
    
    def nombre_completo(self):
        """Método específico para clientes"""
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
        line = file.readline() # Leo encabezado
        if line == "":
            return db
        keys = line.split(",")
        tran = Transforma(keys, self.tipo_registro)
        line = file.readline() # Leo la primera linea
        while line != "":
            values = line.split(",")
            # Ahora creamos objetos del tipo especificado
            obj = tran.toObject(values)
            if obj:  # Solo agregamos si el objeto se creó correctamente
                db.append(obj)
            line = file.readline()
        file.close()
        return db

    def write(self, registros):
        if len(registros) == 0:
            return
        keys = list(registros[0].__dict__.keys())
        file = open(self.filename, "wt")
        encabezado = ",".join(keys) + "\n"
        file.writelines([encabezado])
        for r in registros:
            fila = ",".join([r.__dict__[k] for k in keys]) + "\n"
            file.writelines([fila])
        file.close()

    @classmethod
    def crear_db_clientes(cls, filename):
        """Método de clase para crear una DB específica para clientes"""
        return cls(filename, Cliente)



diccionario = {
    "name": "Emiliano",
    "edad": 43,
    "dni": 12821838
}

print(diccionario)
print("Hola Mundo")

for clave, valor in diccionario.items():
    print("La clave es:", clave, "y el valor es:", valor)


r = Registro(arnoldswartzennegger="Emiliano", edad=43, sexo="M")
print(r.arnoldswartzennegger)
print("\nHola\nMundo\n".replace("\n", ""))