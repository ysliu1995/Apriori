import itertools
class Tree:

    def __init__(self):
        self.child = []
        self.position = [None] * 3
    
    def insert(self, obj):
        self.child.append(obj)

def CreateTree(data, k):
    root = Tree()
    for item in data:
        index = (item[k-1] % 3)
        p = root
        s = k
        flag = 0
        if p.position[index] == None:
            p.position[index] = Tree()
            p.position[index].insert(item)
        elif p.position[index].child == []:
            while p.position[item[s-1] % 3].child == [] :
                index = (item[s-1] % 3)
                p = p.position[index]
                s += 1
                if p.position[item[s-1] % 3] == None:
                    flag = 1
                    break
            if flag == 0:
                p.position[item[s-1] % 3].insert(item)
                if len(p.position[item[s-1] % 3].child) > 3 and k <= len(data[0]):
                    tmp_data = p.position[item[s-1] % 3].child
                    p.position[item[s-1] % 3]= CreateTree(tmp_data, s+1)
            else:
                p.position[item[s-1] % 3] = Tree()
                p.position[item[s-1] % 3].insert(item)
        else:
            p.position[index].insert(item)
            if len(p.position[index].child) > 3 and k <= len(data[0]):
                tmp_data = p.position[index].child
                p.position[index] = CreateTree(tmp_data, k+1)
        

    return root


def Find_In_Tree(root, a, fixed, transaction, level):
    print('---------------------------------------------')
    print(root, a, fixed, transaction, level)
    p = root
    split = transaction[:-(level-len(fixed)-1)]
    print(split)
    for s in split:
        print(s)
        if p.position[s % 3] == None:
            print(123)
        elif p.position[s % 3].child == []:
            print(456)
            aa = s
            index = transaction.index(aa)
            bb = transaction[index+1:]
            # print(aa, bb)
            Find_In_Tree(p.position[s % 3], a, [aa], bb, level)
        else:
            print(789)
    print('************')
    # print(root, a, transaction, level, fixed)
    # p = root
    # split = transaction[:-(level-2)]
    # print(fixed, transaction, split)                        #fixed 已固定, split 可分離出來結合的
    # if len(fixed) + len(transaction) == level:
    #     compare = fixed + transaction
    #     if compare in p.position[len(fixed)+1 % 3].child:
    #         if frozenset(compare) not in a:
    #             a[frozenset(compare)] = 1
    #         else:
    #             a[frozenset(compare)] += 1
    # else:
    #     # if len(fixed) == level-1:
    #     #     for i in transaction:
    #     #         compare = pre + [i]
    #     #             if compare in p.position[split[i] % 3].child:
    #     #                 if frozenset([i]) not in a:
    #     #                     a[frozenset([i])] = 1
    #     #                 else:
    #     #                     a[frozenset([i])] += 1
    #     for i in range(len(split)):
    #         pre = fixed + [split[i]]
    #         print(split[i], pre)
    #         if p.position[split[i] % 3] == None:
    #             pass
    #         elif p.position[split[i] % 3].child == []:
    #             # print(pre, transaction[i+1:])
    #             Find_In_Tree(p.position[split[i] % 3], a, transaction[i+1:], level, pre)
    #         else:
    #             ls = itertools.combinations(transaction[i+1:], level-len(pre))
    #             for com in ls:
    #                 print(com)
    #                 # compare = pre + list(com)
    #                 # if compare in p.position[split[i] % 3].child:
    #                 #     if frozenset(compare) not in a:
    #                 #         a[frozenset(compare)] = 1
    #                 #     else:
    #                 #         a[frozenset(compare)] += 1
    #             print('-------------')
        


if __name__ == '__main__':

    # data = [[1,4,5],[1,2,4],[4,5,7],[1,2,5],[4,5,8],[1,5,9],[1,3,6],[2,3,4],[5,6,7],[3,4,5],[3,5,6],[3,5,7],[6,8,9],[3,6,7],[3,6,8]]
    # data = [[3,4,5],[3,5,6],[3,5,7],[6,8,9],[3,6,7],[3,6,8]]
    # data = [[2,3,4],[5,6,7]]
    data = [[1,4,5],[1,2,4],[4,5,7],[1,2,5],[4,5,8],[1,5,9],[1,3,6]]

    root = CreateTree(data, 1)
    # print('-----------------------------')
    # print(root.position[0].position[0].child)
    # print(root.position[0].position[1].child)
    # print(root.position[0].position[2].child)
    # print(root.position[1].position[0].child)
    # print(root.position[1].position[1].child)
    # print(root.position[1].position[2].position[0].child)
    # print(root.position[1].position[2].position[1].child)
    # print(root.position[1].position[2].position[2].child)
    # print(root.position[2].child)
    # print('-----------------------------')
    

    a = {}

    transaction = [1,2,3,5,6]
    Find_In_Tree(root, a, [], transaction, 3)
    print(a)

    