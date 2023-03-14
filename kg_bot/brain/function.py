import sys
import re

from py2neo.client import Result
sys.path.append("..")

from db.searchNeo4j import *
from brain.say import *

# load_dict()

def get_list_from_triple(triple):
    arr = re.split('[()\[\{\}\] -> ]', triple)
    return list( filter(None,arr))

# √
def fun_000(temp):
    print("head:0, relation:0, tail:0\n")
    return ""

def match_tail(tail):
    search_language = "MATCH p=(h)-[r]->(n) WHERE n.name = '{}' RETURN r ".format(tail)
    result = search_db(search_language)
    print(str(result))
    
    ans = ""
    l = len(result)
    triple_list = []
    if l > 0:
        for i in range(l):
            triple = str(result[i]['r'])
            arr = get_list_from_triple(triple)
            triple_list.append(arr)
            print(str(triple_list))
        ans = speak_with_triple(triple_list, tail, subject_is_head=False)
    return ans

# √
def fun_001(temp):
    print("head:0, relation:0, tail:1\n")
    return match_tail(temp.get_tail())

# √
def fun_00n(temp):
    print("head:0, relation:0, tail:n\n")
    ans = ""
    for tail in temp.tail_arr:
        ans += match_tail(tail)
    return ans

# √
def fun_010(temp):
    print("head:0, relation:1, tail:0\n")
    return ""

def standard_search(h, r):
    search_language = "match(n) -[:"+r+"]->(p) WHERE n.name = '"+h+"' return p.name"
    result = search_db(search_language)
    print("graphresult:"+str(result))

    result_arr = []
    for it in result:
        result_arr.append(str(it["p.name"]).replace("\'",""))
    print(str(result_arr))
    return speak_with_entity(result_arr, h, r)

def get_heads_with_rt(r, t):
    search_language = 'MATCH p=(h)-[:{}]->(n) WHERE n.name = \'{}\' RETURN h.name'.format(r, t)
    result = search_db(search_language)
    print('neo4j:', str(result))

    heads = []
    if len(result) > 0:
        for res in result:
            heads.append(res["h.name"])
        return speak_with_entity(heads)
    else:
        return ""

def get_niko(t):
    al_arr = ['英文名','外文名','别名','全称','简称','缩写']
    for al in al_arr:
        search_language = 'MATCH p=(h)-[:{}]->(n) WHERE n.name = \'{}\' RETURN h.name'.format(al, t)
        result = search_db(search_language)
        print('neo4j:', str(result))
        if (len(result) == 1):
            return result[0]['h.name']
    return None

# √
def fun_011(temp):
    print("head:0, relation:1, tail:1\n")
    r = temp.get_relation()
    t = temp.get_tail()
    res = get_heads_with_rt(r, t)
    if len(res) > 0:
        return res
    
    h = get_niko(t)
    if h != None:
        data = standard_search(h, r)
        return data
    return ''


# √
def fun_01n(temp):
    print("head:0, relation:1, tail:n\n")
    res = ""
    for t in temp.tail_arr:
        res += get_heads_with_rt(temp.get_relation(), t)
    return res

# 不做回答
def fun_0n0(temp):
    print("head:0, relation:n, tail:0\n")
    return ""

# √
def fun_0n1(temp):
    res = ""
    h = get_niko(temp.get_tail())
    if h != None:
        for r in temp.relation_arr:
            res += standard_search(h, r)
    else:
        for r in temp.relation_arr:
            res += get_heads_with_rt(r, temp.get_tail())
    return res

# 不回答
def fun_0nn(temp):
    print("head:0, relation:n, tail:n\n")
    return ""

# √
def fun_100(temp):
    print("head:1, relation:0, tail:0\n")
    data = standard_search(temp.get_head(), '定义')
    return data

def get_triple_with_entitys(h, t):
    search_language = "MATCH p = (h)-[]->(t) WHERE h.name='{}' AND t.name = '{}' RETURN p".format(h, t)
    result = search_db(search_language)
    print("graphresult:"+str(result))
    res = []
    for triple in result:
        s = str(triple['p'])
        print(s)
        arr = get_list_from_triple(s)
        res.append(arr[1])
    return res

# √
def fun_101(temp):
    print("head:1, relation:0, tail:1\n")
    h = temp.get_head()
    t = temp.get_tail()
    arr = get_triple_with_entitys(h, t)
    print(str(arr))
    if len(arr) > 0:
        return speak_with_relations(arr, h, t)
    return ""

def fun_10n(temp):
    print("head:1, relation:0, tail:n\n")
    return ""

def fun_110(temp):
    print("head:1, relation:1, tail:0\n")
    return standard_search(temp.get_head(), temp.get_relation())

def fun_111(temp):
    print("head:1, relation:1, tail:1\n")
    for x in temp.relation_arr:
        res = standard_search(temp.head_arr[0], x)
        if res != '':
            return res
    return ""

def fun_11n(temp):
    print("head:1, relation:1, tail:n\n")
    for x in temp.relation_arr:
        res = standard_search(temp.head_arr[0], x)
        if res != '':
            return res
    return ""

def fun_1n0(temp):
    print("head:1, relation:n, tail:0\n")
    for x in temp.relation_arr:
        res = standard_search(temp.head_arr[0], x)
        if res != '':
            return res
    return ""

def fun_1n1(temp):
    print("head:1, relation:n, tail:1\n")
    for x in temp.relation_arr:
        res = standard_search(temp.head_arr[0], x)
        if res != '':
            return res
    return ""


def fun_1nn(temp):
    print("head:1, relation:n, tail:n\n")
    for x in temp.relation_arr:
        res = standard_search(temp.head_arr[0], x)
        if res != '':
            return res
    return ""


def fun_n00(temp):
    print("head:n, relation:0, tail:0\n")
    return ""


def fun_n01(temp):
    print("head:n, relation:0, tail:1\n")
    ans = ""
    for x in temp.head_arr:
        result = get_triple_with_entitys(x, temp.get_tail())
        ans += speak_with_triple(result,x)

    return ans


def fun_n0n(temp):
    print("head:n, relation:0, tail:n\n")
    return ""

def fun_n10(temp):
    print("head:n, relation:1, tail:0\n")
    return ""

def fun_n11(temp):
    print("head:n, relation:1, tail:1\n")
    return ""

def fun_n1n(temp):
    print("head:n, relation:1, tail:n\n")
    return ""

def fun_nn0(temp):
    print("head:n, relation:n, tail:0\n")
    return ""

def fun_nn1(temp):
    print("head:n, relation:n, tail:1\n")
    return ""

def fun_nnn(temp):
    print("head:n, relation:n, tail:n\n")
    return ""

function = [
    fun_000, fun_001, fun_00n, fun_010, fun_011, fun_01n, fun_0n0, fun_0n1, fun_0nn,
    fun_100, fun_101, fun_10n, fun_110, fun_111, fun_11n, fun_1n0, fun_1n1, fun_1nn,
    fun_n00, fun_n01, fun_n0n, fun_n10, fun_n11, fun_n1n, fun_nn0, fun_nn1, fun_nnn,
    ]