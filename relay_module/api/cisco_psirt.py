import requests
import json

def get_cisco_cloudsso_token(client_id, client_secret):
    url = "https://cloudsso.cisco.com/as/token.oauth2?client_id={}&client_secret={}&grant_type=client_credentials".format(client_id, client_secret)
    payload={}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    token = requests.request("POST", url, headers=headers, data=payload).text
    return token

def build_advisory_data(client_id, client_secret):
    token = json.loads(get_cisco_cloudsso_token(client_id, client_secret))['access_token']
    url = "https://api.cisco.com/security/advisories/cvrf/latest/25"
    payload = {}
    headers = {'Authorization': 'Bearer {}'.format(token)}
    response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
    advisory_data = []
    for advisory in response['advisories']:
        sinlge_advisory = {}
        sinlge_advisory['lastUpdated'] = advisory['lastUpdated']
        sinlge_advisory['sir'] = advisory['sir']
        cves = ''
        for cve in advisory['cves']:
            cves += '{} '.format(cve)
        sinlge_advisory['cves'] = cves
        sinlge_advisory['advisoryTitle'] = advisory['advisoryTitle']
        sinlge_advisory['publicationUrl'] = advisory['publicationUrl']
        advisory_data.append(sinlge_advisory)
    return advisory_data
