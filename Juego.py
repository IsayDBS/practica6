#from termcolor import colored
import time
import mysql.connector
import random
import subprocess as sp
from colorama import *
from Jugador import *
#from Bcolors import *
class Juego():
    def __init__(self, jugador1, jugador2, tablero,cursor, connection, jugadorenturno=None, identificador=0):
        self.__creador = jugador1
        self.__Jugador2 = jugador2
        if jugadorenturno == None:
            self.__jugador_en_turno = self.__turnoInicio()
        else:
            self.__jugador_en_turno = jugadorenturno
        #tablero es una lista de listas = [[],[],[],[],[],[]]
        #donde cada lista representa el renglon
        self.__tablero = self.__setTablero(tablero)
        self.identificador = identificador
        self.cursor = cursor
        self.connection = connection

    def guardar(self):
        string_guardar = "INSERT INTO Partida( tablero_cifrado, fk_id_jugador_en_turno, fk_id_creador, fk_id_oponente, resultado) VALUES (" + self.__cifradoTablero() + self.__getEnturno() + self.__getCreador() + self.__getOponente() + self.__getResultado() + ")"
        self.cursor.execute(string_guardar)
        self.connection.commit()

    def update(self):
        string_update = "UPDATE Partida SET tablero_cifrado = "+ self.__cifradoTablero() + " fk_id_jugador_en_turno = " + self.__getEnturno() + " resultado = " + self.__getResultado() + " WHERE pk_id_partida = " + self.__getPKPartida()
        self.cursor.execute(string_update)
        self.connection.commit()

    def __revisa(self):
        if self.__getPKPartida() ==[]:
            return []
        else:
            string_revisa = "SELECT * FROM Partida WHERE pk_id_partida = " + self.__getPKPartida()[0][0]
            self.cursor.execute(string_revisa)
            return self.cursor.fetchall()

    def __getPKPartida(self):
        string_select = "SELECT pk_id_partida FROM Partida WHERE " + str(self.identificador)
        self.cursor.execute(string_select)
        lista = self.cursor.fetchall()
        return lista

    def __turnoInicio(self):
        numero = random.randint(1,101)
        if numero <= 50:
            return self.__Jugador2
        else:
            return self.__creador

    def __getResultado(self):
        #El resultado es en referencia a quien creo el juego
        if self.__revisarEmpate()==True:
            return "'empate'"

        #if self.empate() == True:
        #    return "NULL"

        for i in range(0,7):
            for j in range(0,6):
                if self.__verMovimiento(i,j,self.__creador.getColor()) == True:
                    return "'gana'"
                elif self.__verMovimiento(i,j,self.__Jugador2.getColor())  == True:
                    return "'pierde'"
        return "NULL"

    def empate(self):
        for i in range(0,7):
            for j in range(0,6):
                if self.__tablero[i][j]==Fore.BLACK:
                    return True
        return False

    def __setTablero(self, cifrado):
        #cifrado es un string, agregamos desde 0 hasta 41
        #Es de la forma 'RYRYRYRYRYR' R=Fond.RED, del jugador creador, Y=Fond.YELLOW, del jugador oponente
        cypher = [[],[],[],[],[],[],[]]
        if cifrado == "":
            for i in range(0,7):
                for j in range(0,6):
                    cypher[i].append(Fore.BLACK)
            return cypher
        else:
            contador = 0
            for i in range(0,7):
                for j in range(0,6):
                    letter = cifrado[contador]
                    if letter == "R":
                        cypher[i].append(Fore.RED)
                    elif letter == "Y":
                        cypher[i].append(Fore.YELLOW)
                    elif letter == "'":
                        pass
                    else:
                        cypher[i].append(Fore.BLACK)
                    contador += 1
            return cypher

    def __getOponente(self):
        string_oponente = ""
        string_oponente += str(self.__Jugador2.identificador) +", "
        return string_oponente

    def getIdentificador(self):
        string_identificador = "SELECT pk_id_partida FROM Partida WHERE fk_id_creador = " + self.__creador.identificador + " AND fk_id_oponente = " + self.__Jugador2.identificador
        self.cursor.execute(string_identificador)
        lista = self.cursor.fetchall()


    def __getEnturno(self):
        string_turno = ""
        string_turno += str(self.__jugador_en_turno.identificador)+", "
        return string_turno

    def __getCreador(self):
        string_creador = ""
        string_creador += str(self.__creador.identificador) +", "
        return string_creador

    def __cifradoTablero(self):
        string_cifrado = "'"
        for i in range(0,7):
            for j in range(0,6):
                if self.__tablero[i][j]==Fore.RED:
                    string_cifrado += "R"
                elif self.__tablero[i][j]== Fore.YELLOW:
                    string_cifrado += "Y"
                else:
                    string_cifrado += "B"
        string_cifrado += "' ,"
        return string_cifrado

    def __cambiodeJugador(self):
        if self.__jugador_en_turno == self.__Jugador2:
            self.__jugador_en_turno = self.__creador
        else:
            self.__jugador_en_turno = self.__Jugador2

    def __revisarEmpate(self):
        contador = 0
        for i in range(0,7):
            for j in range(0,6):
                if self.__tablero[i][j]== Fore.BLACK:
                    contador += 1
        if contador == 0:
            return True#Si hay empate
        else:
            return False#NO lo hay

    def jugar(self):
        contador = 0
        ultimo = False
        while ultimo ==False:
            self.imprimir()
            eleccion = input("Agrega en la columna que tu quieras\nPresiona 1 para guardar la partida\n")
            ultimo,repeticion = self.agregar(eleccion, self.__jugador_en_turno)
            if repeticion == True:
                self.__cambiodeJugador()
                contador += 1
            if contador == 42:
                ultimo = True
            #ultimo = self.__revisarEmpate()
        self.imprimir()
        self.__cambiodeJugador()
        seleccion = input("Partida terminada, deseas guardar?(y/no= aprieta cualquier otra tecla)\n").lower()
        if seleccion == "y":
            self.guardar()
        if self.__revisarEmpate() == True:
            print("No hubo ganadores")
        else:
            print("Ganador " + self.__jugador_en_turno.getNombre())


    def agregar(self,argument, jugador):
        arg = argument.lower()
        #print("Agrega tu eleccion:\n")
        repeticion = False
        if arg == 'a':
            repeticion, linea = self.__revisa_agrega(0,jugador.getColor())
            columna = 0
        elif arg == 'b':
            repeticion, linea = self.__revisa_agrega(1,jugador.getColor())
            columna = 1
        elif arg == 'c':
            repeticion, linea = self.__revisa_agrega(2,jugador.getColor())
            columna = 2
        elif arg == 'd':
            repeticion, linea = self.__revisa_agrega(3,jugador.getColor())
            columna = 3
        elif arg == 'e':
            repeticion, linea = self.__revisa_agrega(4,jugador.getColor())
            columna = 4
        elif arg == 'f':
            repeticion, linea = self.__revisa_agrega(5,jugador.getColor())
            columna = 5
        elif arg == '1':
            print("Opcion de guardado")
            self.__cambiodeJugador()
            self.guardar()
            repeticion = False
            linea, columna = -1,-1
            print("Partida guardada")
        else:
            "Opcion no valida, ingresa una nueva"
            linea, columna = -1,-1
            repeticion = False
        if self.__verMovimiento(linea, columna, jugador.getColor()) == True and arg != "1":
            #print("Ganaste")
            return True, True
        return False, repeticion


    def __verMovimiento(self, fila, columna,color):
        if fila-3 >= 0:#revisamos
            if self.__tablero[fila][columna]==color and self.__tablero[fila-1][columna]==color and self.__tablero[fila-2][columna]==color and self.__tablero[fila-3][columna]==color:
                return True

                #print("Si se cumplio")
        for r in range(0,4):#revisa diagonalmente con combinados
            if fila+r-3 >= 0 and fila+r >= 0 and fila+r < 7 and columna-r+3 >= 0 and columna+r+3 >= 0 and columna+r+3 < 6:#esto pregunta si existen las 4 diagonales
                if self.__tablero[fila+r-3][columna-r+3]==color and self.__tablero[fila+r-2][columna-r+2]==color and self.__tablero[fila+r-1][columna-r+1]==color and self.__tablero[fila+r][columna-r]==color:#pregunta si son las mismas
                    return True
                    #print("Si se cumplio")
            #revisa diagonalmente positivos
            if fila+r-3 >= 0 and fila+r >= 0 and fila+r < 7 and columna+r-3 >= 0 and columna+r >= 0 and columna+r < 6:
                if self.__tablero[fila+r-3][columna+r-3]==color and self.__tablero[fila+r-2][columna+r-2]==color and self.__tablero[fila+r-1][columna+r-1]==color and self.__tablero[fila+r][columna+r]==color:
                    return True

            if columna+r-3 >= 0 and columna+r < 6:
                if self.__tablero[fila][columna+r-3] == color and self.__tablero[fila][columna+r-2]==color and self.__tablero[fila][columna+r-1] == color and self.__tablero[fila][columna+r]== color:
                    return True
                    #print("Si se cumplio")
        return False


    def __revisa_agrega(self, columna, color):
        for row in range(0,7):
            if self.__tablero[row][columna] == Fore.BLACK:#revisa si esta vacio el espacio
                self.__tablero[row][columna] = color
                return True, row
        print("Columna llena, ingresa en otra")
        time.sleep(1)
        return False, 0#regresa esto, significa que no se pudo agregar porque la columna ya esta llena

    def imprimir(self):
        tmp = sp.call('clear',shell=True)
        print("Tu turno " + self.__jugador_en_turno.getNombre())
        bl = Fore.BLACK
        g = Fore.GREEN
        b = Fore.BLUE
        r = Fore.RESET
        print(g + "               A               B               C               D               E               F               " + r)
        print(b + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++" + r + self.__tablero[6][0] + "O" + b + "+++++++++++++++" + r + self.__tablero[6][1] + "O" + b + "+++++++++++++++" +
        r + self.__tablero[6][2] + "O" + b + "+++++++++++++++" + r + self.__tablero[6][3] + "O" + b + "+++++++++++++++" + r +
        self.__tablero[6][4] + "O" + b + "+++++++++++++++" + r + self.__tablero[6][5] + "O" + b + "++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++" + r + self.__tablero[5][0] + "O" + b + "+++++++++++++++" + r + self.__tablero[5][1] + "O" + b + "+++++++++++++++" +
        r + self.__tablero[5][2] + "O" + b + "+++++++++++++++" + r + self.__tablero[5][3] + "O" + b + "+++++++++++++++" + r +
        self.__tablero[5][4] + "O" + b + "+++++++++++++++" + r + self.__tablero[5][5] + "O" + b + "++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++" + r + self.__tablero[4][0] + "O" + b + "+++++++++++++++" + r + self.__tablero[4][1] + "O" + b + "+++++++++++++++" +
        r + self.__tablero[4][2] + "O" + b + "+++++++++++++++" + r + self.__tablero[4][3] + "O" + b + "+++++++++++++++" + r +
        self.__tablero[4][4] + "O" + b + "+++++++++++++++" + r + self.__tablero[4][5] + "O" + b + "++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++" + r + self.__tablero[3][0] + "O" + b + "+++++++++++++++" + r + self.__tablero[3][1] + "O" + b + "+++++++++++++++" +
        r + self.__tablero[3][2] + "O" + b + "+++++++++++++++" + r + self.__tablero[3][3] + "O" + b + "+++++++++++++++" + r +
        self.__tablero[3][4] + "O" + b + "+++++++++++++++" + r + self.__tablero[3][5] + "O" + b + "++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++" + r + self.__tablero[2][0] + "O" + b + "+++++++++++++++" + r + self.__tablero[2][1] + "O" + b + "+++++++++++++++" +
        r + self.__tablero[2][2] + "O" + b + "+++++++++++++++" + r + self.__tablero[2][3] + "O" + b + "+++++++++++++++" + r +
        self.__tablero[2][4] + "O" + b + "+++++++++++++++" + r + self.__tablero[2][5] + "O" + b + "++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++" + r + self.__tablero[1][0] + "O" + b + "+++++++++++++++" + r + self.__tablero[1][1] + "O" + b + "+++++++++++++++" +
        r + self.__tablero[1][2] + "O" + b + "+++++++++++++++" + r + self.__tablero[1][3] + "O" + b + "+++++++++++++++" + r +
        self.__tablero[1][4] + "O" + b + "+++++++++++++++" + r + self.__tablero[1][5] + "O" + b + "++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++" + r + self.__tablero[0][0] + "O" + b + "+++++++++++++++" + r + self.__tablero[0][1] + "O" + b + "+++++++++++++++" +
        r + self.__tablero[0][2] + "O" + b + "+++++++++++++++" + r + self.__tablero[0][3] + "O" + b + "+++++++++++++++" + r +
        self.__tablero[0][4] + "O" + b + "+++++++++++++++" + r + self.__tablero[0][5] + "O" + b + "++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"+r)
