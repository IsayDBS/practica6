from dotenv import load_dotenv
from os.path import join, dirname, isdir
from os import environ
import mysql.connector
from Registro import *


def conectar():
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


def switch(argument):
    if argument == 1:
        pass
        #print("Partida nueva")
    elif argument == 2:
        print("Elegiste registrarte")
        name = input("Introduce tu nombre de usuario que desees\n")
        test = False
        while test == False:
            password = input("Introduce tu contrasenia\n")
            repassword = input("Vuelve a introducir tu contrasenia\n")
            if password != repassword:
                print("Tus contrasenias no concuerdan, hazlo de nuevo")
            else:
                test = True
        nuevo_registro = Registro(connection, cursor, name, password)
        nuevo_registro.registrar()
        #print("Registrarse")
    elif argument == 3:
        pass
        #print("Cargar partida")
    elif argument == 4:
        pass
        #print("Como se juega")
    else:
        print("Adios")

def main():
    connection, cursor = conectar()
    print("Bienvenido al juego de conecta 4")
    prueba = False
    while prueba == False:
        print("Elige una opcion")
        print("1) Partida nueva")
        print("2) Registrarse")
        print("3) Cargar partida")
        print("4) Como se juega")
        print("0) Salir")
        argumento = int(input())
        switch(argumento)
        if argumento == 0:
            prueba = True
        #except:
        #    print("No es un argumento valido, intenta de nuevo ")


if __name__ == '__main__':
    main()
