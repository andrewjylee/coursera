import sys, json
from count_cfg_freq import Counts

def get_low_freq_words(counter):
    low_words = {}
    for entry in counter.unary.iteritems():
        if entry[1] < 5:
            low_words.setdefault(entry[0][1], 1)

    return low_words

def get_words(tree):
    words = []
    if isinstance(tree, basestring):
        return 
    if len(tree) == 3:
        return words + get_words(tree[1]) + get_words(tree[2])
    elif len(tree) == 2:
        words.append(tree[1])
        return words

def replace(tree):
    words = get_words(tree)

def replace_wrapper(input_fn, output_fn, low_words):
    output_f = open(output_fn, "w")

    for l in open(input_fn):
        new_line = l
        t = json.loads(l)
        words = get_words(t)
        for word in words:
            if word in low_words:
                new_line = new_line.replace("\""+word+"\"", "\"_RARE_\"", 1)
        output_f.write(new_line)

def convert(input_filename, output_filename):
    counter = Counts()
    for l in open(input_filename):
        t = json.loads(l)
        counter.count(t)
    low_words = get_low_freq_words(counter)
    replace_wrapper(input_filename, output_filename, low_words)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("""Usage: python part1.py input_file output_file\n""")

    convert(sys.argv[1], sys.argv[2])
