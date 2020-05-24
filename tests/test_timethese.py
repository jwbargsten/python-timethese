import time
from timethese import timethese, cmpthese
from pprint import pprint


def test_timethese():
    def a():
        time.sleep(0.3)

    def b():
        time.sleep(0.6)

    res = timethese(2, {"aa": a, "bb": b})
    pprint(res)


def test_cmpthese_iter():
    def a():
        time.sleep(1)

    def b():
        time.sleep(2)

    res = cmpthese(2, {"aa": a, "bb": b}, repeat=2)
    print("")
    print(res)


def test_cmpthese_rate():
    def a():
        time.sleep(1)

    def b():
        time.sleep(0.01)

    def c():
        time.sleep(0.02)

    res = cmpthese(2, {"aa": a, "bb": b, "cc": c}, repeat=2)
    print("")
    print(res)
