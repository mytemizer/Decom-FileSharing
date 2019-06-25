import socket
import os


# Prints whether original or hash file is being received to console

def printInfo(printInfo):
    print()
    print("----------------------------------------------------------------")
    print("-----------------------%s-----------------------" %printInfo)
    print("----------------------------------------------------------------")
    print()
    print("                       New File Hashes : ")
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
    print("----------------------------------------------------------------------------------------------------")
    print()
    print("                                       Change Is Detected!!!")
    print()
    print("                                    Index Of Missing Part Is : ", missingPart)
    print()
    print("                                 Missing Parts Are Being Recieved... ")
    print("----------------------------------------------------------------------------------------------------")



# Basic bashScript executor

def sh(script):
    os.system("bash -c '%s'" % script)


# Socket initializer
# Returns socket

def init():
    s = socket.socket()
    s.bind(("127.0.0.1", 9875))
    s.listen(10)
    sc, address = s.accept()
    return sc


# Gets the file name from source

def getFileName():
    temp = sc.recv(2)
    temp = sc.recv(int(temp.decode()))
    fileName = temp.decode( )
    return fileName


# If the file exists, open it as read-only
# Else creates new one.

def openFile():
    try:
        fileToReadOrig = open(fileName, "rb")
        return True, fileToReadOrig
    except:
        fileToWriteOrig = open(fileName, "wb")
        return False, fileToWriteOrig


# Returns the type of the file which is sent from source
# Can be original file or hash file

def getTypeOfFile():
    type = sc.recv(8)
    return type


# Original file sending is done here
# File is got with 1Mb packages

def originalFileOp():
    printInfo("New File Receiving")
    tempFileData = sc.recv(1024 * 1024)
    while tempFileData:
        if tempFileData == b'finished':
            break
        fileToWriteOrig.write(tempFileData)
        tempFileData = sc.recv(1024 * 1024)
    fileToWriteHash = open(".hash%s" % fileName, "wb")
    l = sc.recv(1024)
    for i in range(0, int(len(l)/32)):
        print("           " + str(i) + ". hash : " + l.decode()[i*32:(i+1)*32])
        print()

    print("                        COMPLETED!")
    print()
    fileToWriteHash.write(l)
    fileToWriteHash.close()


# Reject the getting already existed file

def abortGettingFile():
    sc.send(b'-1')


# Gets the missing parts of the file from source

def getMissingParts(counter, hashFile, newHashFile):
    # Open a temp file and start getting missing parts
    #####################
    tempFile = open("tempFile.txt", "w+")
    for i in range(0, counter):
        tempFile.write(fileToReadOrig.read(1024 * 1024).decode())
    changedData = sc.recv(1024 * 1024)
    #####################
    # Write the changed parts to the file
    ######################
    while changedData:
        tempFile.write(changedData.decode())
        changedData = sc.recv(1024 * 1024)
    ######################
    # Close files
    ######################
    tempFile.close()
    fileToReadOrig.close()
    hashFile.close()
    newHashFile.close()
    ######################
    # Rearrange file names
    ######################
    sh("mv newHashFile .hash%s" % fileName)
    sh("rm -rf %s" % fileName)
    sh("mv tempFile.txt %s" % fileName)
    ######################


# Determines whether the any part of the file is missing
# Compares the old hash values with new ones

def isMissing(hashFile, newHashValue):
    isMissing = False
    counter = 0
    print("         - New File Hashes -                                              - Old File Hashes -")
    print("         -------------------                                              -------------------")
    print()
    size = int(len(newHashValue) / 32)
    for i in range(1, size + 1):
        tempHashData = hashFile.read(32)
        if newHashValue[(i - 1) * 32:i * 32] == tempHashData:
            print(newHashValue[(i - 1) * 32:i * 32], "    <<<<--  Same  -->>>>   ", tempHashData)
            counter += 1
            print()

        else:
            print(newHashValue[(i - 1) * 32:i * 32], "    <<<<- Not Same ->>>>   ", tempHashData)
            sc.send(str(i - 1).encode())
            isMissing = True
            counter = i - 1
            print()
            break
    return isMissing, counter


# If the file exists, this method will be called and comparison operation and
# adding new parts to the file is handled here.

def hashFileOp():
    newHashValue = sc.recv(1024)
    hashFile = open(".hash%s"%fileName, "rb")
    newHashFile = open("newHashFile", "wb")
    newHashFile.write(newHashValue)
    isMissingBool, counter = isMissing(hashFile, newHashValue)
    if isMissingBool:
        printChangeInfo(counter)
        getMissingParts(counter, hashFile, newHashFile)
    else:
        abortGettingFile()

    print("                                             COMPLETED!")
    print()

    sh("rm -rf newHashFile")


# Deciding the file operation

def writeToTheFile():
    if type == b'original':
        originalFileOp()
    else:
        hashFileOp()


# Start point of the program

if __name__ == '__main__':
    sc = init()
    fileName = getFileName()
    state, fileOrig = openFile()
    if state:
        fileToReadOrig = fileOrig
    else:
        fileToWriteOrig = fileOrig

    type = getTypeOfFile()

    writeToTheFile()
