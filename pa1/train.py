import sys
import count_freqs
from collections import defaultdict
import operator


def e(counter, x, y):
    """
    e(x|y) = count(y->x) / count(y)
    """
    if count_word(x, counter) < 5:
        x = "_RARE_"
    top = counter.emission_counts[(x, y)]
    bottom = counter.ngram_counts[0][(y,)]
    return float(top) / bottom
    
def q(counter, y, y2, y1):
    """
    if y1 == "*":
        assert y1 == y2
        return 0
    elif y2 == "*":
        # y1 != "*"
        return 0
    elif y == "STOP":
        return 0
    """
    if counter.ngram_counts[1][(y2, y1)] == 0:
        return 0
    top = counter.ngram_counts[2][(y2, y1, y)]
    bottom = counter.ngram_counts[1][(y2, y1)]
    return float(top) / bottom

def count_word(x, counter):
    return counter.emission_counts[(x, 'O')] + counter.emission_counts[(x, 'I-GENE')]

def replace_low_freq(input_f, counter, threshold):
    input_f.seek(0, 0)
    output_f = open(sys.argv[1] + "_new", "w")
    l = input_f.readline()
    while l:
        line = l.strip()
        if line:
            fields = line.split(" ")
            word = " ".join(fields[:-1])
            word_count = count_word(word, counter)
            if word_count < threshold:
                output_f.write(l.replace(word, '_RARE_', 1))
            else:
                output_f.write(l)
        l = input_f.readline()
    output_f.close()
    return sys.argv[1] + "_new"

def test_baseline(counter, input_filename, output_filename):
    tags = ['O', 'I-GENE']

    input_f = open(input_filename, "r")
    output_f = open(output_filename, "w")
    line = input_f.readline()
    while line:
        word = line.strip("\n")
        if word:
            e_values = [e(counter, word, tag) for tag in tags]
            tag = tags[e_values.index(max(e_values))]
            output_f.write(word + " " + tag + " \n")
        else:
            output_f.write(line)

        line = input_f.readline()
    input_f.close()
    output_f.close()
    return

def viterbi(counter, sentence, n, output_f):
    tags = ['O', 'I-GENE']
    Y = []
    pi = [defaultdict(float) for i in range(0, n+1)]
    bp = [defaultdict(str) for i in range(0, n)]
    pi[0][("*", "*")] = 1
    prev2 = "*"
    prev1 = "*"

    for i in xrange(n):
        x = sentence[i]
        for tag in tags:
            pi[i+1][(prev1, tag)] = pi[i][(prev2, prev1)] * q(counter, tag, prev2, prev1) * e(counter, x, tag) * 10000
        next_tag = max(pi[i+1].iteritems(), key=operator.itemgetter(1))[0]
        print x, next_tag[1]
        output_f.write(x + " " + next_tag[1] + "\n")
        prev2 = next_tag[0]
        prev1 = next_tag[1]
        Y.append(prev1)





        #pi[i+1] = [pi[i][(prev2, prev1)] * q(counter, tag, prev2, prev1) * e(counter, x, tag) for tag in tags]

            
        #e_values = [e(counter, x, tag) for tag in tags]
        #tag = tags[e_values.index(max(e_values))]
        #output_f.write(x + " " + tag + " \n")
 

def test_corpus_iterator(fd):
    l = fd.readline()
    while l:
        line = l.strip()
        if line:
            word = line
            yield word
        else:
            yield None
        l = fd.readline()

def test_sentence_iterator(iterator):
    curr_sent = []
    for l in iterator:
        if l == None:
            if curr_sent:
                yield curr_sent
                curr_sent = []
            else:
                sys.stderr.write("WARNING: Got empty input file/stream.\n")
                raise StopIteration
        else:
            curr_sent.append(l)

    if curr_sent:
        yield curr_sent

def viterbi_wrapper(input_fname, output_fname, counter):
    input_f = test_corpus_iterator(open(input_fname))
    test_sentences = test_sentence_iterator(input_f)
    output_f = open(output_fname, "w")

    for sentence in test_sentences:
        viterbi(counter, sentence, len(sentence), output_f)
        output_f.write("\n")

    #viterbi(counter, "gene.test", "gene_test.p2.out")
    #q(counter, 'O', 'O', 'O')

    input_f.close()
    output_f.close()



def main():
    """
    input_f = open(sys.argv[1], "r")
    counter = count_freqs.Hmm(3)
    counter.train(input_f)

    new_input_filename = replace_low_freq(input_f, counter, 5)
    input_f.close()

    input_f = open(new_input_filename, "r")
    counter = count_freqs.Hmm(3)
    counter.train(input_f)
    """
    input_f = open(sys.argv[1], "r")
    counter = count_freqs.Hmm(3)
    counter.train(input_f)

    #test_baseline(counter, "gene.dev", "gene_dev.p1.out")
    #viterbi_wrapper("gene.test", "gene_test.p2.out", counter)
    viterbi_wrapper("gene.dev", "gene_test.p2.out", counter)





   
    


if __name__ == "__main__":
    main()

