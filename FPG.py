import itertools
import numpy as np
import pandas as pd
import time

min_support = 2
ans = []



class FPtree:

    def __init__(self):
        self.parent = None
        self.child = []
        self.item = None
        self.cnt = 0


def CreateInitSet(dataset):
    dic = {}
    for i in dataset:
        dic[frozenset(i)] = 1
    return dic

def Load_Data():

    # df = pd.read_csv('dataset.csv')
    # dataset = []
    # for i in df.values:
    #     tmp = []
    #     for j in range(len(i)):
    #         if i[j]:
    #             tmp.append(j+1)
    #     dataset.append(tmp)

    # dataset = []
    # dataset.append(['a', 'c', 'd', 'f', 'g', 'i', 'm', 'p'])
    # dataset.append(['a', 'b', 'c', 'f', 'i', 'm', 'o'])
    # dataset.append(['b', 'f', 'h', 'j', 'o'])
    # dataset.append(['b', 'c', 'k', 's', 'p'])
    # dataset.append(['a', 'c', 'e', 'f', 'l', 'm', 'n', 'p'])

    # dataset = []
    # dataset.append(['Milk', 'Bread', 'Beer'])
    # dataset.append(['Bread', 'Coffee'])
    # dataset.append(['Bread', 'Egg'])
    # dataset.append(['Milk', 'Bread', 'Coffee'])
    # dataset.append(['Milk', 'Egg'])
    # dataset.append(['Bread', 'Egg'])
    # dataset.append(['Milk', 'Egg'])
    # dataset.append(['Milk', 'Bread', 'Egg', 'Beer'])
    # dataset.append(['Milk', 'Bread', 'Egg'])

    dataset = []
    dataset.append(['A', 'C', 'D'])
    dataset.append(['B', 'C', 'E'])
    dataset.append(['A', 'B', 'C', 'E'])
    dataset.append(['B', 'E'])

    # dataset = []
    # dataset.append([1, 2, 3])
    # dataset.append([3, 4, 2, 1])
    # dataset.append([4, 5, 1])
    # dataset.append([2, 1])

    return dataset

def Reorder(dataset, min_support):

    # print(dataset)
    dataset = [ sorted(i) for i in dataset]
    # print(dataset)
    # print('--------------')
    itemset_1 = [ i for l in dataset for i in l]
    itemset_1 = list(set(itemset_1))
    # print(itemset_1)

    a = {}
    for d in dataset:
        for item in itemset_1:
            if item in d:                       
                if item not in a:               
                    a[item] = 1
                else:
                    a[item] += 1
    #去掉support以下的itemset
    tmp = [ item for item in a if a[item] < min_support]
    for t in tmp:
        del a[t]
    # print(a)
    
    aa = list(a.keys())
    bb = list(a.values())
    t = []
    for i in range(len(list(a.keys()))):
        tmp = [aa[i],bb[i]]
        t.append(tmp)
    t = sorted(t, key=lambda s : s[-1],reverse = False)
    # print(t)
    # print(t[::-1])

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
    
    # print(reorder)
    
    return reorder, t

def CreateFPtree(reorder, a):

    pointer = [item[0] for item in a]
    store = {}
    for i in pointer:
        store[i] = []

    root = FPtree()
    for customer in reorder:
        p = root
        for item in customer:
            tmp = p
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
    return root, store


def FindPath(item, node_list):
    # print(item)
    # print(node_list)
    tmp1, tmp2 = [], []
    flag = 0
    for n in node_list:
        p = n
        tmp2.append(p.cnt)
        t = []
        p = p.parent
        while p.item != None:
            t.append(p.item)
            p = p.parent
        t = t[::-1]
        if t != []:
            tmp1.append(t)
        else:
            tmp2.pop()
    print('element :', item)
    print('parent :', tmp1)
    print('cnt :', tmp2)
    print('-----')
    new_set = {}
    for k in range(len(tmp1)):
        new_set[frozenset(tmp1[k])] = tmp2[k]
    
    return new_set



def Mining_Frequent_Set(Tree, header_table, list_store, prefix):
    for item in header_table:               #每個元素
        newFreqSet = prefix.copy()
        newFreqSet.add(item[0])
        ans.append(newFreqSet)
        # if item[0] in list_store:
        #     condPattBases = FindPath(item[0], list_store[item[0]])
        #     data = [list(i) for i in condPattBases]
        #     reorder_data, new_header_table = Reorder(data, min_support)
        #     CondTree, new_list_store = CreateFPtree(reorder_data, new_header_table)
        #     if list_store != None:   
        #         Mining_Frequent_Set(CondTree, header_table, new_list_store, newFreqSet)
        condPattBases = FindPath(item[0], list_store[item[0]])
        data = [list(i) for i in condPattBases]
        reorder_data, new_header_table = Reorder(data, min_support)
        CondTree, new_list_store = CreateFPtree(reorder_data, new_header_table)

    
min_support = 2

if __name__ == '__main__':

    dataset = Load_Data()
    initSet = CreateInitSet(dataset)
    data = [ list(i) for i in initSet]
    print(initSet)
    print(data)
    reorder_data, header_table = Reorder(data, min_support)
    print(header_table)
    # Tree, list_store = CreateFPtree(reorder_data, header_table)
    # Mining_Frequent_Set(Tree, header_table, list_store, set([]))
    # print(ans)
    