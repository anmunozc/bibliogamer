import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector

# Conexión 
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
        messagebox.showerror("Error", "No se pudo conectar. Intentelo más tarde.")
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
        listbox.delete(0, tk.END)
        for reg in registros:
            listbox.insert(tk.END, f"ID: {reg[0]} | Título: {reg[1]} | Género: {reg[2]} | Clasificación: {reg[3]} | Plataforma: {reg[4]}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo recuperar la lista:\n{err}")
    finally:
        conexion.close()

def limpiar_campos():
    titulo_entry.delete(0, tk.END)
    genero_entry.delete(0, tk.END)
    clasificacion_entry.delete(0, tk.END)
    plataforma_entry.delete(0, tk.END)

def cargar_campos(event):
    seleccionado = listbox.curselection()
    if not seleccionado:
        return
    linea_seleccionada = listbox.get(seleccionado[0])
    partes = linea_seleccionada.split('|')
    try:
        titulo = partes[1].split(':',1)[1].strip()
        genero = partes[2].split(':',1)[1].strip()
        clasificacion = partes[3].split(':',1)[1].strip()
        plataforma = partes[4].split(':',1)[1].strip()
        titulo_entry.delete(0, tk.END)
        titulo_entry.insert(0, titulo)
        genero_entry.delete(0, tk.END)
        genero_entry.insert(0, genero)
        clasificacion_entry.delete(0, tk.END)
        clasificacion_entry.insert(0, clasificacion)
        plataforma_entry.delete(0, tk.END)
        plataforma_entry.insert(0, plataforma)
    except Exception:
        limpiar_campos()

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
        limpiar_campos()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo agregar el videojuego:\n{err}")
    finally:
        conexion.close()

def eliminar_videojuego():
    seleccionado = listbox.curselection()
    if not seleccionado:
        messagebox.showwarning("Ningún Videojuego Seleccionado", "Por favor, selecciona un videojuego de la lista para eliminar.")
        return
    linea_seleccionada = listbox.get(seleccionado[0])
    try:
        videojuego_id = int(linea_seleccionada.split('|')[0].replace('ID:', '').strip())
    except (ValueError, IndexError):
        messagebox.showerror("Error de Selección", "Formato de ID incorrecto en la selección. Por favor, intenta de nuevo.")
        return
    confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar el videojuego con ID: {videojuego_id}?")
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

def actualizar_videojuego():
    seleccionado = listbox.curselection()
    if not seleccionado:
        messagebox.showwarning("Ningún Videojuego Seleccionado", "Por favor, selecciona un videojuego de la lista para actualizar.")
        return
    linea_seleccionada = listbox.get(seleccionado[0])
    try:
        videojuego_id = int(linea_seleccionada.split('|')[0].replace('ID:', '').strip())
    except (ValueError, IndexError):
        messagebox.showerror("Error de Selección", "Formato de ID incorrecto en la selección. Por favor, intenta de nuevo.")
        return
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
            messagebox.showwarning("No Actualizado", "El videojuego no pudo ser actualizado. Verifica el ID o los datos.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo actualizar el videojuego:\n{err}")
    finally:
        conexion.close()

# -------- INTERFAZ --------
ventana = tk.Tk()
ventana.title("Gestor de Videojuegos")
ventana.geometry("700x500")

# Cargar imagen de fondo
try:
    imagen = Image.open("chrono1.jpg")
    imagen = imagen.resize((700, 500))
    fondo_tk = ImageTk.PhotoImage(imagen)
    label_fondo = tk.Label(ventana, image=fondo_tk)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
except Exception:
    pass

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

tk.Button(ventana, text="Agregar", command=agregar_videojuego, bg="green", fg="white").place(x=130, y=230)

tk.Button(ventana, text="Actualizar", command=actualizar_videojuego, bg="orange", fg="white").place(x=330, y=230)
tk.Button(ventana, text="Eliminar", command=eliminar_videojuego, bg="red", fg="white").place(x=430, y=230)
tk.Button(ventana, text="Limpiar campos", command=limpiar_campos, bg="gray", fg="white").place(x=530, y=230)

listbox = tk.Listbox(ventana, width=80, height=10)
listbox.place(x=30, y=280)
listbox.bind("<<ListboxSelect>>", cargar_campos)

mostrar_videojuegos() # Mostrar al arrancar

ventana.mainloop()