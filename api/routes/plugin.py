from flask import Blueprint, jsonify

plugin_bp = Blueprint('plugin', __name__)

@plugin_bp.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return jsonify({
        "schema_version": "v1",
        "name_for_human": "OKX Market Data",
        "name_for_model": "okx_market_data",
        "description_for_human": "获取实时 OKX 币种行情、K线数据",
        "description_for_model": "Plugin to fetch live OKX market data such as tickers and candlesticks",
        "auth": {
            "type": "none"
        },
        "api": {
            "type": "openapi",
            "url": "https://okx-trading.vercel.app/openapi.yaml"
        },
        "logo_url": "https://okx-trading.vercel.app/logo.png",
        "contact_email": "you@example.com",
        "legal_info_url": "https://yourdomain.com/legal"
    })
