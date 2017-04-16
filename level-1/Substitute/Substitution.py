execfile("freqAnalysis.py")
name = raw_input("Enter file name:\n> ")
m = open(name,"rt").read()
guess = getTranslationAlphabet(m)
print guess
#guessed = substitute(m, guess)

guessed = substitute(m ,'AYWMCNOPHQRSTJIPKDLEGXUVFB')