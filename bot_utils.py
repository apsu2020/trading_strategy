import pandas as pd

def set_dataframe(msg:str):
    df = pd.DataFrame([msg])
    df = df.loc[:,["s", "E", "p", "q"]]
    df.columns = ["symbol", "Time", "Price", "Quantity"]
    df.Time = pd.to_datetime(df.Time, unit="ms")
    df.set_index("Time", drop=True, inplace=True)
    return df