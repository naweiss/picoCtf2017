import md5 #Must be run in python 2.7.x

#code used to calculate successive hashes in a hashchain. 
seed = "b2f627fff19fda463cb386442eac2b3d"
last = "6c7c2dab26bca389b940dd5e417986c2"

#this will find the 5th hash in the hashchain. This would be the correct response if prompted with the 6th hash in the hashchain
hashc = seed
i = 0
while True:
    tmp = md5.new(hashc).hexdigest()
    if tmp == last:
	    break;
    i+=1
    hashc = tmp
print hashc+","+str(i)