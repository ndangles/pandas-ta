import os
from pandas import DatetimeIndex, read_csv

VERBOSE = True

ALERT = f"[!]"
INFO = f"[i]"

CORRELATION = "corr"  # "sem"
CORRELATION_THRESHOLD = 0.99  # Less than 0.99 is undesirable

sample_data = read_csv(
    f"data/SPY_D.csv",
    index_col=0,
    parse_dates=True,
    infer_datetime_format=True,
    keep_date_col=True,
)
sample_data.set_index(DatetimeIndex(sample_data["date"]), inplace=True, drop=True)
sample_data.drop("date", axis=1, inplace=True)


def error_analysis(df, kind, msg, icon=INFO, newline=True):
    if VERBOSE:
        s = f"{icon} {df.name}['{kind}']: {msg}"
        if newline:
            s = f"\n{s}"
        print(s)


def load(**kwargs):
    kwargs.setdefault("ticker", "SPY")
    kwargs.setdefault("prefix", "PDR_")
    kwargs.setdefault("interval", "d")

    kwargs.setdefault("index_col", 0)
    kwargs.setdefault("parse_dates", True)
    kwargs.setdefault("infer_datetime_format", True)
    kwargs.setdefault("keep_date_col", True)

    kwargs.setdefault("verbose", False)

    print(f"\n{TEST} Pandas TA on {datetime.datetime.now()}")
    filename = f"{kwargs['prefix']}{kwargs['ticker']}_{kwargs['interval']}.csv"
    try:
        df = read_csv(
            filename,
            index_col=kwargs["index_col"],
            parse_dates=kwargs["parse_dates"],
            infer_datetime_format=kwargs["infer_datetime_format"],
            keep_date_col=kwargs["index_col"],
        )
        _mode = "Loading"
    except BaseException as err:
        print(f"{ALERT} {err}")
        if kwargs["verbose"]: print(f"{INFO} Downloading: {kwargs['ticker']} from YF")
        df = pdr.get_data_yahoo(kwargs['ticker'], interval=kwargs['interval'])
        df.to_csv(filename, mode="a")
        _mode = "Downloading"

    kwargs.setdefault("n", 0)
    if kwargs['n'] > 0:
        df = df[:kwargs['n']]
    elif kwargs['n'] < 0:
        df = df[kwargs['n']:]

    df.columns = df.columns.str.lower()
    if kwargs["verbose"]:
        print(f"{INFO} {_mode} {kwargs['ticker']}{df.shape} from {filename}")
        print(f"{INFO} From {df.index[0]} to {df.index[-1]}\n{df}\n")
    return df

_tdpy = pandas_ta.RATE["TRADING_DAYS_PER_YEAR"]
# At least 90 (88 with trix with default values) bars/rows/observations are
# needed to test All indicators individually and within the DataFrame extension
sample_data = load(
        n = [
            -2 * _tdpy, -_tdpy,
            -90, 0, 90,
            _tdpy, 2 * _tdpy
        ][0],
        verbose=VERBOSE
    )


# Example multiindex download code
# _df = DataFrame()
# tickers =["SQ", "PLTR"]
# data = {t:_df.ta.ticker(t, period="1y", timed=True) for t in tickers if len(t) > 1}
# assets = concat(data, names=["ticker", "datetime"], verify_integrity=True)