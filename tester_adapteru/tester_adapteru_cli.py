#!python3



verbose = 50


# lib_check_install v2
import importlib.util
import pip
def lib_check_install(*packages):
	for p in packages:
		spec = importlib.util.find_spec(p)
		if spec is None:
			print(p +" is not installed, trying to install...")
			pip.main(['install', p])


lib_check_install('pyvisa', 'pyvisa-py')
import pyvisa #pip install pyvisa pyvisa-py

import time

#lib_check_install('pyqtgraph')
#import pyqtgraph as pg #pip install pyqtgraph

lib_check_install('matplotlib')
import matplotlib.pyplot as plt

lib_check_install('mplcursors')
import mplcursors



data_loadReqA = []
data_loadV = []
data_loadA = []
data_loadW = []


if False: #fake demo/test measurings
	data_loadReqA = [0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4]
	data_loadA =  [0.0, 0.500547, 0.600448, 0.699854, 0.799964, 0.899635, 0.99913, 1.099376, 0.0, 1.300171, 1.399442, 1.494956, 1.59529, 1.69556, 1.799899, 1.900312, 2.000822, 2.100236, 2.200443, 2.294846, 2.39518, 2.500621, 2.600104, 2.700486, 2.799766, 2.89998, 3.000602, 3.099993, 3.200127, 0.154693, 0.155484]
	data_loadV =  [20.110512, 19.90115, 19.857828, 19.818253, 19.779373, 19.736511, 19.692806, 19.652285, 0.000429, 4.552769, 4.509553, 4.466291, 4.425251, 4.38199, 4.337087, 4.293545, 4.250551, 4.207586, 4.164163, 4.123359, 4.079357, 4.033477, 3.990113, 3.945801, 3.902156, 3.857874, 3.815471, 3.769044, 3.724066, 0.186585, 0.000444]
	data_loadW =  [0.0, 9.961804, 11.923586, 13.869891, 15.822795, 17.755629, 19.675667, 21.605242, 0.0, 5.919187, 6.310858, 6.676911, 7.059631, 7.429928, 7.806316, 8.159076, 8.504566, 8.836926, 9.163002, 9.462538, 9.770794, 10.086198, 10.374709, 10.655582, 10.925121, 11.187757, 11.448711, 11.683687, 11.917484, 0.028863, 6.9e-05]

else: # do real measure

	loadResource = 'TCPIP0::10.10.134.5::INSTR'

	rm = pyvisa.ResourceManager()
	print('Connecting to ' + loadResource)
	PVload = rm.open_resource(loadResource)
	# Query if instrument is present
	# Prints e.g. "RIGOL TECHNOLOGIES,DL3021,DL3A204800938,00.01.05.00.01"
	print(PVload.query("*IDN?"))


	loadReqmAstart = 500
	loadReqmAstep = 100
	loadReqmAmax = 6000
	loadVmin = 1
	loadVminAttempts = 3
	time_step_delay = 0.8


	PVload.write(":SOURCE:FUNCTION CURRent")    # Set to  mode CURRent

	PVload.write(':SOURCE:CURRent:LEVEL:IMMEDIATE 0') #set load to 0 Amps

	PVload.write(":SOURCE:INPUT:STATE On")    # Enable electronic load

	loadReqmA = 0
	while loadReqmA < loadReqmAmax:
		loadReqA = str(loadReqmA/1000)
		print('loadReqA=', loadReqA, ', ', end='')
		PVcommand = ':SOURCE:CURRent:LEVEL:IMMEDIATE ' + loadReqA
		#print(PVcommand)
		PVload.write(PVcommand)
		time.sleep(time_step_delay)
		# Measure!
		loadV = PVload.query(":MEASURE:VOLTAGE?").strip()
		loadA = PVload.query(":MEASURE:CURRENT?").strip()
		loadW = PVload.query(":MEASURE:POWER?").strip()
		print("Voltage: ", loadV, ', ', end='')
		print("Current: ", loadA, ', ', end='')
		print("Power: ", loadW)

		data_loadReqA.append(float(loadReqA)) 
		data_loadV.append(float(loadV))
		data_loadA.append(float(loadA))
		data_loadW.append(float(loadW))
		#pw.setData(data_loadReqA, data_loadV, data_loadA, data_loadW)

		if loadReqmA == 0: # first cycle with 0 load - just measure
			loadReqmA = loadReqmAstart
		else:
			loadReqmA += loadReqmAstep
		if float(loadV) < loadVmin:
			loadVminAttempts -= 1
		if loadVminAttempts == 0:
			break

	PVload.write(":SOURCE:INPUT:STATE Off")



