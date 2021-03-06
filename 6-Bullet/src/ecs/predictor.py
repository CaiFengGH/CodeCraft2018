# coding=utf-8

from datetime import datetime

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
    
    #VM={'flavor1':[1,1024],'flavor2':[1,2048],'flavor3':0,'flavor4':0,'flavor5':0,'flavor6':0,'flavor7':0,'flavor8':0,'flavor9':0,'flavor10':0,'flavor11':0,'flavor12':0,'flavor13':0,'flavor14':0,'flavor15':0}
    
    vmName_all=['flavor1','flavor2','flavor3','flavor4','flavor5','flavor6','flavor7','flavor8','flavor9','flavor10','flavor11','flavor12','flavor13','flavor14','flavor15']
    vmVCPU_all=[1,1,1,2,2,2,4,4,4,8,8,8,16,16,16]
    #vmMEM_all=[1024,2048,4096,2048,4096,8192,4096,8192,4096,8192,16384,8192,16384,8192,16384,32768,16384,32768,65536]
    vmMEM_all=[1,2,4,2,4,8,4,8,16,8,16,32,16,32,64]
    ############读取输入文件
    server = ecs_lines[0].split(" ")
    serverCPU = int(server[0])  #服务器的核数
    serverMEM = int(server[1]) #服务器的内存
    
    vm_num= int(ecs_lines[2].rstrip())  #预测的虚拟机总数
    if vm_num<=0:
        return ["0","","0"]
    flavorNameAll = {} # 预测的所有虚拟机的名称
    CPUAll={}        #预测的所有虚拟机的核数
    MEMAll = {}       #预测的所有虚拟机的创建时间
    
    for item in ecs_lines[3:(3+vm_num)]:
        values = item.split(" ")
       
        #flavorNameAll.append(values[0])
        if values[0] in ['flavor3','flavor4','flavor14','flavor15','flavor13','flavor6','flavor7','flavor12','flavor10']:
            flavorNameAll[values[0]]=4
        else:
            flavorNameAll[values[0]]=5
        flavorNameAll['flavor1']=7
        CPUAll[values[0]] = int(values[1])
        MEMAll[values[0]] = int(int(values[2].rstrip()) / 1024.0)
    dim =ecs_lines[4+vm_num].rstrip()  #需优化的资源维度
    
    pre_starttime=datetime.strptime(ecs_lines[6+vm_num].rstrip(),'%Y-%m-%d %H:%M:%S')  #预测开始时间
    pre_endtime= datetime.strptime(ecs_lines[7+vm_num].rstrip(),'%Y-%m-%d %H:%M:%S')    #预测结束时间
    
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
    boundary=pre_starttime-(pre_endtime-pre_starttime)
    ##e二分查找boundary的索引

    
    index=findSortedPosition(VMtime, boundary)
    
    for name in VMname[index:]:
        if name in flavorNameAll:
            flavorNameAll[name]=flavorNameAll[name]+1
    #添加分类，这种分类的服务器需求量比较大
    
    label = ['flavor1','flavor2','flavor5','flavor8']
    month = ['12','01','02']
    start_month = str(pre_starttime)[5:7]
    end_month = str(pre_endtime)[5:7]

    #根据月份进行弥补
    if start_month in month or end_month in month:
    	for key in flavorNameAll:
    		flavorNameAll[key] = flavorNameAll[key] + 1
    

    #根据预测服务器进行值弥补
    for key in flavorNameAll: 
    	if key in label:
    		flavorNameAll[key] = flavorNameAll[key] + 1

    #######暂时
	#for name in flavorNameAll:
    #    flavorNameAll[name]=int(flavorNameAll[name]*1.3)
    
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

    for i in name:
        demand.append(flavorNameAll.get(i))

    record=[str(sum(demand))]   #用于记录使用了哪个虚拟机去装箱
    if len(flavorNameAll)!=0:
        for i in name:
            record.append(i+" "+str(flavorNameAll.get(i)))
    record.append("")
    
    if sum(demand)>310:    
        for i in dataIndex:       
            #record.append(vmName_all[i]+" "+str(demand[i]))
            vcpu.append(vmVCPU_all[i])
            mem.append(vmMEM_all[i])        
        nKind=len(name)

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
   
    else:
         
        c=[]
        m=[]
        data=[]
        T=0
        for i in range(14,-1,-1):
          
            name=vmName_all[i]
            if name in flavorNameAll:
                T=T+flavorNameAll[name]
                for j in range(flavorNameAll[name]):
                    c.append(CPUAll[name])
                    m.append(MEMAll[name])
                    data.append(name)
       # print("---"*12)
       #  print(data)
        #############################
        
        def allocate_path(U, V, T, w , a, b):
            f = [[[0.0 for j in range(V+1)] for i in range(U+1)]for _ in range(T+1)]
        
            for i in range(1,T+1):
                for u in range(1, U+1):
                    for v in range(1, V+1):
                        if a[i-1] <= u and b[i-1] <= v:
                            f[i][u][v] = max(f[i - 1][u][v], f[i - 1][u - a[i - 1]][v - b[i - 1]] + w[i - 1])
                        else:
                            f[i][u][v] = f[i-1][u][v]
        
            m = U
            n = V
            path = []
            for i in range(T,1,-1):
                if f[i][m][n] == f[i-1][m][n]:
                    continue
                else:
                    path.append(i-1)
                    m -= a[i-1]
                    n -= b[i-1]
            if f[1][m][n] > 0 :
                path.append(0)
           # print(path)
            
          #  print(sum([a[i] for i in path]))
          #  print(sum([b[i] for i in path]))
            return path
        
        #record=[]
        
        j=0
        if dim=='CPU' :
            
            while(T>0):
                j=j+1
                tem={}
                path=allocate_path(serverCPU, serverMEM, T, c , c, m)
                T=T-len(path)
                for i in path:
                    del c[i]
                    del m[i]
                    tem[data[i]]=tem.get(data[i], 0)+1
                    del data[i]
                    
                ss=""+str(j)
                for i in tem:
                    ss=ss+" "+i+" "+str(tem[i]) 
                record.append(ss)
          
            
        elif dim=='MEM':
            
            j=0
            while(T>0):
                j=j+1
                tem={}
                path=allocate_path(serverCPU, serverMEM, T, c , c, m)
                T=T-len(path)
                for i in path:
                    del c[i]
                    del m[i]
                    tem[data[i]]=tem.get(data[i], 0)+1
                    del data[i]
                    
                ss=""+str(j)
                for i in tem:
                    ss=ss+" "+i+" "+str(tem[i]) 
                record.append(ss)
        if j==0:
            record.append(str(j))
        else:
            record.insert(-j,str(j))
        
   
   # for s in record:
        
    #    print(s)
   
    
        
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
