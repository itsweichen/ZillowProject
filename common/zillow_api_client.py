import requests

from json import dumps
from json import loads

from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring

ZILLOW_ENDPOINT = '''http://www.zillow.com/webservice'''
GET_SEARCH_RESULT_API_NAME = 'GetSearchResults.htm'
ZWS_ID = '''X1-ZWz1fk5y3xqn7v_10irx'''

def build_url(api_name):
    return '%s/%s' % (ZILLOW_ENDPOINT, api_name)

""" Zillow API: GetSearchResult """
def getSearchResult(address, citystatezip, rentzestimate=False):
    payload = {
        'zws-id': ZWS_ID,
        'address': address,
        'citystatezip': citystatezip,
        'rentzestimate': rentzestimate
    }

    response = requests.get(build_url(GET_SEARCH_RESULT_API_NAME), params=payload)
    res_json = loads(dumps(bf.data(fromstring(response.text))))

    # extract info from response
    for key in res_json:
        if (res_json[key] is not None and
            res_json[key]['response'] is not None and
            res_json[key]['response']['results'] is not None):
            return res_json[key]['response']['results']['result']
        else:
            return {}