if verbose > 150:
	print('data_loadReqA = ', data_loadReqA)
	print('data_loadA = ', data_loadA)
	print('data_loadV = ', data_loadV)
	print('data_loadV = ', data_loadW)


#graph
if True:

	# pyplot example for multiple y axis
	#  https://matplotlib.org/stable/gallery/spines/multiple_yaxis_with_spines.html
	#
	fig, axs = plt.subplots(3, sharex=False, sharey=False)

	linesA = axs[0].plot(data_loadReqA, data_loadA, marker='o', label='Measured Current [A]')
	#axs[0].set(xlim=(0, None), ylim=(0, None))
	#axs[0].tick_linesArams(axis='y', colors=linesA.get_color())
	axs[0].legend(loc='best', shadow=True)



	linesV = axs[1].plot(data_loadReqA, data_loadV, marker='+', label='Measured Voltage [V]')
	axs[1].set(ylim=(0, None))
	#axs[1].tick_linesArams(axis='y', colors=linesV.get_color())
	axs[1].legend(loc='best', shadow=True)

	linesW = axs[2].plot(data_loadReqA, data_loadW, marker='x', label='Measured Power [W]')
	axs[2].set(ylim=(0, None), xlabel="'Requested current [A]'")
	#twin2.tick_linesArams(axis='y', colors=linesW.get_color())
	axs[2].legend(loc='best', shadow=True)


	def create_mplcursor_for_points_on_line(lines, ax=None, annotation_func=None, **kwargs):
		ax = ax or plt.gca()
		scats = [ax.scatter(x=line.get_xdata(), y=line.get_ydata(), color='none') for line in lines]
		cursor = mplcursors.cursor(scats, highlight=True, **kwargs)
		if annotation_func is not None:
			cursor.connect('add', annotation_func)
		return cursor

	#fig.tight_layout()

	#mplcursors.cursor(hover=True, highlight=False)

	#annotation_func = ()"add", lambda sel: sel.annotation.set_text("TIC ID = {}\nTmag = {}\nGaia ID = {}\nGmag = {}".format(ticID[sel.target.index],
                                                                                                            
	def af0(sel):
		sel.annotation.get_bbox_patch().set(fc="yellow", alpha=0.7)
		sel.annotation.arrow_patch.set(arrowstyle="simple", fc="yellow", alpha=0.7)
		return(sel.annotation.set_text(
			'Measured current: '+str(sel.target[1])+' A\n'+
			'Requested current: '+str(sel.target[0])+' A')
		)
	create_mplcursor_for_points_on_line(linesA, ax=axs[0], hover=True, annotation_func=af0)

	def af1(sel):
		sel.annotation.get_bbox_patch().set(fc="yellow", alpha=0.7)
		sel.annotation.arrow_patch.set(arrowstyle="simple", fc="yellow", alpha=0.7)
		return(sel.annotation.set_text(
			'Measured voltage: '+str(sel.target[1])+' V\n'
			+'Requested current: '+str(sel.target[0])+' A')
		)
	create_mplcursor_for_points_on_line(linesV, ax=axs[1], hover=True, annotation_func=af1)
	
	def af2(sel):
		sel.annotation.get_bbox_patch().set(fc="yellow", alpha=0.7)
		sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=0.7)
		return(sel.annotation.set_text(
			'Measured power: '+str(sel.target[1])+' W\n'+
			'Requested current: '+str(sel.target[0])+' A')
		)
	create_mplcursor_for_points_on_line(linesW, ax=axs[2], hover=True, annotation_func=af2)

	plt.show()