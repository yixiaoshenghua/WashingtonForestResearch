import os
import csv

dir="G:\\中美华盛顿科考\\扰动图像\\Washington\\NBR CSV"
fileList=os.listdir(dir)
for file in fileList:
    with open(dir+"\\"+file, "r") as tmpfile:
        tmpreader = csv.reader(tmpfile)

        YearList = []
        FittedList = []
        i = 0
        for item in tmpreader:
            if i > 0:
                YearList.append(int(item[0][0] + item[0][2:5]))
                FittedList.append(float(item[2]))
            i += 1

        DifferList=[]
        for i in range(len(FittedList)-1):
            differ=FittedList[i]-FittedList[i+1]
            DifferList.append(differ)

        