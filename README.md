
# Project
A simple Python server that runs two sockets for transferring files

## UDP Socket
When client connects, send the client a list of files, and an available TCP port to connect.

## TCP/IP Socket
Client connects with `get` or `put` command and provides `local_filename` and `remote_filename`, along with `port` for file transfer.

# Assumptions 
- home_folder directory exists in the same place as server.sh


# Instructions 

1) Run ./server.sh and provide a UDP port (optional) in the console. If no UDP port is specified, it will pick one and print it to the console. 
2) Modify command line arguments in client.sh (all parameters are required, but IP address can be "" for localhost)
3) Run ./client.sh
4) To close server, press Ctrl+C (may need to do it twice)


# Tested on    
Python 2.7.6


#  References  
Sample code adapted from the following sources: 

http://www.tutorialspoint.com/python/python_basic_syntax.htm
http://www.pythonforbeginners.com/dictionary/python-split
https://stackoverflow.com/questions/15599639whats-perfect-counterpart-in-python-for-while-not-eof
https://stackoverflow.com/questions/23828264how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
http://www.tutorialspoint.com/python/python_command_line_arguments.htm
http://www.binarytides.com/programming-udp-sockets-in-python/
https://stackoverflow.com/questions/11815947/cannot-kill-python-script-with-ctrl-c

