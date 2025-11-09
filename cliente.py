class Cliente():
    def __init__(self, nombre: str, apellido: str, telefono: str):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.telefono}"
        

