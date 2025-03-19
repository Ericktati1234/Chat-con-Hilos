import socket
import threading

clientes = []
mensajes = []  # Lista para almacenar el historial de mensajes

def manejar_cliente(cliente_socket, direccion):
    print(f"[*] Nueva conexión desde {direccion}")

    # Enviar historial de mensajes al nuevo cliente con saltos de línea
    for mensaje in mensajes:
        cliente_socket.send((mensaje + "\n").encode("utf-8"))

    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode("utf-8").strip()
            if not mensaje:
                break

            mensaje_formateado = f"{direccion}: {mensaje}"
            print(mensaje_formateado)

            # Guardar mensaje en el historial
            mensajes.append(mensaje_formateado)

            # Enviar el mensaje a todos los clientes con salto de línea
            for cliente in clientes:
                cliente.send((mensaje_formateado + "\n").encode("utf-8"))

        except:
            break

    print(f"[*] {direccion} se ha desconectado")
    clientes.remove(cliente_socket)
    cliente_socket.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("0.0.0.0", 12345))
    servidor.listen(5)
    print("[*] Servidor escuchando en el puerto 12345...")

    while True:
        cliente_socket, direccion = servidor.accept()
        clientes.append(cliente_socket)
        hilo = threading.Thread(target=manejar_cliente, args=(cliente_socket, direccion))
        hilo.start()

if __name__ == "__main__":
    iniciar_servidor()
