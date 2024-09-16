# import xlwings as xw
import pandas as pd
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
        for i in self.distancias:
            print(i)
    
    def calcularDistanciaMinima(self, ciudadOrigen):
        print("calculando distancia minima")
        print(ciudadOrigen)

