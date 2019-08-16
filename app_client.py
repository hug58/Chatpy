#!/usr/bin/python3

import tkinter as tk 
from network import Client
import threading as th 

class App:
	def __init__(self):

		#---------All-Messages------------
		self._all_messages = []
		#---------------SOCKET-------------
		addr = ('localhost',6000)
		self._client = Client(addr)

		#---------------RAIZ---------------
		self._raiz = tk.Tk()
		self._raiz.title('CLIENT')
		self._raiz.resizable(width=False,height=False)
		
		#--------------VARIABLE------------
		self._var_send = tk.StringVar()
		
		#---------------FRAME--------------
		self._frame = tk.Frame(self._raiz,width = 400, height = 400)
		self._frame.pack()

		#-------------MESSAGES------------
		self._list_messages = tk.StringVar(value=self._all_messages)

		#---------LISTBOX-MESSAGES---------
		self._listbox_messages = tk.Listbox(self._frame,width = 42,
		listvariable = self._list_messages,selectmode = tk.EXTENDED, bg = 'beige')
		self._listbox_messages.grid(row = 0,column = 0,columnspan = 2)

		#--------------ENTRY---------------
		self._entry_send = tk.Entry(self._frame,width = 25,textvariable = self._var_send )
		self._entry_send.grid(row = 1,column = 0)
		
		#---------------BUTTON-------------
		self._send = tk.Button(self._frame,text = 'Send',width = 10,
								command= lambda:self._messages(self._var_send
								))
		self._send.grid(row = 1,column = 1)


		'''Demonio que actualizar la lista sin blquear el flujo de la aplicacion'''
		self._rc = th.Thread(target = self._update_list_messages,daemon = True)
		self._rc.start()

	def _get_raiz(self):
		return self._raiz

	def _messages(self,msg):

		if msg.get():
			
			'''Añade el nombre del autor'''
			data = msg.get()

			'''Enviando mensaje al servidor...'''
			self._client._send(data)

			'''Borrando contenido de Entry'''
			msg.set('')


	def _update_list_messages(self):
		'''actualizar la lista indefinidamente'''
		while 1:
			msgs_server = self._client._messages
			self._list_messages.set(value=msgs_server)

	def __str__(self):
		return 'Chat hecha con sockets y tkinter'


	def loop(self):
		self._raiz.mainloop()



def main():
	app = App()
	app.loop()


if __name__ == '__main__':
	main()
