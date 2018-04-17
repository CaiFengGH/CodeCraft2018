import re
import copy as cp
import datetime
import Flavor
import HardWare
import OnePack
import pandas as pd
import numpy as np
from math import sqrt
import os
import sys
from sklearn.linear_model import LinearRegression
import json
def output_results(total_nums_vm, flavors, total_nums, computer_num, outputs):
    results = []
    str = "{}".format(total_nums_vm)
    results.append(str)


    for i in range(len(total_nums)):
        str = "{} {}".format(flavors[i].name, total_nums[i])
        results.append(str)
    str = ""
    results.append(str)
    str = "{}".format(computer_num)
    results.append(str)
    for item in outputs:
        results.append(item)
    return results


def evaluate_arima_model(counts):
    X = cp.deepcopy(counts)

    PERIOD = 7
    train_x = []
    train_y = []
    for i in range(len(X)-PERIOD):
        tmp = []
        for j in range(PERIOD):
            tmp.append(X[i+j])
        train_x.append(tmp)
        train_y.append(X[i+PERIOD])

    train_x = np.array(train_x)
    train_y = np.array(train_y)

    clf = LinearRegression()
    clf.fit(train_x, train_y)

    weights = clf.coef_.tolist()
    bias = clf.intercept_
    return weights, bias

def predict_vm(lines):
    BEGINNING_TIME = "2015-01-01 00:00:00"
    START_TIME = "2015-05-31 23:59:59"
    days = (datetime.datetime.strptime(START_TIME,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(BEGINNING_TIME,'%Y-%m-%d %H:%M:%S')).days

    flavors = ["flavor1","flavor2","flavor3","flavor4","flavor5",
               "flavor6","flavor7","flavor8","flavor9","flavor10",
               "flavor11","flavor12","flavor13","flavor14","flavor15"]
    for flavor in flavors:
        counts = [0.0 for _ in range(days)]
        average_counts = 0
        for index, item in enumerate(lines):
            values = item.strip().split("\t")
            flavorName = values[1]
            createTime = values[2]
            if flavorName == flavor and (datetime.datetime.strptime(START_TIME,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(createTime,'%Y-%m-%d %H:%M:%S')).days >0:
                day = days - (datetime.datetime.strptime(START_TIME,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(createTime,'%Y-%m-%d %H:%M:%S')).days - 1
                counts[day] +=1.0
                average_counts +=1.0

        weights, bias = evaluate_arima_model(counts)
        lr_model = {"name":flavor,"weights":weights,"bias":bias}
        with open("config/{}.json".format(flavor), "w") as f:
            json.dump(lr_model, f)

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
def main():
    lines = read_lines("../../data/total_data/train_total.txt")
    predict_vm(lines)
if __name__ == "__main__":
    main()

