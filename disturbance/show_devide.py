import matplotlib.pyplot as plt
import csv

file='G:\\中美华盛顿科考\\扰动图像\\大兴安岭小兴安岭\\daxinganling_datafeatures.csv'
with open(file,'r') as fr:
    csvreader=csv.reader(fr)
    y=[]
    i=0
    for line in csvreader:
        if i>0:
            y.append(float(line[2]))
        i+=1
    x=[index for index in range(0,len(y))]
    plt.scatter(x,y)
    plt.show()