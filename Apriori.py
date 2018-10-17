import numpy as np
import pandas as pd
import time

support = 0.2
confidence = 0.5
total_itemset = {}


df = pd.read_csv('dataset.csv')
dataset = []
for i in df.values:
    tmp = []
    for j in range(len(i)):
        if i[j]:
            tmp.append(j+1)
    dataset.append(tmp)
# print(dataset)

# dataset = []
# dataset.append([1, 3, 4])
# dataset.append([2, 3, 5])
# dataset.append([1, 2, 3, 5])
# dataset.append([2, 5])
# print(dataset)


def creatC(data):
    c = []
    for l in data:
        for i in l:
            if i not in c:
                c.append(i)
    return [[i] for i in sorted(c)]
    # return sorted(c)

def checkinside(a, b):
    if (a & b) == a:
        return True
    else:
        False

def GenLk(itemset, dataset, support):
    #每個itemset在DB裏頭的加總
    s = time.time()
    a = {}
    for d in dataset:
        for item in itemset:
            if checkinside(frozenset(item), frozenset(d)):  #item在不在DB當中
                if frozenset(item) not in a:                #item在不在itemset當中
                    a[frozenset(item)] = 1
                else:
                    a[frozenset(item)] += 1
    e = time.time()
    print('計數所花時間：{}'.format(e-s))
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



start = time.time()

itemset = creatC(dataset)
i = 1
while(1):
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

# for relation in total_itemset:
#     if len(relation) > 1:
#         # print(relation)
#         re_list = list(relation)