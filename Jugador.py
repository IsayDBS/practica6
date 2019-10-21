from colorama import *
class Jugador():

    def __init__(self, cursor, connection,nombre,identificador):
        self.__nombre=nombre
        self.cursor = cursor
        self.connection = connection
        self.identificador= identificador
        self.__color = None

    def getColor(self):
        return self.__color

    def setColor(self, color):
        self.__color = color

    def getNombre(self):
        return self.__nombre

    def getIdentificador(self):
        string_id = "SELECT pk_id_jugador FROM Jugador WHERE nombre='" + self.__nombre+"'"
        self.cursor.execute(string_id)
        self.connection.commit()
        id = self.cursor.fetchall()
        return id[0][0]

    def setNombre(self, name):
        self.__nombre = name

    def setIdentificador(self, id):
        self.identificador = id
