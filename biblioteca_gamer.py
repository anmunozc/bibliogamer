import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector

# Conexión con la base de datos MySQL
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="videojuegos_db"
        )
        return conexion
    except mysql.connector.Error:
        messagebox.showerror("Error", "No se pudo conectar. Inténtelo más tarde.")
        return None

#Variable global para guardar el mapeo entre el indice de la lista y el ID real de la bd en MySQL
ids_videojuegos = []

"""
Consulta los juegos almacenados, limpia la lista en la interfaz y la actualiza con los registros en orden ascendente. 
Tambien guarda los IDs reales para operaciones posteriores.(edit, delete, update)
"""

def mostrar_videojuegos():
    global ids_videojuegos
    conexion = conectar_bd()
    if conexion is None:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM Videojuegos ORDER BY ID ASC")
        registros = cursor.fetchall()
        listbox.delete(0, tk.END)
        ids_videojuegos.clear()
        for i, reg in enumerate(registros, start=1):
            ids_videojuegos.append(reg[0])
            listbox.insert(
                tk.END,
                f"No. {i} | Título: {reg[1]} | Género: {reg[2]} | Clasificación: {reg[3]} | Plataforma: {reg[4]}"
            )
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo recuperar la lista:\n{err}")
    finally:
        conexion.close()

"""
Limpia los campos de entrada para permitir nuevos datos.
"""
def limpiar_campos():
    titulo_entry.delete(0, tk.END)
    genero_entry.delete(0, tk.END)
    clasificacion_entry.delete(0, tk.END)
    plataforma_entry.delete(0, tk.END)

"""
Cuando el usuario selecciona un juego de la lista, carga sus datos en los campos para permitir su actualizacion.
"""
def cargar_campos(event):
    seleccionado = listbox.curselection()
    if not seleccionado:
        return
    indice = seleccionado[0]
    conexion = conectar_bd()
    if conexion is None:
        return
    cursor = conexion.cursor()
    try:
        videojuego_id = ids_videojuegos[indice]
        cursor.execute("SELECT Titulo, Genero, Clasificacion, Plataforma FROM Videojuegos WHERE ID = %s", (videojuego_id,))
        datos = cursor.fetchone()
        if datos:
            titulo_entry.delete(0, tk.END)
            titulo_entry.insert(0, datos[0])
            genero_entry.delete(0, tk.END)
            genero_entry.insert(0, datos[1])
            clasificacion_entry.delete(0, tk.END)
            clasificacion_entry.insert(0, datos[2])
            plataforma_entry.delete(0, tk.END)
            plataforma_entry.insert(0, datos[3])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo cargar el videojuego:\n{err}")
    finally:
        conexion.close()

"""
Obtiene los datos de los campos de entrada y crea un nuevo juego en la base de datos.
Actualiza la lista una vez insertado.
"""
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
        limpiar_campos()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo agregar el videojuego:\n{err}")
    finally:
        conexion.close()

"""
Elimina el juego seleccionado de la base de datos y actualiza la lista.
"""
def eliminar_videojuego():
    seleccionado = listbox.curselection()
    if not seleccionado:
        messagebox.showwarning("Ningún Videojuego Seleccionado", "Por favor, selecciona un videojuego de la lista para eliminar.")
        return
    indice = seleccionado[0]
    videojuego_id = ids_videojuegos[indice]
    confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar el videojuego seleccionado?")
    if not confirmar:
        return
    conexion = conectar_bd()
    if conexion is None:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM Videojuegos WHERE ID = %s", (videojuego_id,))
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Videojuego eliminado correctamente.")
            mostrar_videojuegos()
            limpiar_campos()
        else:
            messagebox.showwarning("No Encontrado", "El videojuego no pudo ser eliminado. Posiblemente ya no existe.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo eliminar el videojuego:\n{err}")
    finally:
        conexion.close()

"""
Actualiza la informacion de un juego seleccionado usando los datos de los campos
Refresca la lista para mostrar los cambios.
"""
def actualizar_videojuego():
    seleccionado = listbox.curselection()
    if not seleccionado:
        messagebox.showwarning("Ningún Videojuego Seleccionado", "Por favor, selecciona un videojuego de la lista para actualizar.")
        return
    indice = seleccionado[0]
    videojuego_id = ids_videojuegos[indice]
    titulo = titulo_entry.get()
    genero = genero_entry.get()
    clasificacion = clasificacion_entry.get()
    plataforma = plataforma_entry.get()
    if not (titulo and genero and clasificacion and plataforma):
        messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los campos para actualizar el videojuego.")
        return
    conexion = conectar_bd()
    if conexion is None:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE Videojuegos SET Titulo = %s, Genero = %s, Clasificacion = %s, Plataforma = %s WHERE ID = %s",
            (titulo, genero, clasificacion, plataforma, videojuego_id)
        )
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Videojuego actualizado correctamente.")
            mostrar_videojuegos()
            limpiar_campos()
        else:
            messagebox.showwarning("No Actualizado", "El videojuego no pudo ser actualizado. Verifica los datos.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo actualizar el videojuego:\n{err}")
    finally:
        conexion.close()

# -------- INTERFAZ --------
ventana = tk.Tk()
ventana.title("Gestor de Videojuegos")
ventana.geometry("700x500")

label_bg_color = "#f5e6c5"

# Cargar imagen de fondo si está disponible
try:
    imagen = Image.open("chrono1.jpg")
    imagen = imagen.resize((700, 500))
    fondo_tk = ImageTk.PhotoImage(imagen)
    label_fondo = tk.Label(ventana, image=fondo_tk)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
except Exception:
    ventana.configure(bg=label_bg_color)

# Título principal con fuente Arial
titulo_principal = tk.Label(
    ventana,
    text="Biblioteca de Videojuegos",
    font=("Arial", 22, "bold"),
    bg=label_bg_color,
    fg="#2a2a2a"
)
titulo_principal.place(x=180, y=15)

# Etiquetas y entradas
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

# Botones directamente sobre la ventana sin frame de fondo
btn_agregar = tk.Button(ventana, text="Agregar", command=agregar_videojuego,
                        bg="green", fg="white", width=13, font=('Arial', 10, 'bold'), bd=0, highlightthickness=0)
btn_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_videojuego,
                           bg="blue", fg="white", width=13, font=('Arial', 10, 'bold'), bd=0, highlightthickness=0)
btn_eliminar = tk.Button(ventana, text="Eliminar", command=eliminar_videojuego,
                         bg="red", fg="white", width=13, font=('Arial', 10, 'bold'), bd=0, highlightthickness=0)
btn_limpiar = tk.Button(ventana, text="Limpiar campos", command=limpiar_campos,
                        bg="gray", fg="white", width=13, font=('Arial', 10, 'bold'), bd=0, highlightthickness=0)

btn_agregar.place(x=130, y=230)
btn_actualizar.place(x=270, y=230)
btn_eliminar.place(x=410, y=230)
btn_limpiar.place(x=550, y=230)

# Listbox y scrollbar
listbox = tk.Listbox(ventana, width=80, height=10)
listbox.place(x=30, y=280)

scrollbar = tk.Scrollbar(ventana)
scrollbar.place(x=660, y=280, height=165)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Cargar datos al seleccionar
listbox.bind("<<ListboxSelect>>", cargar_campos)

mostrar_videojuegos()  # Mostrar datos al inicio

ventana.mainloop()