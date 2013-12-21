import socket
import threading

from Helper import Info

"""
@brief Client socket wrapper.
"""
class Connection(object):
	BUFFER_SIZE = 1024

	LOG_FILE = open("IRCLog.txt", "a") # Change this to None to disable logging

	def __init__(self, hostname, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.thread = threading.Thread(target=self.Loop)
		self.running = False

		self.Connect(hostname, port)

	def Connect(self, hostname, port):
		if self.running == True:
			return

		try:
			self.socket.connect((hostname, port))

			self.running = True

			self.thread.start()

		except:
			self.running = False

			Info("Couldn't connect to %s" % hostname)

	def Reconnect(self, hostname, port):
		self.Stop()

		self.socket.__init__(socket.AF_INET, socket.SOCK_STREAM)

		self.thread.__init__(target=self.Loop)

		self.Connect(hostname, port)

	def Disconnect(self):
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()

	def Stop(self):
		if self.running == False:
			return

		self.running = False

		self.thread.join()

		self.Disconnect()

	def Send(self, message):
		if self.running == False:
			return

		try:
			self.socket.sendall(message)

		except:
			self.running = False

			Info("Could not send packet")

	def Loop(self):
		while self.running:
			try:
				data = self.socket.recv(self.BUFFER_SIZE).strip().encode("ascii", "ignore")

			except Exception, E:
				self.running = False

				Info("IRC Socket is dead")
				break

			if len(data) == 0:
				self.running = False

				Info("IRC Socket disconnected")
				break

			if self.LOG_FILE != None:
				self.LOG_FILE.write(data + "\n")

			self.OnMessage(data)
