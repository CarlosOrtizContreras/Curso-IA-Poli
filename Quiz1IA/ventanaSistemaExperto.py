import tkinter as tk
import clips 

from tkinter.scrolledtext import ScrolledText


def ventanaSE(ventana):
    pantallaSE = tk.Toplevel(ventana, height=700, width=1000, bg= "coral1")
    pantallaSE.title("Sistema Experto")
    pantallaSE.resizable(False,False)
    pantallaSE.iconbitmap("iconCacao.ico")
    pantallaSE.attributes("-alpha", 0.9)

    
    frameSE = tk.Frame(pantallaSE)
    frameSE.configure(bg="coral1", width=1000, height=700)

   
    #Titulo pantalla SE
    tituloSE = tk.Label(frameSE, text="""     
                        Gestione las Enfermedades de su Cultivo
                         Ingrese la Siguiente Información""", font=("georgia", 20), fg="black", bg="CORAL1")
    
    #Botones pantalla SE
    botonGestionar = tk.Button (frameSE,text="Gestionar", bg="green", width=20, command= lambda: gestorCajones(cajonEstadoFrutas, cajonPresenciaArbol, cajonPresenciaHojas, reglasClips(), frameSE))
    botonMenuInicial = tk.Button (frameSE, text="Menu Inicial", command= lambda: pantallaSE.destroy(), bg="yellow", width=20)


    #Organizacion Botones y Titulo
    frameSE.pack()
    frameSE.pack_propagate(False)
    tituloSE.place(rely= .1, relx= .4, anchor= "center")
    botonGestionar.place(rely= .65, relx= .3, anchor= "center")
    botonMenuInicial.place(rely= .65, relx= .6, anchor= "center")


    # Estado Fruta
    labelEstadoFruta = tk.Label(frameSE, text="Estado Fruta", bg= "coral1", font=("georgia", 13))
    cajonEstadoFrutas = tk.Listbox(frameSE, width=30 , selectmode= "multiple", exportselection=False)
    elementosEstadoFruta = ["Forma Fresa/Chirimoya/Zanahoria", "Puntos Verdes/Deformaciones", "Maduracion Parcial/Deformacion", "Mancha Marron/Borde Blanco", "Mancha Chocolate"]
   
    for ele in elementosEstadoFruta:
        cajonEstadoFrutas.insert(tk.END, ele)
    
    labelEstadoFruta.place (rely= .3, relx= .2, anchor= "center")
    cajonEstadoFrutas.place(rely= .3, relx= .4, anchor= "center", height=100)
    
    #Presencia Arbol
    labelPresenciaArbol = tk.Label(frameSE, text="Presencia Arbol", bg= "coral1", font=("georgia", 13))
    cajonPresenciaArbol = tk.Listbox(frameSE, width=30 , selectmode= "multiple", exportselection= False)
    elementosPresenciaArbol = ["Ramas Escobas", "Tallo Seco", "Raiz Necrosada", "Tronco Negrosado"]

    for ele in elementosPresenciaArbol:
        cajonPresenciaArbol.insert(tk.END, ele)     

    labelPresenciaArbol.place (rely= .3, relx= .6, anchor= "center")
    cajonPresenciaArbol.place(rely= .3, relx= .8, anchor= "center", height=100)
    
    #Presencia Hoja
    labelPresenciaHojas = tk.Label(frameSE, text="Presencia Hojas", bg= "coral1", font=("georgia", 13))

    cajonPresenciaHojas = tk.Listbox(frameSE, width=30 , selectmode= "multiple", exportselection=False)
    elementosPresenciaHojas =["Hojas Secas"]
 
    for ele in elementosPresenciaHojas:
        cajonPresenciaHojas.insert(tk.END, ele)  
    
    labelPresenciaHojas.place (rely= .5, relx= .4, anchor= "center")
    cajonPresenciaHojas.place(rely= .5, relx= .6, anchor= "center", height=100)




def reglasClips():
    env = clips.Environment()
    env.clear()

    env.build("""
        (defrule monoliasis
        (or
        (estado_fruta "Puntos Verdes/Deformaciones")
        (estado_fruta "Maduracion Parcial/Deformacion")
        (estado_fruta "Mancha Marron/Borde Blanco")
        )
        =>
        (assert (diagnostico "Monoliasis"))
        )
        """)
    
    env.build("""
        (defrule escobaBruja
        (estado_fruta "Forma Fresa/Chirimoya/Zanahoria")
        (presencia_arbol "Ramas Escobas")
        =>
        (assert (diagnostico "Escoba de Bruja"))
        )
        """)
    
    env.build("""
        (defrule mazorcaNegra
        (or
      (estado_fruta "Mancha Chocolate")
      (presencia_hojas "Hojas Secas")
      (presencia_arbol "Tallo Seco")
      (presencia_arbol "Tronco Necrosado")
      (presencia_arbol "Raiz Necrosada")
         )
         =>
         (assert (diagnostico "Mazorca Negra"))
        )
        """)
    
    env.build("""
        (defrule contaminacionPeligrosa
   (diagnostico "Monoliasis")
   (diagnostico "Mazorca Negra")
   =>
   (assert (recomendacion "Eliminar cultivo: Monoliasis y Mazorca Negra presentes"))
        )
        """)
    
    return env
    



def gestorCajones(cajonEstado, cajonArbol, cajonHojas, env: clips.Environment, frameSE):
    
    env.reset()

    for i in cajonEstado.curselection():
        valor = cajonEstado.get(i)
        env.assert_string(f'(estado_fruta "{valor}")')

    for i in cajonArbol.curselection():
        valor = cajonArbol.get(i)
        env.assert_string(f'(presencia_arbol "{valor}")')

    for i in cajonHojas.curselection():
        valor = cajonHojas.get(i)
        env.assert_string(f'(presencia_hojas "{valor}")')


    env.run()

   
    salidaTexto = ScrolledText(frameSE)
    salidaTexto.config(state= "normal")

    
    salidaTexto.place(rely= .8, relx= .5, anchor= "center", width=700, height=150)

    for hecho in env.facts():
        salidaTexto.insert(tk.END, str(hecho)+"\n")
        print(hecho)





    


