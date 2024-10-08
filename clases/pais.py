# import xlwings as xw
import random
import numpy as np
import pandas as pd
import folium 
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt

from clases.alg_gen import AlgoritmoGenetico


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
        elif opcionMenu == 2:
            m.save(f'mapa_2_{secuencia_viaje[0]}.html')
        else:
            m.save(f'mapa_3_{secuencia_viaje[0]}.html')
    
    def generarGrafico(self, serie, tipo_grafica, elitismo):
        plt.figure(figsize=(10, 6))
        plt.plot(serie)
        plt.title('Convergencia del Algoritmo Genético')
        plt.xlabel('Generación')
        plt.grid(True)
        if tipo_grafica == "fitness":
            plt.ylabel('Fitness (1/distancia)')
            if elitismo:
                plt.savefig('grafico_fitness_elitismo.png')
            plt.savefig('grafico_fitness.png')
        elif tipo_grafica == "distancias":
            plt.ylabel('Distancia (km)') 
            if elitismo:
                plt.savefig('grafico_distancias_elitismo.png')
            plt.savefig('grafico_distancias.png')
        plt.close()
           
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
        
    # def calcularRutaMinimaGeneticoElitismo(self):
    #     print("Calculando distancia minima con algoritmos geneticos")
        
    #     #Parametros
    #     tamanoPoblacion = 50
    #     cantidadCorridas = 200
    #     probabilidadMutacion = 0.05
    #     probabilidadCrossover = 0.75
    #     porcentajeElitismo = 0.20
        
    #     def crear_individuo():
    #         # Crea una permutación de números del 1 al 24
    #         cromosoma = list(range(24)) #de 0 a 23
    #         random.shuffle(cromosoma)
    #         return cromosoma
        
    #     def crear_poblacion_inicial(tamanoPoblacion):
    #         return [crear_individuo() for _ in range(tamanoPoblacion)]
        
    #     def calcular_fitness(individuo):
    #         # Calcula la distancia total del recorrido
    #         distancia_total = 0
    #         for i in range(len(individuo)-1):
    #             ciudad_actual = individuo[i]
    #             ciudad_siguiente = individuo[i + 1]
    #             distancia_total += float(self.distancias.iloc[ciudad_actual, ciudad_siguiente+1])
                
    #         # print("Sin retorno: ", distancia_total)
    #         retorno = float(self.distancias.iloc[individuo[-1], individuo[0]+1])
    #         # print("Retorno: ",retorno)
            
    #         distancia_total += retorno   # Agregar distancia de retorno al origen
    #         fitness = 1 / distancia_total
            
    #         print("Individuo:", individuo," - Distancia total: ", distancia_total," - Fitness: ",fitness)
    #         # print("Distancia total: ", distancia_total)
    #         # print("Fitness: ",fitness)  # A mayor fitness, mejor. (menor distancia)
            
    #         return fitness
        
    #     def seleccion_ruleta(poblacion, fitness_poblacion):
    #         fitness_total = sum(fitness_poblacion)  # Fitness_total es la ruleta completa
    #         valor_ruleta = random.uniform(0, fitness_total)  # Giro de ruleta
    #         suma_actual = 0
    #         for i, individuo in enumerate(poblacion):  # Se acumula hasta saber que individuo resultó seleccionado 
    #             suma_actual += fitness_poblacion[i]
    #             if suma_actual > valor_ruleta:
    #                 return individuo.copy()  #copy para no hacer lio con las referencias
    #         return poblacion[-1].copy()  # En caso de problemas de redondeo
        
        
    #     def crossover(padre1, padre2):
    #         if random.random() > probabilidadCrossover:  #No hay crossover
    #             print("no hay crossover")
    #             return padre1.copy()
            
    #         def cyclic_crossover(p1, p2): 
    #             n = len(p1)
    #             hijo = [-1] * n  # -1 representa posiciones no ocupadas
    #             elementos_usados = set()  # Conjunto para guardar las ciudades ya utilizadas
                
    #             # Empezamos con el primer elemento del padre1
    #             inicio = 0
    #             index = inicio
                
    #             # Primer ciclo
    #             while True:
    #                 # Copiamos el elemento del padre1 al hijo
    #                 hijo[index] = p1[index]
    #                 elementos_usados.add(p1[index])
    #                 # Encontramos el valor correspondiente en padre2
    #                 valor = p2[index]
    #                 # Buscamos dónde está ese valor en padre1
    #                 index = p1.index(valor)
    #                 # Si volvimos al inicio, terminamos el ciclo
    #                 if index == inicio:
    #                     break
    #             # Rellenamos las posiciones restantes con elementos del padre2
    #             # que no hayan sido usados
    #             for i in range(n):
    #                 if hijo[i] == -1:  # Posición vacía
    #                     if p2[i] not in elementos_usados:
    #                         hijo[i] = p2[i]
    #                         elementos_usados.add(p2[i])
    #                     else:
    #                         # Si el elemento de p2 ya está usado, buscamos el primer elemento disponible que no se haya usado
    #                         for elemento in range(n):
    #                             if elemento not in elementos_usados:
    #                                 hijo[i] = elemento
    #                                 elementos_usados.add(elemento)
    #                                 break
                
    #             return hijo
            
    #         hijo1 = cyclic_crossover(padre1, padre2)
    #         return hijo1
    
    #     def mutacion(individuo):
    #         if random.random() < probabilidadMutacion:
    #             i, j = random.sample(range(len(individuo)), 2) #seleccion de dos índices aleatorios distintos del individuo
    #             individuo[i], individuo[j] = individuo[j], individuo[i] # intercambio de los elementos en las posiciones i y j.
            
    #         print("no hay mutacion")
    #         return individuo   
        
    #     def verificar_validez_individuo(individuo):
    #         # Verifica que el individuo sea una permutación válida
    #         numeros = sorted(individuo)
    #         return numeros == list(range(24))
        
    #     #! Algoritmo principal
        
    #     poblacion = crear_poblacion_inicial(tamanoPoblacion)
    #     print("--------------------------------------------------------------------")
    #     print("Población inicial: ")
    #     for  individuo in poblacion:
    #         print(individuo)
    #     print("--------------------------------------------------------------------")
        
    #     # Lista para almacenar el progreso del fitness
    #     historial_fitness = []
    #     # Lista para almacenar el progreso de las distancias
    #     historial_distancias = []     
        
    #     print("\nIniciando algoritmo genético...")
    #     print("-----------------------------------")
        
    #     for generacion in range(cantidadCorridas):
        
    #         # Calcular fitness de la población
    #         fitness_poblacion = [calcular_fitness(ind) for ind in poblacion]
            
    #         individuos_ordenados = sorted(zip(poblacion, fitness_poblacion), key=lambda x: x[1], reverse=True)
            
    #         print("\n Individuos ordenados: ", individuos_ordenados)
    #         cantidad_elites = int(tamanoPoblacion * porcentajeElitismo)
    #         print("Cantidad elites: ",cantidad_elites)
    #         elites = [individuo for individuo, fitness in individuos_ordenados[:cantidad_elites]]
    #         print("Elites: ",elites)
           
    #         # Crear nueva población, comenzando con los individuos elites
    #         nueva_poblacion = [ind[0].copy() for ind in individuos_ordenados[:cantidad_elites]]
    
    #         print("Nueva poblacion antes de reproduccion: ",nueva_poblacion)
    #         print("------------")
            
    #         # Crear el resto de la población mediante selección, crossover y mutación
    #         while len(nueva_poblacion) < tamanoPoblacion:
    #             padre1 = seleccion_ruleta(poblacion, fitness_poblacion)
    #             padre2 = seleccion_ruleta(poblacion, fitness_poblacion)
    #             print("\nRULETA")
    #             print("Padre 1: ",padre1," - Padre 2: ",padre2)

    #             hijo = crossover(padre1, padre2)
    #             print("--Crossover--")
    #             print("Hijo crossover: ",hijo)
               
    #             hijo = mutacion(hijo)
    #             print("--Mutacion--")
    #             print("Hijo mutado: ",hijo)
                
    #             print("\nHIJO: ",hijo)
                
    #             if verificar_validez_individuo(hijo):# and verificar_validez_individuo(hijo2):
    #                 nueva_poblacion.append(hijo)
    #                 # print("Nueva poblacion: ")
    #                 # for individuo in nueva_poblacion:
    #                 #     print(individuo) 
            
    #         print("------------------------------------------")
    #         print("\n\nNueva poblacion post reproduccion: ")
    #         for individuo in nueva_poblacion:
    #             print(individuo)
            
    #         # Aseguramos que la nueva población mantenga el tamaño correcto
    #         poblacion = nueva_poblacion[:tamanoPoblacion]

    #         # Actualizar mejor fitness
    #         mejor_fitness_actual = max(fitness_poblacion)
    #         historial_fitness.append(mejor_fitness_actual)
    #         historial_distancias.append(1/mejor_fitness_actual)
            
    #         print("\nHistorial distancias: ",historial_distancias)
    #         print("Historial fitness: ",historial_fitness)
    #         print(f"Generación {generacion+1}: Mejor distancia = {1/mejor_fitness_actual:.2f} km")
    #         print("---------------------------------------------------------------------------------------------------------")
            
        
    #      # Convertir índices a nombres de ciudades
    #     mejor_ruta = [self.ciudades[i] for i in individuos_ordenados[0][0]]
    #     mejor_ruta.append(mejor_ruta[0])
    #     distancia_total = 1 / individuos_ordenados[0][1]
        
    #     print("\n -------------------------------------------FIN-------------------------------------------------------")
    #     print(f"Menor recorrido encontrado: {distancia_total:.2f} km")
    #     print("Origen:", mejor_ruta[0])
    #     print("Secuencia de viaje:", mejor_ruta)
    #     print("----------------------------------------\n")
        
    #      # Generar mapa
    #     self.generarMapa(mejor_ruta, 3)
        
    #     # Genera gráficos
    #     self.generarGrafico(historial_distancias,"distancias")
    #     self.generarGrafico(historial_fitness,"fitness")

    def calcularRutaMinimaGenetico(self, usar_elitismo=True):
        ag = AlgoritmoGenetico(self.distancias, self.ciudades)  #instancia del algoritmo
        resultado = ag.ejecutar(usar_elitismo)
    
        print("\n-------------------------------FIN----------------------------")
        print(f"Menor recorrido encontrado: {resultado['distancia_total']:.2f} km")
        print("Origen:", resultado['mejor_ruta'][0])
        print("Secuencia de viaje:", resultado['mejor_ruta'])
        print("-----------------------------------------------------------------\n")
    
        # Generar mapa
        self.generarMapa(resultado['mejor_ruta'], 3)
        
        # Genera gráficos
        self.generarGrafico(resultado['historial_distancias'], "distancias",usar_elitismo)
        self.generarGrafico(resultado['historial_fitness'], "fitness",usar_elitismo)

        #TODO PONER TIEMPOS DE EJECUCION.