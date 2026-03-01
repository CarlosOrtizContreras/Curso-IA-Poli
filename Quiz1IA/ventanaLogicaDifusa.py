import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def ventanaLD(ventana):
    pantallaFD = tk.Toplevel(ventana, height=750, width=1200, bg="coral1")
    pantallaFD.title("Sistema Difuso - Viabilidad de Siembra Cacao")
    pantallaFD.resizable(False, False)
    pantallaFD.iconbitmap("iconCacao.ico")
    pantallaFD.attributes("-alpha", 0.95)

    frameFD = tk.Frame(pantallaFD, bg="coral1", width=1200, height=750)
    frameFD.pack()
    frameFD.pack_propagate(False)

    # Titulo 
    tituloFD = tk.Label(frameFD,
                        text="Sistema Difuso de Evaluación\nViabilidad de Siembra de Cacao",
                        font=("georgia", 20),
                        bg="coral1")
    tituloFD.place(rely=.05, relx=.5, anchor="center")

    
    # VARIABLES DIFUSAS
   
    altitud = ctrl.Antecedent(np.arange(0, 2001, 1), 'altitud')
    ph = ctrl.Antecedent(np.arange(4, 8.1, 0.1), 'ph')
    precipitacion = ctrl.Antecedent(np.arange(500, 3001, 1), 'precipitacion')
    viabilidad = ctrl.Consequent(np.arange(0, 11, 1), 'viabilidad')

    altitud['baja'] = fuzz.trapmf(altitud.universe, [0, 0,550, 650])
    altitud['media'] = fuzz.trimf(altitud.universe, [600, 700, 800])
    altitud['alta'] = fuzz.trapmf(altitud.universe, [750, 800, 2000,2000])

    ph['acido'] = fuzz.trapmf(ph.universe, [4, 4,5, 5.8])
    ph['ideal'] = fuzz.trapmf(ph.universe, [5.5, 6, 6.5, 7])
    ph['alcalino'] = fuzz.trapmf(ph.universe, [6.7, 7.5, 8,8])

    precipitacion['baja'] = fuzz.trapmf(precipitacion.universe, [500, 500, 1400,1500])
    precipitacion['media'] = fuzz.trapmf(precipitacion.universe, [1400,1500,2500,2700])
    precipitacion['alta'] = fuzz.trapmf(precipitacion.universe, [2500,2700, 3000, 3000])

    viabilidad['mala'] = fuzz.trapmf(viabilidad.universe, [0, 0,3, 4])
    viabilidad['regular'] = fuzz.trapmf(viabilidad.universe, [3, 4, 6,7])
    viabilidad['buena'] = fuzz.trapmf(viabilidad.universe, [6,7, 10, 10])

   
    # REGLAS
    
    regla1 = ctrl.Rule(altitud['media'] & ph['ideal'] & precipitacion['media'],
                       viabilidad['buena'], label="Regla 1: Altitud media, pH ideal, precipitación media")
    regla2 = ctrl.Rule(ph['alcalino'] | precipitacion['alta'] | altitud['alta'],
                       viabilidad['mala'], label="Regla 2: condiciones extremas altas")
    regla3 = ctrl.Rule(altitud['baja'] & ph['ideal'] & precipitacion['alta'],
                       viabilidad['regular'], label="Regla 3: Condiciones moderadamente estables ")
    regla4 = ctrl.Rule(altitud['baja'] | ph['acido'] | precipitacion['baja'],
                              viabilidad['mala'], label="Regla 4: condiciones extremas bajas")

    sistema_ctrl = ctrl.ControlSystem([regla1, regla2, regla3, regla4])

 
    # INTERFAZ DE ENTRADA
    
    tk.Label(frameFD, text="Altitud (msnm)", bg="coral1").place(rely=.15, relx=.2, anchor="center")
    scaleAltitud = tk.Scale(frameFD, from_=0, to=2000, orient="horizontal", length=300, bg="coral1")
    scaleAltitud.place(rely=.2, relx=.2, anchor="center")

    tk.Label(frameFD, text="pH del Suelo", bg="coral1").place(rely=.28, relx=.2, anchor="center")
    scalePh = tk.Scale(frameFD, from_=4, to=8, resolution=0.1, orient="horizontal", length=300, bg="coral1")
    scalePh.place(rely=.33, relx=.2, anchor="center")

    tk.Label(frameFD, text="Precipitación (mm/año)", bg="coral1").place(rely=.41, relx=.2, anchor="center")
    scalePre = tk.Scale(frameFD, from_=500, to=3000, orient="horizontal", length=300, bg="coral1")
    scalePre.place(rely=.46, relx=.2, anchor="center")

   
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

    def calcular():
        salidaTexto.delete("1.0", tk.END)
        simulador = ctrl.ControlSystemSimulation(sistema_ctrl)
        simulador.input['altitud'] = scaleAltitud.get()
        simulador.input['ph'] = scalePh.get()
        simulador.input['precipitacion'] = scalePre.get()

        try:
            simulador.compute()
            resultado = simulador.output.get('viabilidad', 0)
        except Exception:
            resultado = 0

        salidaTexto.insert(tk.END, f"--- RESULTADOS DEL ANALISIS ---\n\n")
        salidaTexto.insert(tk.END, f"Altitud ingresada: {scaleAltitud.get()} msnm\n")
        salidaTexto.insert(tk.END, f"pH ingresado: {scalePh.get()}\n")
        salidaTexto.insert(tk.END, f"Precipitación ingresada: {scalePre.get()} mm\n\n")
        salidaTexto.insert(tk.END, f"Nivel de Viabilidad: {round(resultado,2)} / 10\n\n")

        if resultado >= 7:
            salidaTexto.insert(tk.END, "Conclusión: Terreno ALTAMENTE viable para cacao.\n")
        elif resultado >= 4 and resultado < 7:
            salidaTexto.insert(tk.END, "Conclusión: Terreno MODERADAMENTE viable.\n")
        else:
            salidaTexto.insert(tk.END, "Conclusión: Terreno NO recomendable para siembra.\n")

        # Reglas activadas
        salidaTexto.insert(tk.END, "\n--- Reglas activadas ---\n")
        for r in sistema_ctrl.rules:
            try:
                grado = r.aggregate_firing[simulador]

                if grado > 0:
                    salidaTexto.insert(
                        tk.END,
                        f"{r.label}: grado activación = {round(float(grado),2)}\n"
                    )

            except Exception:
                pass

    def mostrar_imagenes():
        # Genera los gráficos solo cuando se requiere
        fig, axes = plt.subplots(2,2, figsize=(5,8))
        altitud.view(ax=axes[0,0])
        ph.view(ax=axes[0, 1])
        precipitacion.view(ax=axes[1,0])
        viabilidad.view(ax= axes[1,1])

        plt.tight_layout()

        
       

    # BOTONES

    botonCalcular = tk.Button(frameFD, text="Calcular", bg="green", width=20, command=calcular)
    botonMostrarImg = tk.Button(frameFD, text="Mostrar Imágenes", bg="orange", width=20, command=mostrar_imagenes)
    botonMenu = tk.Button(frameFD, text="Menu Inicial", bg="yellow", width=20, command=pantallaFD.destroy)

    botonCalcular.place(rely=.7, relx=.3, anchor="center")
    botonMostrarImg.place(rely=.7, relx=.5, anchor="center")
    botonMenu.place(rely=.7, relx=.7, anchor="center")