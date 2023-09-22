#python3

import pyvisa #pip install pyvisa pyvisa-py

class VisaDevice():
	
	def __init__(self, VISAresource: str, demo: bool, verbose=30):
		self. VISAresource = VISAresource
		self.demo = demo
		self.verbose = verbose
		

	demo = False	# if True, it does not connect to real device, it provide fake demo values
	#demo_connected = False
	
	def setDemo(self, d: bool): #pokud demo, tak dela sinusovku co 10s a jen kladnou
		self.demo = d
	
	verbose: int

	VISAresource = ''
	connected = False

	def is_connected(self):
		return(self.connected)
	
	def setVISAresource(self, Vr: str):
		self.VISAresource = Vr

	def connect(self):
		# return retCode=True/False, retString=Error str/IDN of device
		if  self.demo == True:
			self.connected = True
			return(True, 'Demo connected')

		if self.connected:
			return(True, 'Already connected')
		self.rm = pyvisa.ResourceManager()
		if self.verbose > 70:
			print('Connecting to ' + self.VISAresource)
		try:
			self.PVdevice = self.rm.open_resource(self.VISAresource)
		except Exception as e:
			print('  Connection failed: ' + str(e))
			self.connected = False
			return(False, ' Connection failed'+str(e))

		# Query if instrument is present
		# Prints e.g. "RIGOL TECHNOLOGIES,DL3021,DL3A204800938,00.01.05.00.01"
		try:
			IDNreply = self.PVdevice.query("*IDN?")
		except Exception as e:
			print('SCPI *IDN? test after connection failed: ' + str(e))
			self.connected = False
			return(False, 'SCPI *IDN? test after connection failed: '+str(e))
		if self.verbose>50:
			print(IDNreply.strip())
		self.connected = True
		return(True, IDNreply)

	def disconnect(self):
		if  self.demo == True:
			self.connected = False
			return(True)

		if self.verbose > 70:
			print('Load disconnecting...')
		try:
			self.rm.close() 
		except:
			None
		#TODO check
		self.connected = False
		return(True)

	def send(self, commandi):
		if  self.connected == True:
			command = commandi.strip()
			if command =='':
				return(False, 'Empty command, nothing to send...') # we have to handle itself, some devices (e.g. Rigol DL3031A) freezes permanently after emty command
			try:
				if self.verbose>170:
					print('Command:' + command)
				if '?' in command: # some devices (e.g. Yokogawa WT310E) have some IDs after ? (e.g. ":NUM:VAL? 1")
					reply = self.PVdevice.query(command)
				else:
					self.PVdevice.write(command)
					reply = ''
				if self.verbose>150:
					print(reply)
				return(True, reply)
			except Exception as e:
				if self.verbose > 50:
					print('  Comand "' + command + '" failed: ' + str(e))
				return(False, str(e))
		else:
			return(False, 'Not connected')

	def write(self, commandi):
		#return(bool (True = OK), <string with error message | ''>)
		if  self.demo == True:
			return(True, '')
		if  self.connected == True:
			command = commandi.strip()
			if command =='':
				return(False, 'Empty command, nothing to send...') # we have to handle itself, some devices (e.g. Rigol DL3031A) freezes permanently after emty command
			try:
				if self.verbose>170:
					print('Command:' + command)
				reply = self.PVdevice.write(command)
				if self.verbose>150:
					print(reply)
				return(True, reply)
			except Exception as e:
				if self.verbose > 50:
					print('  Comand "' + command + '" failed: ' + str(e))
				return(False, str(e))
		else:
			return(False, 'Not connected')

	def query(self, commandi):
		'''
		return(retCode = True (OK) | False (Error), retString (string containig answer | error message))
		'''
		if  self.demo == True:
			return(True, 'Demo')

		if  self.connected == True:
			command = commandi.strip()
			if command =='':
				return(False, 'Empty command, nothing to send...') # we have to handle itself, some devices (e.g. Rigol DL3031A) freezes permanently after emty command
			try:
				if self.verbose>170:
					print('Command:' + command)
				reply = self.PVdevice.query(command)
				reply.strip()
				if self.verbose>150:
					print(reply)
				return(True, reply)
			except Exception as e:
				if self.verbose > 70:
					print('  Comand "' + command + '" failed: ' + str(e))
				return(False, str(e))
		else:
			return(False, 'Not connected')
