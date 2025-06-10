from flask import Blueprint, request, jsonify
from api.okx_market_data import get_kline_cached

kline_bp = Blueprint('kline', __name__)


@kline_bp.route('/kline')
def kline_api():
    instId = request.args.get('instId')
    bar = request.args.get('bar', '1m')
    limit = int(request.args.get('limit', 300))
    return_type = request.args.get('return_type', 'json')

    if not instId:
        return jsonify({"error": "Missing required parameter: instId"}), 400

    try:
        result = get_kline_cached(instId=instId, bar=bar, limit=limit, return_type=return_type)
        if return_type == 'df':
            return result.to_html()  # Jupyter查看方便的话返回html
        else:
            return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500