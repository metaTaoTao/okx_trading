from flask import Flask
from api.routes.kline import kline_bp

app = Flask(__name__)
app.register_blueprint(kline_bp)

if __name__ == "__main__":
    app.run(debug=True)
