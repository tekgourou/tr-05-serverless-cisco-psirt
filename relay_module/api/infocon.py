import requests
import re

def get_infocon():
    url = "https://isc.sans.edu/daily_alert.html"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    threat_level = re.search('<b>(.*)</b>', response.text).group(1).upper()
    try :
        diary_name = re.search(';(.*)</a>', response.text).group(1)
    except:
        diary_name = '----'
    url = re.search('<a href="(.*)">', response.text).group(1)
    return threat_level, diary_name, url

#print (get_infocon())