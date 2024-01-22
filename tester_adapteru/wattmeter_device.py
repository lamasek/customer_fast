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
		#if self.demo == True:
		#	return(r, s)
		
		VisaDevice.write(self, ':NUM:FORM ASCII')
		#todo check ze je ok

		#todo check ze:
		#:integ?
		#kontrolovat ze to je spravne na NORM;0,10,0

		# NUM:NORM? - detekce kterym ITEM odpovidaji V, W, A, MATH (obcas se meni): 
		# bereme prvni ze seznamu
		if self.verbose > 70:
			print("Wattmeter ITEM order autodetection:")
		nn = self.get_NUM_NORM()
		nn = nn.strip()
		#nn = ':NUM:NUM 255;ITEM1 MATH;ITEM2 TIME;ITEM3 U,1;ITEM4 I,1;ITEM5 P,1;ITEM6 S,1;ITEM7 Q,1;ITEM8 LAMB,1;ITEM9 PHI,1;ITEM10 FU,1;ITEM11 UTHD,1;ITEM12 ITHD,1;ITEM13 LAMB,1;ITEM14 PHI,1;ITEM15 F'
		if self.verbose > 100:
			print("Wattmeter NUM:NORM? ==> " + nn)

		try:
			# nn = :NUM:NUM 255;ITEM1 U,1;ITEM2
			i = nn.find(';') 
			if i < 8:
				fallback = True
			else:
				nn = nn[i+1:]
			# nn = 'ITEM1 U,1;ITEM2 ..... 

			nnlist = nn.split(';')
			for i in range(len(nnlist)):
				drop, nnlist[i] = nnlist[i].split(' ')
			#nnlist = ['U,1', 'URMS,1', 'UMN,1', 'UDC,1', ....

			for i in range(len(nnlist)):
				nnlist[i] = nnlist[i].split(',')[0]
			#nnlist = ['U', 'URMS', 'UMN', 'UDC', 'URMN', 'UAC', 'NONE', 'I', 'IRMS', ....

			self.ITEM_U = str(nnlist.index('U')+1) #prvni z moznych vyskytu
			self.ITEM_I = str(nnlist.index('I')+1)
			self.ITEM_P = str(nnlist.index('P')+1)
			self.ITEM_TIME = str(nnlist.index('TIME')+1)
			self.ITEM_MATH = str(nnlist.index('MATH')+1)


		except:
			print("Wattmeter ITEM order autodetection: FAILED; Using fallback values (U=1, I=8, P=215, TIME=17, MATH=16)")
			self.ITEM_U = '1'
			self.ITEM_I = '8'
			self.ITEM_P = '215'
			self.ITEM_TIME = '17'
			self.ITEM_MATH = '16'

		if self.verbose > 70:
			print("Wattmeter ITEM order autodetection: detected indexes" )
			print('  Item index for U: '+self.ITEM_U)
			print('  Item index for I: '+self.ITEM_I)
			print('  Item index for P: '+self.ITEM_P)
			print('  Item index for TIME: '+self.ITEM_TIME)
			print('  Item index for MATH: '+self.ITEM_MATH)

		return(r, s)
		#self.connected = True

	
	def get_NUM_NORM(self):
		# 
		if  self.demo == True:
			return(':NUM:NUM 255;ITEM1 U,1;ITEM2 URMS,1;ITEM3 UMN,1;ITEM4 UDC,1;ITEM5 URMN,1;ITEM6 UAC,1;ITEM7 NONE;'
		  			+'ITEM8 I,1;ITEM9 IRMS,1;ITEM10 IMN,1;ITEM11 IDC,1;ITEM12 IRMN,1;ITEM13 LAMB,1;ITEM14 PHI,1;'
					+'ITEM15 FU,1;ITEM16 MATH;ITEM17 TIME;ITEM18 UK,1,TOT;ITEM19 UK,1,1;ITEM20 UK,1,2;ITEM21 UK,1,3;'
					+'ITEM22 UK,1,4;ITEM23 UK,1,5;ITEM24 UK,1,6;ITEM25 UK,1,7;ITEM26 UK,1,8;ITEM27 UK,1,9;'
					+'ITEM28 UK,1,10;ITEM29 UK,1,11;ITEM30 UK,1,12;ITEM31 UK,1,13;ITEM32 UK,1,14;ITEM33 UK,1,15;'
					+'ITEM34 UK,1,16;ITEM35 UK,1,17;ITEM36 UK,1,18;ITEM37 UK,1,19;ITEM38 UK,1,20;ITEM39 UK,1,21;'
					+'ITEM40 UK,1,22;ITEM41 UK,1,23;ITEM42 UK,1,24;ITEM43 UK,1,25;ITEM44 UK,1,26;ITEM45 UK,1,27;'
					+'ITEM46 UK,1,28;ITEM47 UK,1,29;ITEM48 UK,1,30;ITEM49 UK,1,31;ITEM50 UK,1,32;ITEM51 UK,1,33;'
					+'ITEM52 UK,1,34;ITEM53 UK,1,35;ITEM54 UK,1,36;ITEM55 UK,1,37;ITEM56 UK,1,38;ITEM57 UK,1,39;'
					+'ITEM58 UK,1,40;ITEM59 UK,1,41;ITEM60 UK,1,42;ITEM61 UK,1,43;ITEM62 UK,1,44;ITEM63 UK,1,45;'
					+'ITEM64 UK,1,46;ITEM65 UK,1,47;ITEM66 UK,1,48;ITEM67 UK,1,49;ITEM68 UK,1,50;ITEM69 IK,1,TOT;'
					+'ITEM70 IK,1,1;ITEM71 IK,1,2;ITEM72 IK,1,3;ITEM73 IK,1,4;ITEM74 IK,1,5;ITEM75 IK,1,6;'
					+'ITEM76 IK,1,7;ITEM77 IK,1,8;ITEM78 IK,1,9;ITEM79 IK,1,10;ITEM80 IK,1,11;ITEM81 IK,1,12;'
					+'ITEM82 IK,1,13;ITEM83 IK,1,14;ITEM84 IK,1,15;ITEM85 IK,1,16;ITEM86 IK,1,17;ITEM87 IK,1,18;'
					+'ITEM88 IK,1,19;ITEM89 IK,1,20;ITEM90 IK,1,21;ITEM91 IK,1,22;ITEM92 IK,1,23;ITEM93 IK,1,24;'
					+'ITEM94 IK,1,25;ITEM95 IK,1,26;ITEM96 IK,1,27;ITEM97 IK,1,28;ITEM98 IK,1,29;ITEM99 IK,1,30;'
					+'ITEM100 IK,1,31;ITEM101 IK,1,32;ITEM102 IK,1,33;ITEM103 IK,1,34;ITEM104 IK,1,35;'
					+'ITEM105 IK,1,36;ITEM106 IK,1,37;ITEM107 IK,1,38;ITEM108 IK,1,39;ITEM109 IK,1,40;'
					+'ITEM110 IK,1,41;ITEM111 IK,1,42;ITEM112 IK,1,43;ITEM113 IK,1,44;ITEM114 IK,1,45;'
					+'ITEM115 IK,1,46;ITEM116 IK,1,47;ITEM117 IK,1,48;ITEM118 IK,1,49;ITEM119 IK,1,50;'
					+'ITEM120 PK,1,TOT;ITEM121 PK,1,1;ITEM122 PK,1,2;ITEM123 PK,1,3;ITEM124 PK,1,4;ITEM125 PK,1,5;'
					+'ITEM126 PK,1,6;ITEM127 PK,1,7;ITEM128 PK,1,8;ITEM129 PK,1,9;ITEM130 PK,1,10;ITEM131 PK,1,11;'
					+'ITEM132 PK,1,12;ITEM133 PK,1,13;ITEM134 PK,1,14;ITEM135 PK,1,15;ITEM136 PK,1,16;ITEM137 PK,1,17;'
					+'ITEM138 PK,1,18;ITEM139 PK,1,19;ITEM140 PK,1,20;ITEM141 PK,1,21;ITEM142 PK,1,22;ITEM143 PK,1,23;'
					+'ITEM144 PK,1,24;ITEM145 PK,1,25;ITEM146 PK,1,26;ITEM147 PK,1,27;ITEM148 PK,1,28;ITEM149 PK,1,29;'
					+'ITEM150 PK,1,30;ITEM151 PK,1,31;ITEM152 PK,1,32;ITEM153 PK,1,33;ITEM154 PK,1,34;ITEM155 PK,1,35;'
					+'ITEM156 PK,1,36;ITEM157 PK,1,37;ITEM158 PK,1,38;ITEM159 PK,1,39;ITEM160 PK,1,40;ITEM161 PK,1,41;'
					+'ITEM162 PK,1,42;ITEM163 PK,1,43;ITEM164 PK,1,44;ITEM165 PK,1,45;ITEM166 PK,1,46;ITEM167 PK,1,47;'
					+'ITEM168 PK,1,48;ITEM169 PK,1,49;ITEM170 PK,1,50;ITEM171 LAMBDAK,1,1;ITEM172 PHIK,1,1;'
					+'ITEM173 PHIU,1,TOT;ITEM174 PHIU,1,1;ITEM175 PHIU,1,2;ITEM176 PHIU,1,3;ITEM177 PHIU,1,4;'
					+'ITEM178 PHIU,1,5;ITEM179 PHIU,1,6;ITEM180 PHIU,1,7;ITEM181 PHIU,1,8;ITEM182 PHIU,1,9;'
					+'ITEM183 PHIU,1,10;ITEM184 PHIU,1,11;ITEM185 PHIU,1,12;ITEM186 PHIU,1,13;ITEM187 PHIU,1,14;'
					+'ITEM188 PHIU,1,15;ITEM189 PHIU,1,16;ITEM190 PHIU,1,17;ITEM191 PHIU,1,18;ITEM192 PHIU,1,19;'
					+'ITEM193 PHIU,1,20;ITEM194 PHIU,1,21;ITEM195 PHIU,1,22;ITEM196 PHIU,1,23;ITEM197 PHIU,1,24;'
					+'ITEM198 PHIU,1,25;ITEM199 PHIU,1,26;ITEM200 PHIU,1,27;ITEM201 U,1;ITEM202 URMS,1;ITEM203 UMN,1;'
					+'ITEM204 UDC,1;ITEM205 URMN,1;ITEM206 UAC,1;ITEM207 NONE;ITEM208 I,1;ITEM209 IRMS,1;ITEM210 IMN,1;'
					+'ITEM211 IDC,1;ITEM212 IRMN,1;ITEM213 IAC,1;ITEM214 NONE;ITEM215 P,1;ITEM216 S,1;ITEM217 TIME;'
					+'ITEM218 U,1;ITEM219 U,1;ITEM220 U,1;ITEM221 U,1;ITEM222 U,1;ITEM223 U,1;ITEM224 U,1;ITEM225 U,1;'
					+'ITEM226 U,1;ITEM227 U,1;ITEM228 U,1;ITEM229 U,1;ITEM230 U,1;ITEM231 U,1;ITEM232 U,1;ITEM233 U,1;'
					+'ITEM234 U,1;ITEM235 U,1;ITEM236 U,1;ITEM237 U,1;ITEM238 U,1;ITEM239 U,1;ITEM240 U,1;ITEM241 U,1;'
					+'ITEM242 U,1;ITEM243 U,1;ITEM244 U,1;ITEM245 U,1;ITEM246 U,1;ITEM247 U,1;ITEM248 U,1;ITEM249 U,1;'
					+'ITEM250 U,1;ITEM251 U,1;ITEM252 U,1;ITEM253 U,1;ITEM254 U,1;ITEM255 U,1')
		
		# alternative (default values);ITEM1 MATH;ITEM2 TIME;ITEM3 U,1;ITEM4 I,1;ITEM5 P,1;ITEM6 S,1;ITEM7 Q,1;ITEM8 LAMB,1;ITEM9 PHI,1;ITEM10 FU,1;ITEM11 UTHD,1;ITEM12 ITHD,1;ITEM13 LAMB,1;ITEM14 PHI,1;ITEM15 F

		retCode, retString = VisaDevice.query(self, "NUM:NORM?")

		return(retString)


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
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? "+self.ITEM_MATH)
			self.verbose += 100
			f = float(retString.strip())
			if type(f) == float:
				return(f)
			else:
				return(None)
		if varName == 'TIME':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? "+self.ITEM_TIME)
			self.verbose += 100
			f = float(retString.strip())
			if type(f) == float:
				return(f)
			else:
				return(None)
		elif varName == 'V':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? "+self.ITEM_U)
			self.verbose += 100
			f = float(retString.strip())
			if type(f) == float:
				return(f)
			else:
				return(None)
		elif varName == 'A':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? "+self.ITEM_I)
			self.verbose += 100
			f = float(retString.strip())
			if type(f) == float:
				return(f)
			else:
				return(None)
		elif varName == 'W':
			retCode, retString = VisaDevice.query(self, ":NUM:VAL? "+self.ITEM_P)
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
	def __init__(self, VISAresource: str, demo: bool, status: QtWidgets.QTextEdit, verbose: int):
		Wattmeter. VISAresource = VISAresource
		Wattmeter.demo = demo
		self.status = status
		self.verbose = verbose

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
