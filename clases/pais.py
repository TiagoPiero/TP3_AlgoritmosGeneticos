# import xlwings as xw
import pandas as pd
from tabulate import tabulate
class pais:
    ciudades = []
    distancias = [] #matriz de distancias entre ciudades

    def __init__(self):
        df = pd.read_excel('clases\TablaCapitales.xlsx')
        df_ciudad = df.iloc[:0,1:25]
        self.ciudades = df_ciudad.columns
        df_distancias = df.iloc[:24,:25]
        self.distancias = df_distancias

    def mostrarCiudades(self):
        for i in self.ciudades:
            print(i)

    def mostrarDistancias(self):
        print(self.distancias)
    
    def calculaDistanciasDadaCiudad(self, indiceCiudad):
        return self.distancias.iloc[indiceCiudad]

    def calcularDistanciaMinima(self, indexCiudad):
        sumaKilometros = 0
        ciudad = self.ciudades[indexCiudad]
        print("calculando distancia minima")
        ciudad_distancias = self.calculaDistanciasDadaCiudad(indexCiudad)
        print(ciudad_distancias)
        secuencia_viaje = []
        secuencia_viaje.append(ciudad)
    
        for i in range(len(self.ciudades)-1):
            listDistancias = []
            count = 1
            for j in self.ciudades:
                if(j in secuencia_viaje):
                    listDistancias.append(10000000) #esto es para que no se tome en cuenta la ciudad que ya se visitó
                else:
                    print(ciudad_distancias)
                    listDistancias.append(ciudad_distancias.iloc[count]) 
                count = count + 1

            print("listDistancias: ",listDistancias)
            min_valor = min(listDistancias)
            print("minimo: ",min_valor)

            for k in range(len(listDistancias)):
                if(listDistancias[k] == min_valor):
                    sumaKilometros = sumaKilometros + listDistancias[k]
                    secuencia_viaje.append(self.ciudades[k])
                    ciudad_distancias = self.calculaDistanciasDadaCiudad(k) #esto esta bien,ya corroboré
                    print("distancias desde la ciudad: ",self.ciudades[k], "son: ",ciudad_distancias)
                    indexCiudad = k
                    break
        print("----------------------------------------------------------------------")
        print("Secuencia de viaje: ",secuencia_viaje)
        print("----------------------------------------------------------------------")
        print("----------------------------------------------------------------------")
        print("Distancia total recorrida: ",sumaKilometros,"km")


