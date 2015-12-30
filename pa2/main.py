import sys, json
from count_cfg_freq import Counts
import part1
from collections import defaultdict

def count_word(x, counter):
    keys = [k for k, v in counter.unary.iteritems() if x == k[1]]
    return sum([counter.unary[k] for k in keys])

def count_x(x, counter):
    return counter.nonterm[x]

def count_xyy(x, y1, y2, counter):
    return counter.binary[(x, y1, y2)]

def count_xw(x, w, counter):
    if (x, w) in counter.unary.keys():
        return counter.unary[(x, w)]
    return 0

def q1(X, w, counter):
    #q(X->w) = Count(X->w) / Count(X)
    return float(count_xw(X, w, counter)) / count_x(X, counter)

def q2(x, y1, y2, counter):
    #q(X->Y1 Y2) = Count(X->Y1 Y2) / Count(X)
    return float(count_xyy(x, y1, y2)) / count_x(x)

def get_sentences(test_f):
    for l in test_f:
        yield l.split()

def parse(sentence, counter):
    n = len(sentence)
    N = [k[0] for k in counter.nonterm.iteritems()]

    # Init
    pi = [[defaultdict(float) for i in range(n)] for j in range(n)]
    bp = [[defaultdict() for i in range(n)] for j in range(n)]

    for i in range(n):
        w = sentence[i]
        for x in N:
            if count_xw(x, w, counter):
                pi[i][i][x] = q1(x, w, counter)

    # Recursion

if __name__ == "__main__":
    input_f = "parse_train_rare.dat"
    #convert(sys.argv[1], sys.argv[2])

    counter = Counts()
    for l in open(input_f):
        t = json.loads(l)
        counter.count(t)
    #counter.show()

    test_f = open("parse_dev.dat", "r")
    for s in get_sentences(test_f):
        parse(s, counter)
