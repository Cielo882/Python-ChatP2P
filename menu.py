import tkinter as tk
import subprocess

tcp_server_proc = None
tcp_client_proc = None



def start_tcp_server():
    global tcp_server_proc
    subprocess.Popen(["python", "Servidor.py"])


def start_tcp_client():
    global tcp_client_proc
    subprocess.Popen(["python", "Cliente.py"])


def exit_program():
    global tcp_server_proc, tcp_client_proc
    if tcp_server_proc:
        tcp_server_proc.terminate()
    if tcp_client_proc:
        tcp_client_proc.terminate()
    root.destroy()


root = tk.Tk()
root.title("Chat menu")

root.geometry("300x180")
root.pack_propagate(0)
root.resizable(0, 0)

# Color azul claro para los primeros dos botones
tcp_button = tk.Button(root, text="Servidor", command=start_tcp_server, bg="#ADD8E6")
tcp_button.pack(fill="both", expand=True)

tcp_client_button = tk.Button(root, text="Cliente", command=start_tcp_client, bg="#ADD8E6")
tcp_client_button.pack(fill="both", expand=True)


# Color rojo claro para el último botón
exit_button = tk.Button(root, text="Salir", command=exit_program, bg="#FFA07A")
exit_button.pack(fill="both", expand=True)

root.mainloop()
