import sys, json
from count_cfg_freq import Counts
import part1
from collections import defaultdict
import time


class PCFG:
    def __init__(self, counter, train_f, test_f):
        self.unary = counter.unary
        self.binary = counter.binary
        self.nonterm = counter.nonterm
        self.wordcount = counter.wordcount
        self.rules = {}
        self.test_f = open(test_f, "r")
        self.train_f = open(train_f, "r")

        for x,y,z in self.binary.keys():
            self.rules.setdefault(x, [])
            if x in self.rules:
                self.rules[x].append((y, z))
            else:
                self.rules[x] = [(y, z)]
            

    def count_x(self, x):
        return self.nonterm[x]

    def count_xyy(self, x, y1, y2):
        if (x, y1, y2) in self.binary:
            return self.binary[(x, y1, y2)]
        return 0

    def count_xw(self, x, w):
        if (x, w) in self.unary:
            return self.unary[(x, w)]
        return 0

    def q1(self, X, w):
        #q(X->w) = Count(X->w) / Count(X)
        if w not in self.wordcount or self.wordcount[w] < 5:
            w = "_RARE_"
        return float(self.count_xw(X, w)) / self.count_x(X)

    def q2(self, x, y1, y2):
        #q(X->Y1 Y2) = Count(X->Y1 Y2) / Count(X)
        return float(self.count_xyy(x, y1, y2)) / self.count_x(x)

    def get_rules(self, x):
        if x in self.rules:
            return self.rules[x]
        return []

    def argmax(self, l):
        if not l: return None, 0.0
        return max(l, key = lambda x: x[1])

    def backtrace(self, back, bp):
        if not back: return None
        if len(back) == 6:
            (x,y,z,i,s,j) = back
            return [x, self.backtrace(bp[i][s][y], bp), self.backtrace(bp[s+1][j][z], bp)]
        else:
            (x, y, i, i) = back
            return [x, y]


    def parse(self, sentence):
        n = len(sentence)
        N = [k[0] for k in self.nonterm.iteritems()]

        # Init
        pi = [[defaultdict(float) for i in range(n+1)] for j in range(n+1)]
        bp = [[defaultdict() for i in range(n+1)] for j in range(n+1)]

        for i in range(1, n+1):
            w = sentence[i-1]
            for x in N:
                pi[i][i][x] = self.q1(x, w)

        # Recursion
        for l in range(1, n):
            for i in range(1, n - l + 1):
                j = i + l
                for x in N:
                    rules = self.get_rules(x)
                    back, score = \
                        self.argmax([((x, y, z, i, s, j), self.q2(x, y, z) * pi[i][s][y] * pi[s+1][j][z]) \
                        for s in range(i, j) for y, z in rules if pi[i][s][y] > 0 and pi[s+1][j][z] > 0])
                    #tmp = [self.q2(x, y, z) * pi[i][s][y] * pi[s+1][j][z] for s in range(i, j) for y, z in rules]
                    #if len(tmp):
                    #    pi[i][j][x] = max(tmp)
                    #    index = tmp.index(max(tmp))
                    #    s = index / len(range(i, j))
                    #    y1 = rules[(index - s) % len(rules)]
                    #    y2 = rules[(index - s) % len(rules) + 1]
                    #    bp[i][j][x] = (y1, y2, s)
                    if score > 0.0: bp[i][j][x], pi[i][j][x] = back, score
                 
        #if pi[1][n]['SBARQ']
        #print pi[1][n]['SBARQ']
        if 'SBARQ' in pi[1][n]:
            tree = self.backtrace(bp[1][n]["SBARQ"], bp)
            return tree, score


def get_sentences(test_f):
    for l in test_f:
        yield l.split()

if __name__ == "__main__":
    input_f = "parse_train_rare.dat"
    test_filename = "parse_dev.dat"
    output_filename = "parse_test.p2.out"
    #convert(sys.argv[1], sys.argv[2])

    counter = Counts()
    for l in open(input_f):
        t = json.loads(l)
        counter.count(t)
    #counter.show()

    start = time.time() 
    parser = PCFG(counter, input_f, test_filename)

    test_f = open("parse_dev.dat", "r")
    output_f = open(output_filename, "w")
    for s in get_sentences(test_f):
        tree, score = parser.parse(s)
        output_f.write(json.dumps(tree))
        

    print time.time() - start
