import statistics as stat
import timeit

from more_itertools import quantify

__version__ = "0.0.1"


def _timeit(n, args, repeat=1):
    if isinstance(args, dict):
        kwargs = args
    else:
        kwargs = {"stmt": args}
    run_times = timeit.repeat(**kwargs, repeat=repeat, number=n)
    times = [dt / n for dt in run_times]
    rates = [1 / (t + 0.000000000000001) for t in times]

    return {
        "n": n,
        "nruns": repeat,
        "run_times": run_times,
        "times": times,
        "best_time": min(times),
        "mean": stat.mean(times),
        "median": stat.median(times),
        "stdev": stat.stdev(times) if len(times) >= 2 else 0,
        "rates": rates,
        "best_rate": max(rates),
    }


def _format_perf(perf, is_rate):
    # We assume that we'll never get a 0 rate.
    if perf >= 100:
        fmt = f"{perf:0.0f}"
    elif perf >= 10:
        fmt = f"{perf:0.1f}"
    elif perf >= 1:
        fmt = f"{perf:0.2f}"
    elif perf >= 0.1:
        fmt = f"{perf:0.3f}"
    else:
        fmt = f"{perf:0.2e}"

    if is_rate:
        return fmt + "/s"

    return fmt


def _fmt_stmt(i, stmt):
    if callable(stmt):
        return "{}.{}".format(i, stmt.__name__)
    else:
        return "{}.{}".format(i, str(stmt)[:11])


def timethese(n=1, funcs=None, repeat=3):
    """Time multiple functions

    Parameters
    ----------
    n : the number of times the function is executed

    funcs : the statements/functions or arguments supplied to timeit (timeit is
        used internally, the elements of funcs are mapped to the `stmt` parameter of
        timeit). `funcs` can be a list `[stmt1, stmt2, ...]`, a dict
        `{ "stmt1": stmt1, "stmt2": stmt2, ...}`. If you need advanced functionality,
        you can also supply a dict which is used as kwargs for timeit instead of
        the statement itself: `[{stmt:'...', setup:'...', timer: ... }, ...]`.

    repeat : times to repeat the complete performance measurement. This can be
        useful to mitigate "noise" created by other programs. The minimum time
        is taken from the repeats.

    Returns
    -------
    a dict with the run time results of each function/statement. Keys of the dict are:

    n: the supplied parameter n
    nruns: repeats
    run_times time of each repeat
    times: the run_times divided by n
    best_time: min(times),
    mean: stat.mean(times),
    median: stat.median(times),
    stdev: stat.stdev(times) if len(times) >= 2 else 0,
    rates: rates = 1/time
    best_rate: max(rates)
    """
    if funcs is None:
        return None
    if isinstance(funcs, dict):
        return {name: {"name": name, **_timeit(n, args, repeat=repeat)} for name, args in funcs.items()}
    elif isinstance(funcs, list):
        return [
            {"name": _fmt_stmt(i, args), **_timeit(n, args, repeat=repeat)} for i, args in enumerate(funcs)
        ]
    else:
        raise TypeError("Unknown type of funcs parameter.")


def cmpthese(n=1, funcs=None, repeat=3):
    """Compare run time of multiple functions.

    Parameters
    ----------
    n : the number of times the function is executed

    funcs : the statements/functions or arguments supplied to timeit (timeit is
        used internally, the elements of funcs are mapped to the `stmt` parameter of
        timeit). `funcs` can be a list `[stmt1, stmt2, ...]`, a dict
        `{ "stmt1": stmt1, "stmt2": stmt2, ...}`. If you need advanced functionality,
        you can also supply a dict which is used as kwargs for timeit instead of
        the statement itself: `[{stmt:'...', setup:'...', timer: ... }, ...]`.

    repeat : times to repeat the complete performance measurement. This can be
        useful to mitigate "noise" created by other programs. The minimum time
        is taken from the repeats.

    Returns
    -------
    the comparison results as dict. The dict contains following keys:

    data: a matrix (list of lists) with the comparison results, a comparison
        results of 1 indicates 100% faster, -.5 means 50% slower
    names: list of column/row names (column names == row names)
    times: the best time of each func
    rates: the best rate of each func, rate = 1/time
    """
    results = timethese(n=n, funcs=funcs, repeat=repeat)
    if isinstance(funcs, dict):
        results = results.values()

    results = sorted(results, key=lambda r: r["best_time"])
    names = [r["name"] for r in results]
    times = [r["best_time"] for r in results]
    rates = [r["best_rate"] for r in results]

    rows = []
    for row_idx, row_res in enumerate(results):
        row = []

        # Column 1 = performance
        row_rate = row_res["best_rate"]

        for col_idx, col_res in enumerate(results):
            if row_idx == col_idx:
                out = 0
            else:
                col_rate = col_res["best_rate"]
                out = row_rate / col_rate - 1

            row.append(out)
        rows.append(row)
    return {"data": rows, "names": names, "times": times, "rates": rates}


def pprint_cmp(result, as_rate=None):
    """Pretty print a result from timethese

    Parameters
    ----------
    result: a result from timethese
    as_rate: if None, the display format is determined automatically.
        if True, a rate is shown as function performance (unit 1/s),
        if False, the time is shown (unit s)

    Returns
    -------
    a string table with the results
    """
    if as_rate is None:
        # determine rate display automatically
        big_rates_count = quantify(result["times"], lambda t: t < 1)
        as_rate = result and big_rates_count / len(result["times"]) > 0.5

    perf = result["rates"] if as_rate else result["times"]
    perf = [_format_perf(p, as_rate) for p in perf]

    names = result["names"]
    top_row = ["", "Rate" if as_rate else "s/iter", *names]
    rows = [top_row] + [list(x) for x in zip(names, perf)]

    col_widths = [len(x) for x in top_row]
    col_widths[0] = max([len(n) for n in names])
    col_widths[1] = max([len(rows[i][1]) for i in range(len(rows))])

    for ridx, r in enumerate(result["data"]):
        for cidx, c in enumerate(r):
            if ridx == cidx:
                val = "."
            else:
                val = f"{c*100:.0f}%"

            rows[ridx + 1].append(val)

            if len(val) > col_widths[cidx + 2]:
                col_widths[cidx + 2] = len(val)

    def format_row(row, widths):
        return "  ".join(["{:>{fill}s}".format(x[0], fill=x[1]) for x in zip(row, widths)])

    return "\n".join([format_row(r, col_widths) for r in rows])
