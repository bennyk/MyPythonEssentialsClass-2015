
import game
import random
import math


def createRandomBoard():
    r = game.RandomGen({'a': .25, 'b': .25, 'c': .25, 'd': .25})
    b = game.Board(8, 8, r)
    return b

def testRand():
    occ = {}
    r = game.RandomGen({'a': .25, 'b': .25, 'c': .25, 'd': .25}, limit=1000)
    for x in r:
        if x not in occ:
            occ[x] = 1
        else:
            occ[x] += 1

    print(occ)

def testBoard():
    b = createRandomBoard()
    print(b)

def testRemoveFromTile():
    b = createRandomBoard()
    print("new board {}".format(b))

    i = math.floor(random.uniform(0, b.cols))
    j = math.floor(random.uniform(0, b.rows))
    print("removing", i, j)

    tile = b.get(i, j)
    tile.removeCookie()
    print("post removal {}".format(b))


def testSearchAnyConnection():
    b = createRandomBoard()
    print("new board {}".format(b))

    i = math.floor(random.uniform(0, b.cols))
    j = math.floor(random.uniform(0, b.rows))

    game.findAnyConnection(b, (i, j))


def testSearchValidConnection():
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

def playMultiply(times=10):
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



def testPlay():
    b = createRandomBoard()
    print("new board {}".format(b))
    g = game.Game(b)
    g.play()

def testPlayMultiply():
    playMultiply()

