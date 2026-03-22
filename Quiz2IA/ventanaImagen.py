import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import numpy as np
import random as rd

RUTA_IMAGEN = "mario.png"

def imagen(ventana):
   
    pantallaFD = tk.Toplevel(ventana, height=750, width=1200, bg="coral1")
    pantallaFD.title("Algoritmo Genetico")
    pantallaFD.resizable(False, False)
    pantallaFD.iconbitmap("iconCacao.ico")
    pantallaFD.attributes("-alpha", 0.95)

    frameFD = tk.Frame(pantallaFD, bg="coral1", width=1200, height=750)
    frameFD.pack()
    frameFD.pack_propagate(False)

    # Titulo 
    tituloFD = tk.Label(frameFD,
                        text="Algoritmo Genetico, Procesamiento de Imagen",
                        font=("georgia", 20),
                        bg="coral1")
    tituloFD.place(rely=.05, relx=.5, anchor="center")

    
    
    tk.Label(frameFD, text="Generaciones", bg="coral1").place(rely=.15, relx=.2, anchor="center")
    entrada_generaciones = tk.Entry(frameFD)
    entrada_generaciones.place(rely=.2, relx=.2, anchor="center")
    
    tk.Label(frameFD, text="Probabilidad de Mutacion", bg="coral1").place(rely=.40, relx=.2, anchor="center")
    entrada_probabilidad = tk.Scale(frameFD, from_=0.1, to=0.99, resolution=0.02, orient="horizontal", length=300, bg="coral1")
    entrada_probabilidad.place(rely=.44, relx=.2, anchor="center")
    
    tk.Label(frameFD, text="Tamaño de la Poblacion", bg="coral1").place(rely=.28, relx=.2, anchor="center")
    entrada_poblacion = tk.Entry(frameFD)
    entrada_poblacion.place(rely=.33, relx=.2, anchor="center")

    tk.Label(frameFD, text="Original", bg="coral1").place(rely=.3, relx=.5, anchor="center")
    original= tk.Label(frameFD, bg="coral1")
    original.place(relx=0.7, rely=0.3, anchor="center")

    tk.Label(frameFD, text="Generada", bg="coral1").place(rely=.7, relx=.5, anchor="center")
    generada= tk.Label(frameFD, bg="coral1")
    generada.place(relx=0.7, rely=0.7, anchor="center")
    # FUNCIONES

  
    def ejecutar():
        generaciones=  int(entrada_generaciones.get())
        probabilidad=  float(entrada_probabilidad.get())
        tamanoPoblacion = int(entrada_poblacion.get())

        img = Image.open(RUTA_IMAGEN).convert("RGB")
        img_tk = ImageTk.PhotoImage(img)

        original.config(image= img_tk)
        original.img = img_tk
        frameFD.update()

        img_array = np.array(img)

        poblacion = getPoblacion(tamanoPoblacion,img_array)
        padres =[]
        

        for k in range(generaciones):
            listaValorados = [(fitness(individuo, img_array), individuo) for individuo in poblacion]
            listaValorados.sort(key=lambda x: x[0])

            padres = [dato for _, dato in listaValorados[:2]]

            poblacion = cruce(padres, poblacion)
            poblacion = mutacion(poblacion,img_array, probabilidad)

         
        
        actualizarImagen(padres[0])

    def actualizarImagen (array):
        img = Image.fromarray(array.astype(np.uint8))
        img_tk = ImageTk.PhotoImage(img)

        generada.config(image= img_tk)
        generada.img = img_tk
        frameFD.update()

    def getIndividuo(imagen):
        return np.random.randint(0, 256, size=imagen.shape, dtype=np.uint8)
    
    def getPoblacion (tamano, imagen):
        return [getIndividuo(imagen) for i in range (tamano)]
    
    def cruce(padres: list, poblacion:list):
        hijo = np.zeros_like(padres[0])
        alto, ancho,_ = hijo.shape
        for i in range(len(poblacion)):
            corte = rd.randint(0, ancho -1)

            hijo[:,:corte] = padres[0][:,:corte]
            hijo[:,corte:] = padres[1][:,corte:]
            poblacion[i] = hijo
        
        return poblacion


    def mutacion(poblacion, original, probabilidad, intensidad=10, umbral=5):
        for i in range(len(poblacion)):
            imagen = poblacion[i].astype(np.float32)

            mask = np.random.rand(*imagen.shape[:2]) < probabilidad
            mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)

            # diferencia con la imagen original
            diferencia = np.abs(imagen - original)

            mask_no_cambiar = diferencia < umbral

            mask_final = mask & (~mask_no_cambiar)

            cambio = np.random.uniform(-intensidad, intensidad, imagen.shape)

            # aplicar mutación
            imagen[mask_final] += cambio[mask_final]

            # limitar valores
            poblacion[i] = np.clip(imagen, 0, 255).astype(np.uint8)

        return poblacion

    def fitness(individuo, original):
        error =0
        diff = individuo.astype(int) - original.astype(int)
        error = np.sum(np.abs(diff))

        return error

    botonCalcular = tk.Button(frameFD, text="Calcular", bg="green", width=20, command=ejecutar)
    botonMenu = tk.Button(frameFD, text="Menu Inicial", bg="yellow", width=20, command=pantallaFD.destroy)

    botonCalcular.place(rely=.7, relx=.2, anchor="center")
    botonMenu.place(rely=.7, relx=.4, anchor="center")