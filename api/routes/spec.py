from flask import Blueprint, send_file
import os

spec_bp = Blueprint('spec', __name__)

@spec_bp.route('/openapi.yaml')
def serve_openapi_yaml():
    file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'openapi.yaml')
    return send_file(file_path, mimetype='text/yaml')
