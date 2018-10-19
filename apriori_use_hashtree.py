import numpy as np
import pandas as pd
import itertools
import time

class Tree:

    def __init__(self):
        self.child = []
        self.position = [None] * 10
    
    def insert(self, obj):
        self.child.append(obj)
    
    

def CreateTree(data, k):
    root = Tree()
    for item in data:
        index = (item[k-1] % 10)
        p = root
        s = k
        flag = 0
        if p.position[index] == None:
            p.position[index] = Tree()
            p.position[index].insert(item)
        elif p.position[index].child == []:
            while p.position[item[s-1] % 10].child == [] :
                index = (item[s-1] % 10)
                p = p.position[index]
                s += 1
                if p.position[item[s-1] % 10] == None:
                    flag = 1
                    break
            if flag == 0:
                p.position[item[s-1] % 10].insert(item)
                if len(p.position[item[s-1] % 10].child) > 10 and s < len(data[0]):
                    tmp_data = p.position[item[s-1] % 10].child
                    p.position[item[s-1] % 10]= CreateTree(tmp_data, s+1)
            else:
                p.position[item[s-1] % 10] = Tree()
                p.position[item[s-1] % 10].insert(item)
        else:
            p.position[index].insert(item)
            if len(p.position[index].child) > 10 and k < len(data[0]):
                tmp_data = p.position[index].child
                p.position[index] = CreateTree(tmp_data, k+1)
                

    return root


def Find_In_Tree(root, a, fixed, transaction, level):
    # print('---------------------------------------------')
    # print(root, a, fixed, transaction, level)
    p = root
    if len(fixed)+len(transaction) == level:
        compare = fixed + transaction
        if p.position[transaction[0] % 10] == None:
            pass
        elif compare in p.position[transaction[0] % 10].child:
            if frozenset(compare) not in a:
                a[frozenset(compare)] = 1
            else:
                a[frozenset(compare)] += 1
        # else:
        #     print('數量已到達但沒有找到')
    else:
        split = transaction[:-(level-len(fixed)-1)]
        # print('split : {}'.format(split))
        if split == []:
            # print('split為空')
            ls = itertools.combinations(transaction, level-len(fixed))
            for com in ls:
                compare = fixed + list(com)
                # print(compare, list(com)[0])
                if p.position[list(com)[0] % 10] == None:
                    pass
                elif compare in p.position[list(com)[0] % 10].child:
                    if frozenset(compare) not in a:
                        a[frozenset(compare)] = 1
                    else:
                        a[frozenset(compare)] += 1
                # else:
                    # print('下面樹有值但沒有找到')
        else:
            for s in split:
                # print(s)
                if p.position[s % 10] == None:
                    pass
                    # print('下面沒有樹')
                elif p.position[s % 10].child == []:
                    # print('下面的樹split了')
                    aa = fixed + [s]
                    index = transaction.index(s)
                    bb = transaction[index+1:]
                    # print(aa, bb)
                    Find_In_Tree(p.position[s % 10], a, aa, bb, level)
                else:
                    # print('下面樹有值')
                    ls = itertools.combinations(transaction[transaction.index(s)+1:], level-len(fixed)-1)
                    for com in ls:
                        # print(com)
                        compare = fixed + [s] + list(com)
                        # print(compare)
                        if p.position[s % 10] == None:
                            pass
                        elif compare in p.position[s % 10].child:
                            if frozenset(compare) not in a:
                                a[frozenset(compare)] = 1
                            else:
                                a[frozenset(compare)] += 1
        #                 else:
        #                     print('下面樹有值但沒有找到')
        # print('**********')
    
    


def Load_Data():

    df = pd.read_csv('dataset.csv')
    dataset = []
    for i in df.values:
        tmp = []
        for j in range(len(i)):
            if i[j]:
                tmp.append(j+1)
        dataset.append(tmp)

    # dataset = []
    # dataset.append([1, 3, 4])
    # dataset.append([2, 3, 5])
    # dataset.append([1, 2, 3, 5])
    # dataset.append([2, 5])

    return dataset


def creatC(data):
    c = []
    for l in data:
        for i in l:
            if i not in c:
                c.append(i)
    return [[i] for i in sorted(c)]

def checkinside(a, b):
    if (a & b) == a:
        return True
    else:
        False

def GenLk(itemset, dataset, support):
    a = {}

    s = time.time()
    root = CreateTree(itemset, 1)
    e = time.time()
    print('建樹所花時間：{}'.format(e-s))
    
    s = time.time() 
    for transaction in dataset:
        Find_In_Tree(root, a, [], transaction, len(itemset[0]))
    e = time.time()
    print('計數所花時間：{}'.format(e-s))
    # print(a)

    #去掉support以下的itemset
    s = time.time()
    tmp = []
    for item in a:
        if a[item] < len(dataset) * support:
            tmp.append(item)
    for t in tmp:
        del a[t]
    e = time.time()
    print('剪枝所花時間：{}'.format(e-s))

    #將Li加入total當中
    total_itemset.update(a)

    ans = []
    for i in a.keys():
        ans.append(sorted(list(i)))
    return sorted(ans)

def GenCk(L):
    # print(L)
    #排列組合
    s = time.time()
    c = []
    for i in range(len(L)):
        for j in range(i+1,len(L)):
            union = set(L[i]) | set(L[j])
            c.append(union)
    
    C = [sorted(list(i)) for i in c]

    e = time.time()
    print('排列組合所花時間：{}'.format(e-s))

    #將itemset中重複的以及去掉不屬於此階段itemset數量的候選
    s = time.time()

    C_tmp = []
    for i in C:
        if len(i) == len(L[0])+1:
            C_tmp.append(tuple(i))
    C = [list(i) for i in list(set(C_tmp))]

    e = time.time()
    print('去掉重複的所花時間：{}'.format(e-s))

    return C


support = 0.2
confidence = 0.9
total_itemset = {}



dataset = Load_Data()
itemset = creatC(dataset)
i = 1
while(1):
# for i in range(2):
    start = time.time()

    L = GenLk(itemset, dataset, support)
    # print('L : {}'.format(L))
    print(len(L))
    if len(L) <= 1:
        break
    C = GenCk(L)
    # print('C : {}'.format(C))
    print(len(C))
    itemset = C

    end = time.time()
    print('第{}層花費時間:'.format(i), end-start)
    i += 1

    print('-------------------------')

print(total_itemset)
print('********************')

for subset in total_itemset:
    if len(subset) > 1:
        subset = list(subset)
        # print(subset)
        for j in range(int(len(subset)/2)):
            ls = itertools.combinations(subset, j+1)
            for com in ls:
                tmp = subset
                # print(list(com), list(set(tuple(subset)).difference(set(com))))
                con1 = total_itemset[frozenset(subset)]/total_itemset[frozenset(list(com))]
                if con1 >= confidence:
                    print('{}->{}, confidence : {}'.format(list(com), list(set(tuple(subset)).difference(set(com))), con1))
                con2= total_itemset[frozenset(subset)]/total_itemset[frozenset(list(set(tuple(subset)).difference(set(com))))]
                if con2 >= confidence:
                    print('{}->{}, confidence : {}'.format(list(set(tuple(subset)).difference(set(com))), list(com), con2))
        # print('-')
print('********************')

