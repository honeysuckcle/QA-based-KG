import re
import jieba
import jieba.posseg as pseg
import sys   #导入sys模块
sys.path.append("..")
from brain.template import *

jieba.load_userdict("./data/user_dict.txt")
# jieba.enable_parallel(5) 
# jieba: parallel mode only supports posix system


# 取出句子中被判定为h r t的词
def rinse(words):
    useful_id = ['hh', 'rr', 'tt', 'hhrr', 'hhtt', 'hhrrtt','rrtt']
    res = []
    for x in words:
        # print(x.flag, x.flag in useful_id)
        if x.flag in useful_id:
            res.append(x)
    return res

def deal_multi_type_flag(flag):
    res = []
    l = len(flag)
    for i in range(l//2):
        res.append(flag[i*2 : i*2+2])
    return res

def display(words):
    s  = ""
    for x in words:
        s += "("+ str(x.word) + ", "+ str(x.flag)+") "
    print(s)

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

def first_step(words, none_flag = 0):
    temp = Template()
    special = []
    for x in words:
        if len(x.flag) > 2:
            special.append(x)
        else:
            none_flag = temp.add(x.word, x.flag, none_flag)
    return temp, special, none_flag

# 返回一个Template数组
def get_template_with_his(sentence, history):
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
    
    if history == "":
        return res    

    his_words = pseg.cut(history, use_paddle=True) #paddle模式
    his_words = rinse(his_words)
    
    print('none_flag:', none_flag)
    if none_flag in [1, 2, 4]:
        his_temp, special, n = first_step(his_words)

        if none_flag < 4:
            for i in range(len(res)):
                for x in his_temp.head_arr:
                    res[i].add(x, 'hh')
            res = enlarge_temp(res, special, 4)
        if none_flag & 2 == 0:
            for i in range(len(res)):
                for x in his_temp.relation_arr:
                    res[i].add(x, 'rr')
            res = enlarge_temp(res, special, 2)
        if none_flag & 1 == 0:
            for i in range(len(res)):
                for x in his_temp.tail_arr:
                    res[i].add(x, 'tt')
            res = enlarge_temp(res, special, 1)
        
    return res

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

            
        

def test():           
    string = "尽量发现所有可能被攻击者利用的安全隐患我和你的关系以及他和他们的关系是什么测试环境安装环境白盒测试程序分析"
    temp = get_template(string)
    print(temp.__len__())
    for x in temp:
        x.display()
