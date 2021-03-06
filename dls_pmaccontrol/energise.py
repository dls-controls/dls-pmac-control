# -*- coding: utf-8 -*-

import sys, re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from formEnergise import Ui_formEnergise

class energiseform(QDialog, Ui_formEnergise):

	def __init__(self, pmac, parent = None):
		QDialog.__init__(self,parent)
		self.setupUi(self)
		
		self.pmac = pmac
		self.parent = parent

		self.createCheckBoxes()
		(self.val7501, self.val7503) = self.readM750x()
		self.updateScreen()

	# Create the 2 columns of check-boxes
	def createCheckBoxes(self):
		chkGroupLayout = self.chkGroup.layout()
		chkGroupLayout.setAlignment(Qt.AlignTop)
		self.lstCheckBoxes = []
		for axis in range(1, 33):
			qCheckBox = QCheckBox("chkBox" + str(axis), self.chkGroup)
			qCheckBox.setText(str(axis))
			if axis <= 16:
				row = axis - 1
				chkGroupLayout.addWidget(qCheckBox, row, 0)
			else:
				row = axis - 17
				chkGroupLayout.addWidget(qCheckBox, row, 1)
			self.lstCheckBoxes.append(qCheckBox)

	class PmacIOError(IOError):
		pass

	# Get values of m7501, m7503 from PMAC. This does *not* update self.val7501, self.val7503.
	def readM750x(self):
		(retStr, retStatus) = self.pmac.sendCommand("m7501 m7503")
		if not retStatus:
			raise PmacIOError('Cannot read m7501, m7503')
		lstRetStr = re.split(r'\r', retStr)
		val7501 = int(lstRetStr[0]) # just a local variable, not self.var7501
		val7503 = int(lstRetStr[1]) # just a local variable, not self.var7503
		return (val7501, val7503)

	# Update the axis energised checkboxes using the values in self.val7501 and self.val7503.
	def updateScreen(self):
		for axis in range(1,33):
			if axis <= 16:
				isAxisChecked = bool(self.val7501 & (1 << (axis-1)))
			else:
				isAxisChecked = bool(self.val7503 & (1 << (axis-17)))
			self.lstCheckBoxes[axis-1].setChecked(isAxisChecked)

	# Return True if: the value of self.val7501 is equal to the actual M7501 on the PMAC, and
	#                 the value of self.val7503 is equal to the actual M7503 on the PMAC.
	# During comparisons consider only the 2 LSBs of the variables 
	def isScreenUpToDate(self):
		(val7501, val7503) = self.readM750x()
		return (self.val7501 & 0x00FFFF == val7501 & 0x00FFFF) and (self.val7503 & 0x00FFFF == val7503 & 0x00FFFF)

	# public slot
	# Send energise axis command to the pmac.
	# Functionality: create the hex value of the bitmap of axis to energise.
	#                send the command to the pmac
	#                read back the two parts (16 axes per read)
	#                set the corresponding checkboxes to reflect the read back value.
	def sendCommand(self):

		# Make sure that self.val7501 and self.val7503 truly reflect the current values of M7501 and M7503 (on the PMAC)
		if not self.isScreenUpToDate():
			QMessageBox.information(self,
						"Error",
						"The screen is out of date, even if ignoring your changes!\n" +
						"This may be e.g. due to PLCs running in the background which de/energised some motors.\n"
						"To avoid inconsistency, the screen will reload now. Re-do your changes and submit again."
						)
			(self.val7501, self.val7503) = self.readM750x()
			self.updateScreen()
			return
		
		# Find out new values of m7501, m7503 using current energize bits
		newVal7501 = self.val7501 & 0xFF0000   # keep MSB unchanged
		newVal7503 = self.val7503 & 0xFF0000   # keep MSB unchanged
		for i, axis in enumerate(self.lstCheckBoxes):
			if axis.isChecked():
				if i < 16:
					newVal7501 = newVal7501 | (1 << i)
				else:
					newVal7503 = newVal7503 | (1 << (i-16))
		self.val7501 = newVal7501
		self.val7503 = newVal7503

		# Write m7501, m7503 to the PMAC
		cmd = "m7501=$%x m7503=$%x" %(self.val7501,self.val7503)
		(retStr, retStatus) = self.pmac.sendCommand(cmd)
		if not retStatus:
			QMessageBox.information(self, "Error", "Send command error:\n" + retStr)
			return

		# Update the shell 
		if self.parent.chkShowAll.isChecked():
			self.parent.txtShell.append(cmd)
			self.parent.txtShell.append(retStr)

if __name__ == "__main__":
	a = QApplication(sys.argv)
	QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
	w = energiseform()
	a.setMainWidget(w)
	w.show()
	a.exec_loop()
	
## \file
# \section License
# Author: Diamond Light Source, Copyright 2011
#
# 'dls_pmaccontrol' is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 'dls_pmaccontrol' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with 'dls_pmaccontrol'.  If not, see http://www.gnu.org/licenses/.
