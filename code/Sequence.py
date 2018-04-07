"""
Created on Tue Mar 20 15:26:10 2018
function:描绘每种规格虚拟机，
@author: Ethan
"""
import os

def main(file_paths):
    
    sequence_momths = []
    
    #1-计算每个月各种虚拟机信息
    for i in range(len(file_paths)):
        
        print(str(i)+"------")
        
        #读取info
        input_lines = read_lines(file_paths[i])
        
        sequence = generate_seq(input_lines)
        #print(sequence)
        
        #生成序列
        sequence_momths.append(sequence)
    
    #2-将每个月每种规格的flavor进行输出
    outputFilePath = "F:\lzw\yunDong\data\\flavor1.txt"
    
    output_file(sequence_momths,outputFilePath)
    
    #描绘图像
    #Draw.drawMonth(sequence)    
    
def generate_seq(input_lines):
    
    sequence = {}
    
    #初始化sequence
    for i in range(1,16):
        prefix = "flavor"
        sequence[prefix + str(i)] = [0 for i in range(1,32)]

    pre_date = input_lines[0].split('\t')[2].split(' ')[0]
    index = 0

    i = 0        
    
    for line in input_lines:
        values = line.split('\t')
        
        i += 1
        
        print(i)
        
        curr_date = values[2].split(' ')[0]

        if int(values[1][6:]) >= 16:
            continue

        if pre_date != curr_date:
            #日期之差
            temp = int(curr_date[8:]) - int(pre_date[8:]) 
            
            index = index + temp
            sequence[values[1]][index] += 1
            pre_date = curr_date
        else:
            sequence[values[1]][index] += 1

    return sequence
    
def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print( 'file not exist: ') + file_path
        return None

def output_file(sequence_momths,outputFilePath):
    #currOutputPath = outputFilePath
        
        #outputFilePath = currOutputPath + str(index) + ".txt"
    with open(outputFilePath, 'a') as output_file:
        for index in range(1,16):
            flavor = "flavor"+str(index)
            output_file.write("%s\n" % flavor)
            for i in range(len(sequence_momths)):
                sequence = sequence_momths[i][flavor]
                sum = 0
                for item in sequence:
                    sum += item
                    output_file.write("%s " % item)
                output_file.write("  %d\n" % sum)
            

if __name__ == "__main__":
    #file_paths = ["F:\lzw\yunDong\data\data_2015_1.txt","F:\lzw\yunDong\data\data_2015_2.txt","F:\lzw\yunDong\data\data_2015_3.txt","F:\lzw\yunDong\data\data_2015_4.txt","F:\lzw\yunDong\data\data_2015_5.txt"]
    file_paths = ["F:\lzw\yunDong\data\data_2015_12.txt","F:\lzw\yunDong\data\data_2016_1.txt"]
    main(file_paths)
    