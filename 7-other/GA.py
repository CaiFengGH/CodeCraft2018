import random
class GA:
    def __init__(self, TARGET_MAX, OTHER_MAX, total, VALUES, OTHERS, flavors_names,pop_size=1000, iteration=10, cross_prob=0.8, mutate_prob=0.1):
        random.seed(2018)

        self.flavors_names = flavors_names
        self.pop_size = pop_size
        self.iteration = iteration
        self.cross_prob = cross_prob
        self.mutate_prob = mutate_prob
        self.d = total
        self.solution = [[random.random() for i in range(self.d)] for _ in range(self.pop_size)]
        self.scores = [0.0 for _ in range(self.pop_size)]
        self.TARGET_MAX = TARGET_MAX
        self.OTHER_MAX = OTHER_MAX
        self.VALUES = VALUES
        self.OTHERS = OTHERS

        self.flavor_sum = sum(VALUES)

        self.get_fitness()

    def allocate(self, w, a, b):
        U = self.TARGET_MAX
        V = self.OTHER_MAX
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

    def fitness(self, solution):
        tmp = sorted(range(len(solution)), key=lambda k: solution[k])
        W = []
        B = []
        for i in tmp:
            W.append(self.VALUES[i])
            B.append(self.OTHERS[i])
        cnt = 0

        sum1 = 0.0
        sum2 = 0.0
        for i, j in zip(W,B):
            if sum1+i <= self.TARGET_MAX and sum2+j <= self.OTHER_MAX:
                sum1 += i
                sum2 += j
            else:
                sum1 = 0
                sum2 = 0
                cnt+=1
        return self.flavor_sum / (cnt * self.TARGET_MAX * 1.0)

    def get_fitness(self):
        for index, solution in enumerate(self.solution):
            self.scores[index] = self.fitness(solution)

    def generate(self,paraent_index):
        next_pop = []
        for index in paraent_index:
            next_pop.append(self.solution[index])

        while len(next_pop) <  self.pop_size:
            paraent1 = random.choice(paraent_index)
            paraent2 = random.choice(paraent_index)
            if paraent1 != paraent2 and random.random() < self.cross_prob:
                position = random.randint(0,self.d)
                new_solution = self.solution[paraent1][0:position]
                new_solution.extend(self.solution[paraent2][position:])
                next_pop.append(new_solution)
        for i in range(self.pop_size):
            if random.random() < self.mutate_prob:
                position = random.randint(0, self.d-1)
                next_pop[i][position] *= random.random()
        return next_pop
    def train(self):
        for _ in range(self.iteration):
            tmp = sorted(range(len(self.scores)), key=lambda k: self.scores[k])
            paraent_index = tmp[int(self.pop_size * 0.9):]
            for i in range(int(self.pop_size * 0.4)):
                paraent_index.append(random.choice(tmp))
            self.solution = self.generate(paraent_index)
            self.get_fitness()
        tmp = sorted(range(len(self.scores)), key=lambda k: self.scores[k])
        best = self.solution[tmp[-1]]
        return best
    def get_path(self, solution):
        tmp = sorted(range(len(solution)), key=lambda k: solution[k])
        W = []
        B = []
        names = []
        for i in tmp:
            W.append(self.VALUES[i])
            B.append(self.OTHERS[i])
            names.append(self.flavors_names[i])

        outputs = []
        total = 0
        cnt = 0
        sum1 = 0.0
        sum2 = 0.0

        record = {}
        for i, j in zip(W,B):
            if sum1+i <= self.TARGET_MAX and sum2+j <= self.OTHER_MAX:
                sum1 += i
                sum2 += j
                total +=1
                record[names[i]] = record.get(names[i], 0) + 1
            else:
                sum1 = 0
                sum2 = 0
                cnt+=1
                output = "" + str(cnt) + " "
                for name in record:
                    output = output + str(name) + " " + str(record[name]) + " "
                outputs.append(output)
                record = {}
        for output in outputs:
            print(output)

        '''
        while T > 0:
            record = {}
            path = self.allocate(W, W, B)

            sum1 = 0
            sum2 = 0
            for i in path:
                total += 1
                record[names[i]] = record.get(names[i], 0) + 1
                if sum1 + W[i] > self.TARGET_MAX or sum2 + B[i] > self.OTHER_MAX:
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
            '''

        for output in outputs:
            print(output)



def quick_allocate(V, U, T, w , a, b):
    f = [[0.0 for j in range(V + 1)] for i in range(U + 1)]
    for i in range(T):
        for u in range(U, a[i]-1, -1):
            for v in range(V, b[i]-1, -1):
                f[u][v] = max(f[u - a[i]][v - b[i]] + w[i], f[u][v])
    print(f[-1][-1])

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


    w = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
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
     'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor11', 'flavor10', 'flavor10', 'flavor10']




    myGA = GA(V, U, len(w), w, b, flavors)
    best_solution = myGA.train()
    myGA.get_path(best_solution)

if __name__ == "__main__":
    main()