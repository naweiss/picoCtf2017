#!/usr/bin/python
#Let x be an integer written in binary, y and n be integers
#I'm sure this isn't the best, but this is only called once per program
def binconvert(n):
  barray = []
  if n < 0: 
    raise ValueError, "must be positive"
  if n == 0:
    return 0
  while n > 0:
    #barray = n%2 + barray[:]
    barray.append(n%2)
    n = n >> 1
  barray.reverse()
  return barray
#this is the intuitive but slow way
def modexp(base, pow, mod):
  exponent = 1
  i = 0
  while i < pow:
    exponent = (exponent * base) % mod  
    i += 1
  return exponent
#y**x mod n
def modexp1(y, x, n):
  #convert x to a binary list
  x = binconvert(x)
   
  s = [1]
  r = x[:]
  for k in range (0, len(x)):
    if x[k] == 1:
      r[k] = (s[k] * y) % n
    else:
      r[k] = s[k]
    s.append ((r[k]**2)%n)
  #print s
  #print r
  return r[-1]
#similar to modexp1 except uses the bits in reverse order
def modexp2(y, x, n):
  a = x
  b = 1
  c = y
  while a != 0:
    if a % 2 == 0:
      a = a/2
      c = (c**2) % n
    else:
      a = a -1
      b = (b * c) % n
  return b

if __name__ == "__main__":
  import sys
  #print modexp(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
  print hex(modexp1(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])))[2:-1].decode("hex")
  #print modexp2(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))