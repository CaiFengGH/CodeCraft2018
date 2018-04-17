# -*- coding: utf-8 -*-
"""
@author: Ethan
1-此处先基于Python3.5实战
2-训练集中日期存在缺少情况，对于异常值如何弥补
"""
import os

def main(file_path):
    #生成输入数组
    input_lines = read_lines(file_path)
    
    #统计天数
    days = count_days(input_lines)
    
    sequence = generate_sequence(input_lines,days)
    
    print(sequence)
    
    
def generate_sequence(input_lines,days):

    sequence = {}
    
    #初始化sequence
    for i in range(1,16):
        prefix = "flavor"
        sequence[prefix + str(i)] = [0 for i in range(days)]

    pre_date = input_lines[0].split('\t')[2].split(' ')[0]
    index = 0        

    for line in input_lines:
        values = line.split('\t')        
        curr_date = values[2].split(' ')[0]

        if int(values[1][6:]) >= 16:
            continue

        if pre_date != curr_date:
            index = index + 1
            sequence[values[1]][index] += 1
            pre_date = curr_date
        else:
            sequence[values[1]][index] += 1
                
    return sequence
    
    
def count_days(input_lines):
    days = 1
    pre_date = input_lines[0].split('\t')[2].split(' ')[0]
    for line in input_lines[1:]:
        curr_date = line.split('\t')[2].split(' ')[0]
        print(curr_date)
        if curr_date != pre_date:
            days = days + 1
            pre_date = curr_date
    
    return days

        
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


if __name__ == "__main__":
    file_path = "F:\lzw\yunDong\data\data_2016_1.txt"
    main(file_path)
    