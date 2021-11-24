import socket
import sys
import threading



#from Balena.sensor_node.src.adc import ADDRESS, DISCONNECT_MESSAGE, HEADER, PORT, SERVER

f = open("../../data/sensorlog.txt", "a+")


clients = []








#TODO: Add code to create a socket ready to recieve data
HEADER = 64
PORT = 5000
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
DISCONNECT_MESSAGE = "DISCONNECTED!"


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(ADDRESS)

def broadcast(mess):
    message = mess.encode()
    mesg_length = len(message)
    send_length = str(mesg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    for client in clients:
        client.send(send_length)
        client.send(message)


def handle_client(newconnection, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(newconnection)

    conected = True
    while conected:
        data_len = newconnection.recv(HEADER).decode(FORMAT)
        if data_len:
           # print("RESULTS IS>>>>> ",data_len)
            data = None
            #if not isinstance(data_len, str):
            data_len = int(data_len)
            data = newconnection.recv(data_len).decode(FORMAT)
           
           # broadcast(data)
            print('\nReceived', repr(data))
            f.write("\nReceived: ")
            f.write(repr(data))
            f.flush()
            if data == "EXIT":
                conected = False
    newconnection.close()


def start():
    serverSocket.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, addres = serverSocket.accept()
        thread = threading.Thread(target=handle_client, args=(connection, addres))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")




print(f"[STARTING] server is starting......")
start()

#with newconnection:
#    while True:
#        data = newconnection.recv(1024)
#        print('\nReceived', repr(data))
#        f.write("\nReceived: ")
#        f.write(repr(data))
#        f.flush()
#        if not data: break


