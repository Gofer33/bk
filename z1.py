import re
import string
import itertools

cryptoToDecode = ''
cryptos = []
cryptosToUse = 20

def readCryptos():
	global cryptos
	global cryptoToDecode
	f = open("cryptos", "r")
	filecontent = f.read()

	x = re.split(r"\n\nkryptogramm nr \d+:\n", filecontent, maxsplit = 20)
	t = x[20].find(':')+2
	cryptoToDecode = x[20][t : len(x[20])].split()

	x[20] = x[20][0 : x[20].find('\n')]

	cryptos = x[1:21]
	cryptos[:] = [x.split() for x in cryptos]

def maxBytes(cryptos):
	max = 0
	for c in cryptos:
		if len(c) > max:
			max = len(c)
	return max

def xorTwoBytes(b1, b2):
	y = int(b1, 2)^int(b2,2)
	return bin(y)[2:].zfill(len(b1))

def isResultAlpha(a):
	w = chr(int(a, 2))
	if(w in string.printable and w.isalpha()):
		return True
	return False

readCryptos()
maxbytes = maxBytes(cryptos)
key = ['00000000'] * maxbytes

for idx1 in range(0, cryptosToUse):
	spacesProbability = [0] * maxbytes
	for idx2 in range(0, cryptosToUse):
		if(idx1 == idx2):
			continue
		shorterMsg = min(len(cryptos[idx1]), len(cryptos[idx2]))
		# shorterMsg = 15
		for i in range(0, shorterMsg):
			result = xorTwoBytes(cryptos[idx1][i], cryptos[idx2][i])
			isResultAlphaChar = isResultAlpha(result)
			if isResultAlphaChar == True:
				spacesProbability[i] = spacesProbability[i] + 1

	for idx, val in enumerate(spacesProbability):
		if(val >= 0.6 * cryptosToUse):
			key[idx] = xorTwoBytes(cryptos[idx1][idx], '00100000')

text = ''
for idx, c in enumerate(cryptoToDecode):
	decodedChar = xorTwoBytes(c, key[idx])
	text += (chr(int(decodedChar, 2)))

print(text)

# for idx, c in enumerate(cryptos):
# 	text = ''
# 	for idx2, c2 in enumerate(c):
# 		decodedChar = xorTwoBytes(c2, key[idx2])
# 		text += (chr(int(decodedChar, 2)))
# 	print()
# 	print(text)


