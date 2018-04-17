import random
import datetime
import copy as cp


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
    return path


def bullet(U, V, w, b):
    start_time = datetime.datetime.now()

    random.seed(2018)

    best_solution = None
    min_cnt = 10000
    while True:
        solution = list(range(len(w)))
        random.shuffle(solution)
        cnt = 1
        sum1 = 0
        sum2 = 0
        for i in solution:
            if sum1 + w[i] <= U and sum2 + b[i] <= V:
                sum1 += w[i]
                sum2 += b[i]
            else:
                sum1 = w[i]
                sum2 = b[i]
                cnt += 1

        if cnt < min_cnt:
            min_cnt = cnt
            best_solution = cp.deepcopy(solution)
        end_time = datetime.datetime.now()
        print(cnt, min_cnt,  (end_time - start_time).seconds)

        if (end_time - start_time).seconds > 2:
            break
    return best_solution


def allocate(U, V, w, a, b):
    T = len(w)

    f = [[[0.0 for j in range(V + 1)] for i in range(U + 1)] for _ in range(T + 1)]
    for i in range(1, T + 1):
        for u in range(1, U + 1):
            for v in range(1, V + 1):
                if a[i - 1] <= u and b[i - 1] <= v:
                    f[i][u][v] = max(f[i - 1][u][v], f[i - 1][u - a[i - 1]][v - b[i - 1]] + w[i - 1])
                else:
                    f[i][u][v] = f[i - 1][u][v]
    m = U
    n = V
    path = []
    for i in range(T, 1, -1):
        if f[i][m][n] == f[i - 1][m][n]:
            continue
        else:
            path.append(i - 1)
            m -= a[i - 1]
            n -= b[i - 1]
    if f[1][m][n] > 0:
        path.append(0)
    return path


def get_path(solution, U, V, VALUES, OTHERS, flavors_names):
    tmp = sorted(range(len(solution)), key=lambda k: solution[k])
    W = []
    B = []
    names = []
    for i in tmp:
        W.append(VALUES[i])
        B.append(OTHERS[i])
        names.append(flavors_names[i])

    T = len(W)
    outputs = []
    total = 0
    cnt = 0

    TOTAL_PREDICT = {}
    while T > 0:
        record = {}
        path = allocate(U, V, W, W, B)

        sum1 = 0
        sum2 = 0
        for i in path:
            total += 1
            TOTAL_PREDICT[names[i]] = TOTAL_PREDICT.get(names[i], 0) + 1
            record[names[i]] = record.get(names[i], 0) + 1
            if sum1 + W[i] > U or sum2 + B[i] > V:
                print("error")
            sum1 += W[i]
            sum2 += B[i]
            del W[i]
            del B[i]
            del names[i]
        T = T - len(path)
        cnt +=1
        output = "" + str(cnt) + " "
        for name in record:
            output = output + str(name) + " " + str(record[name]) + " "
        outputs.append(output)

    for output in outputs:
        print(output)
    print(TOTAL_PREDICT)

def main():

    U= 56
    V= 128

    w = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4,
     4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
     4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 8, 8, 8, 8, 8, 8, 8, 8, 8,
     8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4,
     4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
     4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 8, 8, 8, 8, 8, 8, 8, 8, 8,
     8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    b =[4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
     4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 16,
     16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
     8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 64, 64, 64, 32, 32, 32, 32, 16, 16, 16, 32, 32, 32, 32,
     32, 32, 32, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 8, 8, 8, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
     4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 16,
     16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
     8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 64, 64, 64, 32, 32, 32, 32, 16, 16, 16, 32, 32, 32, 32,
     32, 32, 32, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 8, 8, 8]
    flavors = ['flavor3', 'flavor3', 'flavor3', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2',
     'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2',
     'flavor2', 'flavor2', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1',
     'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1',
     'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1',
     'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor7', 'flavor7', 'flavor7', 'flavor7', 'flavor7', 'flavor7',
     'flavor7', 'flavor6', 'flavor6', 'flavor6', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5',
     'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5',
     'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5',
     'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5',
     'flavor5', 'flavor4', 'flavor4', 'flavor4', 'flavor4', 'flavor4', 'flavor4', 'flavor4', 'flavor4', 'flavor4',
     'flavor4', 'flavor4', 'flavor4', 'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor9',
     'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor8', 'flavor8', 'flavor8',
     'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8',
     'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8',
     'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8',
     'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor15', 'flavor15',
     'flavor15', 'flavor14', 'flavor14', 'flavor14', 'flavor14', 'flavor13', 'flavor13', 'flavor13', 'flavor12',
     'flavor12', 'flavor12', 'flavor12', 'flavor12', 'flavor12', 'flavor12', 'flavor11', 'flavor11', 'flavor11',
     'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11',
     'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor10', 'flavor10', 'flavor10',
               'flavor3', 'flavor3', 'flavor3', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2',
               'flavor2',
               'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2', 'flavor2',
               'flavor2',
               'flavor2', 'flavor2', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1',
               'flavor1',
               'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1',
               'flavor1',
               'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor1',
               'flavor1',
               'flavor1', 'flavor1', 'flavor1', 'flavor1', 'flavor7', 'flavor7', 'flavor7', 'flavor7', 'flavor7',
               'flavor7',
               'flavor7', 'flavor6', 'flavor6', 'flavor6', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5',
               'flavor5',
               'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5',
               'flavor5',
               'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5',
               'flavor5',
               'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5', 'flavor5',
               'flavor5',
               'flavor5', 'flavor4', 'flavor4', 'flavor4', 'flavor4', 'flavor4', 'flavor4', 'flavor4', 'flavor4',
               'flavor4',
               'flavor4', 'flavor4', 'flavor4', 'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor9',
               'flavor9',
               'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor9', 'flavor8', 'flavor8',
               'flavor8',
               'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8',
               'flavor8',
               'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8',
               'flavor8',
               'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8',
               'flavor8',
               'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor8', 'flavor15',
               'flavor15',
               'flavor15', 'flavor14', 'flavor14', 'flavor14', 'flavor14', 'flavor13', 'flavor13', 'flavor13',
               'flavor12',
               'flavor12', 'flavor12', 'flavor12', 'flavor12', 'flavor12', 'flavor12', 'flavor11', 'flavor11',
               'flavor11',
               'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11',
               'flavor11',
               'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor10', 'flavor10', 'flavor10'
               ]

    solution = bullet(U, V, w, b)
    get_path(solution, U,V,w,b,flavors)

if __name__ == "__main__":
    main()