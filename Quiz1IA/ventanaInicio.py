import tkinter as tk


from ventanaSistemaExperto import ventanaSE
from ventanaLogicaDifusa import ventanaLD


# Configuración de la Ventana
def ventanaInicio():
    ventana = tk.Tk()

    ventana.geometry("1000x600")
    ventana.resizable(False,False)
    ventana.configure(bg= "chocolate3")
    ventana.iconbitmap("iconCacao.ico")
    ventana.title("Cultivo de Cacao")
    ventana.attributes("-alpha", 0.9)

    frameInicio = tk.Frame(ventana)
    frameInicio.configure(bg="chocolate3", width=1000, height=600)

    #Titulo de la pagina de Inicio

    tituloInicio = tk.Label(frameInicio, text="""     Cultivo de Cacao
            Ingrese en alguna de las Opciones para gestionar su Cultivo""", font=("georgia", 20), fg="black", bg="chocolate3")

   
   #Botones de la Pagina de Inicio
    botonSE = tk.Button(frameInicio, text= "Sistema Experto", command= lambda: ventanaSE(ventana), bg="lawn green", width=20)
    botonLD = tk.Button(frameInicio, text= "Logica Difusa", command= lambda: ventanaLD(ventana), bg="lawn green", width=20)
    botonSalir = tk.Button(frameInicio, text= "Salir", command= lambda:ventana.destroy() , bg="red", width=20)



    frameInicio.pack()
    tituloInicio.place(rely=0.25, relx= 0.5, anchor="center")
    botonSE.place(rely=0.5, relx= 0.5, anchor= "center")
    botonLD.place(rely=0.65, relx= 0.5, anchor= "center")
    botonSalir.place(rely=.8, relx= 0.5, anchor="center")
    ventana.mainloop()



if __name__ == '__main__':
    ventanaInicio()