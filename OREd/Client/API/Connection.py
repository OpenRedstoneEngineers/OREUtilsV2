import socket
import ssl

PORT = 15411
ANDYSDUMBPORT = 4242

class Connection(object):
	def Init(self, host):
		self.socket = ssl.wrap_socket(socket.socket(), keyfile=None)

		self.socket.connect((ANDYSDUMBPORT, host))
		self.socket.recv(1024)
		self.alive = True

	def Loop(self):
		while self.alive:
			yield (self.socket.recv(1024))
	
	def Send(self, message):
		pass
