# coding=utf-8
from cross_virus import solve
from stage import STAGE

__author__ = 'kzm4269'


def main():
    import sys
    # noinspection PyArgumentList
    sys.setrecursionlimit(int(1e4))

    for i, stage in enumerate(STAGE):
        print "STAGE{:02d}".format(i)
        result = solve(stage, n=5)
        print result
        print "score:", result.score
        print "-" * 40
        print


if __name__ == '__main__':
    main()
