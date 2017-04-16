import math
import random

############################
## Wiener's Attack module ##
############################

# Calculates bitlength
def bitlength(x):
  assert x >= 0
  n = 0
  while x > 0:
    n = n+1
    x = x>>1
  return n
  
# Squareroots an integer
def isqrt(n):
  if n < 0:
    raise ValueError('square root not defined for negative numbers')  
  if n == 0:
    return 0
  a, b = divmod(bitlength(n), 2)
  x = 2**(a+b)
  while True:
    y = (x + n//x)//2
    if y >= x:
      return x
    x = y

# Checks if an integer has a perfect square
def is_perfect_square(n):
  h = n & 0xF; #last hexadecimal "digit"    
  if h > 9:
    return -1 # return immediately in 6 cases out of 16.
  # Take advantage of Boolean short-circuit evaluation
  if ( h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8 ):
    # take square root if you must
    t = isqrt(n)
    if t*t == n:
      return t
    else:
      return -1    
  return -1

# Calculate a sequence of continued fractions
def partial_quotiens(x, y):
  partials = []
  while x != 1:
    partials.append(x // y)
    a = y
    b = x % y
    x = a
    y = b
  #print partials
  return partials

# Helper function for convergents
def indexed_convergent(sequence):
  i = len(sequence) - 1
  num = sequence[i]
  denom = 1
  while i > 0:
    i -= 1
    a = (sequence[i] * num) + denom
    b = num
    num = a
    denom = b
  #print (num, denom)
  return (num, denom)

# Calculate convergents of a  sequence of continued fractions
def convergents(sequence):
  c = []
  for i in range(1, len(sequence)):
    c.append(indexed_convergent(sequence[0:i]))
  #print c
  return c

# Calculate `phi(N)` from `e`, `d` and `k`
def phiN(e, d, k):
  return ((e * d) - 1) / k

# Wiener's attack, see http://en.wikipedia.org/wiki/Wiener%27s_attack for more information
def wiener_attack(N,e):
  (p,q,d) = (0,0,0)
  conv=convergents(partial_quotiens(e,N))
  for frac in conv:
    (k,d)=frac
    if k == 0:
      continue
    y = -(N - phiN(e, d, k) + 1)
    discr = y*y - 4*N
    if(discr>=0):
      # since we need an integer for our roots we need a perfect squared discriminant
      sqr_discr = is_perfect_square(discr)
      # test if discr is positive and the roots are integers
      if sqr_discr!=-1 and (-y+sqr_discr)%2==0:
        p = ((-y+sqr_discr)/2)
        q = ((-y-sqr_discr)/2)
        return p, q, d
  return p, q, d

################################
## End Wiener's Attack module ##
################################

e = 165528674684553774754161107952508373110624366523537426971950721796143115780129435315899759675151336726943047090419484833345443949104434072639959175019000332954933802344468968633829926100061874628202284567388558408274913523076548466524630414081156553457145524778651651092522168245814433643807177041677885126141
n = 380654536359671023755976891498668045392440824270475526144618987828344270045182740160077144588766610702530210398859909208327353118643014342338185873507801667054475298636689473117890228196755174002229463306397132008619636921625801645435089242900101841738546712222819150058222758938346094596787521134065656721069

ans = wiener_attack(n,e)

c = 60109758698128083867894286068285517856121577775873732971271767838094375540242140682860856525076716857853484762310661349595705965454241788627490154678487289327504291223547525832864143253412180183596307295520420578906308624860023542143928885210079178897416418810270090406582415840515326539954964020452551186119
d = ans[2]
print hex(pow(c,d,n))[2:-1].decode("hex")