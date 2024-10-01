# import xlwings as xw
import pandas as pd
import folium 
from geopy.geocoders import Nominatim

class pais:
    ciudades = []
    distancias = [] #matriz de distancias entre ciudades
    coordenadas = [] #coordenadas de las ciudades
    def __init__(self):
        df = pd.read_excel('clases/TablaCapitales.xlsx')
        df_ciudad = df.iloc[:0,1:25]
        self.ciudades = df_ciudad.columns
        df_distancias = df.iloc[:24,:25]
        self.distancias = df_distancias

        #latitud y longitud de las ciudades
        geolocator = Nominatim(user_agent="geolocalizacionCiudadesAG", timeout=5)
        for i in self.ciudades:
           location = geolocator.geocode('Argentina,'+i)
           if(location != None):
               rowCiudadLocation = [i,location.latitude,location.longitude]
               self.coordenadas.append(rowCiudadLocation) 
        # print(len(self.coordenadas))

    def generarMapa(self, secuencia_viaje, opcionMenu):
        m = folium.Map(
                location=[-31.431276116867238, -64.19324578122779],
                zoom_start=0,
                )
        for i in self.coordenadas:
            folium.Marker([i[1],i[2]], popup=i[0]).add_to(m)
        
        soloCoordenadas = []
        for i in secuencia_viaje:
            for j in self.coordenadas:
                if(i == j[0]):
                    soloCoordenadas.append([j[1],j[2]])
                    break
        folium.PolyLine(locations=soloCoordenadas, color="red", weight=2.5, opacity=1).add_to(m)
        # folium.PolyLine(locations=self.coordenadas, color="red", weight=2.5, opacity=1).add_to(m)
        
        if opcionMenu == 1:
            m.save(f'mapa_{secuencia_viaje[0]}.html')
        else:
            m.save(f'mapa2_{secuencia_viaje[0]}.html')
    
    def mostrarCiudades(self):
        for i in self.ciudades:
            print(i)

    def mostrarDistancias(self):
        print(self.distancias)
    
    def calculaDistanciasDadaCiudad(self, indiceCiudad): #devuelve las distancias de todas las ciudades respecto a una ciudad dada
        return self.distancias.iloc[indiceCiudad]

    def calcularDistanciaMinima(self, indexCiudad,opcionMenu):
        sumaKilometros = 0
        indicePrimeraCiudad = indexCiudad
        indiceUltimaCiudad = -1
        ciudad = self.ciudades[indexCiudad]
        ciudad_distancias = self.calculaDistanciasDadaCiudad(indexCiudad)
        # print(ciudad_distancias)
        secuencia_viaje = []
        secuencia_viaje.append(ciudad)
    
        for i in range(len(self.ciudades)-1):
            listDistancias = []
            count = 1
            for j in self.ciudades:
                if(j in secuencia_viaje):
                    listDistancias.append(10000000) #esto es para que no se tome en cuenta la ciudad que ya se visitó
                else:
                    # print(ciudad_distancias)
                    listDistancias.append(ciudad_distancias.iloc[count]) 
                count = count + 1

            # print("listDistancias: ",listDistancias)
            min_valor = min(listDistancias)
            # print("minimo: ",min_valor)

            #en este punto tenemos una ciudad y las distancias de las ciudades que no se visitaron
            
            index = listDistancias.index(min_valor) #indice de la ciudad con la distancia minima
            sumaKilometros = sumaKilometros + min_valor
            secuencia_viaje.append(self.ciudades[index])
            ciudad_distancias = self.calculaDistanciasDadaCiudad(index) 
            # print("distancias desde la ciudad: ",self.ciudades[index], "son: ",ciudad_distancias)
            indiceUltimaCiudad = index
        
        #fin del blucle for
        secuencia_viaje.append(secuencia_viaje[0])
        #calcular distancia de retorno
        ciudad_distancias = self.calculaDistanciasDadaCiudad(indicePrimeraCiudad)
        distanciaRetorno = ciudad_distancias.iloc[indiceUltimaCiudad+1]
        # print("distancia de retorno: ",distanciaRetorno)
        sumaKilometros = sumaKilometros + distanciaRetorno
        
        if(opcionMenu == 1):
            
            print("\n----------------------------------------------------------------------")
            print("Origen: ",secuencia_viaje[0])
            print("\nSecuencia de viaje: ",secuencia_viaje)
            print("\nDistancia total recorrida: ",sumaKilometros,"kms")
            print("----------------------------------------------------------------------")
            
            self.generarMapa(secuencia_viaje,opcionMenu)
            
            return
        else:
            return sumaKilometros,secuencia_viaje

    def calcularDistanciaMinimaGenetico(self):
        print("Calculando distancia minima con algoritmos geneticos")
        pass

    def calcularRecorridoMinimo(self,opcionMenu):
        distanciaMenor = 10000000
        secuenciaViaje=[]
        for i in range(23):
            [distanciaR,secuencia] = self.calcularDistanciaMinima(i,opcionMenu)
            print("Distancia de recorrido desde ",self.ciudades[i], ": ",distanciaR," kms")
            if(distanciaR<distanciaMenor):
                distanciaMenor = distanciaR
                secuenciaViaje = secuencia
        self.generarMapa(secuenciaViaje,opcionMenu)
        
        print("\n----------------------------------------")
        print("Menor recorrido: ", distanciaMenor," kms")
        print("Origen: ",secuenciaViaje[0])
        print("Secuencia de viaje: ",secuenciaViaje)
        print("----------------------------------------\n\n")
        
