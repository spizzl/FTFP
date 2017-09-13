import socket
import sys
import hashlib
import coding
import _thread
###### Setup #######
WelcomeMessage = "Welcome To my FTFP Server!\n"
PORT = 8131
block_size = 32
####################
class server():
	def __init__(self, Port):
		self.Host = ''
		self.Port = Port
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def password(self):
		new_pass1 = input('Type in new Password: ')
		new_pass2 = input('Repeat: ')
		if new_pass1 != new_pass2:
			print("Password doesn't match!")
		else:
			hash = hashlib.md5(new_pass1.encode('utf-8'))
			hash_file = open("hash", 'w')
			hash_file.write(hash.hexdigest())
			hash_file.close()
			print("Wrote hash to files! KEEP THE FILE SAFE!")

	def socket_start(self):
		try:
			self.serversocket.bind((self.Host, self.Port))
		except socket.error as msg:
			print ("Laeuft Nicht, weil: ", msg)
			sys.exit
		print("Built socket...")
		print("Server is ready. Waiting for connections...")
	
	def listen_for_peer(self):
		self.serversocket.listen(6)
		conn, addr = self.serversocket.accept()
		print ("Got Connection from " + addr[0] + ":" + str(addr[1]))	
		return conn, addr



#FTP
#Florins Transsexuelle
class client():

	def __init__(self, _peer, _addr):
		self.peer = _peer
		self.addr = _addr

	def receive_file(self):
		file_name = coding.string(self.peer.recv(64))
		#self.peer.send(bytes(block_size)) Coming soong doesn't work for now!
		file = open(file_name, 'wb')
		while True:
			data = self.peer.recv(block_size)
			if data != b'':
				file.write(data)
			else:
				print("Transmitted File " + file_name)
				file.close()
				sys.exit()

	def handle_peer(self):
		print("Sending Welcome Message...")
		self.peer.send(coding.byte(WelcomeMessage))
		self.peer.send(coding.byte('c'))
		print("Waiting for Hash...")
		try_login = self.peer.recv(1024)
		hash_file = open("hash", 'r')
		h = hash_file.read()
		hash_file.close()
		if coding.string(try_login) == h:
			print(self.addr[0], " logged in")
			self.peer.send(coding.byte('correct'))
			if coding.string(self.peer.recv(32)) == 't': ## Peer wants to transmit data!
				self.receive_file()
		else:
			print(self.addr[0], " Failed to Login")
			self.peer.send(coding.byte('wrong'))	
			self.peer.close()
			sys.exit()

#############################  Class Ending  ######################################


client_stack = []
ftp = server(PORT)
if len(sys.argv) > 1:
	if sys.argv[1].lower() == "server" or sys.argv[1].lower() == "s":
		ftp.socket_start()
		Quit = False
		while not Quit:
			connected_peer, addr = ftp.listen_for_peer()
			c = client(connected_peer, addr)
			_thread.start_new_thread(c.handle_peer, ())
			client_stack.append(c)
	elif sys.argv[1].lower() == "password" or sys.argv[1].lower() == "p":
		ftp.password()
	else:
		print("ftp: illegal option")
		print("usage: python3 sever.py [ s(erver) | p(assword) ]")
else:
	print("ftp: nothing to do")
	print("usage: python3 sever.py [ s(erver) | p(assword) ]")
#print("Usage: python server.py (password, server)")