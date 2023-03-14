from py2neo import Graph,Node,Relationship
import re

# 在启动后台程序的时候就做好和数据库的连接，加快回复速度
graph = Graph("http://localhost:7474",auth=("neo4j","1114")) # 1114是数据库的密码

def search_db(search_language):
    data = graph.run(search_language).data()
    return data

def get_list_from_triple(triple):
    arr = re.split('[()\[\{\}\] -> ]', triple)
    return list( filter(None,arr))

def format_triples(data, title):
    arr = []
    for d in data:
        s = str(d[title])
        arr.append(get_list_from_triple(s))
    return arr

def get_triples(center):
    cypher = 'MATCH p=(n)-[]->() WHERE n.name=\'{}\' RETURN p LIMIT 10'.format(center)
    data = graph.run(cypher).data()
    data = format_triples(data, 'p')
    for d in data:
        print(d)
    return data

# get_triples('软件度量')
