

#!/usr/bin/python


import socket
import sys
import glob, os
import signal

# Close UDP connection on Ctrl+C interrupt
#https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#http://www.binarytides.com/programming-udp-sockets-in-python/

HOST = ''   
uPort = 8888 
 
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'UDP Socket created'
except socket.error, msg :
    print 'Failed to create UDP socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
# Bind socket to local host and port
try:
    s.bind((HOST, uPort))
except socket.error , msg:
    print 'UDP Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'UDP Socket bind complete'
print 'Clients can connect to '+ socket.gethostbyname(socket.gethostname())
 
#now keep talking with the client
while True:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
     
    if not data: 
        break
     
    #check the file list in home_folder and send it to client
    if data == 'list':
        file_list = ""
        for file in os.listdir("home_folder"):
            file_list += file + ' '
        s.sendto(file_list, addr)
     
s.close()