import os
import socket
import threading
import pymysql

HOST = "0.0.0.0"
PORT = 5000

DB_CONFIG = {
    "user": "socketapp",
    "password": os.getenv("DB_PASSWORD"),
    "database": "agenda",
    "unix_socket": "/run/mysqld/mysqld.sock",
    "cursorclass": pymysql.cursors.DictCursor
}


def consultar_persona(telefono):
    conexion = None

    try:
        conexion = pymysql.connect(**DB_CONFIG)

        with conexion.cursor() as cursor:
            sql = """
                SELECT
                    p.dir_tel,
                    p.dir_nombre,
                    p.dir_direccion,
                    c.ciud_nombre
                FROM personas p
                INNER JOIN ciudades c
                    ON p.dir_ciud_id = c.ciud_id
                WHERE p.dir_tel = %s
            """

            cursor.execute(sql, (telefono,))
            persona = cursor.fetchone()

            if persona:
                return (
                    f"Telefono: {persona['dir_tel']}\n"
                    f"Nombre: {persona['dir_nombre']}\n"
                    f"Direccion: {persona['dir_direccion']}\n"
                    f"Ciudad: {persona['ciud_nombre']}"
                )

            return "Persona dueña de ese número telefónico no existe."

    except Exception as error:
        return f"Error en la consulta: {error}"

    finally:
        if conexion:
            conexion.close()


def atender_cliente(cliente, direccion):
    print(f"[+] Cliente conectado: {direccion}")

    try:
        while True:
            datos = cliente.recv(1024)

            if not datos:
                break

            telefono = datos.decode("utf-8").strip()

            print(f"[+] Telefono recibido: {telefono}")

            respuesta = consultar_persona(telefono)

            cliente.sendall(respuesta.encode("utf-8"))

    except Exception as error:
        print(f"[!] Error con el cliente {direccion}: {error}")

    finally:
        cliente.close()
        print(f"[-] Cliente desconectado: {direccion}")


def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    servidor.bind((HOST, PORT))
    servidor.listen(5)

    print("======================================")
    print("      SOCKET SERVER - SISTEMAS DISTRIBUIDOS")
    print("======================================")
    print(f"Servidor escuchando en el puerto {PORT}")
    print("Esperando conexiones de clientes...")

    while True:
        cliente, direccion = servidor.accept()

        hilo = threading.Thread(
            target=atender_cliente,
            args=(cliente, direccion)
        )

        hilo.start()


if __name__ == "__main__":
    iniciar_servidor()
