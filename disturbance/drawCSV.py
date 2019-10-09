import os
import re
import matplotlib.pyplot as plt
import math

#文件组织
# CHN_csv_dirpath\\
#     CHN_CSV_SUBPATH\\
#         46.778N 123.226E.csv
#         ...
#     output_csv
#     newdirpath\\
#     imagesDirpath\\

#中美csv文件夹
CHN_csv_dirpath='G:\\中美华盛顿科考\\扰动图像\\大兴安岭小兴安岭'
USA_csv_dirpath='G:\\中美华盛顿科考\\扰动图像\\Washington'
CHN_CSV_SUBPATH=CHN_csv_dirpath+'\\NBR CSV'
USA_CSV_SUBPATH=USA_csv_dirpath+'\\NBR CSV'
#执行命令,读取csv
command=0
if command==0:
    csv_dirpath=CHN_csv_dirpath
    csv_path=CHN_CSV_SUBPATH
    files=os.listdir(csv_path)
    output_csv=CHN_csv_dirpath+'\\CHN_result.csv'
    newdirpath=CHN_csv_dirpath+'\\PROCESSED CSV'
    imagesDirpath=CHN_csv_dirpath+'\\NBR Curves'
else:
    csv_dirpath=USA_csv_dirpath
    csv_path=USA_CSV_SUBPATH
    files=os.listdir(csv_path)
    output_csv=USA_csv_dirpath+'\\USA_result.csv'
    newdirpath=USA_csv_dirpath+'\\PROCESSED CSV'
    imagesDirpath=USA_csv_dirpath+'\\NBR Curves'

files=os.listdir(csv_path)

number=0
bad=0
perfect=0
for csvfile in files:
    with open(csv_path+"\\"+csvfile,'r') as fr:
        Year=[]
        OriginaL=[]
        Fitted=[]
        differ=[]
        i=0
        for _line in fr:
            if i>0:
                line=_line.split(',')
                Year.append(int(line[0]))
                OriginaL.append(float(line[1]))
                Fitted.append(float(line[2]))
                differ.append(float(line[2])-float(line[1]))
            i+=1
        square=[difference**2 for difference in differ]
        RMSE=math.sqrt(sum(square)/len(Year))
        
        if RMSE>50:
            label='Bad'
            bad+=1
        else:
            label='Perfect'
            perfect+=1
        
        #确定经纬度
        if command==0:
            longtitude=float(re.findall(r'[ ][1][^E]*',csvfile)[0][1:])
        else:
            longtitude=float(re.findall(r'[ ][1][^W]*',csvfile)[0][1:])
        latitude=float(re.findall(r'[^N]*',csvfile)[0])
        plt.xlabel('Year')
        plt.ylabel('Index:NBR')
        plt.xlim(min(Year),max(Year))
        plt.ylim(-1000,1000)
        plt.title('RMSE:%.2f   '%RMSE+label)
        plt.plot(Year,Fitted,color='red',label='Fitted')
        plt.plot(Year,OriginaL,color='blue',label='OriginaL')
        plt.legend()
        plt.savefig(imagesDirpath+'\\NBR %.3fN %.3fW.png'%(latitude,longtitude))
        plt.close()
        number+=1
        print("Drawing %d figure"%number)
ratio=perfect/(bad+perfect)
print("The percent of perfect is %.2f"%ratio)