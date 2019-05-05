from math import sin, cos, exp, fabs,pi


def I1(x):
    return 0.05 * (x - 1) ** 2 + (3 - 2.9 * exp(-2.77257 * x ** 2)) * (1 - cos(x * (4 - 50 * exp(-2.77257 * x ** 2))))


def I2(x):
    return 1 - 0.5 * cos(1.5 * (10 * x - 0.3)) * cos(31.4 * x) + 0.5 * cos(5 ** 0.5 * 10 * x) * cos(35 * x)


def I3(x):
    x, y = x
    return 0.1 * x ** 2 + 0.1 * y ** 2 - 4 * cos(0.8 * x) - 4 * cos(0.8 * y) + 8


def I4(x):
    x, y = x
    return (0.1 * 1.5 * y) ** 2 + (0.1 * 0.8 * x) ** 2 - 4 * cos(0.8 * 1.5 * y) - 4 * cos(0.8 * 0.8 * x) + 8


def I5(x):
    x, y = x
    return 100 * (y - x ** 2) ** 2 + (1 - x) ** 2


def I6(x):
    x, y = x
    return -10 / (0.005 * (x ** 2 + y ** 2) - cos(x) * cos(y / 2 ** 0.5) + 2) + 10


def I7(x):
    x, y = x
    return -100 / (100 * (x ** 2 - y) + (1 - x) ** 2 + 1) + 100


def I8(x):
    x, y = x
    return (1 - sin((x ** 2 + y ** 2) ** 0.5) ** 2) / (1 + 0.001 * (x ** 2 + y ** 2))


def I9(x):
    x1, x2 = x
    return 0.5 * (x1 ** 2 + x2 ** 2) * (
                2 * 0.8 + 0.8 * cos(1.5 * x1) * cos(3.14 * x2) + 0.8 * cos(5 ** 0.5 * x1) * cos(3.5 * x2))


def I10(x):
    return I9(x)


def I11(x):
    x1, x2 = x
    return x1 ** 2 * fabs(sin(2 * x1)) + x2 ** 2 * fabs(sin(2 * x2)) - 1 / (5 * x1 ** 2 + 5 * x2 ** 2 + 0.2) + 5


def I12(x):
    x1, x2 = x
    return 0.5 * (x1 ** 2 + x1 * x2 + x2 ** 2) * (
                1 + 0.5 * cos(1.5 * x1) * cos(3.2 * x1 * x2) * cos(3.14 * x2) + 0.5 * cos(2.2 * x1) * cos(
            4.8 * x1 * x2) * cos(3.5 * x2))
def I16(x):

    return sin(x)*x**2
def I17(x):

    return sin(x)+x
def myfunc(x):

    return sin(x)

allfuncs = [
    I1,
    I2,
    I3,
    I4,
    I5,
    I6,
    I7,
    I8,
    I9,
    I10,
    I11,
    I12,


    I16,
    I17,
    myfunc
]
# ...............................................................................
allfuncnames = " ".join([f.__name__ for f in allfuncs])
name_to_func = {f.__name__: f for f in allfuncs}

I1._bounds = [-1, 1]
I2._bounds = [-1, 1]
I3._bounds = [-16, 16]
I4._bounds = [-16, 16]
I5._bounds = [-2, 2]
I6._bounds = [-16, 16]
I7._bounds = [-5, 5]
I8._bounds = [-10, 10]
I9._bounds = [-2.5, 2.5]
I10._bounds = [-5, 5]
I11._bounds = [-4, 4]
I12._bounds = [0, 4]

I16._bounds = [-5, 5]
I17._bounds = [-5, 5]
myfunc._bounds = [-pi, pi]
# ...............................................................................
def getfuncs(names, dim=0):
    """ for f in getfuncs( "a b ..." ):
            y = f( x )
    """
    if names == "*":
        return allfuncs
    funclist = []
    for nm in names.split():
        if nm not in name_to_func:
            raise ValueError("getfuncs( \"%s\" ) not found" % names)
        funclist.append(name_to_func[nm])
    return funclist


def getbounds(funcname, dim):
    """ "ackley" or ackley -> [-15, 30] """
    funcname = getattr(funcname, "__name__", funcname)
    func = getfuncs(funcname)[0]
    b = func._bounds[:]
    if isinstance(b[0], (bytes, str)):  b[0] = eval(b[0])
    if isinstance(b[1], (bytes, str)):  b[1] = eval(b[1])
    return b


# ...............................................................................
_minus = ""


def allfuncs_minus(minus=_minus):
    return [f for f in allfuncs
            if f.__name__ not in minus.split()]


def funcnames_minus(minus=_minus):
    return " ".join([f.__name__
                     for f in allfuncs_minus(minus=minus)])

# -------------------------------------------------------------------------------
