from flask import Flask, jsonify
from api.routes.kline import kline_bp
from api.routes.health import health_bp
from api.routes.plugin import plugin_bp

app = Flask(__name__)
app.register_blueprint(kline_bp)
app.register_blueprint(health_bp)
app.register_blueprint(plugin_bp)

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=False)

