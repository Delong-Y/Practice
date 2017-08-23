# test1
# test2
# test3
# test4
# test5
# test6
# test7
# test8
# test9
# test10
# test11
# test12
# test13
from multiprocessing import Pool

d = {}

def f1(i):
    global  d
    d[i] = i
    print(d)

def process_way1(i):
    workers = 10
    with Pool(workers) as p:
        r = p.map(f1, i)
    return r

def f2():
    global d
    g =  [1,2,3,4]
    r = process_way1(g)
    for i in r:
        print(i)
    print(d)

if __name__ == '__main__':
    f2()
