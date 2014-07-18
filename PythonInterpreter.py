import sys
import code
import utils

from PySide import QtGui, QtCore

class stdout:
    """ Dirty hack for overriding default print behavior """
    def __init__(self, *writers) :
        self.writers = writers
        
    def write(self, text):
        for w in self.writers:
            if text != "\n":
                w.append(text)

class stderr:
    def __init__(self, *writers) :
    	self.writers = writers
    	
    def write(self, text):
        for w in self.writers :
            if text != "\n":
                w.append(text.rstrip())

class CLI(QtGui.QWidget):
    def __init__(self):
        super(CLI, self).__init__()
        self.interpreter = code.InteractiveInterpreter()

        self.history = QtGui.QTextEdit(self)
        self.history.setReadOnly(True)
        self.history.setFont(utils.codefont())

        self.commands = QtGui.QLineEdit(self)
        self.commands.returnPressed.connect(self.run)
        self.commands.setFont(utils.codefont())

        sys.stdout = stdout(self.history)
        sys.stderr = stderr(self.history)
        self.render()

    def run(self):
        command = self.commands.text()
        commands = {"hash": utils.hash}
        try:
            command = command.split(' ')
            args = tuple(command[1:])
            command = command[0]
            if command in commands.keys():
                commands[command](*args)
            else:
                raise Exception
            return
        except:
            command = self.commands.text()
        res = self.interpreter.runcode(command)
        self.write(res)
        self.commands.setText("")

    def write(self, text):
        self.history.append(text)

    def render(self):
        frame = QtGui.QVBoxLayout(self)
        frame.setContentsMargins(0,0,0,0)

        frame.addWidget(self.history)
        frame.addWidget(self.commands)
