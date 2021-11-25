from typing import Text
from flask import Flask, send_file, render_template
import socket



SERVER = "127.0.1.1"
PORT = 5000
HEADER = 64
ADDRESS = (SERVER, PORT)

app = Flask(__name__)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(ADDRESS)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/SensorStream')
def sensor_stream():
    #TODO: Add code that displays the contents of log file /data/sensorlog.txt 
    with open("../../data/sensorlog.txt", "r") as file:
        return render_template('index.html', Text=file.read())

@app.route('/download')
def download_file():
    #TODO: Add code to download the file /data.sensorlog.txt
    PATH = "../../data/sensorlog.txt"
    return send_file(PATH, as_attachment=True)

@app.route('/on')
def sensor_on():
    dat = "SENDON"
    data = dat.encode()
    data_len = len(dat)
    send_len = str(data_len).encode('utf-8')
    send_len += b' ' * (HEADER - len(send_len))

    sock.send(send_len)
    sock.send(data)
    return "SUCCESS"

# Sends instruction status to Pi-01 for it to update its current
# status and writes it to a file
# the file is then received and the current status is shown to
# the user.
@app.route('/status')
def sensor_status():
    dat = "STATUS"
    data = dat.encode()
    data_len = len(dat)
    send_len = str(data_len).encode('utf-8')
    send_len += b' ' * (HEADER - len(send_len))

    sock.send(send_len)
    sock.send(data)
    
    PATH = "../../data/status.txt"
    return send_file(PATH, as_attachment=True)


# Routes sends the exit instruction to Pi-01 to exit
@app.route('/off')
def sensor_off():
    dat = "SENDOFF"
    data = dat.encode()
    data_len = len(dat)
    send_len = str(data_len).encode('utf-8')
    send_len += b' ' * (HEADER - len(send_len))

    sock.send(send_len)
    sock.send(data)
    return "SUCCESS"



# Routes sends the exit instruction to Pi-01 to exit
@app.route('/exit')
def server_exit():
    dat = "EXIT"
    data = dat.encode()
    data_len = len(dat)
    send_len = str(data_len).encode('utf-8')
    send_len += b' ' * (HEADER - len(send_len))

    sock.send(send_len)
    sock.send(data)
    return "SUCCESS"


#TODO Add the remaining functions requested either by adding more pages to the template or get fancy with more templates and better formatting
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5080, debug=True) #Use this line to test basic functionality locally before trying to deploy on Pi
 #   app.run(host='0.0.0.0', port=80)
    
