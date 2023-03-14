"""
    该文件将会清空数据库并利用data.txt重新构建新的数据库，只需要调用一次，后续无需
    再次调用。
"""

from py2neo import Graph,Node,Relationship
graph = Graph("http://localhost:7474",auth=("neo4j","1114"))
print("Neo4j数据库连接成功")
graph.run('match (n) detach delete n')
print("已删除旧数据库")
#删除当前已有的neo4j数据库
with open("../data/data.txt",'r',encoding='utf-8') as f:
    data = f.read().split("\n")
    f.close()



lastentity=""
a = Node("unresolved", name="start")
s = Node("unresolved", name="start")
for key in data:
    temp = key.split("\t")
    if (lastentity!=temp[0]):
        lastentity = temp[0]
        a = Node("unresolved",name=temp[0])
        b = Node("unresolved",name=temp[2])
        ab = Relationship(a, temp[1], b)
        s = s | a | b | ab
    else:
        b = Node("unresolved",name=temp[2])
        ab = Relationship(a, temp[1], b)
        s = s | b | ab

print("正在添加到数据库")
graph.create(s)#创建子图
print("neo4j创建成功")

