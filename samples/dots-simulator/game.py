
import random
import math

class Board:
    def __init__(self, rows, cols, gen):
        assert isinstance(gen, RandomGen)

        self.data = []
        self.rows = rows
        self.cols = cols
        self.gen = gen
        for j in range(rows):
            row = []
            self.data.append(row)
            for i in range(cols):
                row.append(Tile(j, i))

        for j in range(rows):
            for i in range(cols):
                x = next(gen)
                c = Dot(x)
                self.put(i, j, c)

    def get(self, i, j):
        return self.data[j][i]

    def put(self, i, j, cookie):
        assert isinstance(cookie, Dot)
        t = self.get(i, j)
        assert isinstance(t, Tile)
        t.put(cookie)

    def remove(self, conn):
        assert isinstance(conn, Connection)

        for p in conn:
            i, j = p
            t = self.get(i, j)
            assert isinstance(t, Tile)

            t.removeCookie()


    def move(self, src, dst):
        i, j = src
        p, q = dst
        srcTile = self.get(i, j)
        dstTile = self.get(p, q)

        assert isinstance(srcTile, Tile)
        assert isinstance(dstTile, Tile)
        assert srcTile.cookie is not None, "src tile can't be empty in move(): {}".format(srcTile)
        assert dstTile.cookie is None, "dst tile must be empty in move(): {}".format(dstTile)

        srcCookie = srcTile.cookie
        assert isinstance(srcCookie, Dot)

        srcTile.removeCookie()
        dstTile.put(srcCookie)

    def fillHolesByGravity(self, debug = False):
        for i in range(self.cols):
            for j in range(self.rows):
                t = self.get(i, j)
                if t.cookie is None:
                    # i,j is empty
                    if debug:
                        print("{} is empty".format((i, j)))
                    for q in range(j, 0, -1):
                        # move i,q-1 to i,q
                        srcPos = (i, q-1)
                        dstPos = (i, q)
                        srcTile = self.get(srcPos[0], srcPos[1])
                        if srcTile.cookie is not None:
                            if debug:
                                print("moving {} to {}".format(srcPos, dstPos))
                            self.move(srcPos, dstPos)
                        else:
                            if debug:
                                print("skipping {}".format(srcPos))

            if debug:
                print("finished col %d" % i)

    def fillHolesWithNewCookies(self, debug = False):
        for i in range(self.cols):
            for j in range(self.rows):
                t = self.get(i, j)
                if t.cookie is None:
                    # i,j is empty
                    if debug:
                        print("{} is empty".format((i, j)))

                    c = Dot(next(self.gen))
                    t.put(c)

    def __str__(self):
        result = "Board {}x{}:\n".format(self.cols, self.rows)

        row1 = self.data[0]
        result += "\t   "
        for i in range(len(row1)):
            result += "%d " % i
        result += '\n'

        for j, row in enumerate(self.data):
            result += '\t%d  ' % j
            for x in row:
                assert isinstance(x, Tile)
                if x.cookie is not None:
                    result += x.cookie.color
                else:
                    result += '_'

                result += ' '
            result += '\n'
        return result

class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.cookie = None

    def put(self, cookie):
        assert isinstance(cookie, Dot)
        assert self.cookie is None, "Tile must be empty in put()!"

        self.cookie = cookie
        cookie.tile = self

    def removeCookie(self):
        if self.cookie is not None:
            self.cookie.removeFromTile()

    def __str__(self):
        if self.cookie is not None:
            return "<Tile .cookie {self.cookie}, .row {self.row}, .col {self.col}>".format(self=self)
        return "<Tile .cookie None, .row {self.row}, .col {self.col}>".format(self=self)

class Dot:
    def __init__(self, color):
        self.color = color
        self.tile = None

    def removeFromTile(self):
        if self.tile is not None:
            tile = self.tile
            assert isinstance(tile, Tile)
            tile.cookie = None
            self.tile = None

    def __str__(self):
        if self.tile is not None:
            return "<Cookie .color '{self.color}', .tile {tile.row}, {tile.col}>".format(self=self, tile=self.tile)
        return "<Cookie .color '{self.color}', .tile None>".format(self=self)

