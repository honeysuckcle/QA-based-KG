from mfile import *

finded_entity = read_file("websites.txt")[0]
dic = read_file("../data/data.txt")[0]

for d in dic:
    if d  not in finded_entity:
        print(d)
