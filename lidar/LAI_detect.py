LAI_dirpath="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Deforestation\\2010_LeafOn_PC_029\\newsub"
LAIfilepath=LAI_dirpath+'\\'+'result_LAIe.txt'

with open(LAIfilepath,'r') as fr:
    LAI=[]
    for line in fr:
        LAI.append(float(line.split(' ')[2]))
    print("LAI max:",max(LAI))
    print("LAI min:",min(LAI))