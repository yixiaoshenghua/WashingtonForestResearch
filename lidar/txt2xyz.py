filepath="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Afforestation\\2010_LeafOn_PC_090\\off-ground points.txt"
medium="\\Afforestation\\2010_LeafOn_PC_090"


outputdir="D:\\Panther Creek\\data2TreeHeight"
outputheaderpath=outputdir+medium+"\\off_ground_points_xyz_header.txt"
outputfilepath=outputdir+medium+"\\normal_off_ground_points_xyz.txt"

with open(filepath,'r') as fr:
    for line in fr:
        info=line.split(' ')
        x_max=float(info[0])
        x_min=float(info[0])
        y_max=float(info[1])
        y_min=float(info[1])
        break
    for line in fr:
        info=line.split(' ')
        x=float(info[0])
        y=float(info[1])
        if x>x_max:
            x_max=x
        if x<x_min:
            x_min=x
        if y>y_max:
            y_max=y
        if y<y_min:
            y_min=y

    with open(outputheaderpath,'w') as fw:
        fw.write('ori_min_x=%.2f\nori_max_x=%.2f\nori_min_y=%.2f\nori_max_y=%.2f\nmean_x=(ori_min_x+ori_max_x)/2\nmean_y=(ori_min_y+ori_max_y)/2'%(x_min,x_max,y_min,y_max))

with open(filepath,'r') as fr,open(outputfilepath,'w') as fw:
    for line in fr:
        data=line.split(' ')
        x=float(data[0])-x_min
        y=float(data[1])-y_min
        newline=str(x)+' '+str(y)+' '+data[2]+'\n'
        fw.write(newline)