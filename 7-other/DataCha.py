# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 16:14:48 2018
function:统计数据特征,选择不同的方式去统计
@author: Ethan
"""
import Sequence

def main(file_paths):
    
    sequence_months = Sequence.generate_seq_months(file_paths)
    print(sequence_months)
    #

#统计每个规格的虚拟机五个月的使用总量    
def countSum(sequence_months):
    return 0
    
    
    if __name__ == "main":
        file_paths = ["F:\lzw\yunDong\data\data_2015_1.txt",
                     "F:\lzw\yunDong\data\data_2015_2.txt",
                     "F:\lzw\yunDong\data\data_2015_3.txt",
                     "F:\lzw\yunDong\data\data_2015_4.txt",
                     "F:\lzw\yunDong\data\data_2015_5.txt"]
        main(file_paths)