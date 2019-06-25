import sys
import socket
import hashlib



# Prints whether original or hash file is being received to console

def printInfo(printInfo):
    print()
    print("---------------------------------------------------------------")
    print("---------------------%s---------------------" %printInfo)
    print("---------------------------------------------------------------")
    print()
    print()
    print("                       Hashes of each Mb")
    print()


# Print when there is no change in file

def printNoChange():
    print("---------------------------------------------------------------")
    print()
    print("             Result : Nothing Changed in the %s " % fileName)
    print()
    print("---------------------------------------------------------------")

# Print when change in the file is detected

def printChangeInfo(missingPart):
    print("---------------------------------------------------------------")
    print()
    print("                    Change Is Detected!!!")
    print()
    print("                 Index Of Missing Part Is : ", missingPart)
    print()
    print("                Missing Parts Are Being Sent... ")
    print("---------------------------------------------------------------")


# Socket initializer
# Returns socket

def init():
    s = socket.socket()
    s.connect(("localhost", 9875))
    return s

# Sends the file name to the destination

def sendFileName():
    temp = b''

    if fileLenght < 10:
        temp = bytes("0" + str(len(fileName)), "utf-8")
    elif fileLenght < 100:
        temp = bytes(str(len(fileName)), "utf-8")
    s.send(temp)
    temp = bytes(fileName, "utf-8")
    s.send(temp)


# Checks whether it is the first time sending the file

def doesExists():
    try:
        open(".hash%s" % fileName, "rb")
        return True
    except:
        return False


# Sending content of the hash file to the destination

def sendHashFile(fileToRead, fileToWrite):
    # Read 1 MB
    tempFileData = fileToRead.read(1024 * 1024)
    hashString = ""
    hashCount = 0
    # Until finish reading file
    while tempFileData:
        # Get hash of each 1 MB
        hashValue = hashlib.md5(tempFileData).hexdigest()
        print("          " + str(hashCount) + ". hash :  " + hashValue)
        fileToWrite.write(hashValue.encode())
        hashString += hashValue
        tempFileData = fileToRead.read(1024 * 1024)
        hashCount += 1
        print()
    s.send(hashString.encode())
    return hashCount


# Sends only missing parts of the file to the destination

def sendMissingParts(fileToRead, fileToWrite):
    s.send("hashrslt".encode())

    printInfo("--Hash File Sending--")

    hashCount = sendHashFile(fileToRead, fileToWrite)

    l = s.recv(1024)
    missingPart = int(l.decode())
    if missingPart == -1:
        printNoChange()
    else:
        printChangeInfo(missingPart)
        fileToRead = open(fileName, "rb")
        for i in range(0, hashCount):
            l = fileToRead.read(1024 * 1024)
            if i >= missingPart:
                s.send(l)


# Sends the whole original file

def sendOriginal(fileToRead, fileToWrite):
    s.send("original".encode())
    printInfo("Original File Sending")


    # Read 1 MB
    tempData = fileToRead.read(1024 * 1024)
    hashString = ""
    counter = 0


    while tempData:
        s.send(tempData)
        hashValue = hashlib.md5(tempData).hexdigest()
        print("           " + str(counter) + ". hash : " + hashValue)
        print()
        fileToWrite.write(hashValue.encode())
        hashString += hashValue
        tempData = fileToRead.read(1024 * 1024)
        counter += 1
    s.send(b'finished')
    s.send(hashString.encode())


# Start operation invoker

def startToSend():

    fileToRead = open(fileName, "rb")
    hashOrOrig = doesExists()
    fileToWrite = open(".hash%s" % fileName, "wb")

    if hashOrOrig:
        sendMissingParts(fileToRead, fileToWrite)

    else:
        sendOriginal(fileToRead, fileToWrite)


# Start point of the program

if __name__ == '__main__':
    s = init()
    fileName = sys.argv[1]
    fileLenght = len(fileName)
    sendFileName()
    startToSend()

    print()
    print("                        COMPLETED!")
    print()
