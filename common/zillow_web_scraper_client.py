import requests

from lxml import html

URL = '''http://www.zillow.com'''
GET_PROPERTY_BY_ZPID_PATH = '''homes'''

# XPATH
SEARCH_XPATH_FOR_ZPID = '''//div[@id='list-results']/div[@id='search-results']/ul[@class='photo-cards']/li/article/@id'''
GET_INFO_XPATH_FOR_STREET_ADDR = '''//header[@class='zsg-content-header addr']/h1[@class='notranslate']/text()'''
GET_INFO_XPATH_FOR_CITY_STATE_ZIP = '''//header[@class='zsg-content-header addr']/h1[@class='notranslate']/span/text()'''
GET_INFO_XPATH_FOR_TYPE = '''//div[@class='loan-calculator-container']/div/@data-type'''
GET_INFO_XPATH_FOR_BEDROOM = '''//header[@class='zsg-content-header addr']/h3/span[@class='addr_bbs'][1]/text()'''
GET_INFO_XPATH_FOR_BATHROOM = '''//header[@class='zsg-content-header addr']/h3/span[@class='addr_bbs'][2]/text()'''
GET_INFO_XPATH_FOR_SIZE = '''//header[@class='zsg-content-header addr']/h3/span[@class='addr_bbs'][3]/text()'''
GET_INFO_XPATH_FOR_SALE = '''//div[@id='home-value-wrapper']/div[@class='estimates']/div/text()'''
GET_INFO_XPATH_LIST_FOR_PRICE = '''//div[@id='home-value-wrapper']/div[@class='estimates']/div[@class='main-row  home-summary-row']/span/text()'''
GET_INFO_XPATH_FOR_LATITUDE = '''//div[@class='zsg-layout-top']/p/span/span[@itemprop='geo']/meta[@itemprop='latitude']/@content'''
GET_INFO_XPATH_FOR_LONGITUDE = '''//div[@class='zsg-layout-top']/p/span/span[@itemprop='geo']/meta[@itemprop='longitude']/@content'''
GET_INFO_XPATH_DESCRIPTION = '''//div[@class='zsg-lg-2-3 zsg-md-1-1 hdp-header-description']/div[@class='zsg-content-component']/div/text()'''
GET_INFO_XPATH_FOR_FACTS = '''//div[@class='fact-group-container zsg-content-component top-facts']/ul/li/text()'''
GET_INFO_XPATH_FOR_ADDITIONAL_FACTS = '''//div[@class='fact-group-container zsg-content-component z-moreless-content hide']/ul/li/text()'''
GET_SIMILAR_HOMES_FOR_SALE_XPATH = '''//ol[@id='fscomps']/li/div[@class='zsg-media-img']/a/@href'''

def build_url(url, path):
    if url[-1] == "/":
        url = url[:-1]
    return '%s/%s' % (url, path)

""" get property information by Zillow property ID (zpid) """
def get_property_by_zpid(zpid):
    request_url = '%s/%s_zpid' % (build_url(URL, GET_PROPERTY_BY_ZPID_PATH), str(zpid))
    session_requests = requests.session()
    response = session_requests.get(request_url)

    try:
        tree = html.fromstring(response.content)
    except Exception:
        return {}

    # street address
    street_address = tree.xpath(GET_INFO_XPATH_FOR_STREET_ADDR)
    if len(street_address) == 0:
        street_address = ''
    else:
        street_address = street_address[0].strip(', ')

    # city, state and zipcode
    city_state_zipcode = tree.xpath(GET_INFO_XPATH_FOR_CITY_STATE_ZIP)
    if len(city_state_zipcode) == 0:
        city_state_zipcode = ''
    else:
        city_state_zipcode = city_state_zipcode[0]
    city = city_state_zipcode.split(',')[0].strip(', ')
    state = city_state_zipcode.split(',')[1].split(' ')[1].strip()
    zipcode = city_state_zipcode.split(',')[1].split(' ')[2].strip()

    return {
        'zpid': zpid,
        'street_address': street_address,
        'city': city,
        'state': state,
        'zipcode': zipcode
    }

""" get similar homes for sale """
def get_similar_homes_for_sales_by_id(zpid):
    pass
