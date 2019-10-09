import os
import re
import math
import csv

with open("G:\\中美华盛顿科考\\扰动图像\\Washington\\Washington_DecisionTree_PreData.csv", "a+", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Lontitude","Latitude","StartYear",
                    "disturb_duration","recovery_duration","Disturbance_Depth",
                    "Disturbance"])

dir="G:\\中美华盛顿科考\\扰动图像\\Washington\\NBR CSV"
fileList=os.listdir(dir)
for file in fileList:
    lon=re.findall(r"([-]\d{3}[.]\d{2}[W])",file)[0]
    lat=re.findall(r"(\d{2}[.]\d{2}[N])",file)[0]

    with open(dir+"\\"+file, "r") as tmpfile:
        tmpreader = csv.reader(tmpfile)

        AreaCondition = {
            "disturb_depth": 0,
            "disturb_duration": 0,
            "recovery_duration":0,
            "startYear": 0,
            "endYear":0,
            "Disturbance":0
        }

        """
        "Fire": 1,
        "Deforestation": 2,
        "Insect": 3,
        "Afforestation": 4,
        """

        YearList = []
        OriginalList = []
        FittedList = []
        i = 0
        for item in tmpreader:
            if i > 0:
                YearList.append(int(item[0][0] + item[0][2:5]))
                OriginalList.append(float(item[1]))
                FittedList.append(float(item[2]))
            i += 1

        DifferList=[]
        for i in range(len(FittedList)-1):
            differ=FittedList[i]-FittedList[i+1]
            DifferList.append(differ)

        #以落差表示干扰
        #30年NBR极差小于20视为无干扰
        if max(FittedList)-min(FittedList)<=20:
            AreaCondition["Disturbance"]=0
        elif max(FittedList)-min(FittedList)>20:
            for i in range(len(YearList)-1):
                if DifferList[i]>50:
                    #相邻两年落差大于50，初步判断可能是砍伐或者火烧
                    AreaCondition["Disturbance"]=1
                    AreaCondition["startYear"]=YearList[0]+i
                    Original_Value=FittedList[i]
                    break
            if AreaCondition["Disturbance"]==1:
                for i in range(AreaCondition["startYear"]-YearList[0]+1,len(YearList)-1):
                    if -DifferList[i]>0:
                        AreaCondition["endYear"]=YearList[0]+i
                        AreaCondition["disturb_duration"]=AreaCondition["endYear"]-AreaCondition["startYear"]
                        break
                for i in range(AreaCondition["endYear"]-YearList[0]+1,len(YearList)-1):
                    if FittedList[i]>Original_Value:
                        AreaCondition["recovery_duration"]=YearList[0]+i-AreaCondition["endYear"]
                        break
                #一直未完全恢复
                if AreaCondition["recovery_duration"]==0:
                    AreaCondition["recovery_duration"]=YearList[-1]-AreaCondition["endYear"]
                AreaCondition["disturb_depth"]=FittedList[AreaCondition["startYear"]-YearList[0]]-FittedList[AreaCondition["endYear"]-YearList[0]]
                #恢复时间过长大于10年，认为是砍伐
                if AreaCondition["recovery_duration"]>10:
                    AreaCondition["Disturbance"]=2
            #如果整个过程较为平稳，没有突变，则可能是虫害或者植树造林
            elif AreaCondition["Disturbance"]!=1:
                disturb_year=0
                recover_year=0
                for i in range(len(YearList)-1):
                    #每年差值大于5，认为可能出现虫害
                    if DifferList[i]>5:
                        disturb_year+=1
                    else:
                        break
                    if disturb_year==1:
                        AreaCondition["startYear"]=YearList[0]+i
                #如果虫害年份大于5，认为确定是虫害
                if disturb_year>=5:
                    AreaCondition["Disturbance"]=3
                    # for i in range(AreaCondition["startYear"]+disturb_year-YearList[0],len(YearList)-1):
                    #     if DifferList[i]<0:
                    #         recover_year+=1
                else:
                    disturb_year=0
                    for i in range(len(YearList)-1):
                        #每年增值大于5，认为可能是植树造林导致
                        if -DifferList[i]>5:
                            disturb_year+=1
                        else:
                            break
                        if disturb_year==1:
                            AreaCondition["startYear"]=YearList[0]+i
                #如果增值年份大于5，认为是植树造林导致
                if disturb_year>5:
                    AreaCondition["Disturbance"]=4

        

        # #以倾角检测干扰
        # minFitted = min(FittedList)
        # alphaList = []
        # disturbanceYearList = []
        # for year in YearList:
        #     slope = (FittedList[year+1-YearList[0]] - FittedList[year-YearList[0]]) / 1000
        #     if slope > 0:
        #         cos = 1 / math.sqrt(slope ** 2 + 1)
        #     else:
        #         cos = -1 / math.sqrt(slope ** 2 + 1)
        #     alpha = math.degrees(math.acos(cos))
        #     alphaList.append(alpha)
        # print(alphaList)

        # # 检测干扰起始年份
        # startYear_Value=0
        # for i in range(0, len(alphaList) - 1):
        #     if alphaList[i + 1] - alphaList[i] > 1:
        #         AreaCondition["startYear"] = YearList[0] + i+1
        #         AreaCondition["disturb_Depth"] = math.fabs(FittedList[i+1] - minFitted)
        #         startYear_Value=FittedList[i+1]
        #         break
        # for i in range(AreaCondition["startYear"]-YearList[0]+1,len(alphaList)-1):
        #     if FittedList[i] > startYear_Value:
        #         AreaCondition["disturb_duration"]=YearList[0]+i-AreaCondition["startYear"]
        #         break


        if AreaCondition["Disturbance"]==0:
            AreaCondition["startYear"]=0
            AreaCondition["disturb_duration"]=0
            AreaCondition["recovery_duration"]=0
            AreaCondition["disturb_depth"]=0
    
        with open("G:\\中美华盛顿科考\\扰动图像\\Washington\\Washington_DecisionTree_PreData.csv","a+",newline="") as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow([lon,lat,AreaCondition["startYear"],AreaCondition["disturb_duration"]
                            ,AreaCondition["recovery_duration"],AreaCondition["disturb_depth"],AreaCondition["Disturbance"]])



