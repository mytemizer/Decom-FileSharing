import socket
import os


def sh(script):
    os.system("bash -c '%s'" % script)


s = socket.socket()
s.bind(("localhost",9875))

s.listen(10) # Accept 10 connection
i=1

# This code first gets the name of the file then the content of the file

flag = False
while True:
    sc, address = s.accept()

    print (address) #open in binary


    i=i+1
    l = sc.recv(2)
    print(int(l))

#   This code checks whether patch file is sent or normal file.
#   If patch is sent, then it simply turn the flag True.

    l = sc.recv(int(l.decode("utf-8")))
    if l == b'msg.patch':
        flag = True

    f = open(l, 'wb')
    while (True):
        # recieve and write the file
        l = sc.recv(2048)
        while (l):
            f.write(l)
            l = sc.recv(2048)
        break
    f.close()

#   If the flag is True (patch file is received.), it executes the bash script
#   where patch file is applied to the file of the receiver.
    if (flag):
        print("patch is being applied")
        sh(
            "patch -t <  msg.patch; "
        )
        flag = False


    sc.close()

