import distorm3
import codecs

def disassemble(shellcode, mode=32):
	if __name__ == '__main__':
		print shellcode.decode('utf-8').strip()
		code = codecs.escape_decode(shellcode.decode('utf-8').strip())[0]
	else:
		code = shellcode
	if mode == 32:
	    return distorm3.Decode(0x0, code, distorm3.Decode32Bits)
	elif mode == 64:
	    return distorm3.Decode(0x0, code, distorm3.Decode64Bits)
	elif mode == 16:
	    return distorm3.Decode(0x0, code, distorm3.Decode16Bits)


def main():
	def value(val):
		global mode
		mode = val

	def render():
		disasm.delete(1.0, tk.END)

		for i in disassemble(shellcode.get(1.0, tk.END), mode):
			disasm.insert(tk.INSERT, "0x%08x (%02x) %-20s %s" % (i[0],  i[1],  i[3],  i[2]) + "\n")

	import Tkinter as tk
	top = tk.Tk()
	top.title("Eggshells")
	top.resizable(0,0)

	shellcode = tk.Text(top)
	shellcode.pack(anchor = tk.W, fill=tk.BOTH, expand=1)

	disasm = tk.Text()
	disasm.pack(anchor = tk.W, fill=tk.BOTH, expand=1)

	var = tk.IntVar()

	R1 = tk.Radiobutton(top, text="16-bit", variable=var, value=1, command=lambda: value(16))
	R1.pack( anchor = tk.W )

	R2 = tk.Radiobutton(top, text="32-bit", variable=var, value=2, command=lambda: value(32))
	R2.pack( anchor = tk.W )

	R3 = tk.Radiobutton(top, text="64-bit", variable=var, value=3, command=lambda: value(64))
	R3.pack( anchor = tk.W)

	B = tk.Button( text ="Disassemble", command = render)
	B.pack( anchor = tk.W)

	top.mainloop()

if __name__ == '__main__':
	main()
