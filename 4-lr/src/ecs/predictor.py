import re
import copy as cp
import datetime
import Flavor
import HardWare
import OnePack
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


class myLinearRegression:
    def __init__(self, weights=None, bias=None):
        self.weights = weights
        self.bias = bias

    def fit(self,X,y):
        train_x = cp.deepcopy(X)
        self.classic_lstsqr(train_x, y)

    def predict(self, x):
        result = 0.0
        for w,x in zip(self.weights, x):
            result += w * x
        return result + self.bias

def evaluate_arima_model(counts,name,days):

    with open("config/{}.json".format(name), 'r') as load_f:
        lr_model = json.load(load_f)
    clf = myLinearRegression(lr_model["weights"],lr_model["bias"])
    X = cp.deepcopy(counts)
    PERIOD = 7
    '''
    train_x = []
    train_y = []
    for i in range(len(X) - PERIOD):
        tmp = []
        for j in range(PERIOD):
            tmp.append(X[i+j])
        train_x.append(tmp)
        train_y.append(X[i+j+1])
    clf.fit(train_x, train_y)
    '''
    results = 0
    for i in range(days):
        test = []
        for j in range(PERIOD):
            test.append(X[-PERIOD+j])
        test_y = int(clf.predict(test))
        if test_y < 0:
            test_y = 0
        X.append(test_y)
        results += test_y
    return int(results)

def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    start_time = datetime.datetime.now()

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
    PERIOD = (datetime.datetime.strptime(END_TIME,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(START_TIME,'%Y-%m-%d %H:%M:%S')).days

    BEGINNING_TIME = ecs_lines[0].strip().split("\t")[2]
    days = (datetime.datetime.strptime(START_TIME,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(BEGINNING_TIME,'%Y-%m-%d %H:%M:%S')).days

    predicts = []
    total = 0
    for flavor in flavors:
        counts = [0.0 for _ in range(days)]
        average_counts = 0
        for index, item in enumerate(ecs_lines):
            values = item.strip().split("\t")
            flavorName = values[1]
            createTime = values[2]
            if flavorName == flavor.name:
                day = days - (datetime.datetime.strptime(START_TIME,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(createTime,'%Y-%m-%d %H:%M:%S')).days - 1
                if day >= days:
                    continue
                counts[day] +=1.0
                average_counts +=1.0
        average_counts /= days
        flavor.setTarget(TARGET)
        pred = evaluate_arima_model(counts,flavor.name,PERIOD)
        predicts.append(pred)
        total += pred

    if TARGET == "CPU":
        TARGET_MAX = computer.cpu
        OTHER_MAX = computer.mem
    else:
        TARGET_MAX = computer.mem
        OTHER_MAX = computer.cpu

    total_paths = []
    total_nums = [0 for _ in range(len(predicts))]
    total_nums_vm = 0
    computer_num = 0
    outputs = []
    while(total>0):
        VALUES = []
        WEIGHTS = []
        OTHERS = []

        index2index = []
        index = 0
        for item, predict in zip(flavors, predicts):
            for _ in range(predict):
                VALUES.append(item.target)
                WEIGHTS.append(item.target)
                OTHERS.append(item.other)
                index2index.append(index)
            index +=1

        path = OnePack.allocate(TARGET_MAX, OTHER_MAX, VALUES, WEIGHTS, OTHERS)
        total -= len(path)
        total_nums_vm += len(path)
        total_paths.append(path)


        nums = [0 for _ in range(len(predicts))]
        for i in path:
            predicts[index2index[i]] -=1
            nums[index2index[i]] += 1
            total_nums[index2index[i]] += 1

        tmp = "{}".format(computer_num)
        for i in range(len(nums)):
            if nums[i] != 0:
                tmp += " {} {}".format(flavors[i].name, nums[i])
        outputs.append(tmp)
        computer_num += 1
        end_time = datetime.datetime.now()
        if (end_time - start_time).seconds > 55:
            return output_results(total_nums_vm, flavors, total_nums, computer_num, outputs)


    result = output_results(total_nums_vm, flavors, total_nums, computer_num, outputs)
    return result
