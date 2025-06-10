import pandas as pd

def list_of_dicts_to_df(data):
    """
    Convert a list of dictionaries to a pandas DataFrame.
    Automatically handles empty or malformed input.
    """
    if not isinstance(data, list) or len(data) == 0:
        print("Input data is not a non-empty list.")
        return pd.DataFrame()

    if not isinstance(data[0], dict):
        print("List elements are not dictionaries.")
        return pd.DataFrame()

    df = pd.DataFrame(data)

    # Try to convert numeric fields if possible
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        except:
            pass

    # Try to convert timestamp column if present
    for time_col in ['ts', 'timestamp']:
        if time_col in df.columns:
            df[time_col] = pd.to_datetime(df[time_col].astype(float), unit='ms')

    return df

def parse_okx_kline(data: list) -> pd.DataFrame:
    """
    将 OKX 返回的 K线数据解析为 DataFrame 并格式化时间戳

    Args:
        data (list): OKX API 返回的 'data' 字段内容（二维数组）

    Returns:
        pd.DataFrame: 含时间、开高低收量的表格
    """
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close",
        "volume", "turnover", "confirm", "status"
    ])

    # 转换数据类型
    df["timestamp"] = pd.to_datetime(df["timestamp"].astype("int64"), unit="ms")
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

    # 只保留前6列
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]

    # 按时间升序排列（OKX 默认是倒序的）
    df = df.sort_values("timestamp").reset_index(drop=True)

    return df