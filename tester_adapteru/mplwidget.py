

# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
# obslehnuto z https://yapayzekalabs.blogspot.com/2018/11/pyqt5-gui-qt-designer-matplotlib.html

from PyQt6.QtWidgets import*

from matplotlib.backends.backend_qtagg import FigureCanvas

from matplotlib.figure import Figure

import matplotlib.pyplot as plt

import mplcursors


class MplWidget(QWidget):
	
	def __init__(self, parent = None):

		QWidget.__init__(self, parent)
		


	def myinit(self, theme=None):
		if theme is None:
			theme = 'none'
		if theme != 'none':
			if theme == 'dark':
				plt.style.use('dark_background')
			if theme == 'light':
				None
			if theme == 'auto':
				None
				#TODO detect

		self.fig = Figure()
		self.canvas = FigureCanvas(self.fig)
		
		vertical_layout = QVBoxLayout()
		vertical_layout.addWidget(self.canvas)
		self.setLayout(vertical_layout)
		
		self.ax1 = self.fig.add_subplot(3, 1, 1)
		self.ax2 = self.fig.add_subplot(3, 1, 2)
		self.ax3 = self.fig.add_subplot(3, 1, 3)
		#axs = self.canvas.figure.add_subplot(3, 1, sharex=False, sharey=False)
		#self.fig, self.axs = self.canvas.figure.subplots(3, sharex=False, sharey=False)

		self.fig.tight_layout()


		self.canvas.draw()
		#plt.show()




	def create_mplcursor_for_points_on_line(self, lines, ax, annotation_func, **kwargs):
		if ax == None:
			ax = self.canvas.gca()
			ax = self.plt.gca()
		scats = [ax.scatter(x=line.get_xdata(), y=line.get_ydata(), color='none') for line in lines]
		cursor = mplcursors.cursor(scats, highlight=True, **kwargs)
		if annotation_func is not None:
			cursor.connect('add', annotation_func)
		return cursor


	#mplcursors.cursor(hover=True, highlight=False)
	#annotation_func = ()"add", lambda sel: sel.annotation.set_text("TIC ID = {}\nTmag = {}\nGaia ID = {}\nGmag = {}".format(ticID[sel.target.index],
																											
	def af1(self, sel):
		sel.annotation.get_bbox_patch().set(fc="yellow", alpha=0.7)
		sel.annotation.arrow_patch.set(arrowstyle="simple", fc="yellow", alpha=0.7)
		return(sel.annotation.set_text(
			'Measured current: '+str(sel.target[1])+' A\n'+
			'Requested current: '+str(sel.target[0])+' A')
		)

	def af2(self, sel):
		sel.annotation.get_bbox_patch().set(fc="yellow", alpha=0.7)
		sel.annotation.arrow_patch.set(arrowstyle="simple", fc="yellow", alpha=0.7)
		return(sel.annotation.set_text(
			'Measured voltage: '+str(sel.target[1])+' V\n'
			+'Requested current: '+str(sel.target[0])+' A')
		)
	
	def af3(self, sel):
		sel.annotation.get_bbox_patch().set(fc="yellow", alpha=0.7)
		sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=0.7)
		return(sel.annotation.set_text(
			'Measured power: '+str(sel.target[1])+' W\n'+
			'Requested current: '+str(sel.target[0])+' A')
		)

	def plot_init(self):
		self.ax1.cla()  # Clear the canvas.
		self.linesA = self.ax1.plot([], [], marker='o', label='Measured Current [A]')
		self.ax1.set(ylim=(0, None))
		#axs[0].tick_linesArams(axis='y', colors=linesA.get_color())
		self.ax1.legend(loc='best', shadow=True)

		self.ax2.cla()  # Clear the canvas.
		self. linesV = self.ax2.plot([], [], marker='+', label='Measured Voltage [V]')
		self.ax2.set(ylim=(0, None))
		#axs[1].tick_linesArams(axis='y', colors=linesV.get_color())
		self.ax2.legend(loc='best', shadow=True)

		self.ax3.cla()  # Clear the canvas.
		self.linesW = self.ax3.plot([], [], marker='x', label='Measured Power [W]')
		self.ax3.set(ylim=(0, None), xlabel="'Requested current [A]'")
		#twin2.tick_linesArams(axis='y', colors=linesW.get_color())
		self.ax3.legend(loc='best', shadow=True)

		self.canvas.draw()


	def plot_update(self, xdata, y1data, y2data, y3data):
			self.ax1.cla()  # Clear the canvas.
			self.linesA = self.ax1.plot(xdata, y1data, marker='o', label='Measured Current [A]')
			self.ax1.set(ylim=(0, None))
			self.ax1.legend(loc='best', shadow=True)


			self.ax2.cla()  # Clear the canvas.
			self. linesV = self.ax2.plot(xdata, y2data, marker='+', label='Measured Voltage [V]')
			self.ax2.set(ylim=(0, None))
			self.ax2.legend(loc='best', shadow=True)


			self.ax3.cla()  # Clear the canvas.
			self.linesW = self.ax3.plot(xdata, y3data, marker='x', label='Measured Power [W]')
			self.ax3.set(ylim=(0, None), xlabel="'Requested current [A]'")
			self.ax3.legend(loc='best', shadow=True)

			try:
				self.cursor1.remove()
			except:
				None
			self.cursor1 = self.create_mplcursor_for_points_on_line(self.linesA, self.ax1, annotation_func=self.af1, hover=False)
			try:
				self.cursor2.remove()
			except:
				None
			self.cursor2 = self.create_mplcursor_for_points_on_line(self.linesV, self.ax2, annotation_func=self.af2, hover=False)
			try:
				self.cursor3.remove()
			except:
				None
			self.cursor3 = self.create_mplcursor_for_points_on_line(self.linesW, self.ax3, annotation_func=self.af3, hover=False)

			self.canvas.draw() # Trigger the canvas to update and redraw.


