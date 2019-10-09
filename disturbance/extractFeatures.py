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
CHN_csv_dirpath='G:\\中美华盛顿科考\\扰动图像\\大兴安岭小兴安岭'
USA_csv_dirpath=''
CHN_CSV_SUBPATH=CHN_csv_dirpath+'\\NBR CSV'
USA_CSV_SUBPATH=USA_csv_dirpath+'\\NBR CSV'
#执行命令,读取csv
command=0
if command==0:
    csv_dirpath=CHN_csv_dirpath
    csv_path=CHN_CSV_SUBPATH
    files=os.listdir(csv_path)
    output_csv=CHN_csv_dirpath+'\\daxinganling_datafeatures.csv'
else:
    csv_dirpath=USA_csv_dirpath
    csv_path=USA_CSV_SUBPATH
    files=os.listdir(csv_path)
    output_csv=USA_csv_dirpath+'\\USA_result.csv'

with open(output_csv,'a',newline='') as result_file:
    result_file_writer=csv.writer(result_file)
    for file in files:
        with open(csv_path+'\\'+file,'r') as csvfile:
            csvfile_reader=csv.reader(csvfile)
            #构建参数字典
            Parameters = {
                        'differ_area':0
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
            #提取参数
            #提取差异面积
            predictArea=(Fitted[0]+Fitted[-1])*(Year[-1]-Year[0])/2
            trueArea=sum(Fitted)-(Fitted[0]+Fitted[-1])/2
            Parameters['differ_area']=predictArea-trueArea
            if Parameters['differ_area']<1e-6:
                Parameters['differ_area']=0
            

            

            #写入resultcsv中
            result_file_writer.writerow([longtitude,latitude,Parameters['differ_area']])

            
