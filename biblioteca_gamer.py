import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector

# Conexión con mensaje
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="videojuegos_db"
        )
        messagebox.showinfo("Conexión Exitosa", "hola gamer, bienvenido a la biblioteca de juegos.")
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error ", f" intentelo mas tarde")
        return None

# Mostrar videojuegos en Listbox
def mostrar_videojuegos():
    conexion = conectar_bd()
    if conexion is None:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM Videojuegos ORDER BY ID ASC")
        registros = cursor.fetchall()
        listbox.delete(0, tk.END)  # Limpiar el Listbox antes de mostrar
        for reg in registros:
            listbox.insert(tk.END, f"ID: {reg[0]} | Título: {reg[1]} | Género: {reg[2]} | Clasificación: {reg[3]} | Plataforma: {reg[4]}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo recuperar la lista:\n{err}")
    finally:
        conexion.close()


# Agregar videojuego
def agregar_videojuego():
    titulo = titulo_entry.get()
    genero = genero_entry.get()
    clasificacion = clasificacion_entry.get()
    plataforma = plataforma_entry.get()

    if not (titulo and genero and clasificacion and plataforma):
        messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los campos.")
        return

    conexion = conectar_bd()
    if conexion is None:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO Videojuegos (Titulo, Genero, Clasificacion, Plataforma) VALUES (%s, %s, %s, %s)",
            (titulo, genero, clasificacion, plataforma)
        )
        conexion.commit()
        messagebox.showinfo("Éxito", "Videojuego agregado correctamente.")
        mostrar_videojuegos()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo agregar el videojuego:\n{err}")
    finally:
        conexion.close()

# ---------------- INTERFAZ ----------------
ventana = tk.Tk()
ventana.title("Gestor de Videojuegos")
ventana.geometry("700x500")

# Cargar imagen de fondo
imagen = Image.open("chrono1.jpg")
imagen = imagen.resize((700, 500))
fondo_tk = ImageTk.PhotoImage(imagen)
label_fondo = tk.Label(ventana, image=fondo_tk)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Campos de entrada
# Color sugerido para fondo de etiquetas tipo "fantasía"
label_bg_color = "#f5e6c5"

tk.Label(ventana, text="Título:", bg=label_bg_color).place(x=30, y=70)
titulo_entry = tk.Entry(ventana)
titulo_entry.place(x=130, y=70)

tk.Label(ventana, text="Género:", bg=label_bg_color).place(x=30, y=110)
genero_entry = tk.Entry(ventana)
genero_entry.place(x=130, y=110)

tk.Label(ventana, text="Clasificación:", bg=label_bg_color).place(x=30, y=150)
clasificacion_entry = tk.Entry(ventana)
clasificacion_entry.place(x=130, y=150)

tk.Label(ventana, text="Plataforma:", bg=label_bg_color).place(x=30, y=190)
plataforma_entry = tk.Entry(ventana)
plataforma_entry.place(x=130, y=190)

# Botones
tk.Button(ventana, text="Agregar", command=agregar_videojuego, bg="green", fg="white").place(x=130, y=230)
tk.Button(ventana, text="Mostrar todos", command=mostrar_videojuegos, bg="blue", fg="white").place(x=200, y=230)

# Listbox
listbox = tk.Listbox(ventana, width=80, height=10)
listbox.place(x=30, y=280)

# Probar conexión al iniciar
conectar_bd()

ventana.mainloop()
