from flask import Flask, jsonify
from api.routes.kline import kline_bp

app = Flask(__name__)
app.register_blueprint(kline_bp)

if __name__ == "__main__":
    app.run()

@app.route("/health")
def health_check():
    return jsonify({"status": "ok"})