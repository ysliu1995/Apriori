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


if __name__ == '__main__':

    data = [[1,4,5],[1,2,4],[4,5,7],[1,2,5],[4,5,8],[1,5,9],[1,3,6],[2,3,4],[5,6,7],[3,4,5],[3,5,6],[3,5,7],[6,8,9],[3,6,7],[3,6,8]]

    root = CreateTree(data, 1)
    print('-----------------------------')
    print(root.position[0].position[0].child)
    print(root.position[0].position[1].child)
    print(root.position[0].position[2].child)
    print(root.position[1].position[0].child)
    print(root.position[1].position[1].child)
    print(root.position[1].position[2].position[0].child)
    print(root.position[1].position[2].position[1].child)
    print(root.position[1].position[2].position[2].child)
    print(root.position[2].child)
    
    