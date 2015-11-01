
import random
import math

class Board:
    """
    A Board object represent the Dots puzzle, which is a container for MxN array of tiles. Each tile in turn may contain
    a 'colored' dot or sometimes can be empty as in blockage tile.
    """
    def __init__(self, rows, cols, gen):
        """
        Create a Board the size as specified by rows X cols. A generator object is used to feed the board with dots.
        :param rows: number of rows
        :param cols: number of columns
        :param gen: a generator object
        """
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
        """
        Get a Tile at location i, j.
        :param i: index i
        :param j: index j
        :return: Tile
        """
        return self.data[j][i]

    def put(self, i, j, dot):
        """
        Place a dot at location i, j.
        :param i: index i
        :param j: index j
        :param dot: dot object to be placed
        """
        assert isinstance(dot, Dot)
        t = self.get(i, j)
        assert isinstance(t, Tile)
        t.put(dot)

    def remove(self, conn):
        """
        Remove a connection from the board.
        :param conn: connection object
        """
        assert isinstance(conn, Connection)

        for p in conn:
            i, j = p
            t = self.get(i, j)
            assert isinstance(t, Tile)

            t.removeCookie()


    def move(self, src, dst):
        """
        Move a dot at location src to dst.
        :param src: tuple (i, j) indicating a source location on the Board
        :param dst: tuple (p, q) indicating a destination location on the Board
        """
        i, j = src
        p, q = dst
        srcTile = self.get(i, j)
        dstTile = self.get(p, q)

        assert isinstance(srcTile, Tile)
        assert isinstance(dstTile, Tile)
        assert srcTile.dot is not None, "src tile can't be empty in move(): {}".format(srcTile)
        assert dstTile.dot is None, "dst tile must be empty in move(): {}".format(dstTile)

        srcCookie = srcTile.dot
        assert isinstance(srcCookie, Dot)

        srcTile.removeCookie()
        dstTile.put(srcCookie)

    def fillHolesByGravity(self, debug = False):
        """
        Fill-up gaps on the puzzle (holes) by moving dots from top to fill-up the gap in the bottom.
        :param debug: debugging flag
        """
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
        """
        Fill-up all remaining holes with new dots sourced from the generator object used to create this Board.
        :param debug: debugging flag
        """
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
        """
        Convenient function to let you visualize the contents on the Board.
        """
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
                if x.dot is not None:
                    result += x.dot.color
                else:
                    result += '_'

                result += ' '
            result += '\n'
        return result

class Tile:
    """
    A Tile object represent a valid placement location on Board. A Tile may contain a dot or represent a blockage
    location on the Board in which case is empty. It may also possess other special properties for added effects in
    the game.
    """
    def __init__(self, row, col):
        """
        Init a Tile object at location row, col on the Board.
        :param row: row
        :param col: col
        """

        self.row = row
        self.col = col
        self.dot = None

    def put(self, dot):
        """
        Put a dot onto this Tile.
        :param dot: dot object
        """
        assert isinstance(dot, Dot)
        assert self.dot is None, "Tile must be empty in put()!"

        self.dot = dot
        dot.tile = self

    def removeCookie(self):
        """
        Remove a dot from this Tile.
        """
        if self.dot is not None:
            self.dot.removeFromTile()

    def __str__(self):
        if self.dot is not None:
            return "<Tile .dot {self.dot}, .row {self.row}, .col {self.col}>".format(self=self)
        return "<Tile .dot None, .row {self.row}, .col {self.col}>".format(self=self)

class Dot:
    """
    Dot object represent a 'colored' dot on a Board. Every dots may move through various Tile locations on the Board
    in a Dots game until it is removed from the game such as when a string of connected dots is discovered. A Dot may
    also possess additional special attributes such as "Bomb", "Anchor" for special effects in the game.
    """

    def __init__(self, color):
        """
        Create a Dot object with color in a game.
        :param color: color attribute for the dot.
        :return:
        """
        self.color = color
        self.tile = None

    def removeFromTile(self):
        """
        Remove this Dot from its current Tile location.
        :return:
        """
        if self.tile is not None:
            tile = self.tile
            assert isinstance(tile, Tile)
            tile.dot = None
            self.tile = None

    def __str__(self):
        if self.tile is not None:
            return "<Cookie .color '{self.color}', .tile {tile.row}, {tile.col}>".format(self=self, tile=self.tile)
        return "<Cookie .color '{self.color}', .tile None>".format(self=self)

class RandomGen:
    def __init__(self, f, limit=None):
        """
        Create a Random generator that generate a random sequence of colors based on a requested frequency distribution
        for colors. We are using this generator mainly to populate our Dots puzzle game.

        :param f: Color versus normalized frequency table. E.g. {'a': .25, 'b': .25, 'c': .25, 'd': .25} creates
                  color 'a', 'b', 'c' and 'd' with 25 percent each among the population.
        """
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
    """
    Connection object represent a sequence of locations attempted by the player on a Board. For a valid dots connection
    in Dots game, all dots on locations must share the same color.
    """
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
    """
    Given a starting position search the board (b) for a connected sequence of dots, all dots in a connection must
    shard the same color.
    :param b: Board object
    :param pos: starting position on the Board for the search
    :param depth: current search depth (debugging only)
    :param connection: current connection object in the search
    :param debug: debugging flag
    :return: a Connection object
    """
    assert isinstance(b, Board)
    assert isinstance(pos, tuple)

    i, j = pos
    t = b.get(i, j)
    assert isinstance(t, Tile)
    assert t.dot is not None

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
            if nextPos not in connection and a.dot is not None:
                if t.dot.color == a.dot.color:
                    findAnyConnection(b, nextPos, depth= depth + 1, connection= connection)
                    break

    return connection

def findAnyValidConnection(b):
    """
    Attempt to find a valid dots connection on a board (b) randomly. A valid dots connection must share the same color
    and must satisfy the minimum length of 3. We will be using this routine as our main AI player to play a game of
    Dots.
    :param b: Board object
    :return: Connection object if found otherwise None when maximum attempts exceeded.
    """
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
    """
    Game host a Dots game. Utility methods we've created so far are consumed and chained together in this class to create
    a playable Dots game.
    """
    def __init__(self, b):
        """
        Create a Dots game with a Board, b.
        :param b: Board object
        """
        assert isinstance(b, Board)
        self.board = b

    def playOnce(self, debug=False):
        """
        Play a Dots game in a single iteration.
        :param debug: debugging flag
        :return: a tuple with color and a valid connection object found in this iteration
        """
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
            result = (t.dot.color, len(conn))
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
        """
        Play a Dots game until iteration limit has been reached.
        :param limit: Iteration limit
        :return: Dict with interesting statistical data in the game
                e.g. Number of dots with a given color has been slashed off in this game.
        """
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



