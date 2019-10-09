
ori_min_x=566342.91
ori_max_x=569653.25
ori_min_y=1307077.23
ori_max_y=1311483.73
mean_x=(ori_min_x+ori_max_x)/2
mean_y=(ori_min_y+ori_max_y)/2

filepath="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Afforestation\\2015_LeafOn_45123C4404\\Porosity.txt"
_filePath="G:\\中美华盛顿科考\\激光雷达\\Data\\Panther Creek\\dataprocess\\Afforestation\\2015_LeafOn_45123C4404\\_Porosity.txt"
# porosity_filepath=porosity_dirpath+'\\'+'Porosity.txt'
# new_porosity_filePath=porosity_dirpath+'\\'+'_Porosity.txt'
# with open(porosity_filepath,'r') as fr,open(new_porosity_filePath,"w") as fw:
#     for line in fr:
#         x=float(line.split(' ')[0])
#         y=float(line.split(' ')[1])
#         x+=mean_x
#         y+=mean_y
#         newline=str(x)+' '+str(y)+' '+line.split(' ')[2]
#         fw.write(newline)
with open(filepath,'r') as fr,open(_filePath,"w") as fw:
    for line in fr:
        x=round(float(line.split(' ')[0]),2)
        y=round(float(line.split(' ')[1]),2)
        x+=mean_x
        y+=mean_y
        newline=str(x)+' '+str(y)+' '+line.split(' ')[2]
        fw.write(newline)
        