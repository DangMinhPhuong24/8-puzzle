from copy import deepcopy
from colorama import  Back

#đích
END = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] 


#in ra lời giải puzzle
def print_puzzle(array):
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print('|', Back.WHITE + ' ' + Back.RESET, end=' ')
            else:
                print('|', i, end=' ')
        print('|')
        
#Lưu trữ các trạng thái
class Node:
    def __init__(self, mt_htai, mt_truoc, g, h, dir):
        self.mt_htai = mt_htai
        self.mt_truoc = mt_truoc
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h


def get_pos(mt, mt1):
    for row in range(len(mt)):
        if mt1 in mt[row]:
            return (row, mt[row].index(mt1))

#tính khoảng cách
def khoangcach(mt1):
    res = 0
    for row in range(len(mt1)):
        for col in range(len(mt1[0])):
            pos = get_pos(END, mt1[row][col])
            res += abs(row - pos[0]) + abs(col - pos[1])
    return res

#Nút liền kề
def getAdjNode(node):
    listNode = []
    pos1 = get_pos(node.mt_htai, 0)

    for dir in DIRECTIONS.keys():
        newPos = (pos1[0] + DIRECTIONS[dir][0], pos1[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.mt_htai) and 0 <= newPos[1] < len(node.mt_htai[0]):
            mt_new = deepcopy(node.mt_htai)
            mt_new[pos1[0]][pos1[1]] = node.mt_htai[newPos[0]][newPos[1]]
            mt_new[newPos[0]][newPos[1]] = 0
            listNode.append(Node(mt_new, node.mt_htai, node.g + 1, khoangcach(mt_new), dir))

    return listNode

#Nút tốt nhất
def bestnut(open_set):
    flag = True
    best1 = ''
    for i in open_set.values():
        if flag or i.f() < best1:
            flag = False
            best = i
            best1 = i.f()
    return best

#Đường đi nhỏ nhất
def ddnn(closed_set):
    node = closed_set[str(END)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.mt_htai
        })
        node = closed_set[str(node.mt_truoc)]
    branch.append({
        'dir': '',
        'node': node.mt_htai
    })
    branch.reverse()
    return branch

#main
def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, khoangcach(puzzle), "")}
    closed_set = {}

    while True:
        n = bestnut(open_set)
        closed_set[str(n.mt_htai)] = n

        if n.mt_htai == END:
            return ddnn(closed_set)

        adj_node = getAdjNode(n)
        for node in adj_node:
            if str(node.mt_htai) in closed_set.keys() or str(node.mt_htai) in open_set.keys() and open_set[
                str(node.mt_htai)].f() < node.f():
                continue
            open_set[str(node.mt_htai)] = node

        del open_set[str(n.mt_htai)]

DIRECTIONS = {'UP': [-1, 0], 'RIGHT': [0, 1],'LEFT': [0, -1],'DOWN': [1, 0],  }
if __name__ == '__main__':
    
    a = main([[0, 2, 3],
               [4, 5, 6],
               [8, 7, 1]])

    print('Vị trí đầu tiên')
    for b in a:
        if b['dir'] != '':
            letter = ''
            if b['dir'] == 'UP':
                letter = '      UP'
            elif b['dir'] == 'RIGHT':
                letter = '    RIGHT'
            elif b['dir'] == 'LEFT':
                letter = '    LEFT'
            elif b['dir'] == 'DOWN':
                letter = '    DOWN'
            print(letter)
        print_puzzle(b['node'])
        print()
    print('tong so buoc : ', len(a) - 1)