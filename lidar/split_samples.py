# --- coding utf-8 --- 
import os
ori_min_x=569652.36
ori_max_x=569652.36
ori_min_y=1311311.78
ori_max_y=1311311.78
mean_x=(ori_min_x+ori_max_x)/2
mean_y=(ori_min_y+ori_max_y)/2


min_x=ori_min_x-mean_x
max_x=ori_max_x-mean_x
min_y=ori_min_y-mean_y
max_y=ori_max_y-mean_y
sample_size=30
Nx=(max_x-min_x)//sample_size+1
Ny=(max_y-min_y)//sample_size+1

#定义抽样块函数
def sample_index(x,y):
    judge_x=(x-ori_min_x)//sample_size+1
    judge_y=(y-ori_min_y)//sample_size+1
    n=Nx*(judge_y-1)+judge_x
    return n

readfile_path="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Afforestation\\2015_LeafOn_45123C4404\\off_ground_points_xyzadp.txt"
subfile_dirpath="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Afforestation\\2015_LeafOn_45123C4404\\sub"
porosity_path="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Afforestation\\2015_LeafOn_45123C4404\\Porosity"

with open(readfile_path,'r') as fread:
    for line in fread:
        info=line.split(" ")
        x=float(info[0])
        y=float(info[1])
        d=sample_index(x,y)
        with open(subfile_dirpath+'\\'+"%d.txt"%d,'a') as fwrite:
            fwrite.write(line)
