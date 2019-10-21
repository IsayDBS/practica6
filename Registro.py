import hashlib
class Registro():

    def __init__(self,connection, cursor, nombre, password):
        self.connection = connection
        self.cursor = cursor
        self.nombre = nombre
        self.password = self.encriptar(password)

    def encriptar(self, string):
        sha_signature = hashlib.sha256(string.encode()).hexdigest()
        return sha_signature


    def registrar(self):
        string_insert = "INSERT INTO Jugador(nombre, password) VALUES ('" + self.nombre + "','" + self.password + "')"
        #print(string_insert)
        self.cursor.execute(string_insert)
        self.connection.commit()
