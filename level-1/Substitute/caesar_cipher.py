def Dodecode(chiper,i):
	text =""
	for c in chiper:
		if("a" <= c <= "z"):
			text += chr((ord(c)-ord("a")+i)%26+ord("a"))
		elif("A" <= c <= "Z"):
			text += chr((ord(c)-ord("A")+i)%26+ord("A"))
		else:
			text += c
	return text
	
def Decode(chiper):
	text =""
	for i in range(1,26):
		text += Dodecode(chiper,i)+"number: " + str(i) + "\n\n"
	return text

name = raw_input("Enter file name:\n> ")
text = open(name,"r")
opt = ""
while (opt != "y" and opt != "n") :
	opt = raw_input("Brute force? [y\\n]\n")
if opt == "y":
	print(Decode(text.readline()[:100]))
else:
	print Dodecode(text.read(),int(raw_input("Enter a number:"))) 
