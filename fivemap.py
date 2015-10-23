# coding=utf-8
__author__ = 'moons'
class Mp:
    # mmap :
    #       0 is None
    mmap = []
    max_row = 16
    max_col = 20

    #create the mmap
    def __init__(self):
        for i in range(0, 17):
            a = [0 for x in range(0, 19)]
            self.mmap.append(a)

    def setPos(self, row, col, color):
        try:
            assert self.max_row > row and row >= 0\
                or self.max_col > col or col >= 0, "out of mmap!!"
        except AssertionError, args:
            print '%s: %s' % (args.__class__.__name__, args)
            print '%s %s | %s %s' % (self.max_row, self.max_col, row, col)
        self.mmap[row][col] = color
        #self.print_map()

    def print_map(self):
        for i in range(0, 17):
            print self.mmap[i]

    def check(self):
        for i in range(0, 17):
            for j in range(0, 19):
                # 没有棋子
                if self.mmap[i][j] == 0:
                    continue
                # 有棋子
                if self.check_row(i, j) or \
                self.check_col(i, j) or\
                self.check_x1(i, j) or\
                self.check_x2(i, j):
                    return (i,j)
        return None

    def check_row(self, x, y):
        cnt = 0
        for j in range(y+1, y+5):
            if j > self.max_col:
               break;
            if self.mmap[x][j] == self.mmap[x][y]:
                cnt = cnt + 1
            else:
                break
        for j in range(y-1, y-5, -1):
            if j <= 0:
                break;
            if self.mmap[x][j] == self.mmap[x][y]:
                cnt = cnt + 1
            else:
                break
        return True if cnt == 4 else False

    def check_col(self, x, y):
        cnt = 0
        for i in range(x+1, x+5):
            if i > self.max_row:
                break
            if self.mmap[i][y] == self.mmap[x][y]:
                cnt = cnt + 1
            else:
                break
        for i in range(x-1, x-5, -1):
            if i <= 0:
                break
            if self.mmap[i][y] == self.mmap[x][y]:
                cnt = cnt + 1
            else:
                break
        return True if cnt == 4 else False

    def check_x1(self, x, y):
        cnt = 0
        for i in range(1, 5):
            if x - i <= 0 or y - i <= 0:
                break
            if self.mmap[x-i][y-i] == self.mmap[x][y]:
                cnt = cnt + 1
            else:
                break
        for i in range(1, 5):
            if x + i > self.max_row or y + i > self.max_col:
                break
            if self.mmap[x+i][y+i] == self.mmap[x][y]:
                cnt = cnt + 1
            else:
                break
        return True if cnt == 4 else False

    def check_x2(self, x, y):
        cnt = 0
        for i in range(1, 5):
            if x - i <= 0 or y + i > self.max_col:
                break
            if self.mmap[x-i][y+i] == self.mmap[x][y]:
                cnt = cnt + 1
            else:
                break
        for i in range(1, 5):
            if x + i > self.max_row or y - i < 0:
                break
            if self.mmap[x+i][y-i] == self.mmap[x][y]:
                cnt = cnt + 1
            else:
                break
        return True if cnt == 4 else False



