[main]
input = 0xAABBCCDD
$6	= 0xAA000000
$16	= 0xBB0000
$7	= 0xCC00
$4 	= 0xDD

$v1 = 0xAA
$2 = 0

[L3]:
while (is $2 smaller then 13)
	$2++
	$v1 -= 13

[L2]:
$v1 -= 6
$5	= ($v1 << 24) #last two bits of v1 and zeros on the right
$16 = ($16 >> 16) = 0xBB #signed shift
$2 = $16-81
$8 = ($2 << 6) 
$v1 = ($2 << 8) 
$v1 -= $8
$v1 = $2 - $v1
$7 = ($7 >> 8) = 0xCC #signed shift
$2 = ($4 << 1) = 0xDD*2
$2 += 3
if $2 != $7: Goto L7
$v1 = ($v1 << 16) #add four zeros on the right
$2 = 94
Goto L4

[L7]:
$2 = 165

[L4]:
$2 -= 94
$2 = ($2 << 8)
$6 = ($6 >> 24) = 0xAA #unsigned shift
$16 = $6 - $16 = 0xAA-0xBB
$4 -= $16 = 0xDD - (0xAA - 0xBB)
$v1 += $5
$v1 += $2
$16 = $4 + $v1
if $16 != 0: Goto Faild
Goto Success
