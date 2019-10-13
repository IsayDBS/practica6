#from termcolor import colored
import subprocess as sp
from colorama import *
#from Bcolors import *
class Juego():
    def __init__(self, jugador1 = None, jugador2 = None, tablero=[]):
        self.__Jugador1 = jugador1
        self.__Jugador2 = jugador2
        #tablero es una lista de listas = [[],[],[],[],[],[]]
        #donde cada lista representa el renglon
        self.__tablero = tablero

    def imprimir(self):
        tmp = sp.call('clear',shell=True)
        g = Fore.GREEN
        b = Fore.BLUE
        r = Fore.RESET
        print(g + "    A     B     C     D     E     F     G    " + r)
        print(b + "+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + + " + r + "X" + b + " + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +")
        print("+ + + + + + + + + + + + + + + + + + + + + + +" + r)


if __name__ == '__main__':
    clase = Juego()
    clase.imprimir()
