import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ClienteChat:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Cliente")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)
        self.chat_area.config(state=tk.DISABLED)

        self.mensaje_entry = tk.Entry(root, width=50)
        self.mensaje_entry.pack(padx=10, pady=5)
        self.mensaje_entry.bind("<Return>", self.enviar_mensaje)

        self.boton_enviar = tk.Button(root, text="Enviar", command=self.enviar_mensaje)
        self.boton_enviar.pack(pady=5)

        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect(("127.0.0.1", 12345))

        # Hilo para recibir mensajes del servidor
        self.hilo_recepcion = threading.Thread(target=self.recibir_mensajes, daemon=True)
        self.hilo_recepcion.start()

    def enviar_mensaje(self, event=None):
        mensaje = self.mensaje_entry.get()
        if mensaje:
            self.cliente.send(mensaje.encode("utf-8"))
            self.mensaje_entry.delete(0, tk.END)

    def recibir_mensajes(self):
        while True:
            try:
                mensaje = self.cliente.recv(1024).decode("utf-8")
                self.mostrar_mensaje(mensaje)
            except:
                break

    def mostrar_mensaje(self, mensaje):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, mensaje + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteChat(root)
    root.mainloop()
