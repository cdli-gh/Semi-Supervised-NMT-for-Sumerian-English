
import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def read_lines(filename):
    return open(filename, encoding='utf-8').read().split('\n')[:-1]

def preprocessing():
    #store sentences in form of lists
    data_trs_lines = read_lines(filename= 'src_train_pre.txt')
    data_vals_lines = read_lines(filename= 'src_val_pre.txt')
    data_tss_lines = read_lines(filename= 'src_test_pre.txt')
    data_trg_lines = read_lines(filename= 'tgt_train_pre.txt')
    data_valg_lines = read_lines(filename= 'tgt_val_pre.txt')
    data_tsg_lines = read_lines(filename= 'tgt_test_pre.txt')

    #set used to remove dupsrc_trainlicate strings from list data_en_lines and data_ta_lines
    seen_trs = set()
    seen_vals = set()
    seen_tss = set()
    seen_trg = set()
    seen_valg = set()
    seen_tsg = set()
    #store final sentences after preprocessing steps
    data_trs = []
    data_vals = []
    data_tss = []
    data_trg = []
    data_valg = []
    data_tsg = []

    for i in range(len(data_trs_lines)):
        seen_trs.add(data_trs_lines[i])
        data_trs.append(data_trs_lines[i])
        seen_trg.add(data_trg_lines[i])
        data_trg.append(data_trg_lines[i])

    for i in range(len(data_vals_lines)):
        if data_vals_lines[i] not in seen_trs and data_valg_lines[i] not in seen_trg:
            seen_vals.add(data_vals_lines[i])
            data_vals.append(data_vals_lines[i])
            seen_valg.add(data_valg_lines[i])
            data_valg.append(data_valg_lines[i])

    for i in range(len(data_tss_lines)):
        if data_tss_lines[i] not in seen_trs and data_tsg_lines[i] not in seen_trg and data_tss_lines[i] not in seen_vals and data_tsg_lines[i] not in seen_valg:
            seen_tss.add(data_tss_lines[i])
            data_tss.append(data_tss_lines[i])
            seen_tsg.add(data_tsg_lines[i])
            data_tsg.append(data_tsg_lines[i])

    with open('src_val_pred.txt', 'w') as file:
        for item in data_vals:
            file.write("{}\n".format(item))

    with open('tgt_val_pred.txt', 'w') as file:
        for item in data_valg:
            file.write("{}\n".format(item))

    with open('src_test_pred.txt', 'w') as file:
        for item in data_tss:
            file.write("{}\n".format(item))

    with open('tgt_test_pred.txt', 'w') as file:
        for item in data_tsg:
            file.write("{}\n".format(item))

if __name__ == '__main__':
    preprocessing()
