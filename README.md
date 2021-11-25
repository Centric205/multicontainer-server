# multicontainer-server
PART 2 OF PRACTICAL 6

This multi-container server contains:
  1. A TCP server:
       - This communicates with another raspberry pi using the TCP/IP protocol. It receives ADC values from the other Pi
         and stores them into a csv file.
  2. A webserver:
       - The web server was created using flask and has a web interface that allows the user to controll the other
         raspberry pi transmitting sensory data.
         
After testing the code locally and seeing that it works perfectly, the multi-container was deployed to the Balena cloud.

![image](https://user-images.githubusercontent.com/68051817/143429614-ac9fcfba-35d9-4964-a921-841e5ff57f86.png)

