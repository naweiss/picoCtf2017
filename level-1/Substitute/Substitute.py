def rot13(char):
   return chr(ord('A')+(ord(char)-ord('A')+13)%26)

f = open("cipher.txt","r").read()
chrs=['A','B' , 'C' , 'D' , 'E' , 'F' , 'G' , 'H' , 'I' , 'J' , 'K' , 'L' , 'M' , 'N' , 'O' , 'P' , 'Q' , 'R' , 'S' , 'T' , 'U' , 'V' , 'W' , 'X' , 'Y' , 'Z']
ans =""
for char in f:
    if char in chrs:
        ans += rot13(char)
    else:
         ans+=char
print ans