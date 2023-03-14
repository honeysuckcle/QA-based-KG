import sys
sys.path.append('..')
import data_prepare.mfile as mfile
import codecs

def update(data_file_name):
    triples = mfile.read_file(data_file_name)
    f = codecs.open("../data/user_dict.txt","w","utf-8")
    h = triples[0]
    r = triples[1]
    t = triples[2]
    for x in h:
        if x in t:
            if x in r:
                f.write(x + " hhrrtt\n")
                r.remove(x)
            else:
                f.write(x + " hhtt\n")
            t.remove(x)
        else:
            f.write(x + " hh\n")
    for x in r:
        if x in t:
            f.write(x + " rrtt\n")
            t.remove(x)
        else:
            f.write(x + " rr\n")
    for x in t:
        if len(x) <= 21:
            f.write(x + " tt\n")

update("../data/data.txt")