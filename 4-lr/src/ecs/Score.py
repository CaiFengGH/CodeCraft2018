import sys
import os
import predictor
import re
import copy as cp
import datetime
import Flavor
import HardWare


def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print 'file not exist: ' + file_path
        return None


def get_true(input_lines, test_data):
    flavors = []
    computer = None
    TARGET = None
    TIMES = []
    for index, item in enumerate(input_lines):
        values = item.strip().split(" ")
        if values[0] == "":
            continue
        if index == 0:
            computer = HardWare.HardWare(int(values[0]), int(values[1]))
        if re.match(r'^flavor\d+$',values[0]):
            flavors.append(Flavor.Flavor(values[0], int(values[1]), int(values[2])))
        if re.match(r'^CPU$', values[0]) or re.match(r'^MEM$', values[0]):
            TARGET = values[0]
        if len(values) == 2:
            time = "{} {}".format(values[0],values[1])
            TIMES.append(time)

    START_TIME = TIMES[0]
    END_TIME = TIMES[1]

    test_y = []
    for flavor in flavors:
        average_counts = 0
        for index, item in enumerate(test_data):
            values = item.strip().split("\t")
            flavorName = values[1]
            createTime = values[2]
            if flavorName == flavor.name and (datetime.datetime.strptime(createTime,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(START_TIME,'%Y-%m-%d %H:%M:%S')).days >=0 and (datetime.datetime.strptime(END_TIME, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(createTime,'%Y-%m-%d %H:%M:%S')).days >= 0:
                average_counts += 1.0
        test_y.append(average_counts)
    return test_y, TARGET, computer, flavors


def get_predict(result_data):
    allocation = []
    predict_y = []
    for index, item in enumerate(result_data):
        values = item.strip().split(" ")
        if values[0] == "":
            continue
        if index == 0:
            continue
        if re.match(r'^flavor\d+$',values[0]):
            predict_y.append(int(values[1]))
        if re.match(r'^\d+$',values[0]) and index > 0 and len(values) >= 1:
            tmp = {}
            for i in range(1,len(values)):
                if re.match(r'^flavor\d+$', values[i]):
                    tmp[values[i]] = 0
                else:
                    tmp[values[i-1]] += int(values[i])
            allocation.append(tmp)
    return predict_y, allocation

def get_TIC(test_y, predict_y):
    N = len(test_y)
    RMSE_total = 0.0
    RMSE_true = 0.0
    RMSE_predict = 0.0
    for t, y in zip(test_y, predict_y):
        RMSE_total += (t-y)**2
        RMSE_predict += y**2
        RMSE_true += t**2
    score = 1 - (RMSE_total / N)**0.5 / ((RMSE_true / N)**0.5 +(RMSE_predict / N)**0.5)
    return score

def get_score(test_y, TARGET, computer, flavors, predict_y, allocation):
    TIC =  get_TIC(test_y, predict_y)

    if TARGET == "CPU":
        TARGET_MAX = computer.cpu
        OTHER_MAX = computer.mem
    else:
        TARGET_MAX = computer.mem
        OTHER_MAX = computer.cpu

    maps = {}
    for flavor in flavors:
        flavor.setTarget(TARGET)
        maps[flavor.name] = flavor

    TOTAL_USE = 0.0
    for instances in allocation:
        target_use = 0.0
        other_use = 0.0
        for key in instances:
            target_use += maps[key].target * instances[key]
            other_use += maps[key].other * instances[key]
        if target_use > TARGET_MAX:
            print "The {} utilized resource is more than the limition".format(TARGET)
        if other_use > OTHER_MAX:
            print "The other utilized resource is more than the limition"
    TOTAL_USE += target_use
    ratio = TOTAL_USE / (len(allocation) * TARGET_MAX)

    print "test_y:{}".format(test_y)
    print "predict_Y:{}".format(predict_y)
    print "TIC: {} \nRATIO:{} \nSCORE:{}".format(TIC, ratio, TIC*ratio)
def main():
    input_file_array = read_lines("../../data/case1/input.txt")
    test_file_array = read_lines("../../data/case1/TrainData.txt")
    predict_file_array = read_lines("../../data/Restlt.txt")

    test_y, TARGET, computer, flavors = get_true(input_lines=input_file_array, test_data=test_file_array)
    predict_y, allocation = get_predict(predict_file_array)
    get_score(test_y, TARGET, computer, flavors, predict_y, allocation)


if __name__ == "__main__":
    main()