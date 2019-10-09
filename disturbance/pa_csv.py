import re
import csv

dirpath='G:\\中美华盛顿科考\\算法\\csv1\\'
txtpath="G:\\中美华盛顿科考\\算法\\1.txt"
with open(txtpath,"r") as fr:
    for line in fr:
        info=line.split('<hr class="divider">')
    length=len(info)
    i=0
    while i<length:
        lonlat=re.findall(r'([>][A][^<]*)',info[i])
        long=lonlat[0].split(',')[0]
        lat=lonlat[0].split(',')[1]
        with open(dirpath+str(round(float(lat),3))+'N '+str(round(float(long[3:]),3))+'E.csv','w',newline='') as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(['x','y-original','y-fitted'])
            for index in range(2,33):
                line=re.findall(r'(\d+[^<]*)',info[i+index])
                a=line[0].split(',')[0]
                b=str(round(float(line[0].split(',')[1]),2))
                c=str(round(float(line[0].split(',')[2]),2))
                writer.writerow([a,b,c])
        i+=33
