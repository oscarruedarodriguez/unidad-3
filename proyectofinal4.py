import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

# -------------------------
# TICKET
# -------------------------
def mostrar_ticket(producto, precio, cantidad, total):
    ticket = tk.Toplevel()
    ticket.title("Ticket de Venta")
    ticket.geometry("300x350")
    ticket.resizable(False, False)

    # Fecha y hora
    fecha_hora = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

    # Texto del ticket
    texto = (
        " *** PUNTO DE VENTA ***\n"
        "--------------------------------------\n"
        f"Fecha: {fecha_hora}\n"
        "--------------------------------------\n"
        f"Producto: {producto}\n"
        f"Precio: ${precio}\n"
        f"Cantidad: {cantidad}\n"
        "--------------------------------------\n"
        f"TOTAL: ${total}\n"
        "--------------------------------------\n"
        " ¡GRACIAS POR SU COMPRA!\n"
    )

    lbl_ticket = tk.Label(ticket, text=texto, justify="left", font=("Consolas", 11))
    lbl_ticket.pack(pady=15)

    btn_cerrar = ttk.Button(ticket, text="Cerrar", command=ticket.destroy)
    btn_cerrar.pack(pady=10)



# -------------------------
# REGISTRO DE PRODUCTOS
# -------------------------
def abrir_registro_productos():
   
    reg = tk.Toplevel()
    reg.title("Registro de Productos")
    reg.geometry("400x400")
    reg.resizable(False, False)

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

    def guardar_producto():
        id_prod = txt_id.get().strip()
        descripcion = txt_desc.get().strip()
        precio = txt_precio.get().strip()
        categoria = txt_categoria.get().strip()

        if id_prod == "" or descripcion == "" or precio == "" or categoria == "":
            messagebox.showwarning("Campos Vacíos", "Por favor complete todos los campos.")
            return

        try:
            float(precio)
        except:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(BASE_DIR,"productos.txt")

        with open(archivo, "a", encoding="utf-8") as archivo:
            archivo.write(f"{id_prod}|{descripcion}|{precio}|{categoria}\n")
            messagebox.showinfo("Guardado", "Producto registrado correctamente.")
            txt_id.delete(0, tk.END)
            txt_desc.delete(0, tk.END)
            txt_precio.delete(0, tk.END)
            txt_categoria.delete(0, tk.END)

    btn_guardar = tk.Button(reg, text="Guardar Producto", command=guardar_producto)
    btn_guardar.pack(pady=20)


