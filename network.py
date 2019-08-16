import threading as th 
import socket

from package import _pack,_unpack

class Client:

	def __init__(self,addr):
		self._socket = socket.socket()
		self._socket.connect(addr)
		
		#self._send('Estamos conectados!')


		self._messages = []

		self._rc = th.Thread(target = self._recevie,daemon=True)
		self._rc.start()


	def _recevie(self):
		while 1:
			try:
				data_server = self._socket.recv(1024)
				if data_server:
					data = _unpack(data_server)
					self._messages.append(data)
			except:
				pass 



	def _send(self,msg):
		data = _pack(msg)
		self._socket.send(data)


if __name__ == '__main__':
	addr = ('localhost',6000)
	c = Client(addr)