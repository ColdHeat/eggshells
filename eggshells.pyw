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


def main():
    def value(val):
        '''
        Sets disassembler mode (e.g. 16bit, 32bit, or 64bit)
        '''
        global mode
        mode = val

    def clean(shellcode):
        '''
        Cleans the format that we get from tkinter into a format we can disassemble easily. (i.e. \x00\x00)
        '''
        return codecs.escape_decode(shellcode.decode('utf-8').strip())[0]

    def render():
        '''
        Cleans out the Text widget, does the disassembly and inserts it.
        '''
        disasm.delete(1.0, tk.END)
        disasm.insert(tk.INSERT, disassemble(clean(shellcode.get(1.0, tk.END)), mode))

    import Tkinter as tk

    top = tk.Tk()
    top.title("Eggshells - " + module)

    shellcode = tk.Text(top)
    shellcode.pack(anchor=tk.W, fill=tk.BOTH, expand=1)
    shellcode.config(height=4, bd=2)

    disasm = tk.Text()
    disasm.pack(anchor=tk.W, fill=tk.BOTH, expand=1)
    disasm.config(height=4, bd=2)

    var = tk.IntVar()

    R1 = tk.Radiobutton(top, text="16-bit", variable=var, value=1, command=lambda: value(16))
    R1.pack(anchor=tk.W)

    R2 = tk.Radiobutton(top, text="32-bit", variable=var, value=2, command=lambda: value(32))
    R2.pack(anchor=tk.W)

    R3 = tk.Radiobutton(top, text="64-bit", variable=var, value=3, command=lambda: value(64))
    R3.pack(anchor=tk.W)

    B = tk.Button(text="Disassemble", command=render)
    B.pack(anchor=tk.W)

    top.mainloop()


if __name__ == '__main__':
    main()
