
from re import sub
import sys
sys.path.append("..")

dict = {}

def read_file(file_name):
    res = []
    with open(file_name,"r",encoding='utf-8')  as f:
        dd = f.read().split("\n")
        for line in dd:
            if len(line) > 0:
                l = line.split("\t")
                res.append(l)
        f.close()
    return res

def load_dict():
    global dict
    global inverse_dict
    file_contain = read_file('./data/relation_subwords.txt')
    print('dictory size:', len(file_contain))
    # print(file_contain)
    his = []
    for i in range(len(file_contain)):
        word = file_contain[i][0]
        if word in his:
            dict[word]['related'].append(file_contain[i][2])
        else:
            dict[word] = {'type':file_contain[i][1], 'related':[]}
            his.append(word)
    
# 读入动词relation
verb = read_file('./data/relations_v.txt')
for i in range(len(verb)):
    verb[i] = verb[i][0]
print("relation(verb): ", str(verb))

# graph_result 是一个triple数组
def speak_with_triple(graph_result, subject, subject_is_head=True):
    ans = ""
    if subject_is_head:
        if (len(graph_result)==2):
            return ""
        # if (len(graph_result)==3):
        #     if relation in relation_v:
        #          ans = ans[0]+ans[1]+ans[2]
        #     else:
        #         ans = ans[0]+"的"+ans[1]+"是"+ans[2]
        
        # else:
        #     if relation in relation_v:
        #         ans = "、".join(ans)
        #         ans = ans.replace("、","",2)
        #     else:
        #         ans = "、".join(ans)
        #         ans = ans.replace("、","的",1)
        #         ans = ans.replace("、","包括",1)
    else:
        ans = subject
        l = len(graph_result)
        if l <= 0:
            return ""
        for i in range(l):
            arr = graph_result[i]
            relation = arr[1]
            v = []
            # print(relation)
            if relation in verb:
                print(relation, "is verb.")
                v.append(arr)
            else:
                ans += "是{}的{}".format(arr[0], arr[1])
                if i == l-1:
                    ans += '。'
                else:
                    if i == l-2:
                        ans +='，也'
                    else:
                        ans += '，'
        if ans == subject:
            ans = ""
        for arr in v:
            for i in arr:
                ans += i
            ans += '。'
    return ans

# graph_result 是一个entity数组
def speak_with_entity(graph_result, subject, relation, subject_is_head = True):
    ans = ""
    num = len(graph_result)
    if subject_is_head:
        if num <= 0:
            return ""
        # 只有一个结果
        if num == 1:
            if relation in verb:
                ans = subject + relation + graph_result[0]
            else:
                ans = subject + "的" + relation +"是" + graph_result[0]
        # 有多个结果
        else:
            ans = subject
            if relation in verb:
                ans += relation
                ans = "，".join(graph_result)
            else:
                ans += "的" + relation + "包括"
                ans += "，".join(graph_result)
        return ans + '。'
    else:
        if len(graph_result) > 0:
            s = '、'.join(graph_result)
            if relation in verb:
                ans = s + relation + subject
            else:
                ans = "{}是{}的{}。".format(subject, s, relation)
        
        return ans

# graph_result 是relation的数组
def speak_with_relations(graph_result, head, tail):
    v = []  # graph_result 里的动词
    ans = ""
    for r in graph_result:
        if r in verb:
            v.append(r)
            graph_result.remove(r)
    if len(graph_result) > 0:
        ans += "{}是{}的{}。".format(tail, head, '、'.join(graph_result))
    if len(v) > 0:
        ans += head + '、'.join(v) + tail
    return ans

   