class RandomGen:
    def __init__(self, f, limit=None):
        assert isinstance(f, dict)
        s = 0
        self.cdf = {}
        for x in sorted(f.keys()):
            s += f[x]
            # print(x, f[x] * 100, s)
            if s > 1.0:
                print("Warning: sum {} exceed >1.0 at letter '{}'".format(s, x))
            self.cdf[x] = s

        self.limit = limit
        self.count = 0

        # see CDF https://en.wikipedia.org/wiki/Cumulative_distribution_function

        # print("cdf")
        # for a in sorted(self.cdf.keys()):
        #     print(a, self.cdf[a] * 100)


    def __iter__(self):
        return self

    def __next__(self):
        if self.limit is not None:
            if self.count > self.limit:
                raise StopIteration()

        x = random.uniform(0, 1.0)
        for a in sorted(self.cdf.keys(), key=lambda x: self.cdf[x]):
            if x < self.cdf[a]:
                self.count += 1
                return a
            #print(a, self.cdf[a])

class Connection:
    def __init__(self):
        self.positions = []

    def append(self, pos):
        self.positions.append(pos)

    def __contains__(self, item):
        return item in self.positions

    def __len__(self):
        return len(self.positions)

    def __iter__(self):
        return iter(self.positions)

    def __str__(self):
        result = ''
        first = True
        for p in self.positions:
            if not first:
                result +=" -> "
            else:
                first = False
            result += " {}".format(p)
        return result

    def __getitem__(self, index):
        return self.positions[index]

def findAnyConnection(b, pos, depth = 0, connection = None, debug=False):
    assert isinstance(b, Board)
    assert isinstance(pos, tuple)

    i, j = pos
    t = b.get(i, j)
    assert isinstance(t, Tile)
    assert t.cookie is not None

    if debug:
        print('  ' * depth, t)

    if connection is None:
        connection = Connection()

    connection.append(pos)

    searchOrders = [(t.col + 1, t.row), (t.col - 1, t.row), (t.col, t.row - 1), (t.col, t.row + 1)]
    random.shuffle(searchOrders)

    for nextPos in searchOrders:
        i, j = nextPos
        if 0 <= i < b.cols and 0 <= j < b.rows:
            a = b.get(i, j)
            assert isinstance(a, Tile)
            if nextPos not in connection and a.cookie is not None:
                if t.cookie.color == a.cookie.color:
                    findAnyConnection(b, nextPos, depth= depth + 1, connection= connection)
                    break

    return connection


def findAnyValidConnection(b):
    assert isinstance(b, Board)

    result = None
    nattempt = 0
    while nattempt < 100:
        i = math.floor(random.uniform(0, b.cols))
        j = math.floor(random.uniform(0, b.rows))
        conn = findAnyConnection(b, (i, j))
        if len(conn) >= 3:
            result = conn
            break
        nattempt += 1

    return result

class Game:
    def __init__(self, b):
        assert isinstance(b, Board)
        self.board = b

    def playOnce(self, debug=False):
        result = None
        conn = findAnyValidConnection(self.board)
        if conn is None:
            print("can't find any connection after max attempt")
        else:
            if debug:
                print("connection found.", conn)
            i, j = conn[0]
            t = self.board.get(i, j)
            assert isinstance(t, Tile)
            result = (t.cookie.color, len(conn))
            self.board.remove(conn)

        if conn is not None:
            if debug:
                print("post removal {}".format(self.board))

            self.board.fillHolesByGravity()
            if debug:
                print("post fillHolesByGravity {}".format(self.board))

            self.board.fillHolesWithNewCookies()
            if debug:
                print("post fillHolesWithNewCookies {}".format(self.board))

        return result

    def play(self, limit=30):
        stat = {}
        for i in range(limit):
            print("iteration %d" % (i + 1))
            color, count = self.playOnce()
            if color not in stat:
                stat[color] = 0
            stat[color] += count
            print('-'*60)

        print("game stat:", stat)
        return stat



