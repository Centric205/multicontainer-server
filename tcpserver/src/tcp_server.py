import socket
import sys
import threading
import time
import datetime



#from Balena.sensor_node.src.adc import ADDRESS, DISCONNECT_MESSAGE, HEADER, PORT, SERVER

f = open("../../data/sensorlog.txt", "a+")


clients = []  # stores connections that are active
ldr_values = []  # stores sensor ldr values
temp_values_raw = []  # stores temp ldr values
temp_values = []
date_values = []



# Writes data in a nice format
def write_results():
    ts = time.time()
    for i in range(len(ldr_values)):
        f.write(f"{date_values[i]}s\t <{temp_values_raw[i]}>\t <{temp_values[i]}> C  <{ldr_values[i]}>\t")




#TODO: Add code to create a socket ready to recieve data
HEADER = 64
PORT = 5000
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())  # gets local host IP
ADDRESS = (SERVER, PORT)
DISCONNECT_MESSAGE = "DISCONNECTED!"


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(ADDRESS)

# Server uses this function to send broadcast messages to active clients
def broadcast(mess):
    message = mess.encode()
    mesg_length = len(message)
    send_length = str(mesg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    for client in clients:
        client.send(send_length)
        client.send(message)


# Handles active clients connected to the server
def handle_client(newconnection, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(newconnection)

    LDR = None
    TEMP = None

    conected = True
    while conected:
        data_len = newconnection.recv(HEADER).decode(FORMAT)
        if data_len:
           # print("RESULTS IS>>>>> ",data_len)
            data = None
            #if not isinstance(data_len, str):
            data_len = int(data_len)
            data = newconnection.recv(data_len).decode(FORMAT)
            
            if data == "LDR":
                LDR_len = int(data_len)
                LDR = newconnection.recv(data_len).decode(FORMAT)
                ldr_values.append(LDR)
            
            elif data == "TEMP":
                TEMP_len = int(data_len)
                TEMP = newconnection.recv(data_len).decode(FORMAT)
                temp_values.append(TEMP)

                # Temp values converted to degrees
                TEMP_len = int(data_len)
                TEMP = newconnection.recv(data_len).decode(FORMAT)
            
            elif data == "SENDON" or data == "SENDOFF" or data == "STATUS":
                broadcast(data)  # This is for when the used interacts with the buttons on the web UI
                                 # the message gets sent to Pi-01

            else:
                date_len = int(data_len)
                date_ = newconnection.recv(date_len).decode(FORMAT)
                date_values.append(date_)


            print('\nReceived', repr(data))
            f.write("\nReceived: ")
            f.write(repr(data))
            f.flush()
            write_results()    # writes to file
            if data == "EXIT":
                conected = False
    newconnection.close()


# Starts the connection and continues listening on any incoming messages
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


