#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import capstone
import code
from PySide import QtGui, QtCore

from PythonInterpreter import *
from Disassembler import *
from utils import *

class UI(QtGui.QWidget):

    def __init__(self):
        super(UI, self).__init__()
        self.render()

    def render(self):
        frame = QtGui.QVBoxLayout(self)

        self.dis = Disassembler()
        self.cli = CLI()

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)

        splitter.addWidget( self.dis )
        splitter.addWidget( self.cli )

        frame.addWidget(splitter)

        for x in self.dis.disassemble('\x90\x90\x90'*50, 'x86', 32):
            self.dis.append( "0x%08x (%02x) %-20s %s %s" % (x[0], x[1], x[2], x[3], x[4]) )

        self.setLayout(frame)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        self.setWindowTitle('Disassembler')
        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet("QTextEdit, QLineEdit {background-color:black; color: green; selection-background-color: grey;}")
    dis = UI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()