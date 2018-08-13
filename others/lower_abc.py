import sys

def main(string):
    res = []
    for i in range(len(string)):
        c = string[i]
        if ord('a') <= ord(c) <= ord('z'):
            res.append(chr(ord('A') + ord(c) - ord('a')))
        elif ord('A') <= ord(c) <= ord('Z'):
            res.append(chr(ord('a') + ord(c) - ord('A')))
        else:
            res.append(c)
    return ''.join(res)


if __name__=='__main__':
    # string = 'ASdfwfes&%Usjb'
    #string = sys.stdin.readline()
    #print(main(string))

    # 读取第一行的n
    n = int(sys.stdin.readline().strip())
    ans = 0
    for i in range(n):
        # 读取每一行
        line = sys.stdin.readline().strip()
        # 把每一行的数字分隔后转化成int列表
        values = list(map(int, line.split()))
        print(main(line))
