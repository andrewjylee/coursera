import sys
import count_freqs


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

def viterbi(counter, input_filename, output_filename):
    tags = ['O', 'I-GENE']

    pi[0] = list()
    pi[0]["*"] = list()
    bp = list()
    bp[0] = list()
    bp[0]["*"] = list()
    pi[0]["*"]["*"] = 1
    bp[0]["*"]["*"] = 1

    input_f = open(input_filename, "r")
    output_f = open(output_filename, "w")
    line = input_f.readline()
    k = 1
    prev2 = "*"
    prev1 = "*"
    while line:
        word = line.strip("\n")
        if word:
            values = [pi[k-1][prev2][prev1] * q(tag, prev2, prev1) * e(counter, word, tag) for tag in tags]
            k += 1

            
            print values
            
            #e_values = [e(counter, word, tag) for tag in tags]
            #tag = tags[e_values.index(max(e_values))]
            #output_f.write(word + " " + tag + " \n")
        else:
            output_f.write(line)

        line = input_f.readline()
    input_f.close()
    output_f.close()
 

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

def viterbi_wrapper(input_f, output_f, counter):
    test_f = test_corpus_iterator(open(input_f))
    test_sentences = test_sentence_iterator(test_f)
    output_f = open(output_f, "w")

    for sentence in test_sentences:
        #print sentence

    #viterbi(counter, "gene.test", "gene_test.p2.out")
    #q(counter, 'O', 'O', 'O')




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
    viterbi_wrapper("gene.test", "gene_test.p2.out", counter)





   
    


if __name__ == "__main__":
    main()

