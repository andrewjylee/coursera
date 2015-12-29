import sys, json
from count_cfg_freq import Counts
import part1

def count_word(x, counter):
    keys = [k for k, v in counter.unary.iteritems() if x == k[1]]
    return sum([counter.unary[k] for k in keys])

def count_x(x, counter):
    return counter.nonterm[x]

def count_xyy(x, y1, y2, counter):
    return counter.binary[(x, y1, y2)]

def count_xw(x, w, counter):
    return counter.unary[(x, w)]

def q1(X, w, counter):
    #q(X->w) = Count(X->w) / Count(X)
    return float(count_xw(X, w, counter)) / count_x(X, counter)

def q2(x, y1, y2, counter):
    #q(X->Y1 Y2) = Count(X->Y1 Y2) / Count(X)
    return float(count_xyy(x, y1, y2)) / count_x(x)

if __name__ == "__main__":
    input_f = "parse_train_rare.dat"
    #convert(sys.argv[1], sys.argv[2])

    counter = Counts()
    for l in open(input_f):
        t = json.loads(l)
        counter.count(t)
    #counter.show()

