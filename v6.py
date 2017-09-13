# Echo client program
import socket
import sys
import coding
import hashlib
import re
import os.path
import numbers
import time
### elA568HDOM-0
## Setup ####
default_port = '8131'
##################

class Client():

	def __init__(self, _file, _host, _port):
		self.file = _file
		self.host = _host
		self.port = _port
		if not self.check_parameters():
			print("Usage: python3 v6.py [file] [host_ip] [host_port]")
			sys.exit()
		try:
			banner = open("banner.txt", 'r')
			print(banner.read())
		except FileNotFoundError:
			print("[-] Banner is missing :(")
		finally:
			banner.close()
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def check_parameters(self):
		state = True
		if not os.path.exists(self.file):
			print("[-] ERROR: No such file: " + self.file)
			state = False
		ip_format = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
		if not ip_format.match(self.host):
			print("[-] ERROR: Can't take first argument as ipv4 address")
			state =  False
		if self.port.isdigit():  #This block looks stupid but it fits ( ⸌ ل͜ ⸍ )
			self.port = int(self.port)
			if not 1 <= self.port <= 65534:
				print("[-] ERROR: Can't take first argument as host port")
				state = False
		else:
			print("[-] ERROR: Port isn't a number")
			state = False
		return state

	def connect(self):
		print("[*] Trying contacting server")
		try:
			self.connection.connect((self.host, self.port))
		except Exception as e:
			print("[-] Server cant reached: ", e)
			sys.exit()
		message = self.connection.recv(1024)
		print(coding.string(message))

	def login(self):
		login_instruction = self.connection.recv(32)
		if coding.string(login_instruction) == 'c':
			typed_password = input("Type in server password: ")
			hash = hashlib.md5(typed_password.encode('utf-8'))
			self.transmit(coding.byte(hash.hexdigest()))
			if coding.string(self.connection.recv(32)) == 'wrong':
				print("[-] ERROR Server password wasn't correct")
				sys.exit()
		print("[+] Server Password was correct beginning transmision")
	
	def transmit_file(self):
		self.transmit(coding.byte('t')) #Sending Server client want's to Transmit data
		self.transmit(coding.byte(os.path.basename(self.file))) ## Sending Filename
		block_size = 32#int(self.connection.recv(32))Gettin block_size from Server <-- Doesn't work
		file = open(os.path.abspath(self.file), 'rb')
		chunk = file.read(block_size)
		while chunk != b'':
			self.transmit(chunk)
			chunk = file.read(block_size)
		print("[+] Sent file " + self.file)
	def transmit(self, data):
		self.connection.send(data)

if len(sys.argv) > 2:
	HOST = sys.argv[2]
	
	if len(sys.argv) == 4:
		PORT = sys.argv[3]
	else:
		print("[*] No Port was defined: using default port")
		PORT = default_port
	
	c = Client(sys.argv[1], HOST, PORT)
	c.connect()
	c.login()
	c.transmit_file()
	print("Fertig!!")
else:
	print("Usage: python3 v6.py [file] [host_ip] [host_port]") # Wrong Syntax