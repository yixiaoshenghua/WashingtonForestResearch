# --- coding utf-8 ---

ori_min_x=569652.36
ori_max_x=569652.36
ori_min_y=1311311.78
ori_max_y=1311311.78
mean_x=(ori_min_x+ori_max_x)/2
mean_y=(ori_min_y+ori_max_y)/2


#打开txt
openfile="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Afforestation\\2015_LeafOn_45123C4404\\off_ground_points_xyzadp.txt"
writefile="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Afforestation\\2015_LeafOn_45123C4404\\normal_off_ground_points_xyzadp.txt"
with open(openfile,"r") as fr,open(writefile,"w") as fw:
    for line in fr:
        info=(line.split(" "))
        x=float(info[0])
        x-=mean_x
        y=float(info[1])
        y-=mean_y
        info[0]=str(x)
        info[1]=str(y)
        newline=info[0]+' '+info[1]+' '+info[2]+' '+info[3]+' '+info[4]+' '+info[5]
        fw.write(newline) 


