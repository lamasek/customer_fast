

# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
# obslehnuto z https://yapayzekalabs.blogspot.com/2018/11/pyqt5-gui-qt-designer-matplotlib.html

from PyQt6.QtWidgets import*

from matplotlib.backends.backend_qtagg import FigureCanvas

from matplotlib.figure import Figure

    
class MplWidget(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)
        
        self.ax1 = self.fig.add_subplot(3, 1, 1)
        #axs = self.canvas.figure.add_subplot(3, 1, sharex=False, sharey=False)
        #self.fig, self.axs = self.canvas.figure.subplots(3, sharex=False, sharey=False)

        linesA = self.ax1.plot([], [], marker='o', label='Measured Current [A]')
        self.ax1.set(ylim=(0, None))
        #axs[0].tick_linesArams(axis='y', colors=linesA.get_color())
        self.ax1.legend(loc='best', shadow=True)

        self.ax2 = self.fig.add_subplot(3, 1, 2)
        linesV = self.ax2.plot([], [], marker='+', label='Measured Voltage [V]')
        self.ax2.set(ylim=(0, None))
        #axs[1].tick_linesArams(axis='y', colors=linesV.get_color())
        self.ax2.legend(loc='best', shadow=True)

        self.ax3 = self.fig.add_subplot(3, 1, 3)
        linesW = self.ax3.plot([], [], marker='x', label='Measured Power [W]')
        self.ax3.set(ylim=(0, None), xlabel="'Requested current [A]'")
        #twin2.tick_linesArams(axis='y', colors=linesW.get_color())
        self.ax3.legend(loc='best', shadow=True)

        self.canvas.draw()

        #plt.show()


    def update_plot(self, xdata, y1data, y2data, y3data):
            self.ax1.cla()  # Clear the canvas.
            self.ax1.plot(xdata, y1data)

            self.ax2.cla()  # Clear the canvas.
            self.ax2.plot(xdata, y2data)

            self.ax3.cla()  # Clear the canvas.
            self.ax3.plot(xdata, y3data)
            
            self.canvas.draw() # Trigger the canvas to update and redraw.


