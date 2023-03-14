import jieba.posseg as pseg
import sys
import codecs
sys.path.append('..')
import data_prepare.mfile as mfile

f = codecs.open('../data/relation_subwords.txt',"w","utf-8")

relations_list = mfile.read_file('../data/all_relations.txt')[0]

for x in relations_list:
    words = pseg.cut(x, use_paddle=True) #paddle模式
    for w in words:
        f.write(w.word + '\t' + w.flag + '\t' + x + '\n')


f.close()