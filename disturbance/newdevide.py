import csv
import os
import re

#文件组织
# CHN_csv_dirpath\\
#     CHN_CSV_SUBPATH\\
#         46.778N 123.226E.csv
#         ...
#     output_csv
#     newdirpath\\

#中美csv文件夹
CHN_csv_dirpath=''
USA_csv_dirpath=''
CHN_CSV_SUBPATH=CHN_csv_dirpath+'\\NBR CSV'
USA_CSV_SUBPATH=USA_csv_dirpath+'\\NBR CSV'
#执行命令,读取csv
command=0
if command==0:
    csv_dirpath=CHN_csv_dirpath
    csv_path=CHN_CSV_SUBPATH
    files=os.listdir(csv_path)
    output_csv=CHN_csv_dirpath+'\\CHN_result.csv'
else:
    csv_dirpath=USA_csv_dirpath
    csv_path=USA_CSV_SUBPATH
    files=os.listdir(csv_path)
    output_csv=USA_csv_dirpath+'\\USA_result.csv'
#分类文件
newdirpath=csv_dirpath+'\\dividedCSV'
Afforestation_path=newdirpath+"\\Afforestation"
Deforestation_path=newdirpath+"\\Deforestation"
Fire_path=newdirpath+"\\Fire"
Insect_path=newdirpath+"\\Insect"
None_path=newdirpath+"\\None"
with open(output_csv,'a',newline='') as result_file:
    result_file_writer=csv.writer(result_file)
    for file in files:
        with open(csv_dirpath+'\\'+file,'r') as csvfile:
            csvfile_reader=csv.reader(csvfile)
            #构建参数字典
            AreaCondition = {
                        "disturb_depth": 0,
                        "disturb_duration": 0,
                        "recovery_duration":0,
                        "startYear": 0,
                        "endYear":0,
                        "Disturbance":"None",
                        "depth/disturb_duration":0,
                        "depth*disturb_duration":0,
                        "depth/recovery_duration":0,
                        "depth*recovery_duration":0,
                        "depth/totalYear":0,
                        "depth*totalYear":0
                    }
            #确定经纬度
            if command==0:
                longtitude=re.findall(r'[ ][1][^E]*',file)[0][1:]
            else:
                longtitude=re.findall(r'[ ][1][^W]*',file)[0][1:]
            latitude=re.findall(r'[^N]*',file)[0]
            #提取年份和NBR信息
            Year = []
            Fitted = []
            i = 0
            for item in csvfile_reader:
                if i > 0:
                    Year.append(int(item[0]))
                    Fitted.append(float(item[2]))
                i += 1
            
            #开始分类
            

            
            #扩充参数
            if AreaCondition["disturb_duration"]==0:
                AreaCondition["depth/disturb_duration"]=0
            else:
                AreaCondition["depth/disturb_duration"]=AreaCondition["disturb_depth"]/AreaCondition["disturb_duration"]
            if AreaCondition["recovery_duration"]==0:
                AreaCondition["depth/recovery_duration"]=0
            else:
                AreaCondition["depth/recovery_duration"]=AreaCondition["disturb_depth"]/AreaCondition["recovery_duration"]
            if AreaCondition["disturb_duration"]+AreaCondition["recovery_duration"]==0:
                AreaCondition["depth/totalYear"]=0
            else:
                AreaCondition["depth/totalYear"]=AreaCondition["disturb_depth"]/(AreaCondition["disturb_duration"]+AreaCondition["recovery_duration"])
            AreaCondition["depth*disturb_duration"]=AreaCondition["disturb_depth"]*AreaCondition["disturb_duration"]
            AreaCondition["depth*recovery_duration"]=AreaCondition["disturb_depth"]*AreaCondition["recovery_duration"]
            AreaCondition["depth*totalYear"]=AreaCondition["disturb_depth"]*(AreaCondition["disturb_duration"]+AreaCondition["recovery_duration"])

            if AreaCondition["Disturbance"]=="None":
                AreaCondition["startYear"]=0
                AreaCondition["disturb_duration"]=0
                AreaCondition["recovery_duration"]=0
                AreaCondition["disturb_depth"]=0
                AreaCondition["depth/disturb_duration"]=0
                AreaCondition["depth*disturb_duration"]=0
                AreaCondition["depth/recovery_duration"]=0
                AreaCondition["depth*recovery_duration"]=0
                AreaCondition["depth/totalYear"]=0
                AreaCondition["depth*totalYear"]=0
            

            #写入resultcsv中
            result_file_writer.writerow([longtitude,latitude])

            #将csv重新分类
            old_filepath=csv_dirpath+'\\'+file
            if AreaCondition["Disturbance"]=="Insect":
                new_filepath=Insect_path+'\\'+file
            elif AreaCondition["Disturbance"]=='Afforestation':
                new_filepath=Afforestation_path+'\\'+file
            elif AreaCondition["Disturbance"]=='Deforestation':
                new_filepath=Deforestation_path+'\\'+file
            elif AreaCondition["Disturbance"]=='Fire':
                new_filepath=Fire_path+'\\'+file
            else:
                new_filepath=None_path+'\\'+file
            os.rename(old_filepath,new_filepath)
