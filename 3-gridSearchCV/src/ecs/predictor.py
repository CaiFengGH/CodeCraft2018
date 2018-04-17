# coding=utf-8
from datetime import datetime
import sys
def initial_trend(series, slen):
    sum = 0.0
    for i in range(slen):
        sum += float(series[i+slen] - series[i]) / slen
    return sum / slen
def initial_seasonal_components(series, slen):
    seasonals = {}
    season_averages = []
    n_seasons = int(len(series)/slen)
    # compute season averages
    for j in range(n_seasons):
        season_averages.append(sum(series[slen*j:slen*j+slen])/float(slen))
    # compute initial values
    for i in range(slen):
        sum_of_vals_over_avg = 0.0
        for j in range(n_seasons):
            sum_of_vals_over_avg += series[slen*j+i]-season_averages[j]
        seasonals[i] = sum_of_vals_over_avg/n_seasons
    return seasonals
def triple_exponential_smoothing(series, slen, alpha, beta, gamma, n_preds):
    result = []
    seasonals = initial_seasonal_components(series, slen)
    for i in range(len(series)+n_preds):
        if i == 0: # initial values
            smooth = series[0]
            trend = initial_trend(series, slen)
            result.append(series[0])
            continue
        if i >= len(series): # we are forecasting
            m = i - len(series) + 1
            result.append((smooth + m*trend) + seasonals[i%slen])
        else:
            val = series[i]
            last_smooth, smooth = smooth, alpha*(val-seasonals[i%slen]) + (1-alpha)*(smooth+trend)
            trend = beta * (smooth-last_smooth) + (1-beta)*trend
            seasonals[i%slen] = gamma*(val-smooth) + (1-gamma)*seasonals[i%slen]
            result.append(smooth+trend+seasonals[i%slen])
    if(int(sum(result[-n_preds:])) < 0):
        pred = 0
    else:
        pred = int(sum(result[-n_preds:]))
    return  pred
def exponential_smoothing(series, alpha, period):
    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return int(result[-1] * period), result

def double_exponential_smoothing(series, alpha, beta, period):
    result = [series[0]]
    length = len(series)
    for n in range(1, length + 1 + period):
        if n == 1:
            level, trend = series[0], series[1] - series[0]
        if n >= len(series): # we are forecasting
          value = result[-1]
        else:
          value = series[n]

        last_level, level = level, alpha*value + (1-alpha)*(level+trend)
        trend = beta*(level-last_level) + (1-beta)*trend
        result.append(level+trend)
        if n >= length:
            series.append(level + trend)
    return int(sum(result[-period:]))

def gridCV_exponential_smoothing(counts):
    parameters = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    scores = []
    MAX_MSE = sys.maxint
    best_para = 0.0
    for i,para in enumerate(parameters):
        _, predict = exponential_smoothing(counts, period=1, alpha=para)
        MSE = 0.0

        for j in range(len(counts)):
            MSE = (int(counts[j]) - int(predict[j])) ** 2 + MSE
        if MAX_MSE > MSE:
            MAX_MSE = MSE
            best_para = para
        scores.append(MSE)
    return best_para
def evaluate_arima_model(counts,period,alpha=0.716,beta=0.029,gamma=0.993, slen=1):
    best_alpha =  gridCV_exponential_smoothing(counts)
    predict, _ = exponential_smoothing(counts, period=period,alpha=best_alpha)
    #predict = double_exponential_smoothing(counts, 0.1, 0.1,period=days)
    #predict = triple_exponential_smoothing(counts, 1, 0.716, 0.029, 0.993, days)
    print(predict)
    return predict
    #predict = double_exponential_smoothing(counts,alpha=alpha,beta=beta,period=period)
    #predict = triple_exponential_smoothing(counts, slen, alpha, beta, gamma, period)
    print(predict)
    return predict
