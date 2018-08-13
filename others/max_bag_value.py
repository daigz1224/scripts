import sys

def bag(n, c, w, v):
    res = [[-1 for j in range(c + 1)] for i in range(n + 1)]
    for j in range(c + 1):
        res[0][j] = 0
    for i in range(1, n + 1):
        for j in range(1, c + 1):
            res[i][j] = res[i - 1][j]
            if j >= w[i - 1] and res[i][j] < res[i - 1][j - w[i - 1]] + v[i - 1]:
                res[i][j] = res[i - 1][j - w[i - 1]] + v[i - 1]
    return res


def show(n, c, w, res):
    print(res[n][c])
    # x = [False for i in range(n)]
    # j = c
    # for i in range(1, n + 1):
    #     if res[i][j] > res[i - 1][j]:
    #         x[i - 1] = True
    #         j -= w[i - 1]
    # print('选择的物品为:')
    # for i in range(n):
    #     if x[i]:
    #         print('第', i, '个,', end='')
    # print('')


if __name__ == '__main__':
    line = sys.stdin.readline().strip()
    weight = list(map(int, line.split()))

    line = sys.stdin.readline().strip()
    value = list(map(int, line.split()))

    c = sys.stdin.readline().strip()

    # num = 5 # 物品数量
    # c = 10 # 承重
    # weight = [2, 2, 6, 5, 4]  # 每个物品的重量
    # value = [6, 3, 5, 4, 6]  # 每个物品的价值
    result = bag(len(weight), c, weight, value)
    show(len(weight), c, weight, result)
