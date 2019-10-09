import os


ori_min_x=470419.85
ori_max_x=470919.85
ori_min_y=5013860.28
ori_max_y=5014360.27
mean_x=(ori_min_x+ori_max_x)/2
mean_y=(ori_min_y+ori_max_y)/2

min_x=ori_min_x-mean_x
max_x=ori_max_x-mean_x
min_y=ori_min_y-mean_y
max_y=ori_max_y-mean_y
sample_size=30
Nx=(max_x-min_x)//sample_size+1
Ny=(max_y-min_y)//sample_size+1

#获取样方边界阈值
def get_sample_xy(d):
    judge_x=d%Nx
    judge_y=d//Nx+1
    sample_x_min= min_x+(judge_x-1)*sample_size
    sample_x_max= sample_x_min+sample_size
    sample_y_min= min_y+(judge_y-1)*sample_size
    sample_y_max= sample_y_min+sample_size
    return sample_x_min,sample_x_max,sample_y_min,sample_y_max

#返回非空隙网格序号,网格大小3/10=0.3
def is_full(x,y):
    raster_size=3
    _x=(x-sample_x_min)*10//raster_size+1
    _y=(y-sample_y_min)*10//raster_size+1
    d=100*(_y-1)+_x
    return d


dirpath="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Insect\\2010_LeafOn_PC_013\\Porosity"
Porosity_path="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Insect\\2010_LeafOn_PC_013\\Porosity.txt"
files = os.listdir(dirpath)
with open(Porosity_path,'w') as fw:
    for file in files:
        n=int(file.split('.')[0])
        sample_x_min,sample_x_max,sample_y_min,sample_y_max=get_sample_xy(n)
        center_x=(sample_x_min+sample_x_max)/2
        center_y=(sample_y_min+sample_y_max)/2
        with open(dirpath+'\\'+file,'r') as fr:
            raster=[0 for i in range(1,10001)]
            for line in fr:
                x=float(line.split(' ')[0])
                y=float(line.split(' ')[1])
                full_index=int(is_full(x,y))
                
                if raster[full_index] is 0:
                    raster[full_index]=1
            empty_num=10000-sum(raster)
            empty_ratio=empty_num/10000
            newline=str(center_x)+' '+str(center_y)+' '+str(empty_ratio)+'\n'
            fw.write(newline)
                    