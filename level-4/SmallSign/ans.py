#!/usr/bin/python -u
from pwn import *
import time
import sys

print "starting..."

#n = max number
def gen_primes(n):
    if n<=2:
        return []
    sieve=[True]*(n+1)
    for x in range(3,int(n**0.5)+1,2):
        for y in range(3,(n//x)+1,2):
            sieve[(x*y)]=False
    return [2]+[i for i in range(3,n,2) if sieve[i]]

def primes_fact(n):
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)  # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
       primfac.append(n)
    return primfac

primes = gen_primes(700)

while True:
    try:
        r = remote('shell2017.picoctf.com', 10650)
        r.recvline()
        N = int(r.recvline().lstrip("N: "))
        dict = {}
        for prime in primes:
            r.recvuntil("Enter a number to sign (-1 to stop):")
            start_time = time.time()
            r.sendline(str(prime))
            ans = r.recvline().lstrip("Signature: ")
            dict[str(prime)] = ans
        r.sendline("-1")
        
        ans = r.recvline().lstrip("Enter a number to sign (-1 to stop): Challenge: ")
        facts = primes_fact(int(ans))
        if facts[len(facts)-1] > 700:
            continue
        print facts
        sig = 1
        for fact in facts:
            sig = (sig*int(dict[str(fact)]))%N
		print sig
        r.sendline(str(sig).rstrip("L"))
        print r.recvall()
    	r.close()
    	break
    except:
        r.close()