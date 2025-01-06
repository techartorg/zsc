import zbrush

gScriptVersion = 1.0


def check_script_version():
    fred = 1
    gScriptVersion = zbrush.ZbrushInfo(0)


def test_func(arg, arg2):
    print(arg)
    arg2 = arg + 1


def fred():
    zbrush.MemCreate("other", 100, "A")
    memblock = zbrush.MemCreate("memblock", 100, "A")
    zbrush.MemWrite(memblock, 0, "A", 1)
    goof = zbrush.MemRead(memblock, 0, "A", 1)  # noqa
    test = zbrush.ToolGetActiveIndex()
    subtooltst = zbrush.GetSubToolIndex(2)
    allowed = max(1, 2)
    barney = 1
    josh = test_return_string(barney)
    print(josh)
    xxxx = test_return_float(barney)
    print(xxxx)
    wilma = test_return_int(barney)
    pebbles = "a"
    bam_bam = "b"
    """random internal comment"""


def test_loop() -> int:
    for x in range(10):
        if x == 5:
            return x
        else:
            if x in [3, 4]:
                continue
            print(x)


def array_contains(arr, val) -> int:
    loopsize = zbrush.VarSize(arr)
    result = loopsize
    # result = 0
    # for x in range(loopsize):
    #     if arr[x] == val:
    #         """todo return 1"""
    #         result = 1
    #         break
    return result


def test_array_contains(arr, val) -> int:
    result = array_contains(arr, val)


# todo: figure out how to handle retruns in cases inside loops and whiles


def test_while(iterations, cutoff) -> int:
    val = 0
    """random internal comment"""
    otherval = 1.0
    while val < iterations:
        if val == cutoff:
            return val
        val += 1


def test_return_string(arg) -> str:
    """convert 'return val' to return an automatic value"""
    val = arg + "xxx"
    return val


def test_return_float(arg) -> float:
    """convert 'return val' to return an automatic value"""
    val = arg + 1.0
    return val


def test_return_int(arg) -> int:
    """convert 'return val' to return an automatic value"""
    val = arg + 1
    return val
