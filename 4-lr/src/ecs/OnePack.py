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


def main():
    v = [20,10,15,10]
    c = [2,1,2,1]
    o = [5,2,1,6]
    print(allocate(4,10,v,c,o))




if __name__ == "__main__":
    main()