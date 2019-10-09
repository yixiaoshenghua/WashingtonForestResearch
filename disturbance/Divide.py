import os
import re
import math
import csv

with open("G:\\中美华盛顿科考\\扰动图像\\大兴安岭小兴安岭\\大兴安岭\\daxinganling_Disturbance_.csv", "a+", newline="") as csvfile:
    writer = csv.writer(csvfile)
    title = ["Lontitude","Latitude","StartYear",
                    "disturb_duration","recovery_duration","Disturbance_Depth",
                    "depth/disturb_year","depth*disturb_year","depth/recovery_year",
                    "depth*recovery_year","depth/totalYear","depth*totalYear","Disturbance"]
    writer.writerow(title)




        
dir="G:\\中美华盛顿科考\\算法\\CSV1"
devide_result='G:\\中美华盛顿科考\\扰动图像\\大兴安岭小兴安岭\\大兴安岭\\result'
Afforestation_path=dir+"\\Afforestation"
Deforestation_path=dir+"\\Deforestation"
Fire_path=dir+"\\Fire"
Insect_path=dir+"\\Insect"
fileList=os.listdir(dir)
for file in fileList:
    lon=re.findall(r"([ ][1][^E]*)",file)[0]
    lat=re.findall(r"([^N]*)",file)[0]
    with open(dir+"\\"+file, "r") as tmpfile:
        tmpreader = csv.reader(tmpfile)

        AreaCondition = {
            "disturb_depth": 0,
            "disturb_duration": 0,
            "recovery_duration":0,
            "startYear": 0,
            "endYear":0,
            "Disturbance":"None",
            "depth/disturb_year":0,
            "depth*disturb_year":0,
            "depth/recovery_year":0,
            "depth*recovery_year":0,
            "depth/totalYear":0,
            "depth*totalYear":0
        }

        """
        "Fire": 1,
        "Deforestation": 2,
        "Insect": 3,
        "Afforestation": 4,
        """

        YearList = []
        FittedList = []
        i = 0
        for item in tmpreader:
            if i > 0:
                YearList.append(int(item[0]))
                FittedList.append(float(item[2]))
            i += 1

        DifferList=[]
        in_de_creaseList=[]
        for i in range(len(FittedList)-1):
            differ=FittedList[i]-FittedList[i+1]
            DifferList.append(differ)
            if differ>0:
                in_de_crease=1
            elif differ==0:
                in_de_crease=0
            else:
                in_de_crease=-1
            in_de_creaseList.append(in_de_crease)



        #以落差表示干扰
        #30年NBR极差小于20视为无干扰
        if max(FittedList)-min(FittedList)<=20:
            AreaCondition["Disturbance"]="None"
        #相邻两年落差大于150，初步判断可能是砍伐或者火烧
        elif math.fabs(max(DifferList))>150:
            for i in range(len(YearList)-1):
                if DifferList[i]>150:
                    
                    AreaCondition["Disturbance"]="Fire"
                    AreaCondition["startYear"]=YearList[0]+i
                    Original_Value=FittedList[i]
                    break
            if AreaCondition["Disturbance"]=="Fire":
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
                    AreaCondition["Disturbance"]="Deforestation"
        #没有短时期较大变化，判断可能为虫害或者植树造林
        else:
            judge=0
            year=0
            for differ in DifferList:#连续下降超过五年
                if year==5:
                    judge=1
                    break
                if differ>10:
                    year+=1
                    continue
                else:
                    year=0
                    continue
            if judge==1:
                AreaCondition["Disturbance"]="Insect"
                disturb_year=0
                for index,differ in enumerate(DifferList,1):
                    if differ>10:
                        disturb_year+=1
                    elif differ<=10 and disturb_year<5:
                        disturb_year=0
                        continue
                    elif differ<=10 and disturb_year>=5:
                        AreaCondition["endYear"]=YearList[0]+index+1
                        AreaCondition["startYear"]=AreaCondition["endYear"]-disturb_year
                        Original_Value=FittedList[index+1-disturb_year]
                        AreaCondition["disturb_depth"]=FittedList[index+1]-FittedList[index+1-disturb_year]
                        AreaCondition["disturb_duration"]=disturb_year
                        break
                for i in range(AreaCondition["endYear"]-YearList[0]+1,len(YearList)-1):
                    if FittedList[i]>Original_Value:
                        AreaCondition["recovery_duration"]=YearList[0]+i-AreaCondition["endYear"]
                        break
                #一直未完全恢复
                if AreaCondition["recovery_duration"]==0:
                    AreaCondition["recovery_duration"]=YearList[-1]-AreaCondition["endYear"]
            else:
                k=(FittedList[-1]-FittedList[0])/(YearList[-1]-YearList[0])
                if k>0:
                    if FittedList[-1]-FittedList[0]>200:
                        SumList=[0]
                        for differ in DifferList:
                            SumList.append(SumList[-1]+differ)
                        increase_year=0
                        for i in range(len(SumList)-1):
                            if SumList[i+1]-SumList[i]>50:
                                increase_year+=1
                            else:
                                AreaCondition['Disturbance']='Afforestation'
                                AreaCondition["disturb_duration"]=increase_year
                                AreaCondition["endYear"]=YearList[0]+i+1
                                AreaCondition['startYear']=AreaCondition['endYear']-AreaCondition['disturb_duration']
                                AreaCondition['disturb_depth']=FittedList[AreaCondition['endYear']-YearList[0]]-FittedList[AreaCondition['startYear']-YearList[0]]
                                break
                            
        #扩充指数，构建决策树
        if AreaCondition["disturb_duration"]==0:
            AreaCondition["depth/disturb_year"]=0
        else:
            AreaCondition["depth/disturb_year"]=AreaCondition["disturb_depth"]/AreaCondition["disturb_duration"]
        if AreaCondition["recovery_duration"]==0:
            AreaCondition["depth/recovery_year"]=0
        else:
            AreaCondition["depth/recovery_year"]=AreaCondition["disturb_depth"]/AreaCondition["recovery_duration"]
        if AreaCondition["disturb_duration"]+AreaCondition["recovery_duration"]==0:
            AreaCondition["depth/totalYear"]=0
        else:
            AreaCondition["depth/totalYear"]=AreaCondition["disturb_depth"]/(AreaCondition["disturb_duration"]+AreaCondition["recovery_duration"])
        AreaCondition["depth*disturb_year"]=AreaCondition["disturb_depth"]*AreaCondition["disturb_duration"]
        AreaCondition["depth*recovery_year"]=AreaCondition["disturb_depth"]*AreaCondition["recovery_duration"]
        AreaCondition["depth*totalYear"]=AreaCondition["disturb_depth"]*(AreaCondition["disturb_duration"]+AreaCondition["recovery_duration"])

        if AreaCondition["Disturbance"]=="None":
            AreaCondition["startYear"]=0
            AreaCondition["disturb_duration"]=0
            AreaCondition["recovery_duration"]=0
            AreaCondition["disturb_depth"]=0
            AreaCondition["depth/disturb_year"]=0
            AreaCondition["depth*disturb_year"]=0
            AreaCondition["depth/recovery_year"]=0
            AreaCondition["depth*recovery_year"]=0
            AreaCondition["depth/totalYear"]=0
            AreaCondition["depth*totalYear"]=0

    
        with open("G:\\中美华盛顿科考\\扰动图像\\大兴安岭小兴安岭\\大兴安岭\\daxinganling_Disturbance.csv","a+",newline="") as csvfile:
            writer=csv.writer(csvfile)
            detail=[lon,lat,AreaCondition["startYear"],AreaCondition["disturb_duration"],
                            AreaCondition["recovery_duration"],AreaCondition["disturb_depth"],
                            AreaCondition["depth/disturb_year"],AreaCondition["depth*disturb_year"],
                            AreaCondition["depth/recovery_year"],AreaCondition["depth*recovery_year"],
                            AreaCondition["depth/totalYear"],AreaCondition["depth*totalYear"],
                            AreaCondition["Disturbance"]]
            writer.writerow(detail)



