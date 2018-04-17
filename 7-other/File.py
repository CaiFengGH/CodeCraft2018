# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 17:12:34 2018
function:进行文件相关操作
@author: Ethan
"""

def write_result(sequence, outpuFilePath):
    
    with open(outpuFilePath, 'w') as output_file:
        for i in range(1,16):
            for index,item in enumerate(sequence["flavor"+str(i)]):
                output_file.write("%s -" % item)
