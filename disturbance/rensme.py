import os
oldpath = "G:\\中美华盛顿科考\\算法\\csv1"
newpath = "G:\\中美华盛顿科考\\算法\\csv2"
files = os.listdir(oldpath)
for i, file in enumerate(files):
    line=file.split(' ')
    newline=line[0]+' 1'+line[1]
    NewFileName = os.path.join(newpath, newline)
    OldFileName = os.path.join(oldpath, file)
    os.rename(OldFileName, NewFileName)