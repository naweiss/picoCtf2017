#########################
#From page 52 in the pdf#
#########################

import dpkt
import sys

# Start the pcap file parsing
name=raw_input("Please insert file name:\n> ")
f = open(name, 'rb')
pcap = dpkt.pcap.Reader(f)

# Create a partial mapping from keycodes to ASCII chars
keys = {}
keys.update({
  i + 0x4: chr(i + ord('a'))
  for i in range(26)
})

keys.update({
  i + 0x1e: chr(i + ord('1'))
  for i in range(9)
})

keys[0x27] = '0'
keys.update({
  0x28: '\n',
  0x2c: ' ',
  0x2d: '_',#or -
  0x2e: '=',#or +
  0x2f: '{',#or [
  0x30: '}',#or ]
})

for ts, buf in pcap:

  try:
      key_code = ord(buf[29])
      if not key_code and key_code == 0 :
          continue
      sys.stdout.write(keys[key_code])

  except Exception as ex:
      pass
