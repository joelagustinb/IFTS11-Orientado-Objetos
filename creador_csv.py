class Transforma(object):
    def __init__(self,):

        pass
class DB(object):
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        file = open(self.filename, "rt")
        line = file.realine() # Leo encabezado
        db = []
        if line == "":
            return []
        keys = line.split(",")
        tran = Transforma(keys)
        line = file.realine() # Leo primera linea valores
        while line != "":
            values = line.split(",")
            d = tran.toDict(values)
            db.append(d)
            line = file.readline()
        return db
    def write(self, registros):
        pass
db = DB("db.csv")
registros = db.read()
print(registros)