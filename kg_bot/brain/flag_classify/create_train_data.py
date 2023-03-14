import numpy as np
def read_file(file_name):
    res = []
    with open(file_name,"r",encoding='utf-8')  as f:
        dd = f.read().split("\n")
        for line in dd:
            if len(line) > 0:
                l = line.split("\t")
                if len(l) == 1:
                    res.append(line)
                else:
                    res.append(l)
        f.close()
    return res

def get_flag():
    arr = read_file('../../data/relation_subwords.txt')
    f = []
    for x in arr:
        if x[1] not in f:
            f.append(x[1])
    print(f)
    for x in f:
        print(x)


t = ['m', 'ns', 'j', 't', 'd', 'vn', 'n', 'v', 'b', 'p', 'nz', 'l', 'a', 's', 'q', 'ng', 'c', 'k', 'eng', 'nr']

def get_index(string):

    for i in range(len(t)):
        if t[i] == string:
            return i
    return -1

def init_x():
    arr = []
    for x in t:
        arr.append(0)
    return arr


def create_train_data():
    arr = read_file('../../data/relation_subwords.txt')
    verb = read_file('../../data/relations_v.txt')

    dict = {}
    word = ""
    his = []

    for line in arr:
        word = line[2]
        if word not in his:
            if word in verb:
                dict[word] = {'x':[line[1]], 'y': 1}
            else:
                dict[word] = {'x':[line[1]], 'y': 0}
            his.append(word)
        else:
            dict[word]['x'].append(line[1])

    X = []
    Y = []
    for d in his:
        x = init_x()
        for f in dict[d]['x']:
            x[get_index(f)] = 1
        Y.append(dict[d]['y'])
        X.append(x)

    string = ""
    for i in range(len(X)):
        for x in X[i]:
            string += str(x) + ' '
        string += ',' + str(Y[i]) + '\n'
    print(string)

create_train_data()


# get_flag()

