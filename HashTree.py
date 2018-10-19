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
    if len(fixed)+len(transaction) == level:
        compare = fixed + transaction
        if compare in p.position[transaction[0] % 3].child:
            if frozenset(compare) not in a:
                a[frozenset(compare)] = 1
            else:
                a[frozenset(compare)] += 1
        else:
            print('數量已到達但沒有找到')
    else:
        split = transaction[:-(level-len(fixed)-1)]
        print('split : {}'.format(split))
        if split == []:
            print('split為空')
            ls = itertools.combinations(transaction, level-len(fixed))
            for com in ls:
                compare = fixed + list(com)
                print(compare, list(com)[0])
                if compare in p.position[list(com)[0] % 3].child:
                    if frozenset(compare) not in a:
                        a[frozenset(compare)] = 1
                    else:
                        a[frozenset(compare)] += 1
                else:
                    print('下面樹有值但沒有找到')
        else:
            for s in split:
                print(s)
                if p.position[s % 3] == None:
                    print('下面沒有樹')
                elif p.position[s % 3].child == []:
                    print('下面的樹split了')
                    aa = fixed + [s]
                    index = transaction.index(s)
                    bb = transaction[index+1:]
                    print(aa, bb)
                    Find_In_Tree(p.position[s % 3], a, aa, bb, level)
                else:
                    print('下面樹有值')
                    ls = itertools.combinations(transaction[transaction.index(s)+1:], level-len(fixed)-1)
                    for com in ls:
                        print(com)
                        compare = fixed + [s] + list(com)
                        print(compare)
                        if compare in p.position[s % 3].child:
                            if frozenset(compare) not in a:
                                a[frozenset(compare)] = 1
                            else:
                                a[frozenset(compare)] += 1
                        else:
                            print('下面樹有值但沒有找到')
        print('**********')
        


if __name__ == '__main__':

    data = [[1,4,5],[1,2,4],[4,5,7],[1,2,5],[4,5,8],[1,5,9],[1,3,6],[2,3,4],[5,6,7],[3,4,5],[3,5,6],[3,5,7],[6,8,9],[3,6,7],[3,6,8]]
    # data = [[2,3,5],[5,6,7],[3,4,5],[3,5,6],[3,5,7],[6,8,9],[3,6,7],[3,6,8]]
    # data = [[2,3,5],[5,6,7]]
    # data = [[1,4,5],[1,2,4],[4,5,7],[1,2,5],[4,5,8],[1,5,9],[1,3,6]]

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