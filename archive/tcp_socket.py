
#!/usr/bin/python

# http://www.tutorialspoint.com/python/python_basic_syntax.htm
# http://www.pythonforbeginners.com/dictionary/python-split
# https://stackoverflow.com/questions/15599639/whats-perfect-counterpart-in-python-for-while-not-eof

import socket
import sys
import glob, os
from functools import partial


BLOCK_SIZE = 256
EOF = "/eof" # end of file marker for receiver socket

s = socket.socket()
host = socket.gethostname()
tPort = 1234
s.bind((host, tPort))

s.listen(5)


while True:
    c, addr = s.accept()
    print "TCP socket connected to ", addr

    #c.send('Thank you for connecting')
    line = c.recv(512)
    cmd, file_name = line.split()

    if cmd == 'get':
        try:
            if os.path.isfile("home_folder/" + file_name):
                c.send('file found')
            else:
                c.send('error file not found')
            file = open("home_folder/" + file_name, "rb")
            c.send(str(os.stat("home_folder/" + file_name).st_size))
            for block in iter(partial(file.read, BLOCK_SIZE), ""):
                c.send(block)
            c.send(EOF)
            file.close()

        except IOError:
            print "error could not read", file_name
            c.send("error could not read file")
            continue

    elif cmd == 'put':
        try:
            file = open("home_folder/" + file_name, "w")
            file_size = c.recv(512)
            print file_size
            while 1:
                block = c.recv(BLOCK_SIZE)
                if EOF in block: 
                    file.write(block.split(EOF,1)[0])
                    print block.split(EOF, 1)[1]
                    break
                elif "error" in block:
                    print block
                    break
                file.write(block)

            file.close()

            if int(file_size) != os.stat("home_folder/" + file_name).st_size:
                print "error expected file size mismatch"
                continue

        except IOError:
            print "error could not write to", local_filename
            c.send("error could not write to file")
            continue

    c.send("ok")
    print 'Command: ', cmd
    print 'Filename: ', file_name
    c.close()
