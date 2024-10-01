#Problema del viajante
from clases import pais



#Funciones
def menu():
    while (True):
        print("1. Ingresar capital")
        print("2. Recorrido minimo")
        print("3. Recorrido minimo con geneticos")
        print("4. Salir")
        option = int(input("Ingrese una opcion: "))
        if(validar_opcion(option)):
            break
    return option

def validar_opcion(option):
    if(option < 1 or option > 4):
        return False
    return True

def ingresar_capital(pais,opcionMenu):
    for i in range(len(pais.ciudades)):
        print(i+1,'-'+pais.ciudades[i])
    while(True):
        opcion = int(input("Ingrese una ciudad (1-24): "))
        if(opcion > 0 and opcion < 25):
            break
    pais.calcularDistanciaMinima(opcion-1,opcionMenu)

def calcular_distancia(pais):
    pais.mostrarDistancias()


#programa principal
while(True):
    option = menu()
    paisInstance = pais.pais()
    if(option == 4):
        break
    if(option == 1):
        ingresar_capital(paisInstance,option)
    if(option == 2):
        paisInstance.calcularRecorridoMinimo(option)
    if(option == 3):
        calcular_distancia(paisInstance)