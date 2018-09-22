from pwn import *
import os

os.environ["QEMU_LD_PREFIX"] = '/home/naweiss/i386-linux-gnu'
os.environ["LD_LIBRARY_PATH"] = '/home/naweiss/gdb-libs'

def getChars():
    return [chr(i) for i in [95]+range(97,126)]

def getProcess(file_path, args):
    with context.local(log_level = 'ERROR'):
        qemu_port = 55321
        argv = ['qemu-i386','-g', str(qemu_port), file_path]
        qemuserver = process(argv + args)
        argv = ['gdb-multiarch', '--data-directory', '/home/naweiss/gdb-share/gdb/', file_path]
        pre  = 'set architecture %s\n' % 'i386'
        pre += 'set endian %s\n' % 'little'
        pre += 'target remote %s:%d\n' % ('localhost', 55321)
        pre += 'set sysroot %s\n' % '/home/naweiss/i386-linux-gnu'
        p = process(argv)
        p.send(pre)
        p.recvuntil('(gdb) ')
        p.recvuntil('(gdb) ')
        p.recvuntil('(gdb) ')
        p.recvuntil('(gdb) ')
        p.recvuntil('(gdb) ')
        return p, qemuserver

def main():
    SIZE = 51
    with open('found.txt','r') as f:
        prev = f.read()
    with open('string.txt','r') as f:
        clue = f.read()
    with open('found.txt','a') as f:
        for i in range(len(prev),SIZE):
            with log.progress('Flag') as bar:
                for char in getChars():
                    flag = prev+char+(SIZE-len(prev)-1)*'a'
                    p, server = getProcess('./forest',[flag,clue])
                    p.sendline('b *0x80484dd') # address o the checking function
                    p.recvuntil('(gdb) ')
                    p.sendline('c')
                    p.recvuntil('(gdb) ')
                    bar.status(flag)
                    if len(prev)>0:
                        p.sendline('c '+str(len(prev)))
                        p.recvuntil('(gdb) ')
                    p.sendline('i r eax')
                    eax = p.recvuntil('(gdb) ')[-8]
                    with context.local(log_level = 'ERROR'):
                        p.kill()
                        server.kill()
                    if eax == "1":
                        bar.success(flag)
                        f.write(char)
                        prev += char
                        break

if __name__ == "__main__":
    main()