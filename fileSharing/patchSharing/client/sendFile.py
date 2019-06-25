import socket
import sys

print("file is sending")

# This is the code where file is sent through socket byte-by-byte
# It takes the input and send it to the receiver.
# First sends name of the file in order to send original name to the receiver
# Then sends the content of the file.


s = socket.socket()
s.connect(("localhost",9875))
fileName = sys.argv[1]
f = open (fileName, "rb")

fileLenght = len(fileName)
print(fileLenght)
if(fileLenght < 10):
    temp = bytes("0" + str(len(fileName)), "utf-8")
elif (fileLenght < 100):
    temp = bytes(str(len(fileName)), "utf-8")

s.send(temp)

temp = bytes(fileName, "utf-8")
s.send(temp)

l = f.read(2048)
while (l):
    s.send(l)
    l = f.read(2048)
s.close()


