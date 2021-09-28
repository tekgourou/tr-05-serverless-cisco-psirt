from flask import Blueprint
import json
from code.api import get_jwt, jsonify_data
from code.api import get_cisco_cloudsso_token
health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    client_id, client_secret = get_jwt()
    try :
        json.loads(get_cisco_cloudsso_token(client_id, client_secret))['access_token']
        return jsonify_data({'status': 'ok'})
    except:
        return jsonify_data({})
