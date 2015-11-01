"""
A collection of test routines used in our development for dots-simulator.
"""
import game
import random
import math


def createRandomBoard():
    """
    Create a Board with a random population of dots in our test.
    :return: Board object
    """
    r = game.RandomGen({'a': .25, 'b': .25, 'c': .25, 'd': .25})
    b = game.Board(8, 8, r)
    return b

def testRand():
    """
    Routine to try out our random generator.
    """
    occ = {}
    r = game.RandomGen({'a': .25, 'b': .25, 'c': .25, 'd': .25}, limit=1000)
    for x in r:
        if x not in occ:
            occ[x] = 1
        else:
            occ[x] += 1

    print(occ)

def testBoard():
    """
    Routine to try out our random generator and construction of Board.
    """
    b = createRandomBoard()
    print(b)

def testRemoveFromTile():
    """
    Routine to try out removal of any dots from a Board.
    """
    b = createRandomBoard()
    print("new board {}".format(b))

    i = math.floor(random.uniform(0, b.cols))
    j = math.floor(random.uniform(0, b.rows))
    print("removing", i, j)

    tile = b.get(i, j)
    tile.removeCookie()
    print("post removal {}".format(b))


def testSearchAnyConnection():
    """
    Routine to try out our connection searching algorithm.
    """
    b = createRandomBoard()
    print("new board {}".format(b))

    i = math.floor(random.uniform(0, b.cols))
    j = math.floor(random.uniform(0, b.rows))

    game.findAnyConnection(b, (i, j))


def testSearchValidConnection():
    """
    Routine to try out our connected dots searching algorithm. Also attempt to remove it from Board once a valid
    connection were found.
    """
    b = createRandomBoard()
    print("new board {}".format(b))

    conn = game.findAnyValidConnection(b)
    if conn is None:
        print("can't find any connection after max attempt")
    else:
        print("connection found.", conn)
        b.remove(conn)

    print("post removal {}".format(b))

def testFillHoles():
    """
    Routine to try filling up gaps on the Board after some removal attempts.
    """
    b = createRandomBoard()
    print("new board {}".format(b))

    conn = game.findAnyValidConnection(b)
    if conn is None:
        print("can't find any connection after max attempt")
    else:
        print("connection found.", conn)
        b.remove(conn)

    if conn is not None:
        print("post removal {}".format(b))

        b.fillHolesByGravity()
        print("post fillHolesByGravity {}".format(b))

        b.fillHolesWithNewCookies()
        print("post fillHolesWithNewCookies {}".format(b))

def testPlay():
    """
    Play a single game of Dots.
    """
    b = createRandomBoard()
    print("new board {}".format(b))
    g = game.Game(b)
    g.play()

def testPlayMultiply(times=10):
    """
    Play a Dots game multiple times with each play generate multiple moves. At the start of every play, a new random
    Board is created anew to start a play iteration. While we are attempting Dots games we would also like to collect
    interesting statistical data.
    """

    stat = {}
    for i in range(times):
        print('=' * 60)
        print ('starting game %d' % (i))
        b = createRandomBoard()
        print("new board {}".format(b))
        g = game.Game(b)
        s = g.play()
        for kv in s.items():
            k, v = kv
            if k not in stat:
                stat[k] = 0
            stat[k] += v

    avg = {}
    for kv in stat.items():
        color, total = kv
        avg[color] = total / times

    print("final sum after times {}: {}".format(times, stat))
    print("average: {}".format(avg))


