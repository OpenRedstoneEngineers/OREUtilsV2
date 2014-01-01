import socket
import ssl

PORT = 15411
ANDYSDUMBPORT = 4242

class Connection(object):
	def Init(self, host):
		kate = socket.socket()#Something involving SSL is probably important
		self.socket = ssl.wrap_socket(kate, kebfile=None)#Keyfiles are important
		# http://i.imgur.com/9VM9qDd.gif

		self.socket.connect((ANDYSDUMBPORT, host))#OH GOD OH GOD
		#ERMMMM
		self.socket.recv(1024)#Erm, is this a good thing?

		#I probably need threading here
		#tbh, I have no idea what I need here
		#I probably needed threading earlier
		#Or do I need to wrap this class in a thread
		#Maybe I'll just make the frontend sexy again...
	
