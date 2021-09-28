from flask import Blueprint
from datetime import datetime, timedelta
from functools import partial
from code.api import DashboardTileSchema, DashboardTileDataSchema
from code.api import jsonify_data, get_jwt, get_json
from code.api import build_advisory_data

dashboard_api = Blueprint('dashboard', __name__)
get_dashboardtile_form_params = partial(get_json, schema=DashboardTileSchema())
get_dashboardtiledata_form_params = partial(get_json, schema=DashboardTileDataSchema())


def set_valid_time():
    return {
        'start_time': str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
        'end_time': str((datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    }
def set_observed_time(timeframe_in_sec):
    return {
        'start_time': str((datetime.now() - timedelta(seconds=timeframe_in_sec)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
        'end_time': str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    }

def create_tile_data(data_json):
    valid_time = set_valid_time()
    observed_time = set_observed_time(86400)
    data = []
    data.append('[Cisco PSIRT openVuln](https://tools.cisco.com/security/center/publicationListing.x)')
    data.append('&nbsp;')
    data.append('| Last Update | &nbsp; | IMPACT | &nbsp; | ADVISORY | &nbsp; | CVE |')
    data.append('| -- | -- | -- | -- | -- | -- | -- |')
    for advisory in data_json:
        line = '| {} | | {} | | [{}]({}) | | {} | '.format(advisory['lastUpdated'], advisory['sir'], advisory['advisoryTitle'],advisory['publicationUrl'], advisory['cves'])
        data.append(line)

    data = {
        'valid_time': valid_time,
        'hide_legend': True,
        'cache_scope': 'org',
        'observed_time': observed_time,
        'data': data
    }
    return data

def get_tile(description, tags, tile_type, title, tile_id):
    return {
        'description': description,
        'periods': [
            'last_24_hours'
        ],
        'tags': tags,
        'type': tile_type,
        'short_description': description,
        'title': title,
        'default_period': 'last_24_hours',
        'id': tile_id
    }

@dashboard_api.route('/tiles', methods=['POST'])
def tiles():
    get_jwt()
    data = []

    # Tile Circl cve-search last 25
    title = 'Last 25 Cisco PSIRT  Advisories'
    tags = ['Circl', 'CVE']
    tile_type = 'markdown'
    description = 'Get the last 25 Cisco PSIRT  Advisories'
    tile_id = 'cisco_psirt-top25'
    data.append(get_tile(description, tags, tile_type, title, tile_id))

    return jsonify_data(data)

@dashboard_api.route('/tiles/tile', methods=['POST'])
def tile():
    get_jwt()
    return jsonify_data({})

@dashboard_api.route('/tiles/tile-data', methods=['POST'])
def tile_data():
    data = []
    client_id, client_secret = get_jwt()
    params = get_dashboardtiledata_form_params()
    if params['tile_id'] == 'cisco_psirt-top25':
        data_json = build_advisory_data(client_id, client_secret)
        data = create_tile_data(data_json)
    else:
        return jsonify_data(data)

    return jsonify_data(data)
