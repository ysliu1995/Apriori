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


def Find_In_Tree(root, a, v1, v2, level):
    print(root, a, v1, v2, level)
    if v1 == []:                                    #一開始丟進來
        if len(v2) == level:                        #一開始只有v2有值
            count = len(v2)
            p = root
            for i in range(count):
                p = p.position[v2[i] % 3]
                if p == None:
                    break
                elif p.child == []:
                    pass
                else:
                    if v2 in p.child:
                        if frozenset(v2) not in a:
                            a[frozenset(v2)] = 1
                        else:
                            a[frozenset(v2)] += 1
                        break
        elif len(v2) > level:                       #如果v2大於此階段的len(itemset)
            p = root
            split = v2[:-(level-1)]
            for i in range(len(split)):
                aa , bb = v2[i:i+1], v2[i+1:]
                for i in aa:
                    p = p.position[i]
                Find_In_Tree(p, a, aa, bb, level)
    else:                                           #不是一開始
        p = root
        if len(v2) == level-1:                      
            ans = v1 + v2
            count = len(v2)
            for i in range(count):
                p = p.position[v2[i] % 3]
                if p == None:
                    break
                elif p.child == []:
                    pass
                else:
                    if ans in p.child:
                        if frozenset(ans) not in a:
                            a[frozenset(ans)] = 1
                        else:
                            a[frozenset(ans)] += 1
                        break
        else:
            flag = v1
            print(flag)
            split = v2[:-(level-1)]
            # print(split[0:1])
            for i in range(len(split)):
                aa , bb = v1 + v2[i:i+1], v2[i+1:]
                print(aa,bb)
                for i in aa[len(flag):]:
                    p = p.position[i]
                Find_In_Tree(p, a, aa, bb, level)
        


if __name__ == '__main__':

    data = [[1,4,5],[1,2,4],[4,5,7],[1,2,5],[4,5,8],[1,5,9],[1,3,6],[2,3,4],[5,6,7],[3,4,5],[3,5,6],[3,5,7],[6,8,9],[3,6,7],[3,6,8]]

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
    
    customer = [1,2,4,5]

    a = {}
    # v1 =[]
    # v2 = [1,2,4,5]
    # v2 = [1,2,4]
    v1 = [1]
    v2 = [2,3,4,5]
    Find_In_Tree(root.position[v1[0]], a, v1, v2, 3)
    print(a)

    