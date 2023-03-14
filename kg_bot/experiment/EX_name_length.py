import sys   #导入sys模块
sys.path.append("..")
from data_prepare.mfile import read_file
import numpy as np  
import matplotlib.mlab as mlab  
import matplotlib.pyplot as plt  
#如遇中文显示问题可加入以下代码
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

 
triples = read_file('../data/data.txt')
title = ["知识图谱中的头实体的字符长度统计图","知识图谱中的关系的字符长度统计图","知识图谱中的尾实体的字符长度统计图"]
Y = []
for i in range(3):
    X=[]
    arr = triples[i]
    for s in arr:
        l = len(s)
        if X.__len__() <= l:
            for j in range(l - X.__len__() +1):
                X.append(0)
        X[l]+=1
    Y.append(X)


def draw_graph():
    for X in Y:
        fig = plt.figure()
        plt.bar(range(X.__len__()),X,0.4,color="green")
        plt.xlabel("字符长度")
        plt.ylabel("个数")
        plt.title(title[i])

    plt.show()  
    

# i: 0-head entity; 1-relation; 2-tail entity
# x: x*100%
def percent_line(i, x):
    X=Y[i]
    sum = 0
    line = x * arr.__len__()
    for j in range(X.__len__()):
        sum += X[j]
        if sum > line:
            return j


# i: 0-head entity; 1-relation; 2-tail entity
def draw_percent_graph(i):
    sum = 0
    for j in range(X.__len__()):
        sum += X[j]
        X[j] = sum / arr.__len__() * 100
    
    fig = plt.figure()    
    plt.grid(True)
    plt.bar(range(X.__len__()),X,0.4,color="green")
    plt.xlabel("长度")
    plt.ylabel("长度小于x的实体个数占总数的百分比")
    plt.title(title[i])
    plt.show()  

draw_percent_graph(2)