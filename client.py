
#!/usr/bin/python

import glob, os, getopt, sys, socket
from functools import partial

# Constants
BLOCK_SIZE = 256
EOF = "/eof" # end of file marker for receiver socket
SOF = "sof/" # start of file marker 

#-------------#
# SET IP/PORT #
#-------------#

def usage():
	print "client.py expects all of the following parameters:"
	print "  client.py -i <Server IP> -p <UDP port> -c <get | put> -l <localfile> -r <remotefile>"

try: 
	opts, args = getopt.getopt(sys.argv[1:],"hi:p:c:l:r:",["ipAddr=","port=","command=","localfile=", "remotefile="])
except getopt.GetoptError:
	usage()
	sys.exit(2)

if len(opts) != 5:
	usage()
	sys.exit(2)

for opt, arg in opts:
	if opt in ("-i", "--ipAddr"):
		serverAddr = arg
	elif opt in ("-p", "--port"):
		uPort = int(arg)
	elif opt in ("-l", "--localfile"):
		local_filename = arg
	elif opt in ("-r", "--remotefile"):
		remote_filename = arg
	elif opt in ("-c", "--command"):
		cmd = arg

if not serverAddr:
	serverAddr = socket.gethostname()

#---------#
# STAGE 1 #
#---------#

# create dgram udp socket
try:
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print 'Failed to create socket'
	sys.exit()

# Get the list of files via the UDP socket connection and print them to the console
def getFileList(): 
	udp_socket.sendto('list', (serverAddr, uPort))
	file_list = udp_socket.recvfrom(1024)[0].split()
	print "Retrieved files:"
	print "  " + ("\n  ".join(file_list))

# Get available TCP Port via UDP connection
def getTCPPort():
	udp_socket.sendto("port", (serverAddr, uPort))
	return udp_socket.recvfrom(1024)[0]

getFileList()

#---------#
# STAGE 2 #
#---------#

# Create TCP connection and send command
def connectTCP(msg):
	global s
	s = socket.socket()
	tPort = getTCPPort()
	s.connect((serverAddr, int(tPort)))
	s.send(msg)

# Kill TCP connection, print error message and send command
def killTCP(msg):
	print msg
	s.close()
	sys.exit()


if cmd == 'get':
	
	connectTCP('get ' + remote_filename)

	msg = s.recv(512)
	if "error" in msg:
		killTCP(msg)

	# get expected file size
	file_size = s.recv(512)

	try:
	  file = open(local_filename, "w")
	except IOError:
	  print "error writing to", local_filename
	  sys.exit()

	while 1:
		block = s.recv(BLOCK_SIZE)
		if EOF in block: 
			file.write(block.split(EOF,1)[0])
			print block.split(EOF, 1)[1]
			break
		elif "error" in block:
			file.close()
			killTCP(block)
			
		file.write(block)

	file.close()

	# make sure received file is same size as expected, otherwise print error
	if int(file_size) == os.stat(local_filename).st_size:
		data = s.recv(1024)
		print data
	else:
		killTCP("error received file size mismatch")

	s.close

if cmd == 'put':

	if not os.path.isfile(local_filename):
		print "error file not found"
		sys.exit()

	connectTCP('put ' + remote_filename)

	# Send the file size, and mark the beginning of the file
	if s.recv(256) == "req_filesize":
		s.send(str(os.stat(local_filename).st_size) + " " + SOF)

	try:
	  	file = open(local_filename, "rb")
	except IOError:
	  	s.send("error could not read file")
	  	killTCP("error reading", local_filename)

	for block in iter(partial(file.read, BLOCK_SIZE),''):
		s.send(block)
	s.send(EOF)
	file.close()

	data = s.recv(1024)
	print data + ''
	s.close


sys.exit()
 