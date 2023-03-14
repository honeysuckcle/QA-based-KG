# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import codecs
import re

# 去掉空格
def format_r(str):
    return str.replace(" ","")

def format_entity(str):
    return re.sub("\[\d\]","",str)

# 不要的参数
garbage = ["注音","拼音","中文名"]

base_url = "https://baike.baidu.com"
his = ["/item/%E7%94%A8%E6%88%B7%E7%95%8C%E9%9D%A2%E6%B5%8B%E8%AF%95"]
finished_list = []
f = codecs.open("baidu_data/baidu_triples14_original.txt",'a','utf-8')
# 读取已经爬取过的文件列表
with open("websites.txt","r",encoding='utf-8')  as his_file:
    dd = his_file.read().split("\n")
    for item in dd:
        stemp = item.split("\t")
        if len(stemp) > 1:
            finished_list.append(stemp[1])
    his_file.close()

his_file = codecs.open("websites.txt",'a','utf-8')
"""
使用过的root
软件测试 url:"/item/%E8%BD%AF%E4%BB%B6%E6%B5%8B%E8%AF%95/327953" baidu_triples1_original.txt
α测试 /item/%CE%B1%E6%B5%8B%E8%AF%95/1924836 baidu_triples1_original.txt
安全测试 /item/%E5%AE%89%E5%85%A8%E6%B5%8B%E8%AF%95 baidu_triples3_original.txt
安装测试 /item/%E5%AE%89%E8%A3%85%E6%B5%8B%E8%AF%95 baidu_triples4_original.txt
并发测试 /item/%E5%B9%B6%E5%8F%91%E6%B5%8B%E8%AF%95 baidu_triples5_original.txt
测试驱动开发 /item/%E6%B5%8B%E8%AF%95%E9%A9%B1%E5%8A%A8%E5%BC%80%E5%8F%91 baidu_triples6_original.txt
代码走读 /item/%E4%BB%A3%E7%A0%81%E8%B5%B0%E8%AF%BB baidu_triples7_original.txt
基准测试 /item/%E5%9F%BA%E5%87%86%E6%B5%8B%E8%AF%95 baidu_triples7_original.txt
域测试 /item/%E5%9F%9F%E6%B5%8B%E8%AF%95 baidu_triples7_original.txt
代码审查 /item/%E4%BB%A3%E7%A0%81%E5%AE%A1%E6%9F%A5 baidu_triples10_original.txt
恢复测试 /item/%E6%81%A2%E5%A4%8D%E6%B5%8B%E8%AF%95 baidu_triples11_original.txt
健壮性测试 /item/%E5%81%A5%E5%A3%AE%E6%80%A7%E6%B5%8B%E8%AF%95 baidu_triples12_original.txt
用户界面测试 /item/%E7%94%A8%E6%88%B7%E7%95%8C%E9%9D%A2%E6%B5%8B%E8%AF%95 baidu_triples13_original.txt

"""

# 爬取单个页面
# url = base_url + his[-1]
# data = urlopen(url).read().decode('utf-8')
# soup = BeautifulSoup(data,"lxml")
# summer = soup.find("div",{"class":"lemma-summary"}).get_text().split("。")[0]
# print(summer)

# 批量爬取
while len(his) != 0:
    if his[-1] in finished_list:
        his.pop()
        continue
    url = base_url + his[-1]

    data = urlopen(url).read().decode('utf-8')
    # print(data)
    soup = BeautifulSoup(data,"lxml")

    head_entity = soup.find("h1")
    relationships = soup.find_all("dt",{"class":"basicInfo-item name"})
    tail_entity = soup.find_all("dd",{"class":"basicInfo-item value"})
    summer = soup.find("div",{"class":"lemma-summary"})

    """
    print(head_entity)
    print(relationships)
    print(tail_entity)
    """
    h = head_entity.get_text()
    print(h, '    url: ', his[-1])
    his_file.write(str(h) + '\t' + str(his[-1]) +'\n')

    finished_list.append(his[-1])
    his.pop()

    # 输出三元组
    if summer:
        summer = summer.get_text().split("。")[0].strip()
        f.write(str(h)+'\t'+'定义'+'\t'+str(summer)+'\n')

    if relationships.__len__() == tail_entity.__len__():
        for i in range(0,relationships.__len__()):
            r = relationships[i].get_text()
            r = str(r).strip() #remove \n \t 
            r = format_r(r)
            if r in garbage:
                continue
            t = tail_entity[i].get_text()
            t = str(t).strip()
            t = format_entity(t)
            f.write(str(h)+'\t'+str(r)+'\t'+str(t)+'\n')

    content = soup.find_all("div",{"class":"para"})
    # print(content)
    for p in content:
        # print(p)
        sub_urls = p.find_all("a", {"target": "_blank", "href": re.compile("/item/")})
        for sub_url in sub_urls:
            # print(sub_url)
            his.insert(0, sub_url['href'])

f.close()
his_file.close()