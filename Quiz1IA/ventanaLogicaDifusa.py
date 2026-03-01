import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

    # ====== Titulo ======
    tituloFD = tk.Label(frameFD,
                        text="Sistema Difuso de Evaluación\nViabilidad de Siembra de Cacao",
                        font=("georgia", 20),
                        bg="coral1")
    tituloFD.place(rely=.05, relx=.5, anchor="center")

    # ======================
    # VARIABLES DIFUSAS
    # ======================
    altitud = ctrl.Antecedent(np.arange(0, 2001, 1), 'altitud')
    ph = ctrl.Antecedent(np.arange(4, 8.1, 0.1), 'ph')
    precipitacion = ctrl.Antecedent(np.arange(500, 3001, 1), 'precipitacion')
    viabilidad = ctrl.Consequent(np.arange(0, 11, 1), 'viabilidad')

    altitud['baja'] = fuzz.trimf(altitud.universe, [0, 0, 800])
    altitud['media'] = fuzz.trimf(altitud.universe, [600, 1000, 1400])
    altitud['alta'] = fuzz.trimf(altitud.universe, [1200, 2000, 2000])

    ph['acido'] = fuzz.trimf(ph.universe, [4, 4, 5.5])
    ph['ideal'] = fuzz.trimf(ph.universe, [5.5, 6.5, 7])
    ph['alcalino'] = fuzz.trimf(ph.universe, [6.5, 8, 8])

    precipitacion['baja'] = fuzz.trimf(precipitacion.universe, [500, 500, 1200])
    precipitacion['media'] = fuzz.trimf(precipitacion.universe, [1000, 1800, 2500])
    precipitacion['alta'] = fuzz.trimf(precipitacion.universe, [2200, 3000, 3000])

    viabilidad['mala'] = fuzz.trimf(viabilidad.universe, [0, 0, 4])
    viabilidad['regular'] = fuzz.trimf(viabilidad.universe, [3, 5, 7])
    viabilidad['buena'] = fuzz.trimf(viabilidad.universe, [6, 10, 10])

    # ======================
    # REGLAS
    # ======================
    regla1 = ctrl.Rule(altitud['media'] & ph['ideal'] & precipitacion['media'],
                       viabilidad['buena'], label="Regla 1: Altitud media, pH ideal, precipitación media")
    regla2 = ctrl.Rule(ph['acido'] | precipitacion['baja'],
                       viabilidad['mala'], label="Regla 2: pH ácido o precipitación baja")
    regla3 = ctrl.Rule(altitud['alta'] | ph['alcalino'],
                       viabilidad['regular'], label="Regla 3: Altitud alta o pH alcalino")
    regla_defecto = ctrl.Rule(altitud['baja'] | ph['acido'] | precipitacion['baja'],
                              viabilidad['mala'], label="Regla por defecto: condiciones extremas")

    sistema_ctrl = ctrl.ControlSystem([regla1, regla2, regla3, regla_defecto])

    # ======================
    # INTERFAZ DE ENTRADA
    # ======================
    tk.Label(frameFD, text="Altitud (msnm)", bg="coral1").place(rely=.15, relx=.2, anchor="center")
    scaleAltitud = tk.Scale(frameFD, from_=0, to=2000, orient="horizontal", length=300, bg="coral1")
    scaleAltitud.place(rely=.2, relx=.2, anchor="center")

    tk.Label(frameFD, text="pH del Suelo", bg="coral1").place(rely=.28, relx=.2, anchor="center")
    scalePh = tk.Scale(frameFD, from_=4, to=8, resolution=0.1, orient="horizontal", length=300, bg="coral1")
    scalePh.place(rely=.33, relx=.2, anchor="center")

    tk.Label(frameFD, text="Precipitación (mm/año)", bg="coral1").place(rely=.41, relx=.2, anchor="center")
    scalePre = tk.Scale(frameFD, from_=500, to=3000, orient="horizontal", length=300, bg="coral1")
    scalePre.place(rely=.46, relx=.2, anchor="center")

    # ======================
    # SCROLLED TEXT PARA RESULTADOS
    # ======================
    salidaTexto = ScrolledText(frameFD, width=70, height=25)
    salidaTexto.place(rely=.3, relx=.65, anchor="center", height=200)

    # ======================
    # FUNCIONES
    # ======================
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
        elif resultado >= 4:
            salidaTexto.insert(tk.END, "Conclusión: Terreno MODERADAMENTE viable.\n")
        else:
            salidaTexto.insert(tk.END, "Conclusión: Terreno NO recomendable para siembra.\n")

        # Reglas activadas
        salidaTexto.insert(tk.END, "\n--- Reglas activadas ---\n")
        for r in sistema_ctrl.rules:
            try:
                grado = r.antecedent.membership_value({
                    'altitud': scaleAltitud.get(),
                    'ph': scalePh.get(),
                    'precipitacion': scalePre.get()
                })
            except Exception:
                grado = 0
            salidaTexto.insert(tk.END, f"{r.label}: grado activación ~ {round(grado,2)}\n")

    def mostrar_imagenes():
        # Genera los gráficos solo cuando se requiere
        fig, axes = plt.subplots(3,1, figsize=(5,8))
        altitud.view(ax=axes[0])
        ph.view(ax=axes[1])
        precipitacion.view(ax=axes[2])
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frameFD)
        canvas.draw()
       

    # ======================
    # BOTONES
    # ======================
    botonCalcular = tk.Button(frameFD, text="Calcular", bg="green", width=20, command=calcular)
    botonMostrarImg = tk.Button(frameFD, text="Mostrar Imágenes", bg="orange", width=20, command=mostrar_imagenes)
    botonMenu = tk.Button(frameFD, text="Menu Inicial", bg="yellow", width=20, command=pantallaFD.destroy)

    botonCalcular.place(rely=.7, relx=.3, anchor="center")
    botonMostrarImg.place(rely=.7, relx=.5, anchor="center")
    botonMenu.place(rely=.7, relx=.7, anchor="center")