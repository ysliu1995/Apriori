import itertools
import numpy as np
import pandas as pd
import time

class FPtree:

    def __init__(self):
        self.parent = None
        self.child = []
        self.item = None
        self.cnt = 0
    



def Load_Data():

    # df = pd.read_csv('dataset.csv')
    # dataset = []
    # for i in df.values:
    #     tmp = []
    #     for j in range(len(i)):
    #         if i[j]:
    #             tmp.append(j+1)
    #     dataset.append(tmp)

    dataset = []
    dataset.append(['a', 'c', 'd', 'f', 'g', 'i', 'm', 'p'])
    dataset.append(['a', 'b', 'c', 'f', 'i', 'm', 'o'])
    dataset.append(['b', 'f', 'h', 'j', 'o'])
    dataset.append(['b', 'c', 'k', 's', 'p'])
    dataset.append(['a', 'c', 'e', 'f', 'l', 'm', 'n', 'p'])

    return dataset

def creatC(data):
    c = []
    for l in data:
        for i in l:
            if i not in c:
                c.append(i)
    return [i for i in sorted(c)]

def GenLk(itemset, dataset, support):
    #每個itemset在DB裏頭的加總
    a = {}
    for d in dataset:
        for item in itemset:
            if item in d:  #item在不在DB當中
                if item not in a:                #item在不在itemset當中
                    a[item] = 1
                else:
                    a[item] += 1
    # print(a)
    #去掉support以下的itemset
    tmp = []
    for item in a:
        if a[item] < 3:
            tmp.append(item)
    for t in tmp:
        del a[t]
    # print(a)
    return a

def Reorder(dataset, a):
    reorder = []
    for customer in dataset:
        tmp = []
        for item in customer:
            if item in a:
                tmp.append(a[item])
            else:
                tmp.append(0)
        dic = {'item':customer,
                'value':tmp}
        df = pd.DataFrame(dic)
        df = df.sort_values(by=['value'], ascending=False)
        df = df[df['value']>0]
        reorder.append(list(df['item'].values))
    return reorder

def CreateFPtree(reorder, a):

    pointer = list(a.keys())
    store = {}
    for i in pointer:
        store[i] = []


    root = FPtree()
    for customer in reorder:
        # print(customer)
        p = root
        for item in customer:
            tmp = p
            # print(item, tmp.child)
            if tmp.child == []:
                n = FPtree()
                tmp.child.append(n)
                n.parent= tmp
                n.item = item
                n.cnt += 1
                store[item].append(n)
                p = n
            else:
                flag = 0
                for i in tmp.child:
                    if i.item == item:
                        i.cnt += 1
                        p = i
                        flag = 1
                        break
                if flag == 0:
                    n = FPtree()
                    tmp.child.append(n)
                    n.parent= tmp
                    n.item = item
                    n.cnt += 1
                    store[item].append(n)
                    p = n
        # print('****************')
    return root, store


support = 0.5

if __name__ == '__main__':

    dataset = Load_Data()
    print(dataset)
    C = creatC(dataset)
    a = GenLk(C, dataset, support)
    # print(a)
    reorder = Reorder(dataset, a)
    print(reorder)
    print('-----------------')

    root, store = CreateFPtree(reorder, a)
    
    ans = {}
    for i in list(a):
        # print(store[i])
        tmp0 = []
        tmp1 = []
        tmp2 = []
        for n in store[i]:
            # print(n)
            p = n
            tmp0.append(p.item)
            cnt = p.cnt
            t = []
            p = p.parent
            while p.item != None:
                t.append(p.item)
                p = p.parent
            
            tmp1.append(t)
            tmp2.append(cnt)
        print(tmp0)
        print(tmp1)
        print(tmp2)
        if tmp2[0] <3:
            s = set(tmp1[0])
            for k in tmp1[1:]:
                s = s.intersection(set(k))
            print(s)
            if s == set():
                pass
            else:
                # print('-')
                # print(list(set(tmp0[0]))+list(s))
                for j in range(len(list(s))):
                    com = list(itertools.combinations(s, j+1))
                    for c in com:
                        d = list(tmp0[0]) + list(com)
                        ans[tuple(d)] = sum(tmp2)

        else:
            if tmp1[0] != []:
                s = tmp1[0]
                # ans[tuple(tmp1[0])] = tmp2[0]
                for j in range(len(list(s))):
                    com = list(itertools.combinations(s, j+1))
                    for c in com:
                        d = list(tmp0[0]) + list(com)
                        ans[tuple(d)] = sum(tmp2)
        print(ans)
        print('---------')
    print(ans)
    