# -------------------------
# REGISTRO DE VENTAS
# -------------------------
def abrir_registro_ventas():
   
    ven = tk.Toplevel()
    ven.title("Registro de Ventas")
    ven.geometry("420x430")
    ven.resizable(False, False)

    productos = {}

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivof = os.path.join(BASE_DIR,"productos.txt")

        with open(archivof, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split("|")
                if len(partes) == 4:
                    idp, desc, precio, cat = partes
                    productos[desc] = float(precio)

    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo productos.txt")
        ven.destroy()
        return

    lista_productos = list(productos.keys())

    lbl_prod = tk.Label(ven, text="Producto:", font=("Arial", 12))
    lbl_prod.pack(pady=5)

    cb_producto = ttk.Combobox(ven, values=lista_productos, font=("Arial", 12), state="readonly")
    cb_producto.pack(pady=5)

    lbl_precio = tk.Label(ven, text="Precio:", font=("Arial", 12))
    lbl_precio.pack(pady=5)

    txt_precio = tk.Entry(ven, font=("Arial", 12), state="readonly")
    txt_precio.pack(pady=5)

    lbl_cantidad = tk.Label(ven, text="Cantidad:", font=("Arial", 12))
    lbl_cantidad.pack(pady=5)

    cantidad_var = tk.StringVar(ven)
    ven.cantidad_var = cantidad_var
    txt_cantidad = tk.Entry(ven, font=("Arial", 12), textvariable=cantidad_var)
    txt_cantidad.pack(pady=5)

    cantidad_var.trace_add("write", lambda *args: calcular_total())

    lbl_total = tk.Label(ven, text="Total:", font=("Arial", 12))
    lbl_total.pack(pady=5)

    txt_total = tk.Entry(ven, font=("Arial", 12), state="readonly")
    txt_total.pack(pady=5)


    def actualizar_precio(event):
        prod = cb_producto.get()
        if prod in productos:
            txt_precio.config(state="normal")
            txt_precio.delete(0, tk.END)
            txt_precio.insert(0, productos[prod])
            txt_precio.config(state="readonly")
            calcular_total()


    def calcular_total(*args):
        try:
            cant = int(txt_cantidad.get())
            precio = float(txt_precio.get())
            total = cant * precio
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            txt_total.insert(0, total)
            txt_total.config(state="readonly")
        except:
            txt_total.config(state="normal")
            txt_total.delete(0, tk.END)
            txt_total.config(state="readonly")


    def registrar_venta():
        prod = cb_producto.get()
        precio = txt_precio.get()
        cant = txt_cantidad.get()
        total = txt_total.get()

        if prod == "" or precio == "" or cant == "" or total == "":
            messagebox.showwarning("Campos Vacíos", "Todos los campos deben estar completos.")
            return

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivov = os.path.join(BASE_DIR,"ventas.txt")

        with open(archivov, "a", encoding="utf-8") as archivo:
            archivo.write(f"{prod}|{precio}|{cant}|{total}\n")

        messagebox.showinfo("Venta Registrada", "La venta se registró correctamente.")

        mostrar_ticket(prod, precio, cant, total)

        cb_producto.set("")
        txt_precio.config(state="normal"); txt_precio.delete(0, tk.END); txt_precio.config(state="readonly")
        txt_cantidad.delete(0, tk.END)
        txt_total.config(state="normal"); txt_total.delete(0, tk.END); txt_total.config(state="readonly")


    cb_producto.bind("<<ComboboxSelected>>", actualizar_precio)

    btn_guardar = ttk.Button(ven, text="Registrar Venta", command=registrar_venta)
    btn_guardar.pack(pady=25)



# -------------------------
# REPORTES + TOTAL DE VENTAS
# -------------------------
def abrir_reportes():
    ventana = tk.Toplevel()
    ventana.title("Reporte de Ventas")
    ventana.geometry("700x450")
    ventana.configure(bg="#f2f2f2")

    titulo = tk.Label(ventana, text="Reporte de Ventas Realizadas",
                      font=("Arial", 16, "bold"), bg="#f2f2f2")
    titulo.pack(pady=10)

    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(pady=10)

    columnas = ("producto", "precio", "cantidad", "total")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)

    tabla.heading("producto", text="Producto")
    tabla.heading("precio", text="Precio")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("total", text="Total")

    tabla.column("producto", width=250, anchor="center")
    tabla.column("precio", width=100, anchor="center")
    tabla.column("cantidad", width=100, anchor="center")
    tabla.column("total", width=120, anchor="center")
    tabla.pack()

    total_ventas = 0

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(BASE_DIR, "ventas.txt")
        with open(archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.strip():
                    datos = linea.strip().split("|")
                    if len(datos) == 4:
                        tabla.insert("", tk.END, values=datos)
                        total_ventas += float(datos[3])
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo ventas.txt no existe.")
        ventana.destroy()
        return

    lbl_total_ventas = tk.Label(ventana, text=f"TOTAL DE VENTAS: ${total_ventas:.2f}",
                                font=("Arial", 14, "bold"), bg="#f2f2f2", fg="black")
    lbl_total_ventas.pack(pady=15)



def abrir_acerca_de():
    messagebox.showinfo("Acerca de", "Punto de Venta de Ropa\nProyecto Escolar\nVersión 1.0")



# -------------------------
# VENTANA PRINCIPAL
# -------------------------
ventana = tk.Tk()
ventana.title("Punto de Venta - Ropa")
ventana.geometry("500x650")
ventana.resizable(False, False)
ventana.configure(bg="#1E1E1E")

# LOGO
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    imagen = Image.open(os.path.join(BASE_DIR, "ventas2025.png"))
    imagen = imagen.resize((300, 300))
    img_logo = ImageTk.PhotoImage(imagen)

    lbl_logo = tk.Label(ventana, image=img_logo, bg="#1E1E1E")
    lbl_logo.pack(pady=10)

except:
    lbl_sin_logo = tk.Label(ventana, text="(Aquí va el logo del sistema)",
                            font=("Arial", 14), bg="#1E1E1E", fg="white")
    lbl_sin_logo.pack(pady=40)

# ESTILO BOTONES
estilo = ttk.Style()
estilo.theme_use("default")

estilo.configure(
    "RojoNegro.TButton",
    font=("Arial", 12, "bold"),
    padding=12,
    background="#000000",
    foreground="#DC143C",
    bordercolor="#DC143C",
    focustcolor="#DC143C"
)

# BOTONES
btn_productos = ttk.Button(ventana, text="Registro de Productos",
                           style="RojoNegro.TButton", command=abrir_registro_productos)
btn_productos.pack(pady=10)

btn_ventas = ttk.Button(ventana, text="Registro de Ventas",
                        style="RojoNegro.TButton", command=abrir_registro_ventas)
btn_ventas.pack(pady=10)

btn_reportes = ttk.Button(ventana, text="Reportes",
                          style="RojoNegro.TButton", command=abrir_reportes)
btn_reportes.pack(pady=10)

btn_acerca = ttk.Button(ventana, text="Acerca de",
                        style="RojoNegro.TButton", command=abrir_acerca_de)
btn_acerca.pack(pady=10)

ventana.mainloop()
