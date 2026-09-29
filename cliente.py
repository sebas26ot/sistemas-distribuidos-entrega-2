import socket

HOST = "192.168.100.10"
PORT = 5000


def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORT))

        print("======================================")
        print("      SOCKET CLIENTE - SISTEMAS DISTRIBUIDOS")
        print("======================================")
        print(f"Conectado al servidor {HOST}:{PORT}")
        print("Escriba un numero de telefono.")
        print("Escriba 'salir' para terminar.\n")

        while True:
            telefono = input("Ingrese el numero de telefono: ").strip()

            if telefono.lower() == "salir":
                break

            if not telefono:
                print("Debe ingresar un numero de telefono.\n")
                continue

            cliente.sendall(telefono.encode("utf-8"))

            respuesta = cliente.recv(4096).decode("utf-8")

            print("\n--- Respuesta del servidor ---")
            print(respuesta)
            print("------------------------------\n")

    except ConnectionRefusedError:
        print("No fue posible conectarse al servidor.")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        cliente.close()
        print("Conexion cerrada.")


if __name__ == "__main__":
    iniciar_cliente()
