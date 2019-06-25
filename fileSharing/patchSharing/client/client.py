import socket
import sys
import os

# In this function, basic bashscript codes can be executed.
def sh(script):
    os.system("bash -c '%s'" % script)


fileName = sys.argv[1]

# In this script,
# First case
#   We check whether file was sent before by looking if there is hidden version of the file
#   If it is the first time, we copy the file  to the hidden file with same name and send the original file completely
# Second case,
#   If there is hidden version, we diff them and store in the patch file.
#   If patch file size is 0, we don't send anything to the receiver.
# Third case
#   If patch file size is not zero, we send the patch file to the receiver to get the changes.

sh("if [ ! -f .{} ]; "
   "then "
   "cp {} .{}; "
   "python3 sendFile.py {}; "
   "else "
   "diff -u {} .{} > msg.patch; "
   "if [ -s msg.patch ]; "
   "then "
   "cp {} .{}; "
   "echo changed; "
   "python3 sendFile.py msg.patch; "
   "else "
   "echo No change detected; "
   "fi;"
   "fi;"
   .format(fileName, fileName, fileName, fileName, fileName, fileName, fileName,fileName)
   )
