
import socket
import threading as th 
from package import _pack,_unpack

class Server:
	'''docstring for Server'''
	def __init__(self,addr):

		self._clients = []


		self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self._socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

		self._socket.bind(addr)
		self._socket.listen(10)
		self._socket.setblocking(False)

		hilo_1 = th.Thread(target = self._conexions,daemon = True)
		hilo_1.start()

		hilo_2 = th.Thread(target = self._recevie,daemon = True)
		hilo_2.start()

		while 1:
			data = input('>')
			if data == 'exit':
				self._socket.close()
				sys.exit()
				break


	def _conexions(self):
		print('Esperando conexiones ...')
		while 1:
			try:
				if len(self._clients) < 10:
					conn,addr = self._socket.accept()
					conn.setblocking(False)
					
					print(f'Conectado con {addr}')
					conn.send(_pack(f'Bienvenido, {addr} !'))

					client = (conn,addr)
					self._clients.append(client)
					print(f'Numero de conexiones: {len(self._clients)}' )
				else:
					break
			except:
				pass


	def _recevie(self):

		while True:
			if len(self._clients) > 0:
				for conn,addr in self._clients:
					try:
						data = conn.recv(1024)

						if data:
							data = _unpack(data)
							data = f'{addr}: {data}'
							self._messages_client(data,conn)
					
					except:
						pass

	def _messages_client(self,data,client):
		
		data_pack = _pack(data)				

		for conn,addr in self._clients:
			try:
				conn.send(data_pack)
			
			except:
				if client in self._clients:
					self._clients.remove(client)

		'''Por una extraña razón al segundo cliente no se quiere reenviar'''

if __name__ == '__main__':
	addr = ('localhost',6000)
	s = Server(addr)