############################################
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
    vmName_all=['flavor1','flavor2','flavor3','flavor4','flavor5','flavor6','flavor7','flavor8','flavor9','flavor10','flavor11','flavor12','flavor13','flavor14','flavor15']
    vmVCPU_all=[1,1,1,2,2,2,4,4,4,8,8,8,16,16,16]
    vmMEM_all=[1,2,4,2,4,8,4,8,16,8,16,32,16,32,64]
    ############读取输入文件
    server = ecs_lines[0].split(" ")
    serverCPU = int(server[0])  #服务器的核数
    serverMEM = int(server[1]) #服务器的内存
    vm_num= int(ecs_lines[2].rstrip())  #预测的虚拟机总数
    if vm_num<=0:
        return ["0","","0"]
    flavorNameAll = {} # 预测的所有虚拟机的名称
    CPUAll=[]          #预测的所有虚拟机的核数
    MEMAll = []        #预测的所有虚拟机的创建时间
    
    for item in ecs_lines[3:(3+vm_num)]:
        values = item.split(" ")
        flavorNameAll[values[0]] = 0
        CPUAll.append(int(values[1]));
        MEMAll.append(int(values[2].rstrip())/1024.0)
    dim =ecs_lines[4+vm_num].rstrip()  #需优化的资源维度
    
    pre_starttime=datetime.strptime(ecs_lines[6+vm_num].rstrip(),'%Y-%m-%d %H:%M:%S')  #预测开始时间
    pre_endtime= datetime.strptime(ecs_lines[7+vm_num].rstrip(),'%Y-%m-%d %H:%M:%S')    #预测结束时间
    #预测时长
    PERIOD = (pre_endtime - pre_starttime).days
    ################读取训练数据文件
    VMid=[]      #虚拟机id集合
    VMname=[]    #虚拟机名称集合
    VMtime=[]    #虚拟机创建时间
    for item in input_lines:
        values = item.split("\t")
        VMid.append(values[0])
        VMname.append(values[1])
        VMtime.append(datetime.strptime(values[2].rstrip(),'%Y-%m-%d %H:%M:%S'))

    
    ##########################统计最后一个周期中所需预测虚拟机的数量##########################
    BEGINNING_TIME = input_lines[0].strip().split("\t")[2]
    days = (pre_starttime - datetime.strptime(BEGINNING_TIME,'%Y-%m-%d %H:%M:%S')).days
    slen = int(days) / 30
    if slen == 0:
        slen = 1
    for flavor in flavorNameAll:
        counts = [0.0 for _ in range(days)]
        for index, item in enumerate(input_lines):
            values = item.strip().split("\t")
            flavorName = values[1]
            createTime = values[2]
            if flavorName == flavor:
                day = days - (pre_starttime- datetime.strptime(createTime,'%Y-%m-%d %H:%M:%S')).days - 1
                if day >= days:
                    continue
                counts[day] +=1.0

        flavorNameAll[flavor] = evaluate_arima_model(counts,PERIOD,slen=slen)

    
    ###############################多重背包问题解决############
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

    
    for i in dataIndex:
        name.append(vmName_all[i])
        vcpu.append(vmVCPU_all[i])
        mem.append(vmMEM_all[i])
    
    for i in name:
        demand.append(flavorNameAll.get(i))

    record=[str(sum(demand))]   #用于记录使用了哪个虚拟机去装箱
    if len(flavorNameAll)!=0:
        for i in name:
            record.append(i+" "+str(flavorNameAll.get(i)))
    nKind=len(name)
    
    record.append("")
    
    res=[0]*nKind

    
    serverNum=0
    if dim =='MEM':
        while len([x for x in demand if x>0])>0:
            serverNum=serverNum+1
            res=[0]*nKind
            onceBoxing2(vcpu,mem,demand,res,nKind,serverCPU,serverMEM)

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
            onceBoxing2(mem,vcpu,demand,res,nKind,serverMEM,serverCPU)

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
   
    return record
    
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
