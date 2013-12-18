try:
    from distorm import *
    module = 'distorm'
except ImportError:
    try:
        from nasm import *
        module = 'nasm'
    except ImportError:
        raise EnvironmentError("Couldn't find distorm or nasm")
import codecs
from Tkinter import *
from ttk import *
import interpreter

class Disassembler():
    def __init__(self, frame):
        self.shellcode = Text(frame)
        self.shellcode.pack(anchor=W, fill=BOTH, expand=1)
        self.shellcode.config(height=4, bd=2)

        self.disasm = Text(frame)
        self.disasm.pack(anchor=W, fill=BOTH, expand=1)
        self.disasm.config(height=4, bd=2)

        var = IntVar()

        R1 = Radiobutton(frame, text="16-bit", variable=var, value=1, command=lambda: self.value(16))
        R1.pack(anchor=W)

        R2 = Radiobutton(frame, text="32-bit", variable=var, value=2, command=lambda: self.value(32))
        R2.pack(anchor=W)

        R3 = Radiobutton(frame, text="64-bit", variable=var, value=3, command=lambda: self.value(64))
        R3.pack(anchor=W)

        B = Button(frame, text="Disassemble", command=self.render)
        B.pack(anchor=W)

    def value(self, val):
        '''
        Sets disassembler mode (e.g. 16bit, 32bit, or 64bit)
        '''
        global mode
        self.mode = val

    def clean(self, shellcode):
        '''
        Cleans the format that we get from tkinter into a format we can disassemble easily. (i.e. \x00\x00)
        '''
        return codecs.escape_decode(shellcode.decode('utf-8').strip())[0]

    def render(self):
        '''
        Cleans out the Text widget, does the disassembly and inserts it.
        '''
        self.disasm.delete(1.0, END)
        self.disasm.insert(INSERT, disassemble(self.clean(self.shellcode.get(1.0, END)), self.mode))

class Assembler():
    def __init__(self, frame):
        assembler = Text(tab2)
        assembler.pack(anchor=W, fill=BOTH, expand=1)
        assembler.config(height=4, bd=2)

class ConnectBack():
    def __init__(self, frame):
        pass


root = Tk()
root.title("Eggshells - " + module)
note = Notebook(root)

tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
tab4 = Frame(note)
tab5 = Frame(note)

#################DISASM################
Disassembler(tab1)
#######################################

################ASM####################
Assembler(tab2)
#######################################

################Python#################
c = interpreter.Console(tab4)
c.dict["console"] = c
c.pack(fill=BOTH, expand=1)
#######################################

note.add(tab1, text = "Disassembler")
note.add(tab2, text = "Assembler")
note.add(tab3, text = "Sockets")
note.add(tab4, text = "Python")
note.add(tab5, text = "Hex Editor")

note.pack(fill=BOTH, expand=1)
root.mainloop()
exit()