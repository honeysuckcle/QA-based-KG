"""
    系统的主入口文件。
    当前端输入的是用户的问题时，本文件负责将问题解析出实体和属性，给返回机器人的回答。
"""
import flask
from flask_cors import CORS
from brain.nlp import *
import random
from db.searchNeo4j import get_triples
import json

app = flask.Flask(__name__)
CORS(app, resources=r'/*')

# entity_synonym = {}
# # 同义词替换
# with open("./data/Entity_Aalignment.txt","r",encoding='utf-8')  as f:
#     ss = f.read().split("\n")
#     for i in ss:
#         sss = i.split("\t")
#         entity_synonym[sss[0]] = sss[1]
#     f.close()

no_answer = [
    '咦？这个问题我好像看不懂呀。',
    '这个问题我不会哦~',
    '这个问题太难啦！',
    '不好意思，我不知道。'
]

history = ""

@app.route("/kgbot", methods=["GET"])
def chat():
    global entity_synonym
    global history
    input = str(flask.request.args.get('text'))
    print(history, input)
    temp = get_template(input)

    for t in temp:
        t.display()
        ans = t.deal()
        if ans != "":
            del temp
            history += ans
            return ans

    #如果没有查到结果，分析上文
    del temp
    temp = get_template_with_his(input, history)

    for t in temp:
        t.display()
        ans = t.deal()
        if ans != "":
            del temp
            history += ans
            return ans

    history += input
    if len(history) > 100:
        history = history[-100:] 

    #  没有查询到结果，返回不知道的提示语句
    del temp
    i = random.randint(0,len(no_answer)-1)
    return no_answer[i]
    
@app.route("/kg", methods=["GET"])
def get_kg():
    input = str(flask.request.args.get('text'))
    data = get_triples(input)
    json_data = json.dumps(data)
    return  json_data


if __name__=="__main__":
    print("kgbot is processing.")
    app.run(port=5004)

#http://127.0.0.1:5004/kgbot?text=白盒测试是什么


