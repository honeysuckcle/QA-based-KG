import copy
import sys
sys.path.append("..")
from brain.function import function

class Template:
    # model = [0,0,0]
    # tail_arr = []
    # relation_arr = []
    # head_arr = []

    def __init__(self, his = None):
        self.model = [0,0,0]
        self.tail_arr = []
        self.relation_arr = []
        self.head_arr = []
        self.history = his

    def update_model(self):
        self.model[0] = len(self.head_arr)
        self.model[1] = len(self.relation_arr)
        self.model[2] = len(self.tail_arr)


    def get_type(self):
        res = 0
        for i in self.model:
            if i > 1:
                res = res * 3 + 2
            else:
                res = res * 3 + i
        return res

    def get_head(self, i = 0):
        return self.head_arr[i]

    def get_relation(self, i = 0):
        return self.relation_arr[i]
    
    def get_tail(self, i = 0):
        return self.tail_arr[i]

    def get_model(self):
        return self.model

# 返回值 二进制
    def add(self, word, flag, his_flag = 0, id_fliter = 7):
        res = 0
        if flag == 'hh':
            if id_fliter & 4 != 0:
                if word not in self.head_arr:
                    self.head_arr.append(word)
                res = 4 | his_flag
        if flag == 'rr':
            if id_fliter & 5 != 0:
                if word not in self.relation_arr:
                    self.relation_arr.append(word)
                res = 2 | his_flag
        if flag == 'tt':
            if id_fliter & 6 != 0:
                if word not in self.tail_arr:
                    self.tail_arr.append(word)
                res = 1 | his_flag
        self.update_model()
        return res

    def display(self):
        print('model:', self.model)
        print('head:', self.head_arr)
        print('relation:', self.relation_arr)
        print('tail:', self.tail_arr)

    def deal(self):
        # print("model:", str(self.model))
        self.update_model()
        print("type:", self.get_type())
        return function[self.get_type()](self)

        
def copy_Template(orig):
    t = Template()
    t.model = copy.copy(orig.model)
    t.head_arr = copy.copy(orig.head_arr)
    t.relation_arr = copy.copy(orig.relation_arr)
    t.tail_arr = copy.copy(orig.tail_arr)
    t.history = copy.copy(orig.history)
    return t