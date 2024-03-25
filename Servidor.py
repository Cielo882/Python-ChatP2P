import tkinter
import socket
import threading

gui = tkinter.Tk()  # La interfaz principal
gui.title("Servidor")
gui.config(bg='skyblue')
gui.resizable(0, 0)

flag = False

formato = "utf-8"  # Formato en el que se envían y reciben los mensajes

usersTCP = {}
usersUDP = {}


# -----------------------------------------------------------------------------------------------------------------------
# Servidor TCP
def getUsersTCP():
    userList = [user for user in usersTCP]
    return userList


def runTCP(conn, addr):
    try:
        userName = conn.recv(1024)  # Socket del usuario
        usersTCP[userName.decode(formato)] = conn  # decodificación y almacenamiento del usuario
        ip, port = addr
        client_info = f"{ip}:{port}"
        msgConn = f"{userName.decode(formato)} se ha conectado al servidor [{client_info}]\n"
        txt.insert(tkinter.INSERT, msgConn)

        # Enviamos la lista de usuarios conectados al cliente
        userList = getUsersTCP()
        userMsg = "[USERS]" + ",,".join(userList)
        for user_conn in usersTCP.values():
            user_conn.send(userMsg.encode(formato))
        print(userList)

        while True:
            data = conn.recv(1024)  # Recibimos la información enviada por el usuario
            userMsg = data.decode(formato)
            infoList = userMsg.split(":")  # Se divide la cadena para poder acceder solo al nombre de usuario
            usersTCP[infoList[0]].send((userName.decode(formato) + " dice: \n" + infoList[1] + "\n").encode(formato))

    except ConnectionResetError:  # Manejo de excepción cuando se pierde la conexión con el cliente
        disconnected_user = userName.decode(formato)
        del usersTCP[disconnected_user]
        msgDisconn = disconnected_user + " se ha desconectado\n"
        txt.insert(tkinter.INSERT, msgDisconn)
        # Enviamos la lista de usuarios conectados al cliente
        userList = getUsersTCP()
        userMsg = "[USERS]" + ",,".join(userList)
        for user_conn in usersTCP.values():
            user_conn.send(userMsg.encode(formato))
        print(userList)


def startTCP():
    global tcp
    ip = eip.get()  # Vamos a obtener la ip de entrada
    port = 5555  # Obtenemos también el puerto de la entrada
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, int(port)))
    tcp = server

    server.listen(5)
    msg = f"Servidor en linea en {ip}:{port}\n"
    print(f"Servidor en linea en {ip}:{port}\n")
    txt.insert(tkinter.INSERT, msg)

    while True:
        conn, addr = server.accept()  # Se acepta la información recibida por el cliente
        thr = threading.Thread(target=runTCP, args=(conn, addr))  # Se establecen a los clientes conectados como hilos
        thr.start()


def startServerTCP():
    s = threading.Thread(target=startTCP)  # Se abre un hilo para iniciar el servidor
    s.start()  # Abrimos el hilo


# -----------------------------------------------------------------------------------------------------------------------
# Servidor UDP
def getUsersUDP():
    userList = [user for user in usersUDP]
    return userList


def runUDP(ip, port):
    global udp
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    udp = server_socket
    txt.insert(tkinter.INSERT, f"Servidor iniciado correctamente en {ip}:{port}\n")
    print(f"Servidor iniciado correctamente en {ip}:{port}\n")

    while True:
        data, address = server_socket.recvfrom(1024)
        userMsg = data.decode(formato)
        infoList = userMsg.split(":")
        user = infoList[0]
        if infoList[0] not in usersUDP:
            usersUDP[infoList[0]] = address
            msgConn = "" + infoList[0] + " se ha conectado al servidor\n"
            txt.insert(tkinter.END, msgConn)
            userList = getUsersUDP()
            userMsg = "[USERS]" + ",,".join(userList)
            for user_addr in usersUDP.values():
                server_socket.sendto(userMsg.encode(formato), user_addr)
            print(userList)
        elif infoList[2] == "QUIT":  # Si el mensaje es de salida de usuario
            del usersUDP[user]  # Eliminar usuario de la lista
            msgDis = "" + user + " ha dejado el servidor\n"
            txt.insert(tkinter.END, msgDis)
            userList = getUsersUDP()
            userMsg = "[USERS]" + ",,".join(userList)
            for user_addr in usersUDP.values():
                server_socket.sendto(userMsg.encode(formato), user_addr)
        else:
            destName = infoList[1]
            destAddr = usersUDP[destName]
            msg = "Mensaje de " + user + ": \n" + infoList[2] + "\n"
            server_socket.sendto(msg.encode(formato), destAddr)


def startUDP():
    global ip, port
    ip = eip.get()
    port = int(8888)
    t = threading.Thread(target=runUDP, args=(ip, port))
    t.start()


def serverS():
    global flag
    flag = True
    startServerTCP()
    startUDP()


def stop():
    if flag:
        tcp.close()
        udp.close()
        gui.destroy()
    else:
        gui.destroy()


gui.protocol("WM_DELETE_WINDOW", stop)

# Atributos de la interfaz

eip = tkinter.StringVar()
eport = tkinter.StringVar()

labelIp = tkinter.Label(gui, text="IP: ", bg='steelblue', fg='white')
labelIp.grid(row=0, column=0, padx=5, pady=5, sticky='w')

entryIp = tkinter.Entry(gui, textvariable=eip, width=20)
entryIp.grid(row=0, column=1, padx=5, pady=5, sticky='w')

serverButton = tkinter.Button(gui, text="Iniciar Servidor", command=serverS)
serverButton.grid(row=2, column=1, padx=5, pady=5, sticky='w')

button = tkinter.Button(gui, text="Cerrar Servidor", command=stop)
button.grid(row=3, column=1, padx=5, pady=4, sticky='w')

labelTxt = tkinter.Label(gui, text="Mensaje del Servidor: ", bg='steelblue', fg='white')
labelTxt.grid(row=4, column=0, padx=5, pady=5, sticky='w')

txt = tkinter.Text(gui, height=8, width=50)
txt.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Loop para mantener ejecutándose la interfaz
gui.mainloop()
