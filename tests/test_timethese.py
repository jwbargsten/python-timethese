import time

from pytest import approx

from timethese import cmpthese, pprint_cmp, timethese


def test_timethese():
    def a():
        time.sleep(0.3)

    def b():
        time.sleep(0.6)

    res = timethese(2, {"a": a, "b": b})

    assert approx(res["a"]["best_time"], abs=0.1) == 0.3
    assert approx(res["b"]["best_time"], abs=0.1) == 0.6


def test_cmpthese():
    def a():
        time.sleep(0.1)

    def b():
        time.sleep(0.2)

    res = cmpthese(2, {"a": a, "b": b}, repeat=2)
    assert approx(res["data"][0], abs=0.2) == [0, 1]
    assert approx(res["data"][1], abs=0.2) == [-0.5, 0]


def test_pprint_iter():
    res = {"data": [[0, 0.99], [-0.49, 0]], "names": ["a", "b"], "times": [0.10, 0.20], "rates": [9.78, 4.93]}
    expected = """     Rate     a    b
a  9.78/s     .  99%
b  4.93/s  -49%    ."""

    assert pprint_cmp(res) == expected


def test_pprint_rate():
    res = {
        "data": [[0, 0.7415, 84.8878], [-0.4258, 0, 48.3165], [-0.9883, -0.9797, 0]],
        "names": ["b", "c", "a"],
        "times": [0.0011, 0.0020, 0.1015],
        "rates": [845.3621, 485.4044, 9.8426],
    }
    expected = """     Rate     b     c      a
b   845/s     .   74%  8489%
c   485/s  -43%     .  4832%
a  9.84/s  -99%  -98%      ."""
    assert pprint_cmp(res) == expected
