#-*-coding:utf-8-*-
import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
 
def readXYZfile(filename, Separator):
  data = [[], [], []]
  f = open(filename,'r') 
  line = f.readline() 
  num = 0
  while line:  #按行读入点云
     c,d,e = line.split(Separator)
     data[0].append(c)  #X坐标
     data[1].append(d)  #Y坐标
     data[2].append(e)  #Z坐标
     num = num + 1
     line = f.readline()
  f.close() 
 
  #string型转float型 
  x = [ float(data[0] ) for data[0] in data[0] ] 
  y = [ float(data[1] ) for data[1] in data[1] ] 
  z = [ float(data[2] ) for data[2] in data[2] ]
  print("读入点的个数为:{}个。".format(num))
  point = [x,y,z]
  return point
 
#三维离散点图显示点云
def displayPoint(data,title):
    #解决中文显示问题
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
 
    #点数量太多不予显示
    while len(data[0]) > 20000000:
    	print("点太多了！")
    	exit()
 
    #散点图参数设置
    fig=plt.figure() 
    ax=Axes3D(fig) 
    ax.set_title(title) 
    ax.scatter3D(data[0], data[1],data[2], c = 'g', marker = '.') 
    ax.set_xlabel('x') 
    ax.set_ylabel('y') 
    ax.set_zlabel('z') 
    plt.show()
 
        


if __name__ == "__main__":
	data = readXYZfile("E:\\WA_GLIHT\\AMIGACarb_G03_Aug2012\\lidar\\las\\AMIGACarb_G03_Aug2012_l0s2.las\\1000000.txt",' ')
	displayPoint(data, "shu")