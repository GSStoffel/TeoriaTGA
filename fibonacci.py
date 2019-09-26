import sys
import os

def encode_fib(n):
    result = ""
    if n >= 1:
        a = 1
        b = 1
        c = a + b
        fibs = [b]
        while n >= c:
            fibs.append(c)
            a = b
            b = c
            c = a + b
        result = "1"
        for fibnum in reversed(fibs):
            if n >= fibnum:
                n = n - fibnum
                result = "1" + result
            else:
                result = "0" + result
    return result

def byteWriter(bitStr, outputFile):
    global bitStream
    bitStream += bitStr
    while len(bitStream) > 8:
        byteStr = bitStream[:8]
        bitStream = bitStream[8:]
        chr_int_bytestr = chr(int(byteStr, 2))
        outputFile.write(bytes(chr_int_bytestr, 'utf-8'))

def bitReader(n):
    global byteArr
    global bitPosition
    bitStr = ''
    for i in range(n):
        bitPosInByte = 7 - (bitPosition % 8)
        bytePosition = int(bitPosition / 8)
        byteVal = byteArr[bytePosition]
        bitVal = int(byteVal / (2 ** bitPosInByte)) % 2
        bitStr += str(bitVal)
        bitPosition += 1
    return bitStr

if len(sys.argv) != 4:
    sys.argv = ['.\\fibonacci.py', 'd', '.\\output.txt', 'output2.txt']
    print('Usage: Fibonacci.py [e|d] [path]InputFileName [path]OutputFileName')
mode = sys.argv[1]
inputFile = sys.argv[2]
outputFile = sys.argv[3]

fileSize = os.path.getsize(inputFile)
fi = open(inputFile, 'rb')
byteArr = bytearray(fi.read(fileSize))
fi.close()
fileSize = len(byteArr)
print('File size in bytes:', fileSize)
print()

if mode == 'e':
    freqList = [0] * 256
    for b in byteArr:
        freqList[b] += 1

    tupleList = []
    for b in range(256):
        if freqList[b] > 0:
            tupleList.append((freqList[b], b, ''))

    tupleList = sorted(tupleList, key=lambda tup: tup[0], reverse = True)

    for b in range(len(tupleList)):
        tupleList[b] = (tupleList[b][0], tupleList[b][1], encode_fib(b + 1))

    bitStream = ''
    fo = open(outputFile, 'wb')
    chr_len_tuple = chr(len(tupleList) - 1)
    fo.write(bytes(chr_len_tuple, 'utf-8'))
    for (freq, byteValue, encodingBitStr) in tupleList:
      chr_byte_value = chr(byteValue)
      fo.write(bytes(chr_byte_value, 'utf-8'))

    bitStr = bin(fileSize - 1)
    bitStr = bitStr[2:]
    bitStr = '0' * (32 - len(bitStr)) + bitStr
    byteWriter(bitStr, fo)

    dic = dict([(tup[1], tup[2]) for tup in tupleList])

    for b in byteArr:
        byteWriter(dic[b], fo)

    byteWriter('0' * 8, fo)
    fo.close()

elif mode == 'd':
    bitPosition = 0
    n = int(bitReader(8), 2) + 1
    dic = dict()
    for i in range(n):
        byteValue = int(bitReader(8), 2)
        encodingBitStr = encode_fib(i + 1)
        dic[encodingBitStr] = byteValue

    # Doesn't work from here downwards. Maybe long() should be changed to int()
    numBytes = long(bitReader(32), 2) + 1
    print('Number of bytes to decode:', numBytes)

    fo = open(outputFile, 'wb')
    for b in range(numBytes):
        encodingBitStr = ''
        while True:
            encodingBitStr += bitReader(1)
            if encodingBitStr.endswith('11'):
                byteValue = dic[encodingBitStr]
                chr_bytevalue = chr(byteValue)
                fo.write(bytes(chr_bytevalue, 'utf-8'))
                break
    fo.close()