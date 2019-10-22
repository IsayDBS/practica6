from dotenv import load_dotenv
from os.path import join, dirname, isdir
from os import environ
import mysql.connector
from Juego import *
from Registro import *
from Jugador import *
import hashlib

class Main():

    def __init__(self):
        self.connection, self.cursor = self.conectar()
        self.__jugador1 = None
        self.__jugador2 = None

    def conectar(self):
        dotenv_path = join(dirname(__file__), ".env")
        load_dotenv(dotenv_path)
        dbname=environ.get("db_name")
        host=environ.get("db_host")
        username=environ.get("db_username")
        password=environ.get("db_password")
        connection = mysql.connector.connect(database = dbname,
                                            host = host,
                                            username = username,
                                            password = password)
        cursor = connection.cursor()
        return connection, cursor

    def registrar(self):
        test = False
        while test == False:
            name = input("Introduce tu nombre de usuario que desees\n")
            password = input("Introduce tu contrasenia\n")
            repassword = input("Vuelve a introducir tu contrasenia\n")
            if password != repassword:
                print("Tus contrasenias no concuerdan, hazlo de nuevo")
            else:
                try:
                    nuevo_registro = Registro(self.connection, self.cursor, name, password)
                    nuevo_registro.registrar()
                except:
                    print("Usuario ya existente, intenta de nuevo")
                else:
                    test = True
                    print("Felicidades, te has registrado exitosamente")

    def encriptar(self, string):
        sha_signature = hashlib.sha256(string.encode()).hexdigest()
        return sha_signature

    def acceder(self, Invitado = ""):
        fetch = []
        if Invitado == "":
            repeticion = True
            while repeticion == True:
                acceso = input("Introduce tu usuario\n")
                acc = input("Introduce tu contrasenia\n")
                acc_pass = self.encriptar(acc)
                string_acceso = "SELECT nombre,pk_id_jugador FROM Jugador WHERE nombre='" + acceso + "' AND password='"+acc_pass+"'"
                self.cursor.execute(string_acceso)
                fetch = self.cursor.fetchall()
                self.connection.commit()
                #print(fetch)
                if fetch == []:
                    valor = input("El usuario no existe, estas registrado(n)? Si se equivoco en contrasenia o usuario, ingrese lo que sea e intente de nuevo\n")
                    if valor == "n":
                        self.registrar()
                else:
                    jugador = Jugador(self.cursor, self.connection,fetch[0][0],fetch[0][1])
                    repeticion = False
        else:
            string_invitado = "SELECT pk_id_jugador FROM Jugador WHERE nombre='invitado'"
            self.cursor.execute(string_invitado)
            fetch = self.cursor.fetchall()
            self.connection.commit()
            jugador = Jugador(self.cursor, self.connection, "invitado",fetch[0][0])
        #print(jugador.getNombre())
        return jugador;

    def cargas(self):
        self.__jugador1 = self.acceder()
        string_carga = "SELECT * FROM Partida WHERE fk_id_creador = " + str(self.__jugador1.identificador) + " AND resultado IS NULL"
        self.cursor.execute(string_carga)
        lista = self.cursor.fetchall()
        #imprime = ""
        if lista == []:
            print("Ups, parece que no tienes partidas guardadas con este usuario")
        else:
            numeros = []
            for list in lista:
                print(list)
                numeros.append(list[0])
            repite = True
            while repite == True:
                seleccion = int(input("Selecciona el numero de la partida que desees cargar(el que esta mas a la izquierda)\nIntroduce -1 para salir\n"))
                if seleccion == -1:
                    repite = False
                    return []
                elif seleccion in numeros:
                    string_cargarPartida = "SELECT * FROM Partida WHERE pk_id_partida = "+ str(seleccion)
                    self.cursor.execute(string_cargarPartida)
                    cargar = self.cursor.fetchall()
                    repite = False
                    return cargar
                else:
                    print("No es una partida valida, intenta de nuevo")
        return []

    def switch(self, argument):
        if argument == 1:
            self.__jugador1 = self.acceder()
            self.__jugador1.setColor(Fore.RED)
            #Color del jugador que crea la partida es rojo, el del oponente es amarillo
            #print(self.__jugador1.identificador)
            eleccion = int(input("Elige contra quien vas a jugar\n1)Otro jugador registrado\n2)Invitado\n"))
            if eleccion==1:
                self.__jugador2 = self.acceder()
            else:
                self.__jugador2 = self.acceder("invitado")
            self.__jugador2.setColor(Fore.YELLOW)
            juego = Juego(self.__jugador1,self.__jugador2,"",self.cursor,self.connection)
            juego.jugar()
            #print(self.__jugador2.getNombre())
            #jugar = Juego(self.__jugador1,self.__jugador2,[],self.cursor,self.connection)
            #jugar.jugar()
            #print("Partida nueva")
        elif argument == 2:
            print("Elegiste registrarte")
            self.registrar()
            #print("Registrarse")
        elif argument == 3:
            print("Elegiste cargar partida")
            #carga = int(input("Introduce el identificador de la partida que estabas jugando"))
            lista = self.cargas()
            if lista == []:
                pass
            else:
                self.__jugador2 = self.obtenerJugadorpk(lista[0][4])
                self.__jugador1.setColor(Fore.RED)
                self.__jugador2.setColor(Fore.YELLOW)
                #jugador_turno = self.obtenerJugadorpk(lista[0][2])
                if self.obtenerJugadorpk(lista[0][2]) == self.__jugador1:
                #aqui ya existe self.__jugador1
                    juego = Juego(self.__jugador1,self.__jugador2,lista[0][1],self.cursor, self.connection,self.__jugador1,lista[0][0])
                else:
                    juego = Juego(self.__jugador1,self.__jugador2,lista[0][1],self.cursor, self.connection,self.__jugador2,lista[0][0])
                juego.jugar()
                #print("Cargar partida"
        elif argument == 4:
            print("Elegiste estadisticas")
            self.estadisticas()
        else:
            print("Adios")

    def estadisticas(self):
        self.__jugador1 = self.acceder()
        string_carga = "SELECT * FROM Partida WHERE fk_id_creador = " + str(self.__jugador1.identificador)
        self.cursor.execute(string_carga)
        lista_creador = self.cursor.fetchall()
        string_carga0 = "SELECT * FROM Partida WHERE fk_id_oponente = " + str(self.__jugador1.identificador)
        self.cursor.execute(string_carga0)
        lista_oponente = self.cursor.fetchall()
        #imprime = ""
        if lista_creador == [] and lista_oponente == []:
            print("Ups, parece que no tienes partidas terminadas con este usuario")
        else:
            gana_crea = []
            pierde_crea = []
            empate = []
            gana_opo = []
            pierde_opo = []
            if lista_creador != []:
                for list in lista_creador:
                    if list[5] == "gana":
                        gana_crea.append(list)
                    elif list[5] == "pierde":
                        pierde_crea.append(list)
                    elif list[5] == "empate":
                        empate.append(list)
                    #new_list = [gana, pierde, empate]
            if lista_oponente != []:
                for list in lista_oponente:
                    if list[5] == "pierde":
                        gana_opo.append(list)
                    elif list[5] == "gana":
                        pierde_opo.append(list)
                    elif list[5] == "empate":
                        empate.append(list)
            gana = gana_opo + gana_crea
            pierde = pierde_opo + pierde_crea
            if gana != []:
                print(Fore.GREEN + "Partidas ganadas" + Fore.RESET)
                for k in gana:
                    jugador = self.obtenerJugadorpk(k[4])
                    print("Ganaste contra " + jugador.getNombre())
            if pierde != []:
                print(Fore.RED + "Partidas perdidas" + Fore.RESET)
                for k in pierde:
                    jugador = self.obtenerJugadorpk(k[4])
                    print("Perdiste contra " + jugador.getNombre())
            if empate != []:
                print(Fore.YELLOW + "Partidas empatadas" + Fore.RESET)
                for k in empate:
                    jugador = self.obtenerJugadorpk(k[4])
                    print("Empataste contra " + jugador.getNombre())
            if new_list == [[],[],[]]:
                print("Ups, parece que aun no has acabado ninguna partida!")


    def obtenerJugadorpk(self,pk_jugador):
        string_obtener = "SELECT pk_id_jugador, nombre FROM Jugador WHERE pk_id_jugador = " + str(pk_jugador)
        self.cursor.execute(string_obtener)
        lista = self.cursor.fetchall()
        jugador = Jugador(self.cursor, self.connection,lista[0][1],pk_jugador)
        return jugador

    def main(self):
        print("Bienvenido al juego de conecta 4")
        prueba = False
        while prueba == False:
            print("Elige una opcion")
            print("1) Partida nueva")
            print("2) Registrarse")
            print("3) Cargar partida")
            print("4) Estadisticas")
            print("0) Salir")
            try:
                argumento = int(input())
                self.switch(argumento)
                if argumento == 0:
                    prueba = True
            except:
                print("No es entrada valida, intenta de nuevo")
        #except:
        #    print("No es un argumento valido, intenta de nuevo ")


if __name__ == '__main__':
    partida = Main()
    partida.main()
