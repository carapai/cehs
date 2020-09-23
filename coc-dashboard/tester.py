import inspect as ip


def f1(a, b):
    print('yay')


def f2(a, b):
    print('yey')


FUNC_ARG_DICT = {}
arg1 = ip.getfullargspec(f1)[0]
arg2 = ip.getfullargspec(f2)[0]

FUNC_ARG_DICT[f1] = arg1
FUNC_ARG_DICT[f2] = arg2

for x in FUNC_ARG_DICT.keys():
    x('a', 'b')
