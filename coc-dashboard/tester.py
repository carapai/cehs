import inspect as ip


def f1(a, b, *, c, d, **kwargs):
    print('yay')


def f2(a, b, *, c, d, **kwargs):
    print('yey')


print(ip.getfullargspec(f1)[4])

# FUNC_ARG_DICT = {}
# arg1 = ip.getfullargspec(f1)[0]
# arg2 = ip.getfullargspec(f2)[0]

# FUNC_ARG_DICT[f1] = arg1
# FUNC_ARG_DICT[f2] = arg2

# for x in FUNC_ARG_DICT.keys():
#     x('a', 'b')

print(None == None)
