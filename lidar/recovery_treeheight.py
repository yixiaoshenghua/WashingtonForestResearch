import os
mean_x=567998
mean_y=1309280
dir='G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\Information\\Afforestation\\2015_LeafOn_45123C4404'
files=os.listdir(dir)

with open(dir+"\\treeheight.txt",'w') as fw:
    for i in range(1,9):
        with open(dir+"\\off_ground_points_xyz0"+str(i)+".txttreeheight.txt",'r') as fr:
            for line in fr:
                info=line.split(' ')
                x=str(round(float(info[0])+mean_x,2))
                y=str(round(float(info[1])+mean_y,2))
                newline=x+' '+y+' '+info[2]
                fw.write(newline)