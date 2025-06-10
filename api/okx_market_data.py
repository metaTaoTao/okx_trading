from api.utils.parser import parse_okx_kline, list_of_dicts_to_df
import okx.MarketData as MarketData
import pandas as pd
from functools import lru_cache


flag = "0"  # 实盘:0 , 模拟盘：1

marketDataAPI =  MarketData.MarketAPI(flag=flag)

@lru_cache(maxsize=128)
def get_kline_cached(instId, bar='1m', limit=300, return_type='json'):
    return get_kline(instId, bar, limit, return_type)

def get_hist_kline(instId, bar='1m', return_type='json'):
    result = marketDataAPI.get_history_candlesticks(
        instId=instId,
        bar = bar
    )

    df = parse_okx_kline(result["data"])
    if return_type == 'df':
        return df
    else:
        return df.to_dict(orient='records')

def get_kline(instId,bar='1m',limit=300, return_type='json'):
    result = marketDataAPI.get_candlesticks(
        instId=instId,
        bar=bar.upper(),
        limit=limit
    )
    df = parse_okx_kline(result["data"])
    print("get_kline OKX返回内容：", result)
    if return_type == 'df':
        return df
    else:
        return df.to_dict(orient='records')


def get_all_tickers(instType="SWAP",return_type='json'):
    """

    :param instType: 产品类型, SPOT：币币, SWAP：永续合约, FUTURES：交割合约, OPTION：期权
    :return:
    """
    # 获取所有产品行情信息
    result = marketDataAPI.get_tickers(
        instType=instType
    )
    data = result["data"]
    df = list_of_dicts_to_df(data)
    df = df[df['instId'].str.contains('USDT')].copy()

    df['last'] = pd.to_numeric(df['last'], errors='coerce')
    df['vol24h'] = pd.to_numeric(df['vol24h'], errors='coerce')
    # 优先用 quote 币成交额（如果有这个字段）
    if 'volCcyQuote24h' in df.columns:
        df['volume_usd_million'] = pd.to_numeric(df['volCcyQuote24h'], errors='coerce') / 1e6

    # 否则用 volCcy24h * last 来估算
    else:
        df['last'] = pd.to_numeric(df['last'], errors='coerce')
        df['volCcy24h'] = pd.to_numeric(df['volCcy24h'], errors='coerce')
        df['volume_usd_million'] = df['last'] * df['volCcy24h'] / 1e6

    df = df.sort_values(by='volume_usd_million', ascending=False)

    if return_type == 'df':
        return df
    else:
        return df.to_dict(orient='records')

print(get_all_tickers())


