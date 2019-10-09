import os
oldpath ="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Insect\\2010_LeafOn_PC_013\\sub"
newpath ="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Insect\\2010_LeafOn_PC_013\\newsub"

files = os.listdir(oldpath)
for i, file in enumerate(files):
    NewFileName = os.path.join(newpath, str(i+1)+'.txt')
    OldFileName = os.path.join(oldpath, file)
    os.rename(OldFileName, NewFileName)
