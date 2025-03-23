import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox

class ChatCliente:
    def __init__(self, ventana, nombre_usuario):
        self.ventana = ventana
        self.nombre_usuario = nombre_usuario
        self.ventana.title(f"Chat - {self.nombre_usuario}")
        self.ventana.geometry("500x600")
        self.ventana.configure(bg="#2c3e50")

        self.configurar_estilos()
        self.crear_interfaz()

        try:
            self.conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conexion.connect(("127.0.0.1", 12345))
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {error}")
            ventana.destroy()
            return

        self.hilo_recepcion = threading.Thread(target=self.recibir_mensajes, daemon=True)
        self.hilo_recepcion.start()

    def configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure("Marco.TFrame", background="#34495e")
        estilo.configure("Boton.TButton", font=("Arial", 12, "bold"), padding=10, background="#3498db", foreground="white")
        estilo.map("Boton.TButton", background=[("active", "#2980b9")])

    def crear_interfaz(self):
        marco_principal = ttk.Frame(self.ventana, padding=10, style="Marco.TFrame")
        marco_principal.pack(fill=tk.BOTH, expand=True)

        etiqueta_titulo = ttk.Label(
            marco_principal,
            text=f"Bienvenido, {self.nombre_usuario}",
            font=("Arial", 18, "bold"),
            foreground="#ecf0f1",
            background="#34495e",
        )
        etiqueta_titulo.pack(pady=10)

        self.area_chat = scrolledtext.ScrolledText(
            marco_principal,
            wrap=tk.WORD,
            width=60,
            height=25,
            font=("Arial", 12),
            bg="#ecf0f1",
            fg="#2c3e50",
        )
        self.area_chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.area_chat.config(state=tk.DISABLED)

        self.campo_mensaje = ttk.Entry(marco_principal, font=("Arial", 12))
        self.campo_mensaje.pack(padx=10, pady=5, fill=tk.X, ipady=5)
        self.campo_mensaje.bind("<Return>", self.enviar_mensaje)

        boton_enviar = ttk.Button(
            marco_principal, text="Enviar", command=self.enviar_mensaje, style="Boton.TButton"
        )
        boton_enviar.pack(pady=5, fill=tk.X, ipady=8)

    def enviar_mensaje(self, evento=None):
        mensaje = self.campo_mensaje.get()
        if mensaje:
            try:
                self.conexion.send(mensaje.encode("utf-8"))
                self.campo_mensaje.delete(0, tk.END)
            except Exception as error:
                messagebox.showerror("Error", f"Error enviando mensaje: {error}")

    def recibir_mensajes(self):
        while True:
            try:
                mensaje = self.conexion.recv(1024).decode("utf-8")
                if not mensaje:
                    raise ConnectionResetError("Servidor desconectado")
                self.mostrar_mensaje(mensaje)
            except Exception as error:
                self.mostrar_mensaje("[Desconectado del servidor]")
                messagebox.showwarning("Desconectado", "Se perdió la conexión con el servidor.")
                break

    def mostrar_mensaje(self, mensaje):
        self.area_chat.config(state=tk.NORMAL)
        self.area_chat.insert(tk.END, mensaje + "\n")
        self.area_chat.config(state=tk.DISABLED)
        self.area_chat.yview(tk.END)

if __name__ == "__main__":
    nombre = input("Ingresa tu nombre: ")
    ventana_principal = tk.Tk()
    app = ChatCliente(ventana_principal, nombre)
    ventana_principal.mainloop()