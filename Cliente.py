import tkinter
import socket
import threading

gui = tkinter.Tk()
gui.title("Cliente")
gui.config(bg='#B9EDDD')
gui.resizable(0, 0)

flagTCP = False
flagUDP = False

formato = "utf-8"

# -----------------------------------------------------------------------------------------------------------------------
# Cliente TCP
conn = None  # Esta variable va a almacenar la información del cliente


def getInfoTCP():
    while True:
        data = conn.recv(1024)  # Recepción de la información enviada por el servidor
        msg = data.decode(formato)
        if msg.startswith("[USERS]"):  # Si el mensaje es una lista de usuarios
            userList = msg[7:].split(",")  # Extraemos la lista de usuarios
            txt2.delete('1.0', tkinter.END)
            txt2.insert(tkinter.INSERT, userList)
        else:
            txt.insert(tkinter.INSERT, data.decode(formato))


def connectServerTCP():
    global flagTCP
    flagTCP = True
    global conn
    ip = eip.get()
    port = 5555
    user = euser.get()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((ip, int(port)))
    client.send(user.encode(formato))
    conn = client

    txtT.insert(tkinter.INSERT, "Conectado a TCP")

    t = threading.Thread(target=getInfoTCP)
    t.start()


def sendMsgTCP():
    friend = eFriend.get()
    sendStr = esend.get()
    sendStr = friend + ":" + sendStr
    conn.send(sendStr.encode(formato))


def disconnectTCP():
    conn.close()
    gui.destroy()


# gui.protocol("WM_DELETE_WINDOW", disconnectTCP)

# -----------------------------------------------------------------------------------------------------------------------
# Cliente UDP

connUDP = None  # Esta variable va a almacenar la información del cliente


def getInfoUDP():  # Recibir información del servidor
    while True:
        data, addr = connUDP.recvfrom(1024)  # Recepción de la información enviada por el servidor
        msg = data.decode(formato)
        if msg.startswith("[USERS]"):  # Si el mensaje es una lista de usuarios
            userList = msg[7:].split(",")  # Extraemos la lista de usuarios
            txt2.delete('1.0', tkinter.END)
            txt2.insert(tkinter.INSERT, userList)
        else:
            txt.insert(tkinter.INSERT, data.decode(formato))


def connectServerUDP():  # Conectar al servidor
    global flagUDP
    flagUDP = True
    global connUDP
    ip = eip.get()  # Obtener la dirección IP, puerto y nombre de usuario ingresados por el cliente
    port = 8888
    user = euser.get()
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client.sendto(user.encode(formato), (ip, int(port)))  # Enviar el nombre de usuario al servidor
    connUDP = client

    txtT.insert(tkinter.INSERT, "Conectado a UDP")

    t = threading.Thread(target=getInfoUDP)
    t.start()


def sendMsgUDP():  # Obtener el destinatario y el mensaje ingresados por el cliente
    ip = eip.get()  # Obtener la dirección IP, puerto y nombre de usuario ingresados por el cliente
    port = 8888
    friend = eFriend.get()
    user = euser.get()
    sendStr = esend.get()
    sendStr = user + ":" + friend + ":" + sendStr
    connUDP.sendto(sendStr.encode(formato), (ip, int(port)))  # Enviar la cadena de texto al servidor junto con la
    # dirección IP y el puerto


def disconnectUDP():
    ip = eip.get()  # Obtener la dirección IP, puerto y nombre de usuario ingresados por el cliente
    port = 8888
    friend = eFriend.get()
    user = euser.get()
    sendStr = user + ":" + friend + ":" + "QUIT"
    connUDP.sendto(sendStr.encode(formato), (ip, int(port)))
    connUDP.close()
    gui.destroy()


# gui.protocol("WM_DELETE_WINDOW", disconnectUDP)


def msgtype():
    if flagTCP:
        sendMsgTCP()
    elif flagUDP:
        sendMsgUDP()


def disconnectiontype():
    if flagTCP:
        disconnectTCP()
    elif flagUDP:
        disconnectUDP()
    else:
        gui.destroy()


gui.protocol("WM_DELETE_WINDOW", disconnectiontype)

# Interfaz gráfica del cliente
labelUser = tkinter.Label(gui, text="Nombre de usuario:", bg='#569DAA', fg='ghostwhite')
labelUser.grid(row=0, column=0, padx=5, pady=5, sticky='w')

euser = tkinter.Variable()
entryUser = tkinter.Entry(gui, textvariable=euser, width=30)
entryUser.grid(row=0, column=1, padx=5, pady=5, sticky='w')

labelIp = tkinter.Label(gui, text="IP:", bg='#569DAA', fg='ghostwhite')
labelIp.grid(row=1, column=0, padx=5, pady=5, sticky='w')
eip = tkinter.Variable()
entryIp = tkinter.Entry(gui, textvariable=eip, width=30)
entryIp.grid(row=1, column=1, padx=5, pady=5, sticky='w')

'''labelPort = tkinter.Label(gui, text="Puerto:", bg='royalblue', fg='ghostwhite')
labelPort.grid(row=2, column=0, padx=5, pady=5, sticky='w')
eport = tkinter.Variable()
entryPort = tkinter.Entry(gui, textvariable=eport, width=30)
entryPort.grid(row=2, column=1, padx=5, pady=5, sticky='w')'''

button = tkinter.Button(gui, text="Conectarse (TCP)", command=connectServerTCP)
button.grid(row=3, column=1, padx=5, pady=5, sticky='w')

button = tkinter.Button(gui, text="Conectarse (UDP)", command=connectServerUDP)
button.grid(row=4, column=1, padx=5, pady=5, sticky='w')

button = tkinter.Button(gui, text="Salir", command=disconnectiontype)
button.grid(row=1, column=3, padx=5, pady=4, sticky='w')

labelFriend = tkinter.Label(gui, text="Destinatario:", bg='#569DAA', fg='ghostwhite')
labelFriend.grid(row=5, column=0, padx=5, pady=5, sticky='w')
eFriend = tkinter.Variable()
entryFriend = tkinter.Entry(gui, textvariable=eFriend, width=30)
entryFriend.grid(row=5, column=1, padx=5, pady=5, sticky='w')

labelSend = tkinter.Label(gui, text="Mensaje:", bg='#569DAA', fg='ghostwhite')
labelSend.grid(row=6, column=0, padx=5, pady=5, sticky='w')
esend = tkinter.Variable()
entrySend = tkinter.Entry(gui, textvariable=esend, width=30)
entrySend.grid(row=6, column=1, padx=5, pady=5, sticky='w')

button2 = tkinter.Button(gui, text="Enviar", command=msgtype)
button2.grid(row=7, column=1, padx=5, pady=5, sticky='w')

labelTxt = tkinter.Label(gui, text="Mensajes recibidos:", bg='#569DAA', fg='ghostwhite')
labelTxt.grid(row=8, column=0, padx=5, pady=5, sticky='w')
txt = tkinter.Text(gui, height=8, width=40)
txt.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

labelTxt = tkinter.Label(gui, text="Usuarios conectados:", bg='#569DAA', fg='ghostwhite')
labelTxt.grid(row=8, column=3, padx=5, pady=5, sticky='w')
txt2 = tkinter.Text(gui, height=8, width=20)
txt2.grid(row=9, column=3, columnspan=2, padx=5, pady=5)

txtT = tkinter.Text(gui, height=1, width=18)
txtT.grid(row=0, column=3, padx=0, pady=0)

gui.mainloop()
