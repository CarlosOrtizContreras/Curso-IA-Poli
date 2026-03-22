import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import numpy as np
import random as rd


def propio(ventana):
    pantallaFD = tk.Toplevel(ventana, height=750, width=1200, bg="coral1")
    pantallaFD.title("Algoritmo Genetico para la Evaluacion de Parcelaciones")
    pantallaFD.resizable(False, False)
    pantallaFD.iconbitmap("iconCacao.ico")
    pantallaFD.attributes("-alpha", 0.95)

    frameFD = tk.Frame(pantallaFD, bg="coral1", width=1200, height=750)
    frameFD.pack()
    frameFD.pack_propagate(False)

    # Titulo 
    tituloFD = tk.Label(frameFD,
                        text="Algoritmo Genetico para la Evaluacion de Parcelaciones",
                        font=("georgia", 20),
                        bg="coral1")
    tituloFD.place(rely=.05, relx=.5, anchor="center")

 
    # INTERFAZ DE ENTRADA
    
    tk.Label(frameFD, text="Generaciones", bg="coral1").place(rely=.15, relx=.2, anchor="center")
    entrada_generaciones = tk.Entry(frameFD)
    entrada_generaciones.place(rely=.2, relx=.2, anchor="center")
    
    tk.Label(frameFD, text="Tamaño de la Poblacion", bg="coral1").place(rely=.28, relx=.2, anchor="center")
    entrada_poblacion = tk.Entry(frameFD)
    entrada_poblacion.place(rely=.33, relx=.2, anchor="center")

    tk.Label(frameFD, text="Probabilidad de Mutacion", bg="coral1").place(rely=.40, relx=.2, anchor="center")
    entrada_probabilidad = tk.Scale(frameFD, from_=0.1, to=0.99, resolution=0.02, orient="horizontal", length=300, bg="coral1")
    entrada_probabilidad.place(rely=.44, relx=.2, anchor="center")
    
    tk.Label(frameFD, text="Cantidad de Parcelaciones", bg="coral1").place(rely=.48, relx=.2, anchor="center")
    entrada_parcelaciones = tk.Scale(frameFD, from_=8, to=20, resolution=1, orient="horizontal", length=300, bg="coral1")
    entrada_parcelaciones.place(rely=.52, relx=.2, anchor="center")
    
    
   
    # SCROLLED TEXT PARA RESULTADOS
    
    salidaTexto = ScrolledText(frameFD)
    salidaTexto.configure(
    width=70,
    height=25,
    wrap= "word")

    salidaTexto.place(
    relx=0.65,
    rely=0.4,
    anchor="center"
)


    # FUNCIONES

    def ejecutar():
        salidaTexto.delete("1.0", tk.END)
        salidaTexto.insert(tk.END, f"--- RESULTADOS DEL ANALISIS ---\n\n")
        salidaTexto.insert(tk.END, f"--- Datos para ser Parcelacion Optima ---\n") 
        salidaTexto.insert(tk.END, f"Produccion Minima 30\nAbono maximo 50\nGastos Maximos 30\n\n") 

        numeroParcelas = int(entrada_parcelaciones.get())
        datos = datosParcelas(numeroParcelas)
        tamano = int(entrada_poblacion.get())
        poblacion= getPoblacionInicial(tamano, numeroParcelas)
        probabildad= float(entrada_probabilidad.get())
        generaciones = int (entrada_generaciones.get())

        salidaTexto.insert(tk.END, f"--- POBLACIÓN INICIAL ---\n") 
        verLista(poblacion)



        for i in range (generaciones):
            listaValorados = [(fitness(individuo, datos), individuo) for individuo in poblacion]
            listaValorados.sort(reverse=True)

            padres = [dato for _, dato in listaValorados[:2]]

            poblacion = realizarCruce(padres,poblacion,numeroParcelas)
            poblacion = realizarMutacion(poblacion, probabildad, numeroParcelas)


        produccion, gastos, abono = analisis(listaValorados[0][1], datos)
        salidaTexto.insert(tk.END, f"--- POBLACIÓN FINAL ---\n") 
        verLista(listaValorados)

        salidaTexto.insert(tk.END, f"\nMejor parcela luego de {generaciones} generaciones, con un gasto de {gastos}, consumo de abono de {abono} y una produccion de {produccion} es: \n") 
        salidaTexto.insert(tk.END, f"{listaValorados[0][1]} \n") 
       





    # BOTONES

    botonCalcular = tk.Button(frameFD, text="Ejecutar", bg="green", width=20, command=ejecutar)
    botonMenu = tk.Button(frameFD, text="Menu Inicial", bg="yellow", width=20, command=pantallaFD.destroy)

    botonCalcular.place(rely=.7, relx=.3, anchor="center")
    botonMenu.place(rely=.7, relx=.7, anchor="center")


    def getIndividuo(numeroParcelas: int):
        opciones = [0,1]
        individuo = []
        for i in range(0, numeroParcelas):
            individuo.append(rd.choice(opciones))
        return individuo
    
    def getPoblacionInicial(tamano, numeroParcelas):
        opciones = [0,1]
        return [getIndividuo(numeroParcelas) for i in range(0, tamano)]
    
    def verLista(lista):
        for i in lista:
            salidaTexto.insert(tk.END, f" {i} \n")
      
    
    def realizarCruce(padres, poblacion, numeroParcelas):
        for i in range(0, len(poblacion)):
            hijo = []
            corte = rd.randint(0,numeroParcelas-1)
            hijo[:corte] = padres[0][:corte]
            hijo[corte:] = padres[1][corte:]
            poblacion[i] = hijo
        return poblacion
    
    def realizarMutacion(poblacion, probabilidad, numeroParcelas): 
        for i in range(0, len(poblacion)): 
            if rd.random() <= probabilidad: 
                posicion = rd.randint(0,numeroParcelas-1) 
                if poblacion[i][posicion] == 0:
                    poblacion[i][posicion] = 1 
                
                else: 
                    poblacion[i][posicion] = 0 
    
        return poblacion
        
    def datosParcelas(numeroParcelas):
        datos = [(rd.randint(1,10), rd.randint(1,15), rd.randint(3,15)) for i in range (numeroParcelas)]

        salidaTexto.insert(tk.END, f"--- DATOS DE LAS PARCELACIONES ---\n") 
        texGastos ="Gastos: \n"
        texAbono = "Abono: \n"
        texProduccion="Produccion: \n"

        for i in datos:
            texGastos += f"{i[0]}  "
            texAbono += f"{i[1]}  "
            texProduccion += f"{i[2]}  "

        salidaTexto.insert(tk.END, f"{texGastos}\n{texAbono}\n{texProduccion}\n\n") 
        return datos
    
    def fitness(individuo, datos):
        abonoMaximo = 50
        gastosMaximo = 30
        ProduccionMinima =30
        
        produccion, gastos, abono = analisis(individuo, datos)

        if gastos>gastosMaximo or abono >abonoMaximo or produccion< ProduccionMinima:
            return 0
        else:
            return produccion
        
    def analisis(individuo, datos):
        produccion = 0
        gastos= 0
        abono= 0

        for i, dato in enumerate(individuo):
            if dato == 1:
                gastos += datos[i][0]
                abono += datos[i][1]
                produccion += datos[i][2]
        
        return produccion, gastos, abono