import os
import subprocess
import tempfile
import sys
import re

if sys.platform.startswith('linux'):
    NASM = '/usr/bin/nasm'
    NDISASM = '/usr/bin/ndisasm'

elif sys.platform.startswith('win32'):
    NASM = 'nasm/nasm.exe'
    NDISASM = 'nasm/ndisasm.exe'

if not os.path.exists(NASM):
    raise EnvironmentError('nasm not found')
if not os.path.exists(NDISASM):
    raise EnvironmentError('ndisasm not found')


def delete_file(filename):
    """
    Deletes file from the disk if it exists
    """
    if os.path.exists(filename):
        os.unlink(filename)


def assemble(asm, mode="elf"):
    '''
    Assemble using nasm, return raw hex bytes.
    '''
    temp = tempfile.NamedTemporaryFile(delete=False)

    linkme = tempfile.NamedTemporaryFile(delete=False)
    dir = tempfile.gettempdir()
    try:
        temp.write(asm)
        temp.close()
        linkme.close()

        link = subprocess.check_output([NASM, '-f ' + mode, temp.name, '-o ' + dir + '/link.o'])
        out = subprocess.check_output([NASM, temp.name, '-o ' + temp.name + '.elf'])

        asm = open(temp.name + '.elf', 'rb')
        asm = asm.read()
        delete_file(temp.name + '.elf')
        delete_file(linkme.name)
        delete_file(dir + '/link.o')
        delete_file(temp.name)
        return asm
    except:
        delete_file(temp.name + '.elf')
        delete_file(linkme.name)
        delete_file(dir + '/link.o')
        delete_file(temp.name)
        return "assembly failed"


def disassemble(elf, mode=32):
    '''
    Disassemble using ndisasm. Return the output.
    '''
    temp = tempfile.NamedTemporaryFile(delete=False)
    try:
        temp.write(elf)
        temp.close()

        asm = subprocess.check_output([NDISASM, '-a', '-b ' + str(mode), temp.name])
        delete_file(temp.name)

        return asm
        
        #disasm = asm.split('\n') # parse nasm output. Not ready yet because nasm will output a new line if the instruction is too long
        #return [" ".join(x.split()).split(' ', 2) for x in disasm ]
    except:
        delete_file(temp.name)
        return 'disassembly failed'


print disassemble('\x48\x31\xc0\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\xb0\x3b\x48\x89\xe7\x48\x31\xf6\x48\x31\xd2\x0f\x05', 64)


asm = '''
BITS 32
main:
        ; execve("/bin/sh", 0, 0)
        xor eax, eax
        push eax
        push 0x68732f2f         ; "//sh" -> stack
        push 0x6e69622f         ; "/bin" -> stack
        mov ebx, esp                ; arg1 = "/bin//sh\0"
        mov ecx, eax                ; arg2 = 0
        mov edx, eax                ; arg3 = 0
        mov al, 11
        int 0x80
'''
print repr(assemble(asm, "elf"))
