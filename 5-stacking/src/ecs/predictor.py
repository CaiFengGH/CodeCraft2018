# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 09:16:18 2018

@author: Song
"""

# coding=utf-8
#import os
#import matplotlib.pyplot as plt
from datetime import datetime
#from datetime import timedelta
'''
import pandas as pd
import matplotlib.dates as mdate
from sklearn.linear_model import LinearRegression
import copy
from sklearn import metrics
'''
'''
############################################
#def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    
##########################################
ecsDataPath ="C:\\Users\\\Administrator\\Desktop\\huawei\\data\\data\\geshi.txt"
inputFilePath ="C:\\Users\\\Administrator\\Desktop\\huawei\\data\\data\\data_1512_1601.txt"
#data_1512_1601   data_1501_1505     data_1504_1601


#dataPath="C:\\Users\\chang\\Desktop\\huawei\\练习数据\\初赛文档\\"
#ecsDataPath =dataPath+"练习数据\\data_5_21_5_30.txt"
#inputFilePath =dataPath+"练习数据\\data_2015_1_5_20.txt"






def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print ('file not exist: ' + file_path)
        return None
    
ecs_lines = read_lines(ecsDataPath)
input_lines = read_lines(inputFilePath)

'''

def findSortedPosition(theList, target):
    low = 0
    high = len(theList) - 1
    while low <= high:
        mid = (high + low) // 2
        if theList[mid] == target:
            return mid
        elif target < theList[mid]:
            high = mid -1
        else:
            low = mid + 1
    return low
########################第二版#################
'''
W:重量 非优化项的各个值
V:价格 优化项的各个值
N:数量 各种虚拟机的数量
res:用于记录用了那种，用了多少
n:种类 虚拟机的种类
C:最大重量 非优化项的最大值
P: 优化项的最大值  （尽量是P最大化，但不能超过最大值）
'''
def onceBoxing2(W,V,N,res,n,C,P):
    value = 0
    #temp=[0]*(C+1)
    f=[]
    for i in range(n):
        f.append([0]*(C+1))
    #f=[temp]*n
    
    for y in range(1,C+1):
        count =min(N[0],y//W[0])
        temp=count * V[0]
        if temp>P:
            f[0][y]=f[0][y-1]
        else:
            f[0][y] = 0 if(y < W[0] ) else (temp)
       # print (f[0][y],"",end='')
    for i in range(1,n):
        for y in range(1,C+1):
            if y<W[i]:
                f[i][y] = f[i-1][y]
            else:
                count=min(N[i],y//W[i])
                f[i][y] = f[i-1][y]
                for k in range(1,count+1):
                    temp=f[i-1][y-W[i]*k] + k*V[i]
                    if temp>=f[i][y] and temp<=P:
                        f[i][y]=temp

    value =f[n-1][C]
    j=n-1
    y=C
    while j>0:
        count =min(N[j], y//W[j])
        for k in range(count,0,-1):
            if f[j][y] == (f[j-1][y-W[j]*k]+k*V[j]):
                res[j]=k
                y=y-k*W[j]
                break
        j=j-1
    
    res[0]=f[0][y]//V[0]
    return value

def processOutliers(data,data1,length):
    for name in data:
        #print("---"*20)
        for j in range(7):
            data1[name][j]=data[name][j]
        
        
        for i in range(7,length):
            
         #   ave=round(sum(data[name][i-7:i])/7)   ###前7天的数剧
            ave=round(sum(data[name][i-7:i])/7.0)
           # print(sum(data[name][i-7:i])/7)
            if data[name][i]<10 and data[name][i]>5*ave:
                data1[name][i]=data[name][i]
                continue
            if data[name][i]>4*ave:
                data[name][i]=ave
                data1[name][i]=ave #前7天的均值替换
                continue
            if (data[name][i]<0.5*ave and data[name][i]==0):
                data1[name][i]=ave #前7天的均值替换
                continue
            data1[name][i]=data[name][i]

def processVacation(data,length,allTime):
    vacation=["2015-01-01","2015-01-02","2015-01-03","2015-02-18","2015-02-19","2015-02-20","2015-02-21","2015-02-22","2015-02-23",
              "2015-02-24","2015-04-04","2015-04-05","2015-04-06","2015-05-01","2015-05-02","2015-05-03","2015-06-20","2015-06-21",
              "2015-06-22","2015-08-26","2015-08-27","2015-10-01","2015-10-02","2015-10-03","2015-10-04","2015-10-05","2015-10-06",
              "2015-10-07",
              
              "2015-03-05","2015-03-06","2015-03-07","2015-03-08","2015-03-09","2015-03-10","2015-03-11","2015-03-12","2015-03-13",
              "2015-03-14","2015-03-15",
              
              
              "2016-01-01","2016-01-02","2016-01-03","2016-02-07","2016-02-08","2016-02-09","2016-02-10","2016-02-11","2016-02-12",
              "2016-02-13","2016-04-02","2016-04-03","2016-04-04","2016-04-30","2016-05-01","2016-05-02","2016-06-09","2016-06-10",
              "2016-06-11","2016-09-15","2016-09-16","2016-09-17","2016-10-01","2016-10-02","2016-10-03","2016-10-04","2016-10-05",
              "2016-10-06","2016-10-07","2016-12-31",
              
              "2016-03-03","2016-03-04","2016-03-05","2016-03-06","2016-03-07","2016-03-08","2016-03-09","2016-03-10","2016-03-11",
              "2016-03-12","2016-03-13","2016-03-14",
              
              "2017-01-01","2017-01-02","2017-01-27","2017-01-28","2017-01-29","2017-01-30","2017-01-31","2017-02-01","2017-02-02",
              "2017-04-02","2017-04-03","2017-04-04","2017-04-29","2017-04-30","2017-05-01","2017-05-28","2017-05-29","2017-05-30",
              "2017-10-01","2017-10-02","2017-10-03","2017-10-04","2017-10-05","2017-10-06","2017-10-07","2017-10-08","2017-12-30",
              "2017-12-31",
              
              "2017-03-05","2017-03-06","2017-03-07","2017-03-08","2017-03-09","2017-03-10","2017-03-11","2017-03-12","2017-03-13",
              "2017-03-14","2017-03-15",
              
              "2018-01-01","2018-02-15","2018-02-16","2018-02-17","2018-02-18","2018-02-19","2018-02-20","2018-02-21" 
              ]
    
    for name in data:
        for i in range(length):
            if allTime[i] in vacation:
                if i-7>0:
                    data[name][i]=round(sum(data[name][i-7:i])/7.0) #前7天的均值替换
                    
                    #print(i,data[name][i])
                elif (i-1)>=0:
                    data[name][i]=data[name][i-1]

                   # print(i,data[name][i])

######排除异常点########这里只是线性测试，如果线上的话不一定了 因为节假日不一样了
def dropOutliers(data,days,startTime):
    Outliers=[(datetime.strptime("2015-03-05",'%Y-%m-%d')-startTime).days+i for i in range(11)] #两会
 #   Outliers.expend([(datetime.strptime("2015-01-01")-startTime).days+i for i in range(3)] )  #元旦
    Outliers.extend([(datetime.strptime("2015-02-18",'%Y-%m-%d')-startTime).days+i for i in range(7)] )  #春节
    Outliers.extend([(datetime.strptime("2015-04-04",'%Y-%m-%d')-startTime).days+i for i in range(3)] )  #清明节
    Outliers.extend([(datetime.strptime("2015-05-01",'%Y-%m-%d')-startTime).days+i for i in range(3)] )  #劳动节
    Outliers.extend([(datetime.strptime("2015-06-20",'%Y-%m-%d')-startTime).days+i for i in range(3)] )  #端午节
    Outliers.extend([(datetime.strptime("2015-09-26",'%Y-%m-%d')-startTime).days+i for i in range(2)] )  #中秋节
    Outliers.extend([(datetime.strptime("2015-10-01",'%Y-%m-%d')-startTime).days+i for i in range(7)] )  #国庆节
    Outliers.extend([(datetime.strptime("2016-01-01",'%Y-%m-%d')-startTime).days+i for i in range(3)] )  #元旦
    #print (Outliers)
    for name in data:
        for i in range(len(data[name])):
            if i in Outliers:
                if i-7>0:
                    data[name][i]=sum(data[name][i-7:i])//len(data[name][i-7:i]) #前7天的均值替换
                else:
                    data[name][i]=data[name][i-1:i]
    

##按照days来统计几天作为一次计数
def data_manyDays(data,days):
    leng=len(list(data.values())[0])
    #print(length)
    remainDays=leng%days
    for item in data:
        tempItem=[]
        for i in range(leng//days):
            tempItem.append(sum(data[item][remainDays+i*days:remainDays+(i+1)*days]))
        data[item]=tempItem
    return remainDays

########18-4-4##############################################

#指数平滑公式
def exponential_smoothing(alpha, s):
    s2 = [0]*(len(s))
    s2[0] = s[0]
    for i in range(1, len(s2)):
        s2[i] = alpha*s[i]+(1-alpha)*s2[i-1]
    return s2
'''
#预测曲线
def show_data(new_X, pre_X, s_pre_double):

    plt.figure(figsize=(14, 6), dpi=80)
    plt.plot(new_X[:-3], Y, color='blue', label="actual value")#
    plt.plot(new_X[:len(new_X)-1], s_pre_double[1:],color='red', label="double predicted value")#
	
    plt.legend(loc='lower right')
    plt.title('Projects')
    plt.xlabel('X')
    plt.ylabel('number')
    plt.xticks(new_X)#x刻度线new_X
    plt.show()

'''


def double_exponential_smoothing(X,Y,pre_X):
    alpha = .4#设置平滑系数
    
  #  Y=[1,1, 0, 1, 3, 1, 5, 4, 3, 22, 20, 29, 21, 12, 24, 26, 23]
 #   X=[0,1, 2, 3, 4, 5, 6, 7, 8, 36, 37, 38, 39, 40, 41, 42, 43]
    
 #   Y=[22,22, 20, 29, 21, 12, 24, 26, 23]
 #   X=[35,36, 37, 38, 39, 40, 41, 42, 43]
 #   pre_X =[44, 45]#需要预测
    

    s_single = exponential_smoothing(alpha, Y)#计算一次平滑
    s_double = exponential_smoothing(alpha, s_single)#计算二次平滑
    
    
    a = list(map(lambda x: x[0]-x[1], zip([x*2 for x in s_single], s_double)))
    
    b=[x*(alpha*1.0/(1-alpha)) for x in list(map(lambda y:y[0]-y[1],zip(s_single,s_double)))]
    
    s_pre_double = [0]*len(s_double)#预测
    for i in range(1, len(X)):
        s_pre_double[i] = a[i-1]+b[i-1]#计算二次平滑的预测值
    
    
    predict=[]
    for i in range(1,len(pre_X)+1):
        predict.append(a[-1]+b[-1]*i)
       
    
    ##############三次平滑############
    '''
    s_triple = exponential_smoothing(alpha, s_double)

    #temp1=[list(map(lambda y:y[0]-y[1],zip(s_single,s_double)))]
    temp1=[ x*3 for x in s_single]
    temp2=[ x*3 for x in s_double]
    a_triple =list(map(lambda x: x[0]-x[1]+x[2],zip(temp1,temp2,s_triple)))
    
    
    temp1=[ x*(alpha*1.0/(2*((1-alpha)**2)))*(6-5*alpha) for x in s_single]
    temp2=[ x*(alpha*1.0/(2*((1-alpha)**2)))*(-2)*((5-4*alpha)) for x in s_double]
    temp3=[(alpha*1.0/(2*((1-alpha)**2)))*((4-3*alpha)*x) for x in s_triple ]
    b_triple =list(map(lambda x: x[0]+x[1]+x[2], zip(temp1, temp2,temp3)))
   
    temp1=list (map(lambda x: x[0]-2*x[1]+x[2] ,zip(s_single,s_double,s_triple)))
    c_triple =[((alpha**2)*1.0/(2*((1-alpha)**2)))*x for x in temp1]
    
    s_pre_triple = [0]*len(s_triple)
    
    for i in range(1, len(X)):
        s_pre_triple[i] = a_triple[i-1]+b_triple[i-1]*1 + c_triple[i-1]*(1**2)
 #   print("---",a_triple,b_triple,c_triple)
    
    predict=[]
    for i in range(1,len(pre_X)+1):
        predict.append(a_triple[-1]+b_triple[-1]*i+c_triple[-1]*(i**2))
    ''' 
        

        
        
        
    #print(predict)
    '''
    s_pre_double.extend(predict)#组合预测值
    
    X.extend(pre_X)
    print(X)
    print(Y)
      #  print(s_pre_double)
    #    print(s_pre_triple)
    output = [X, s_pre_double]
    #print(output)
    
    
    from sklearn.metrics import mean_squared_error
    from math import sqrt
    
    train=Y[1:]
    pre=s_pre_double[2:-(len(pre_X)-1)]
    
    RMSE=sqrt(mean_squared_error(train,pre))
    
    print("RMSE:",RMSE)
    
   # show_data(X, pre_X,  s_pre_double)#传入预测值和数据
    #   print("---"*20)
    print(sum(output[1][-(len(pre_X)-1):]))
    
    '''
    return predict[1:]

##################################################################################
def predict_vm(input_lines,ecs_lines):
    #Do your work from here
    ##########################################    
    if ecs_lines is None :
        return []
   
    if ecs_lines is None:
        print ('ecs information is none')
        return []
    if input_lines is None:
        print ('input file information is none')
        return []
    if len(input_lines)<=3 :
        return []
    ###初始化虚拟机规格 
    ###初始化虚拟机规格 
    #VM={'flavor1':[1,1024],'flavor2':[1,2048],'flavor3':0,'flavor4':0,'flavor5':0,'flavor6':0,'flavor7':0,'flavor8':0,'flavor9':0,'flavor10':0,'flavor11':0,'flavor12':0,'flavor13':0,'flavor14':0,'flavor15':0}
    
    vmName_all=['flavor1','flavor2','flavor3','flavor4','flavor5','flavor6','flavor7','flavor8','flavor9','flavor10','flavor11','flavor12','flavor13','flavor14','flavor15']
    vmVCPU_all=[1,1,1,2,2,2,4,4,4,8,8,8,16,16,16]
    #vmMEM_all=[1024,2048,4096,2048,4096,8192,4096,8192,4096,8192,16384,8192,16384,8192,16384,32768,16384,32768,65536]
    vmMEM_all=[1,2,4,2,4,8,4,8,16,8,16,32,16,32,64]
    
    
    #历史数据开始的时间、结束时间、时间间隔(天)
    startTime=datetime.strptime(input_lines[0].split("\t")[2].rstrip()[:10],'%Y-%m-%d')
    endTime=datetime.strptime(input_lines[len(input_lines)-1].split("\t")[2].rstrip()[:10],'%Y-%m-%d')
    timeInterval=(endTime-startTime).days+1
    
    ######################################1读取服务器参数文件
    server = ecs_lines[0].split(" ")
    serverCPU = int(server[0])  #服务器的核数
    serverMEM = int(server[1]) #服务器的内存
    
    vm_num= int(ecs_lines[2].rstrip())  #预测的虚拟机总数
    
    flavorNameAll = {} # 预测的所有虚拟机的名称
    CPUAll=[]          #预测的所有虚拟机的核数
    MEMAll = []        #预测的所有虚拟机的创建时间
    data={}#用于统计每个规格的虚拟机历史每天的个数
    for item in ecs_lines[3:(3+vm_num)]:
        values = item.split(" ")
       
        #flavorNameAll.append(values[0])
        flavorNameAll[values[0]]=0
        data[values[0]]=[0]*(timeInterval)
        CPUAll.append(int(values[1]))
        MEMAll.append(int(values[2].rstrip())/1024.0)
    
    dim =ecs_lines[4+vm_num].rstrip()  #需优化的资源维度
    
    pre_starttime=datetime.strptime(ecs_lines[6+vm_num].rstrip()[:10],'%Y-%m-%d')  #预测开始时间
    pre_endtime= datetime.strptime(ecs_lines[7+vm_num].rstrip()[:10],'%Y-%m-%d')    #预测结束时间
    ###############################################1
    
    ###################################2读取训练数据文件
    VMid=[]      #虚拟机id集合
    VMname=[]    #虚拟机名称集合
    VMtime=[]    #虚拟机创建时间
    
    
    data1={}
    data2={}
        
    for name in data.keys():
        data1[name]=[0]*timeInterval
        data2[name]=[0]*timeInterval
        
        
    #data1=copy.deepcopy(data)
    
    
    
    
  #  preTime=datetime.strptime(input_lines[0].split("\t")[2].rstrip(),'%Y-%m-%d %H:%M:%S')-timedelta(minutes=1)
  #  preName=input_lines[0].split("\t")[1]
    
    
    length=0
    for v in data:
        if length!=0:
            break
        length=len(data[v])
        
    
    
    allTime=[0]*length
    
    f=1
    for item in input_lines:
        values = item.split("\t")
        
        VMid.append(values[0])
        VMname.append(values[1])
        tempTime=datetime.strptime(values[2].rstrip(),'%Y-%m-%d %H:%M:%S')
        VMtime.append(tempTime)
        vacationFlag =values[2].rstrip()[:10]
        #对于某种虚拟机其若是所需预测的虚拟机，其对应的第几天的数量就加一。
        if values[1] in data:
            
            #对于同一个规格的虚拟机，认为其在下一时刻一分钟内还是该虚拟机的记录就不在计数。
            
           # if values[1]!=preName or tempTime>=preTime+timedelta(minutes=1):
           
            if True:
              #  if vacationFlag in vacation:
                allTime    
                temp=data[values[1]]
                interval=(tempTime-startTime).days
                temp[interval]=temp[interval]+1
                
                allTime[interval]=vacationFlag
                data[values[1]]=temp
                f=0
            else:
                temp=data1[values[1]]
                temp2=data2[values[1]]
                interval=(tempTime-startTime).days
                if(temp2[interval]==0):
                    temp[interval]=temp[interval]+1
                    temp2[interval]=1
                    f=1
                temp2[interval]=temp2[interval]+1
                
                if f==0 and temp[interval]!=0:
                    temp[interval]=temp[interval]+1
                f=1
                data1[values[1]]=temp   
                data2[values[1]]=temp2
            
       # preTime=tempTime
        #preName=values[1]
    
    
    
    ################################################2
    
    ##########################3统计最后一个周期中所需预测虚拟机的数量##########################
    '''
    boundary=pre_starttime-(pre_endtime-pre_starttime)
    ##e二分查找boundary的索引
    
    index=findSortedPosition(VMtime, boundary)
    
    for name in VMname[index:]:
        if name in flavorNameAll:
            flavorNameAll[name]=flavorNameAll[name]+1
    '''
    
    
    ################################################2
    
    boundary1=pre_starttime-(pre_endtime-pre_starttime)
    ##e二分查找boundary的索引
    boundary2=pre_starttime-2*(pre_endtime-pre_starttime)
    index1=findSortedPosition(VMtime, boundary1)
    index2=findSortedPosition(VMtime, boundary2)
    
    period2={}
    for name in flavorNameAll:
        period2[name]=[0]*2
    
    
    for name in VMname[index1:]:
        if name in flavorNameAll:
           period2[name][1]=period2[name][1]+1
    
    for name in VMname[index2:index1]:
        if name in flavorNameAll:
            period2[name][0]=period2[name][0]+1
    '''
    for name in flavorNameAll:
        #temp=period2[name][1]+0.2*(period2[name][1]-period2[name][0])
        ab=0.1
        temp=period2[name][1]*(1-0)+ab*period2[name][1]
        if temp<0:
            temp=0
        flavorNameAll[name]=int(round(temp))
    '''
    
    
    ################################################2
    
    
    
    
    
    
    
    #############################3
   
    ##########预处理数据###################4
    #1.去除节假日   
    processVacation(data,length,allTime)
    processOutliers(data,data1,length)
    
    data=data1
    
    days=7
    data_manyDays(data,days)
    
    #############################4
    
    '''
    fig=plt.figure(figsize=(25, 10))
    ax1 = fig.add_subplot(1,1,1)
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%m-%d'))#设置时间标签显示格式%Y-%m-%d'
    plt.xticks([(startTime + timedelta((i)*days+rd)) for i in range(timeInterval//days+1)],rotation=90)#设置时间标签显示格式
    for item in ["flavor1"]:
        temp=[0]
        temp.extend(data[item])
        #print (temp)
        plt.plot([(startTime + timedelta((i)*days+rd)) for i in range((timeInterval//days)+1)],temp,label=item,drawstyle='steps-pre')
    #plt.legend(loc='best') 
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width*0.9 , box.height])
    ax1.legend(loc='center right', bbox_to_anchor=(1.12, 0.52),ncol=1)
    plt.show()
    '''
    
    
    preDays=(pre_endtime-pre_starttime).days+1
    print(preDays)
    for name in data:
        
        X=[]
        Y=[]
        for i in range(len(data[name])):
            
            X.append(i+1)
            Y.append(data[name][i])
        X.append(len(data[name])+1)
        Y.insert(0,Y[0])
       # print(X)
        #print(Y)
        
        pre_X=[X[len(X)-1]+1,X[len(X)-1]+2,X[len(X)-1]+3]
        preResult=double_exponential_smoothing(X,Y,pre_X)
        
        
       # result=0
        #if preResult[0]<Y[len(Y)-1]:
        #    result=int(round(Y[len(Y)-1]+((preDays-7)/7.0)*Y[len(Y)-1]))
       # else:
       #     result=int(round(preResult[0]+((preDays-7)/7.0)*preResult[1]))
        
        result=int(round(preResult[0]+((preDays-7)//7.0)*preResult[1]))
        result=result+0
        if result<0:
            result=0
        flavorNameAll[name]=result
        
        
        #print("--"*20)
    for name in flavorNameAll:
        #temp=period2[name][1]+0.2*(period2[name][1]-period2[name][0])
        ab=0.15
        temp=period2[name][1]*(1-0)+ab*period2[name][1]
        if temp<0:
            temp=0
        
        abc=0.5
        flavorNameAll[name]=(int(round(temp*(1-abc)+(flavorNameAll[name])*abc)))
    
    ###########################################################
    
   
    
    
    
    
    
    ###############################多重背包问题解决################################
    '''
    已有数据:
      map:每一种需要分配的虚拟机的预测数量
      服务器的资源信息：核数、内存数
      需要优化的维度：CPU或MEM
    
    需要得到的解：
      每个服务器中是怎么分配的各种虚拟机
    
    '''
    
    name=[] #所需预测的虚拟机对应的名称
    vcpu=[] #所需预测的虚拟机对应的核数
    mem=[] #所需预测的虚拟机对应的内存
    dataIndex=[]
    demand=[]
    
    for key in flavorNameAll.keys():
        dataIndex.append(int(key[6:])-1)
    
    
    #demand=[0,0,50,10,0]
    
    #排序 即后续先放西瓜再放芝麻
    temp=[]
    for i in dataIndex:
        if dim=="CPU":
            temp.append(vmVCPU_all[i])
        else:
            temp.append(vmMEM_all[i])
    temp=(sorted(zip(temp,dataIndex),reverse=True))
    dataIndex=[]
    for i in temp:
        dataIndex.append(i[1])
    
    #print (dataIndex)
    
    for i in dataIndex:
        name.append(vmName_all[i])
        #record.append(vmName_all[i]+" "+str(demand[i]))
        vcpu.append(vmVCPU_all[i])
        mem.append(vmMEM_all[i])
    
    for i in name:
        demand.append(flavorNameAll.get(i))
    
    #print (demand)
    #print (name)
    record=[str(sum(demand))]   #用于记录使用了哪个虚拟机去装箱
    if len(flavorNameAll)!=0:
        for i in name:
            record.append(i+" "+str(flavorNameAll.get(i)))
    nKind=len(name)
    
    record.append("")
    res=[0]*nKind
    
        
    print("maxMEM:",serverMEM)
    print("maxCPU:",serverCPU)
    print("name:",name)
    print("vcpu:",vcpu)
    print("mem",mem)
    print("demand",demand)
    
    
    serverNum=0
    if dim =='MEM':
        while len([x for x in demand if x>0])>0:
            serverNum=serverNum+1
            res=[0]*nKind
            V=onceBoxing2(vcpu,mem,demand,res,nKind,serverCPU,serverMEM)
            print("---"*7,"第"+str(serverNum)+"个服务器"+"---"*7)
            print ("MEM最优值:",V)
            print("各种虚拟机use Num：",res)
            print("mem使用情况",sum(list(map(lambda x: x[0]*x[1], zip(mem, res)))))
            print("vcpu使用情况",sum(list(map(lambda x: x[0]*x[1], zip(vcpu, res)))))
            print("---"*18)
            temp=str(serverNum)
            for i in range(nKind):
                if res[i]>0:
                    temp=temp+" "+name[i]+" "+str(res[i])
            record.append(temp)
            demand = list(map(lambda x: x[0]-x[1], zip(demand, res)))
    else:
        while len([x for x in demand if x>0])>0:
            serverNum=serverNum+1
            res=[0]*nKind
            V=onceBoxing2(mem,vcpu,demand,res,nKind,serverMEM,serverCPU)
            print("---"*7,"第"+str(serverNum)+"个服务器"+"---"*7)
            print ("VCPU最优值:",V)
            print("各种虚拟机use Num：",res)
            print("mem使用情况",sum(list(map(lambda x: x[0]*x[1], zip(mem, res)))))
            print("vcpu使用情况",sum(list(map(lambda x: x[0]*x[1], zip(vcpu, res)))))
            print("---"*18)
            temp=str(serverNum)
            for i in range(nKind):
                if res[i]>0:
                    temp=temp+" "+name[i]+" "+str(res[i])
            record.append(temp)
            demand = list(map(lambda x: x[0]-x[1], zip(demand, res)))
    if serverNum==0:
        record.append(str(serverNum))
    else:
        record.insert(-serverNum,str(serverNum))
       
    return record                ##################################以上 tab以下  除#

    
#predict_vm(input_lines,ecs_lines)



























