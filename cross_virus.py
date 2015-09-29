# coding=utf-8
from itertools import combinations
import heapq
import copy

__author__ = 'kzm4269'

BLOCK_BUFSIZE = 3

EMPTY = -1
VIRUS = -2

EMPTY_SYM = '.'
VIRUS_SYM = '@'
BLOCK_SYM = '#'
SYMBOLS = (EMPTY_SYM, VIRUS_SYM, BLOCK_SYM)


class CrossVirus:
    def __init__(self, field, n, turn=None):
        self.field = field
        self.n = n
        self.turn = turn if turn is not None else 1

        self.virus_count, self.danger_points = CrossVirus._scan_virus(field)
        self.score = self.virus_count + max(0, len(self.danger_points) - 3) * (2 ** n)

    @staticmethod
    def _scan_virus(field):
        rows, cols = len(field), len(field[0])
        virus_count = 0
        virus_neighbors = []
        for i in range(rows):
            for j in range(cols):
                if field[i][j] != VIRUS:
                    continue
                virus_count += 1
                if i > 0:
                    virus_neighbors.append((i - 1, j))
                if i < rows - 1:
                    virus_neighbors.append((i + 1, j))
                if j > 0:
                    virus_neighbors.append((i, j - 1))
                if j < cols - 1:
                    virus_neighbors.append((i, j + 1))
        return virus_count, set(filter(lambda p: field[p[0]][p[1]] == EMPTY, virus_neighbors))

    def next_turn(self, block_points):
        block_points = set(block_points)
        assert len(block_points) <= BLOCK_BUFSIZE
        assert len(block_points) == BLOCK_BUFSIZE or block_points == self.danger_points

        field = copy.deepcopy(self.field)
        for i, j in block_points:
            field[i][j] = self.turn
        for i, j in self.danger_points:
            if (i, j) not in block_points:
                field[i][j] = VIRUS

        return CrossVirus(field, self.n, self.turn + 1)

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        return '\n'.join(' '.join(
            '\x1b[1;37m' + str(c) if c >= 0 else
            '\x1b[0;37m' + EMPTY_SYM if c == -1 else
            '\x1b[1;35m' + VIRUS_SYM if c == -2 else "?"
            for c in line) + '\x1b[0m' for line in self.field)


def parse(lines, n):
    def f(c):
        if c == BLOCK_SYM:
            return 0
        if c == EMPTY_SYM:
            return -1
        if c == VIRUS_SYM:
            return -2

    return CrossVirus([[f(s) for s in line if s in SYMBOLS] for line in lines], n)


def _solve(start, heap=None, best=None):
    if not heap:
        if start.n <= 1:
            return best
        start = CrossVirus(start.field, n=start.n - 1)
        return _solve(start, [start], best)

    print 'n={}  heap={}\r'.format(start.n, len(heap)),
    top = heapq.heappop(heap)

    if len(top.danger_points) <= BLOCK_BUFSIZE:
        top = top.next_turn(top.danger_points)
        return _solve(start, best=top)

    for ps in combinations(top.danger_points, BLOCK_BUFSIZE):  # 探索を続ける
        next_turn = top.next_turn(ps)
        if best is None or next_turn.virus_count + max(0, len(next_turn.danger_points) - 3) < best.score:
            heapq.heappush(heap, next_turn)
    return _solve(start, heap, best)


def solve(lines, n=5):
    cv = parse(lines, n)
    return _solve(cv)
