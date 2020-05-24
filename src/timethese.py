import timeit
import sys
from collections import namedtuple
from more_itertools import quantify

__version__ = "0.0.1"


def _timeit(n, args, repeat=1):
    if isinstance(args, dict):
        kwargs = args
    else:
        kwargs = {"stmt": args}
    times = timeit.repeat(**kwargs, repeat=repeat, number=n)
    return {"n": n, "nrepeats": repeat, "times": times, "min": min(times)}


def _calc_rate(n, t):
    return n / (t + 0.000000000000001)


def _format_rate(rate, is_rate=True):
    # We assume that we'll never get a 0 rate.
    r = rate if is_rate else 1 / rate
    if r >= 100:
        fmt = f"{r:0.0f}"
    elif r >= 10:
        fmt = f"{r:0.1f}"
    elif r >= 1:
        fmt = f"{r:0.2f}"
    elif r >= 0.1:
        fmt = f"{r:0.3f}"
    else:
        fmt = f"{r:0.2e}"

    if is_rate:
        return fmt + "/s"

    return fmt


# timeit.timeit(stmt='pass', setup='pass', timer=<default timer>, number=1000000, globals=None)
def timethese(n=1, funcs=None, repeat=1):
    if not funcs:
        return {}

    return {name: _timeit(n, args, repeat=repeat) for name, args in funcs.items()}


def cmpthese(n=1, funcs=None, repeat=1, as_table=False):
    results = timethese(n=n, funcs=funcs, repeat=repeat)

    results = [
        {"name": name, "rate": _calc_rate(n, res["min"]), **res}
        for name, res in results.items()
    ]
    results = sorted(results, key=lambda r: r["rate"])
    cnt_gt_one = quantify(results, lambda r: r["rate"] > 1)

    display_as_rate = True if results and cnt_gt_one / len(results) > 0.5 else False

    top_row = [
        "",
        "Rate" if display_as_rate else "s/iter",
        *[r["name"] for r in results],
    ]

    rows = [top_row]
    col_widths = [len(x) for x in top_row]

    for row_res in results:
        row = []

        # Column 0 = test name
        row.append(row_res["name"])
        if len(row_res["name"]) > col_widths[0]:
            col_widths[0] = len(row_res["name"])

        # Column 1 = performance
        row_rate = row_res["rate"]

        rate_fmt = _format_rate(row_rate, display_as_rate)

        # Only give a few decimal places before switching to sci. notation,
        # since the results aren't usually that accurate anyway.
        row.append(rate_fmt)
        if len(rate_fmt) > col_widths[1]:
            col_widths[1] = len(rate_fmt)

        # Columns 2..N = performance ratios
        for col_idx, col_res in enumerate(results):
            if row_res["name"] == col_res["name"]:
                out = "."
            else:
                col_rate = col_res["rate"]
                out = f"{100*row_rate/col_rate - 100:.0f}%"

            row.append(out)
            if len(out) > col_widths[col_idx + 2]:
                col_widths[col_idx + 2] = len(out)

            # A little weirdness to set the first column width properly
            if len(col_res["name"]) > col_widths[col_idx + 2]:
                col_widths[col_idx + 2] = len(col_res["name"])

        rows.append(row)

    if as_table:
        return rows

    def format_row(row, widths):
        return "  ".join(
            ["{:>{fill}s}".format(x[0], fill=x[1]) for x in zip(row, widths)]
        )

    return "\n".join([format_row(r, col_widths) for r in rows])
