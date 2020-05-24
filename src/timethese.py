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
        "min_time": min(times),
        "mean": stat.mean(times),
        "median": stat.median(times),
        "stdev": stat.stdev(times) if len(times) >= 2 else 0,
        "rates": rates,
        "max_rate": max(rates),
    }


def format_perf(perf, is_rate):
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


def timethese(n=1, funcs=None, repeat=1):
    if not funcs:
        return {}

    return {name: _timeit(n, args, repeat=repeat) for name, args in funcs.items()}


def cmpthese(n=1, funcs=None, repeat=1):
    results = timethese(n=n, funcs=funcs, repeat=repeat)

    results = [{"name": name, **res} for name, res in results.items()]
    results = sorted(results, key=lambda r: r["min_time"])
    names = [r["name"] for r in results]
    times = [r["min_time"] for r in results]
    rates = [r["max_rate"] for r in results]

    rows = []
    for row_idx, row_res in enumerate(results):
        row = []

        # Column 1 = performance
        row_rate = row_res["max_rate"]

        for col_idx, col_res in enumerate(results):
            if row_idx == col_idx:
                out = 1
            else:
                col_rate = col_res["max_rate"]
                out = row_rate / col_rate - 1

            row.append(out)
        rows.append(row)
    return {"data": rows, "names": names, "times": times, "rates": rates}


def pprint_cmp(result, as_rate=None):
    if as_rate is None:
        # determine rate display automatically
        big_rates_count = quantify(result["times"], lambda t: t < 1)
        as_rate = result and big_rates_count / len(result["times"]) > 0.5

    perf = result["rates"] if as_rate else result["times"]
    perf = [format_perf(p, as_rate) for p in perf]

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
        return "  ".join(
            ["{:>{fill}s}".format(x[0], fill=x[1]) for x in zip(row, widths)]
        )

    return "\n".join([format_row(r, col_widths) for r in rows])
