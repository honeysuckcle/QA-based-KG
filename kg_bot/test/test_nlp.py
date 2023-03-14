# 这个文档无法运行
# FileNotFoundError: [Errno 2] No such file or directory: './data/relations_v.txt'
import jieba
import jieba.posseg as pseg
import sys   #导入sys模块
sys.path.append("..")
from brain.template import *

jieba.load_userdict("./data/user_dict.txt")

def deal_multi_type_flag(flag):
    res = []
    l = len(flag)
    for i in range(l//2):
        res.append(flag[i*2 : i*2+2])
    return res

def enlarge_temp(res, special, id_filter = 7, none_flag =0):
    for x in special:
        id_arr = deal_multi_type_flag(x.flag)
        # print(id_arr)
        new_res = []
        for t in res:
            for id in id_arr:
                # t.display()
                temp = copy_Template(t)
                none_flag = temp.add(x.word, id, none_flag, id_filter)
                new_res.append(temp)
        res = new_res
        # for new_x in res:
        #     new_x.display()
    return res

def rinse(words):
    useful_id = ['hh', 'rr', 'tt', 'hhrr', 'hhtt', 'hhrrtt','rrtt']
    res = []
    for x in words:
        # print(x.flag, x.flag in useful_id)
        if x.flag in useful_id:
            res.append(x)
    return res

def display(words):
    s  = ""
    for x in words:
        s += "("+ str(x.word) + ", "+ str(x.flag)+") "
    print(s)

def first_step(words, none_flag = 0):
    temp = Template()
    special = []
    for x in words:
        if len(x.flag) > 2:
            special.append(x)
        else:
            none_flag = temp.add(x.word, x.flag, none_flag)
    return temp, special, none_flag

def get_template(sentence):
    res = []
    # 分词
    words = pseg.cut(sentence, use_paddle=True) #paddle模式

    # 清洗
    words = rinse(words)
    display(words)
 
    special = []
    # none_flag = 0 此处是二进制表示，000

    temp, special, none_flag = first_step(words)
            
    res.append(temp)
    res = enlarge_temp(res, special)  
    return res


test_arr = [
    '你好',
    '姚明的身高是多少',
]

for x in test_arr:
    temp = get_template(x)
    temp.display()

