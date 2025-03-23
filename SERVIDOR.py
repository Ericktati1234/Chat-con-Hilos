import socket
import threading

class ServidorChat:
    def __init__(self, host="0.0.0.0", puerto=12345):
        self.host = host
        self.puerto = puerto
        self.conexiones = []
        self.historial = []
        self.bloqueo_conexiones = threading.Lock()
        self.bloqueo_historial = threading.Lock()

    def gestionar_cliente(self, cliente, direccion):
        print(f"[+] Conexión establecida con {direccion}")

        with self.bloqueo_historial:
            for mensaje in self.historial:
                cliente.send((mensaje + "\n").encode("utf-8"))

        while True:
            try:
                mensaje = cliente.recv(1024).decode("utf-8").strip()
                if not mensaje:
                    break

                mensaje_formateado = f"{direccion}: {mensaje}"
                print(mensaje_formateado)

                with self.bloqueo_historial:
                    self.historial.append(mensaje_formateado)

                with self.bloqueo_conexiones:
                    for conexion in self.conexiones:
                        try:
                            conexion.send((mensaje_formateado + "\n").encode("utf-8"))
                        except Exception as error:
                            print(f"[!] Error enviando a {conexion.getpeername()}: {error}")

            except Exception as error:
                print(f"[!] Error recibiendo desde {direccion}: {error}")
                break

        print(f"[-] {direccion} se ha desconectado")
        with self.bloqueo_conexiones:
            if cliente in self.conexiones:
                self.conexiones.remove(cliente)
        cliente.close()

    def iniciar(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((self.host, self.puerto))
        servidor.listen(5)
        print(f"[*] Servidor activo en {self.host}:{self.puerto}")

        while True:
            cliente, direccion = servidor.accept()
            with self.bloqueo_conexiones:
                self.conexiones.append(cliente)
            hilo = threading.Thread(target=self.gestionar_cliente, args=(cliente, direccion), daemon=True)
            hilo.start()

if __name__ == "__main__":
    servidor = ServidorChat()
    servidor.iniciar()