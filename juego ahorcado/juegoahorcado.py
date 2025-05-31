import tkinter as tk
from tkinter import messagebox
import random
from temas import temas

palabra_secreta = ""
letras_adivinadas = []
intentos_restantes = 6
letras_usadas = []
partes_dibujo = []

# Función para inicializar el juego
def iniciar_juego():
    global palabra_secreta, letras_adivinadas, intentos_restantes, letras_usadas, partes_dibujo
    tema = tema_var.get()
    palabra_secreta = random.choice(temas[tema])
    letras_adivinadas = ['_' for _ in palabra_secreta]
    intentos_restantes = 6
    letras_usadas = []
    palabra_label.config(text=' '.join(letras_adivinadas))
    letras_usadas_label.config(text="Letras usadas:")
    entrada.config(state="normal")
    boton.config(state="normal")
    canvas.delete("all")
    canvas.create_line(20, 230, 180, 230, width=3)
    canvas.create_line(50, 230, 50, 20, width=3)
    canvas.create_line(50, 20, 110, 20, width=3)
    canvas.create_line(110, 20, 110, 50, width=3)
    
    # Redefinir partes del monito
    partes_dibujo = [
        lambda c: c.create_oval(90, 50, 130, 90, fill="#f1c40f"),
        lambda c: c.create_line(110, 90, 110, 150, width=3),
        lambda c: c.create_line(110, 100, 90, 130, width=3),
        lambda c: c.create_line(110, 100, 130, 130, width=3),
        lambda c: c.create_line(110, 150, 90, 180, width=3),
        lambda c: c.create_line(110, 150, 130, 180, width=3),
    ]

# Procesar letra ingresada
def adivinar():
    global intentos_restantes
    letra = entrada.get().lower()
    entrada.delete(0, tk.END)

    if not letra.isalpha() or len(letra) != 1:
        messagebox.showwarning("Entrada inválida", "Ingresa solo una letra.")
        return
    if letra in letras_usadas:
        messagebox.showinfo("Letra usada", f"Ya usaste la letra '{letra}'.")
        return

    letras_usadas.append(letra)
    letras_usadas_label.config(text="Letras usadas: " + ", ".join(letras_usadas))

    if letra in palabra_secreta:
        for i, l in enumerate(palabra_secreta):
            if l == letra:
                letras_adivinadas[i] = letra
        palabra_label.config(text=' '.join(letras_adivinadas))
    else:
        canvas.after(100, partes_dibujo[6 - intentos_restantes], canvas)
        intentos_restantes -= 1

    if '_' not in letras_adivinadas:
        messagebox.showinfo("🎉 ¡Ganaste!", f"Adivinaste la palabra: {palabra_secreta}")
        entrada.config(state="disabled")
        boton.config(state="disabled")
    elif intentos_restantes == 0:
        messagebox.showerror("💀 ¡Perdiste!", f"La palabra era: {palabra_secreta}")
        entrada.config(state="disabled")
        boton.config(state="disabled")

# --- Interfaz gráfica ---
ventana = tk.Tk()
ventana.title("🎯 Ahorcado con Temas")
ventana.configure(bg="#ecf0f1")

# Título
tk.Label(ventana, text="🎮 Ahorcado Temático", font=("Helvetica", 24, "bold"), bg="#ecf0f1", fg="#2c3e50").grid(row=0, column=0, columnspan=3, pady=10)

# Selector de tema
tk.Label(ventana, text="Elige un tema:", bg="#ecf0f1", font=("Arial", 14)).grid(row=1, column=0)
tema_var = tk.StringVar(value="Animales")
menu_tema = tk.OptionMenu(ventana, tema_var, *temas.keys())
menu_tema.grid(row=1, column=1)
tk.Button(ventana, text="Iniciar Juego", command=iniciar_juego, bg="#2ecc71", fg="white", font=("Arial", 12)).grid(row=1, column=2)

# Canvas para el monito
canvas = tk.Canvas(ventana, width=200, height=250, bg="white", bd=2, relief="sunken")
canvas.grid(row=2, column=0, rowspan=4, padx=10, pady=10)

# Palabra oculta
palabra_label = tk.Label(ventana, text="_ _ _ _", font=("Consolas", 26), bg="#ecf0f1", fg="#34495e")
palabra_label.grid(row=2, column=1, columnspan=2)

# Entrada de letra
entrada = tk.Entry(ventana, font=("Consolas", 16), justify="center", width=5, state="disabled")
entrada.grid(row=3, column=1)

# Botón de adivinar
boton = tk.Button(ventana, text="Adivinar", command=adivinar, font=("Arial", 14), bg="#3498db", fg="white", width=10, state="disabled")
boton.grid(row=3, column=2)

# Letras usadas
letras_usadas_label = tk.Label(ventana, text="Letras usadas:", font=("Arial", 12), bg="#ecf0f1", fg="#7f8c8d")
letras_usadas_label.grid(row=4, column=1, columnspan=2)

ventana.mainloop()

