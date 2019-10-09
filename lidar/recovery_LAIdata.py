
ori_min_x=470419.85
ori_max_x=470919.85
ori_min_y=5013860.28
ori_max_y=5014360.27
mean_x=(ori_min_x+ori_max_x)/2
mean_y=(ori_min_y+ori_max_y)/2

LAI_dirpath="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Insect\\2010_LeafOn_PC_013\\newsub"
LAIfilepath=LAI_dirpath+'\\'+'result_LAIe.txt'
newLAIfilePath=LAI_dirpath+'\\'+'LAIe.txt'
with open(LAIfilepath,'r') as fr,open(newLAIfilePath,"w") as fw:
    for line in fr:
        x=float(line.split(' ')[0])
        y=float(line.split(' ')[1])
        x+=mean_x
        y+=mean_y
        newline=str(x)+' '+str(y)+' '+line.split(' ')[2]
        fw.write(newline)