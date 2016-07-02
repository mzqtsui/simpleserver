
import glob, os, signal, threading, sys, socket, time
from functools import partial

BLOCK_SIZE = 256
EOF = "/eof" # end of file marker for receiver socket
SOF = "sof/" # start of file marker 

class Server(object):

	# Server constructor: 
	#  1) Assign host and uPort
	#  2) Create and bind UDP socket
	#  3) Put UDP socket in its own thread and daemon it 
	#  4) Sleep main thread
	def __init__(self, port):
		self.host = socket.gethostname()
		self.uPort = 0 if not port else port

		# Try to create UDP socket
		try:
			self.uSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.uSocket.bind((self.host, self.uPort))
		except socket.error , msg:
			print "UDP Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1]
			sys.exit()
		print "UDP socket bound to " + socket.gethostbyname(socket.gethostname()) + " on port " + str(self.uSocket.getsockname()[1])

		# Attach thread to main so it dies when main thread is killed
		uThread = threading.Thread(target = self.udpListen, args = ())
		uThread.daemon = True
		uThread.start()

		# Sleep main thread and keep it around for Ctrl+C 
		while True:
			time.sleep(1)
	
	# createTCPConnection
	#  1) Choose available port
	#  2) Create and bind TCP socket
	#  3) Put it in a thread 
	def createTCPConection(self):
		try:
			tSocket = socket.socket()
			tSocket.bind((self.host, 0)) # Select any available port
		except socket.error, msg:
			print "TCP Bind failed. Error Code: " + str(msg[0]) + " Message " + msg[1]
			sys.exit()
		print "TCP socket bound to " + socket.gethostbyname(socket.gethostname()) + " on port " + str(tSocket.getsockname()[1])
		
		# Attach thread to main so it dies when main thread is killed
		tThread = threading.Thread(target = self.tcpListen, args = ([tSocket]))
		tThread.daemon = True
		tThread.start()

		return str(tSocket.getsockname()[1])

	# UDP socket running on separate thread
	# Handles returning file list and available TCP port for connection
	def udpListen(self):

		while True:
			# receive data from client (data, addr)
			d = self.uSocket.recvfrom(1024)
			data = d[0]
			addr = d[1]

			if not data: 
				break
			
			# Check the file list in home_folder and send it to client
			if data == "list":
				file_list = ""
				for file in os.listdir("home_folder"):
					file_list += file + " "
				self.uSocket.sendto(file_list, addr)

			# Create TCP socket and bind to port, send port to client
			if data == "port":
				tPort = self.createTCPConection()
				self.uSocket.sendto(tPort, addr)

	# TCP socket running on separate thread
	def tcpListen(self, tSocket):
		#listen for tcp connection
		tSocket.listen(5)
		while True:
			c, addr = tSocket.accept()
			c.settimeout(30)
			print "TCP socket connected to ", addr

			#c.send('Thank you for connecting')
			line = c.recv(512)
			cmd, file_name = line.split()
			print line

			if cmd == 'get':
				try:
					if os.path.isfile("home_folder/" + file_name):
						c.send('file found')
					else:
						c.send('error file not found')
						continue
					file = open("home_folder/" + file_name, "rb")

					# Send size over before sending file
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
				# Ask client for filesize for later reference
				c.send('req_filesize')
				try:
					file = open("home_folder/" + file_name, "w")
					data = c.recv(256)

					#file size may be in same data block as beginning of file
					file_size, init = data.split(SOF)
					if EOF in init:
						file.write(init.split(EOF,1)[0])
					else:
						file.write(init)

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
			print "Transaction complete"
			c.close()

# main method
if __name__ == "__main__":
	port_num = raw_input("UDP Port (optional): ")
	if not port_num:
		port_num = 0
	Server(int(port_num))



