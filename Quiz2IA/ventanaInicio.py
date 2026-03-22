import tkinter as tk


from ventanaProblemaPropio import propio
from ventanaImagen import imagen


# Configuración de la Ventana
def ventanaInicio():
    ventana = tk.Tk()

    ventana.geometry("1000x600")
    ventana.resizable(False,False)
    ventana.configure(bg= "chocolate3")
    ventana.iconbitmap("iconCacao.ico")
    ventana.title("Algoritmo Genetico")
    ventana.attributes("-alpha", 0.9)

    frameInicio = tk.Frame(ventana)
    frameInicio.configure(bg="chocolate3", width=1000, height=600)

    #Titulo de la pagina de Inicio

    tituloInicio = tk.Label(frameInicio, text="""     Algoritmos Geneticos
        Ingrese en alguna de las Opciones para gestionar sus Algoritmos""", font=("georgia", 20), fg="black", bg="chocolate3")

   
   #Botones de la Pagina de Inicio
    botonSE = tk.Button(frameInicio, text= "Problema Propio", command= lambda: propio(ventana), bg="lawn green", width=20)
    botonLD = tk.Button(frameInicio, text= "Imagen", command= lambda: imagen(ventana), bg="lawn green", width=20)
    botonSalir = tk.Button(frameInicio, text= "Salir", command= lambda:ventana.destroy() , bg="red", width=20)



    frameInicio.pack()
    tituloInicio.place(rely=0.25, relx= 0.5, anchor="center")
    botonSE.place(rely=0.5, relx= 0.5, anchor= "center")
    botonLD.place(rely=0.65, relx= 0.5, anchor= "center")
    botonSalir.place(rely=.8, relx= 0.5, anchor="center")
    ventana.mainloop()



if __name__ == '__main__':
    ventanaInicio()