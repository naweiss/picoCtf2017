import md5 #Must be run in python 2.7.x

#code used to calculate successive hashes in a hashchain. 
seed = "4269"
seed = md5.new(seed).hexdigest()
token = "3a0129cfe57632fc13f2be833a37892c"

#this will find the 5th hash in the hashchain. This would be the correct response if prompted with the 6th hash in the hashchain
hashc = seed
while True:
    tmp = md5.new(hashc).hexdigest()
    if tmp == token:
        break
    hashc = tmp
print hashc #prev hash