with open("G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Afforestation\\2015_LeafOn_45123C4404\\off-ground points.txt",'r') as fr,open("G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Afforestation\\2015_LeafOn_45123C4404\\off_ground_points_xyzadp.txt",'w') as fw:
    i=0
    for line in fr:
        if i>1:
            data=line.split(' ')
            newline=data[0]+' '+data[1]+' '+data[2]+' '+data[10]+' '+data[8]+' '+data[12]
            fw.write(newline)
        i+=1