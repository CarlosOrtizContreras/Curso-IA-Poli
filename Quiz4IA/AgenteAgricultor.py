import tkinter as tk

class AgenteAgricultor:
    def __init__(self):
        self.percepciones = []
        self.reglas = {
            ("Tierra seca",): "Regar planta",
            ("Tierra seca", "Hojas caídas"): "Agregar fertilizante",
            ("Tierra seca", "Hojas caídas", "Plaga detectada"): "Aplicar pesticida",

            ("Hojas caídas", "Crecimiento excesivo"): "Podar planta",
            ("Tierra húmeda", "Hojas amarillas"): "Drenar exceso de agua",
            ("Manchas en hojas", "Humedad alta"): "Aplicar fungicida"
        }

    def agregar_percepcion(self, percepcion):
        if percepcion not in self.percepciones:
            self.percepciones.append(percepcion)

    def tomar_accion(self):
        acciones = []
        for condiciones, accion in sorted(self.reglas.items(), key=lambda x: len(x[0]), reverse=True):
            if all(p in self.percepciones for p in condiciones):
                acciones.append(accion)
        return acciones if acciones else ["No se requiere acción aún"]

    def reiniciar(self):
        self.percepciones.clear()


# Interfaz
class InterfazAgente:
    def __init__(self, root):
        self.agente = AgenteAgricultor()
        self.root = root
        self.root.title("Agente Agricultor Inteligente")
        self.root.geometry("550x520")

        tk.Label(root, text="Agente Agricultor Inteligente", font=("Arial", 16, "bold")).pack(pady=10)

        frame_botones = tk.Frame(root)
        frame_botones.pack()

        self.percepciones = [
            "Tierra seca",
            "Hojas caídas",
            "Plaga detectada",
            "Crecimiento excesivo",
            "Tierra húmeda",
            "Hojas amarillas",
            "Manchas en hojas",
            "Humedad alta"
        ]

        for p in self.percepciones:
            tk.Button(frame_botones, text=p, width=25,
                      command=lambda p=p: self.agregar_y_actualizar(p)).pack(pady=3)

        tk.Label(root, text="Percepciones acumuladas:", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        self.percepciones_text = tk.Label(
            root, text="", font=("Arial", 11),
            bg="white", width=60, height=2, relief="solid",
            wraplength=500, justify="left", anchor="w"
        )
        self.percepciones_text.pack()

        tk.Label(root, text="Acción del agente:", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        self.accion_text = tk.Label(
            root,
            text="(Sin acción aún)",
            font=("Arial", 11),
            bg="white",
            width=60,
            height=6,  
            relief="solid",
            wraplength=500,  
            justify="left",
            anchor="w"
        )
        self.accion_text.pack()

        tk.Button(root, text="Tomar acción", command=self.mostrar_accion,
                  bg="lightgreen", font=("Arial", 11)).pack(pady=10)

        tk.Button(root, text="Reiniciar", command=self.reiniciar,
                  bg="lightcoral", font=("Arial", 11)).pack()

    def agregar_y_actualizar(self, percepcion):
        self.agente.agregar_percepcion(percepcion)
        self.percepciones_text.config(text=", ".join(self.agente.percepciones))
        self.accion_text.config(text="(Aún no se ha tomado acción)")

    def mostrar_accion(self):
        acciones = self.agente.tomar_accion()
        self.accion_text.config(text="\n".join(acciones))  # salto de línea

    def reiniciar(self):
        self.agente.reiniciar()
        self.percepciones_text.config(text="")
        self.accion_text.config(text="(Sin acción aún)")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazAgente(root)
    root.mainloop()