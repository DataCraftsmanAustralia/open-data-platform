from app.api import bp
from flask import jsonify

@bp.route('/test', methods=['GET'])
def test():
    return jsonify({'api':'test'})