import socket

class EnviarDatos:

    def Enviar(self,data):
        
        ip = socket.gethostbyname(socket.gethostname())
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        mensaje_codificado = str(data)

        sock.sendto(mensaje_codificado.encode('utf-8'),(ip,5002))


def main():

    datos = [1,0,0]
    
    mensajero = EnviarDatos()
    mensajero.Enviar(datos)


if __name__ == "__main__":
    main()

