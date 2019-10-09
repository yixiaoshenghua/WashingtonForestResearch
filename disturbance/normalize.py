import os
import re
import csv

oldpath='G:\\中美华盛顿科考\\扰动图像\\Washington\\NBR CSV'
newpath='G:\\中美华盛顿科考\\扰动图像\\Washington\\csv'
files=os.listdir(oldpath)
for file in files:
    with open(oldpath+'\\'+file,'r') as fr:
        csvreader=csv.reader(fr)
        newname=file[:5]+'0'+file[5:13]+'0'+file[13:]
        newline=[]
        for i,line in enumerate(csvreader):
            if i==0:
                newline.append(['x','y-original','y-fitted'])
            if i>0:
                year=line[0][0]+line[0][2:]
                newline.append([year,str(round(float(line[1]),3)),str(round(float(line[2]),3))])

        with open(newpath+'\\'+newname,'w',newline='') as fw:
            csvwriter=csv.writer(fw)
            csvwriter.writerows(newline)

