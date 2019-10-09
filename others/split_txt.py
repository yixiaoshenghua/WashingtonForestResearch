import os
 
def mkSubFile(lines,head,srcName,sub,subdir):
    [des_filename, extname] = os.path.splitext(srcName)
    filename  = subdir +str(sub) + extname
    print( 'make file: %s' %filename)
    fout = open(filename,'w')
    try:
        fout.writelines([head])
        fout.writelines(lines)
        return sub + 1
    finally:
        fout.close()
 

def splitByLineCount(subdir,filename,count):
    fin = open(filename,'r')
    try:
        head = fin.readline()
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mkSubFile(buf,head,filename,sub,subdir)
                buf = []
        if len(buf) != 0:
            sub = mkSubFile(buf,head,filename,sub,subdir)   
    finally:
        fin.close()
 

if __name__ == '__main__':
    subdir='G:\\中美华盛顿科考\\激光雷达\\Data\\AMIGACarb_G03_Aug2012_l1s1.las\\sub\\'
    filename="G:\\中美华盛顿科考\\激光雷达\\Data\\AMIGACarb_G03_Aug2012_l1s1.las\\new_AMIGACarb_G03_Aug2012_l1s1.txt"
    splitByLineCount(subdir,filename,100000)
    
    

        
            


        

