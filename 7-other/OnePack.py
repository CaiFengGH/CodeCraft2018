
def allocate(TARGET_MAX, OTHER_MAX, VALUES, WEIGHTS, OTHERS):
    num = len(VALUES)
    results = [[0 for __ in range(TARGET_MAX+1)] for _ in range(num+1)]


    for i in range(num+1):
        for j in range(TARGET_MAX+1):
            if i == 0:
                continue
            if i > 0 and j >= WEIGHTS[i-1]:
                results[i][j] = max(results[i-1][j], results[i-1][j-WEIGHTS[i-1]] + VALUES[i-1])

    path = []
    j = TARGET_MAX
    for i in range(num,-1,-1):
        if i >= 1:
            if results[i][j] != results[i-1][j]:
                path.append(i-1)
                j = j - WEIGHTS[i-1]


    constraint = 0.0
    for i in range(len(path)-1,-1,-1):
        constraint += OTHERS[path[i]]
        if constraint > OTHER_MAX:
            if i < len(path)-1:
                return path[i+1:]
            else:
                return []
    return path
'''
二维背包问题
V 需要优化的维度
U 约束条件
T 虚拟机总个数
w 虚拟机优化
a 虚拟机第一个约束条件，与虚拟机优化维度相同
b 虚拟机第二个约束条件
return 当次背包问题解，即路径
'''
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

def main():
    V = 56
    U = 128
    T = 3
    w = [6 , 16 , 16]
    a = [6 , 16 , 16]
    b = [64 , 64 , 64]
    allocate_path(V, U, T, w, a, b)

if __name__ == "__main__":
    main()