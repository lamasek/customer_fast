#!python3

import math

import time

from PyQt6 import QtWidgets
#from PyQt6.QtWidgets import*


from visa_device import VisaDevice


class Wattmeter(VisaDevice):

	def connect(self):
		r, s = VisaDevice.connect(self)
		if r == False:
			return(r, s)
		if self.demo == True:
			return(r, s)
		VisaDevice.write(self, ':NUM:FORM ASCII')
		#todo check ze je ok

		#todo check ze:
		#:integ?
		#kontrolovat ze to je spravne na NORM;0,10,0

		return(r, s)
		#self.connected = True

	def measure(self, varName):
		# return float | False -error durinq query | None - device answered NAN or not float
		if  self.demo == True:
			i = 100*math.sin( # sinus, period 5s in time
					(time.time()%5) / 5 * 2*3.1415
				)
			if i < 0: #only positive part
				i = 0
			return( i )
		
		self.verbose -= 100
		# ;ITEM1 MATH;ITEM2 TIME;ITEM3 U,1;ITEM4 I,1;ITEM5 P,1;ITEM6 S,1;ITEM7 Q,1;ITEM8 LAMB,1;ITEM9 PHI,1;ITEM10 FU,1;ITEM11 UTHD,1;ITEM12 ITHD,1;ITEM13 LAMB,1;ITEM14 PHI,1;ITEM15 F
		if varName == 'MATH':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? 1")
			self.verbose += 100
			f = float(retString.strip())
			if type(f) == float:
				return(f)
			else:
				return(None)
		if varName == 'TIME':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? 2")
			self.verbose += 100
			f = float(retString.strip())
			if type(f) == float:
				return(f)
			else:
				return(None)
		elif varName == 'V':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? 3")
			self.verbose += 100
			f = float(retString.strip())
			if type(f) == float:
				return(f)
			else:
				return(None)
		elif varName == 'A':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? 4")
			self.verbose += 100
			f = float(retString.strip())
			if type(f) == float:
				return(f)
			else:
				return(None)
		elif varName == 'W':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? 5")
			self.verbose += 100
			f = float(retString.strip())
			if type(f) == float:
				return(f)
			else:
				return(None)
		else:
			return(False)
	
	def measureNoNAN(self, varName):
		# if measure returns NaN, perform again, max 100 times
		for i in range(100):
			ret = self.measure(varName)
			if ret is not None:
				return(ret)
		return(False)
	
	def measure10Avg(self, varName):
		# measure 10 times and return avg
		sum = 0
		for i in range(10):
			ret = self.measureNoNAN(varName)
			if self.verbose > 170:
				print('measure10Avg:' + str(ret))
			if ret is not None:
				sum += ret
		return(sum / 10)



	# Integrate ------------------------------------
	# procedure how to make integrate measure on Wattmeter:
	# :INTEG:RESET
	# volitelne
	#	:INTEG:TIME 0,10,10
	#	check math, mod, rms, ...
	# :INTEG:START
	# periodicalluy check :INTEGrate:STATe?
	# 	if is STARTt - wait
	# 	if TIMeup - finished, take results
	#	 if other - measuring failed

	integrate = 0 #demo integrate

	def integrateStart(self):
		if  self.demo == True:
			self.integrate = 10
			return(True)
		return(VisaDevice.write(self, ":INTEGrate:STARt"))

	def integrateReset(self):
		if  self.demo == True:
			self.integrate = 0
		VisaDevice.write(self, ":INTEGrate:RESet")
		VisaDevice.write(self, ":INTEGrate:STOP") #in case is running, RESet does not work
		VisaDevice.write(self, ":INTEGrate:RESet")

	def integrateState(self):
		# returns:
		# 	STAR[t] pocita
		# 	TIM[eup] normalni konec vypoctu
		#	ERRor
		# 	RESet	normalni po resetu a spusteni pristroje - tohle je v klidu bez chyb
		# 	STOP
		if  self.demo == True:
			if self.integrate > 0:
				self.integrate -= 1
				return(True, 'STAR')
			else:
				return(True, 'TIM')
		return(VisaDevice.query(self, ":INTEGrate:STATe?"))

class Wattmeter_GUI(Wattmeter):
	def __init__(self, VISAresource: str, demo: bool, status: QtWidgets.QTextEdit):
		Wattmeter. VISAresource = VISAresource
		Wattmeter.demo = demo
		self.status = status

	def connect(self):
		if  self.is_connected() == True:
			return(True, 'Already connected')
		else:
			self.status.setText('Trying to connect...')
			self.status.setStyleSheet('')
			retCode, retStr = Wattmeter.connect(self)
			#retCode, retStr = super().connect()
			if retCode == False:
				self.status.setText('FAILED to connect, error: ' + retStr)
				self.status.setStyleSheet('color:red')
				return(False, retStr)
			else:
				self.status.setText('Connected to: ' + retStr)
				self.status.setStyleSheet('color:green')
				return(True, retStr)

	def disconnect(self):
		if  self.is_connected() == True:
			self.status.setText('Disconnecting...')
			self.status.setStyleSheet(None)
			ret = Wattmeter.disconnect(self)
			if ret == False:
				self.status.setText('Disconnected, FAILED to nice disconnect')
				self.status.setStyleSheet('color:red')
			else:
				self.status.setText('Disconnected ')
				self.status.setStyleSheet(None)
		else:
			self.status.setText('Disconnected ')
			self.status.setStyleSheet(None)
