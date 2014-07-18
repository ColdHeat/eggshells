import capstone

from utils import *
from PySide import QtGui, QtCore


class Disassembler(QtGui.QWidget):

    def __init__(self):
        super(Disassembler, self).__init__()
        self.render()

    def arch(self, arch):
        if arch == 'arm':
            return capstone.CS_ARCH_ARM
        elif arch == 'arm64':
            return capstone.CS_ARCH_ARM64
        elif arch == 'mips':
            return capstone.CS_ARCH_MIPS
        elif arch == 'x86':
            return capstone.CS_ARCH_X86


    def mode(self, mode):
        if mode == 'arm':
            return capstone.CS_MODE_ARM
        elif mode == 'thumb':
            return capstone.CS_MODE_THUMB
        elif mode == '16' or mode == 16:
            return capstone.CS_MODE_16
        elif mode == '32' or mode == 32:
            return capstone.CS_MODE_32
        elif mode == '64' or mode == 64:
            return capstone.CS_MODE_32


    def disassemble(self, code, _arch, _mode):
        _arch = self.arch(_arch)
        _mode = self.mode(_mode)

        md = capstone.Cs(_arch, _mode)

        disassembly = []

        for i in md.disasm(code, 0x0000000):
            disassembly.append(
                (i.address, len(str(i.bytes).encode('hex')) / 2, str(i.bytes).encode('hex'), i.mnemonic, i.op_str))

        return disassembly


    def setText(self, text):
        self.dis.setText(text)

    def append(self, text):
        self.dis.append(text)

    def render(self):
        frame = QtGui.QHBoxLayout(self)
        frame.setContentsMargins(0,0,0,0)

        self.dis = QtGui.QTextEdit(self)
        self.dis.setFont(codefont())

        frame.addWidget( self.dis )
