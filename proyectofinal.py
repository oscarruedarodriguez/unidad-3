import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# -------------------------
# FUNCIONES
# -------------------------
def abrir_registro_productos():
   
   reg = tk.Toplevel()
   reg.title("Registro de Productos")
   reg.geometry("400x400")
   reg.resizable(False, False)

   # --- Etiquetas y Campos de Texto ---
   lbl_id = tk.Label(reg, text="ID del Producto:", font=("Arial", 12))
   lbl_id.pack(pady=5)
   txt_id = tk.Entry(reg, font=("Arial", 12))
   txt_id.pack(pady=5)
   lbl_desc = tk.Label(reg, text="Descripción:", font=("Arial", 12))
   lbl_desc.pack(pady=5)
   txt_desc = tk.Entry(reg, font=("Arial", 12))
   txt_desc.pack(pady=5)
   lbl_precio = tk.Label(reg, text="Precio:", font=("Arial", 12))
   lbl_precio.pack(pady=5)
   txt_precio = tk.Entry(reg, font=("Arial", 12))
   txt_precio.pack(pady=5)
   lbl_categoria = tk.Label(reg, text="Categoría:", font=("Arial", 12))
   lbl_categoria.pack(pady=5)
   txt_categoria = tk.Entry(reg, font=("Arial", 12))
   txt_categoria.pack(pady=5)

   # --- Función para guardar ---
   def guardar_producto():
      id_prod = txt_id.get().strip()
      descripcion = txt_desc.get().strip()
      precio = txt_precio.get().strip()
      categoria = txt_categoria.get().strip()
      # Validaciones
      if id_prod == "" or descripcion == "" or precio == "" or categoria == "":
         messagebox.showwarning("Campos Vacíos", "Por favor complete todos los campos.")
         return
      # Validar precio como número
      try:
         float(precio)
      except:
         messagebox.showerror("Error", "El precio debe ser un número.")
         return

      # Guardar en archivo de texto
      BASE_DIR = os.path.dirname(os.path.abspath(__file__))
      archivo = os.path.join(BASE_DIR,"productos.txt")
      with open(archivo, "a", encoding="utf-8") as archivo:
         archivo.write(f"{id_prod}|{descripcion}|{precio}|{categoria}\n")
         messagebox.showinfo("Guardado", "Producto registrado correctamente.")
         # Limpiar campos
         txt_id.delete(0, tk.END)
         txt_desc.delete(0, tk.END)
         txt_precio.delete(0, tk.END)
         txt_categoria.delete(0, tk.END)
   # --- Botón Guardar ---
   btn_guardar = tk.Button(reg, text="Guardar Producto", command=guardar_producto)
   btn_guardar.pack(pady=20)

def abrir_registro_ventas():
    messagebox.showinfo("Registro de Ventas", "Aquí irá el módulo de registro de ventas.")

def abrir_reportes():
    messagebox.showinfo("Reportes", "Aquí irá el módulo de reportes.")

def abrir_acerca_de():
    messagebox.showinfo("Acerca de", "Punto de Venta de Ropa\nProyecto Escolar\nVersión 1.0")


# -------------------------
# VENTANA PRINCIPAL
# -------------------------
ventana = tk.Tk()
ventana.title("Punto de Venta - Ropa")
ventana.geometry("500x650")
ventana.resizable(False, False)

# Fondo color carbón oscuro
ventana.configure(bg="#1E1E1E")


# -------------------------
# LOGO
# -------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    imagen = Image.open(os.path.join(BASE_DIR, "ventas2025.png"))
    imagen = imagen.resize((300, 300))
    img_logo = ImageTk.PhotoImage(imagen)

    lbl_logo = tk.Label(ventana, image=img_logo, bg="#1E1E1E")
    lbl_logo.pack(pady=10)
except:
    lbl_sin_logo = tk.Label(ventana, text="(Aquí va el logo del sistema)", font=("Arial", 14), bg="#1E1E1E", fg="white")
    lbl_sin_logo.pack(pady=40)


# -------------------------
# ESTILO — NEGRO + ROJO CARMESÍ INTENSO
# -------------------------
estilo = ttk.Style()
estilo.theme_use("default")

estilo.configure(
    "RojoNegro.TButton",
    font=("Arial", 12, "bold"),
    padding=12,
    background="#000000",      # Fondo negro
    foreground="#DC143C",      # LETRAS ROJO CARMESÍ
    bordercolor="#DC143C",     # Borde rojo
    borderwidth=3,
    focusthickness=3,
    focuscolor="#DC143C",
)

# Colores al presionar y al pasar el mouse
estilo.map(
    "RojoNegro.TButton",
    background=[
        ("active", "#1A1A1A"),  # negro más claro al presionar
        ("pressed", "#000000")
    ],
    foreground=[
        ("active", "#FF3355"),  # rojo más brillante al pasar el mouse
        ("pressed", "#FF3355")
    ],
    bordercolor=[
        ("active", "#FF3355"),
        ("pressed", "#FF3355")
    ]
)


# -------------------------
# BOTONES
# -------------------------
btn_reg_prod = ttk.Button(
    ventana, text="Registro de Productos",
    command=abrir_registro_productos, style="RojoNegro.TButton"
)
btn_reg_prod.pack(pady=12)

btn_reg_ventas = ttk.Button(
    ventana, text="Registro de Ventas",
    command=abrir_registro_ventas, style="RojoNegro.TButton"
)
btn_reg_ventas.pack(pady=12)

btn_reportes = ttk.Button(
    ventana, text="Reportes",
    command=abrir_reportes, style="RojoNegro.TButton"
)
btn_reportes.pack(pady=12)

btn_acerca = ttk.Button(
    ventana, text="Acerca de",
    command=abrir_acerca_de, style="RojoNegro.TButton"
)
btn_acerca.pack(pady=12)

# -------------------------
# INICIO
# -------------------------
ventana.mainloop()
