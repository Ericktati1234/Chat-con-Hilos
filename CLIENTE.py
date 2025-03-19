import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

class ClienteChat:
    def __init__(self, root, cliente_nombre):
        self.root = root
        self.cliente_nombre = cliente_nombre
        self.root.title(f"Chat Cliente - {self.cliente_nombre}")
        self.root.geometry("450x550")
        self.root.configure(bg="#1e272e")

        self.estilos()
        
        self.frame_chat = ttk.Frame(root, padding=10, style="TFrame")
        self.frame_chat.pack(fill=tk.BOTH, expand=True)

        self.label_titulo = ttk.Label(self.frame_chat, text=f"Chat - {self.cliente_nombre}", font=("Arial", 16, "bold"), foreground="#f5f6fa", background="#1e272e")
        self.label_titulo.pack(pady=5)

        self.chat_area = scrolledtext.ScrolledText(self.frame_chat, wrap=tk.WORD, width=50, height=20, font=("Arial", 12), bg="#dcdde1", fg="#2c3e50")
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        self.mensaje_entry = ttk.Entry(self.frame_chat, font=("Arial", 12))
        self.mensaje_entry.pack(padx=10, pady=5, fill=tk.X, ipady=5)
        self.mensaje_entry.bind("<Return>", self.enviar_mensaje)

        self.boton_enviar = ttk.Button(self.frame_chat, text="Enviar", command=self.enviar_mensaje, style="TButton")
        self.boton_enviar.pack(pady=5, fill=tk.X, ipady=8)

        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect(("127.0.0.1", 12345))

        self.hilo_recepcion = threading.Thread(target=self.recibir_mensajes, daemon=True)
        self.hilo_recepcion.start()

    def estilos(self):
        estilo = ttk.Style()
        estilo.configure("TFrame", background="#1e272e")
        estilo.configure("TButton", font=("Arial", 14, "bold"), padding=12, background="#0050a0", foreground="black", borderwidth=0, relief="flat")
        estilo.map("TButton", background=[("active", "#003d80")], foreground=[("active", "black")])

    def enviar_mensaje(self, event=None):
        mensaje = self.mensaje_entry.get()
        if mensaje:
            self.cliente.send(mensaje.encode("utf-8"))
            self.mensaje_entry.delete(0, tk.END)

    def recibir_mensajes(self):
        while True:
            try:
                mensajes = self.cliente.recv(1024).decode("utf-8")
                for mensaje in mensajes.splitlines():
                    self.mostrar_mensaje(mensaje)
            except:
                break

    def mostrar_mensaje(self, mensaje):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, mensaje + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    nombre_cliente = input("Ingresa tu nombre: ")
    root = tk.Tk()
    app = ClienteChat(root, nombre_cliente)
    root.mainloop()