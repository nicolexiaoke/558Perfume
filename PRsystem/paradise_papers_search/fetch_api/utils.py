# from .constants import COUNTRIES, JURISDICTIONS, DATASOURCE
from .constants import PERFUME_NAMES

from .models import (
    Perfume,
    Brand,
    SellingPlatform,
    DeliveryOption
)

# For easily access each of the model classes programmatically, create a key-value map.
MODEL_ENTITIES = {
    'Perfume': Perfume,
    'Brand': Brand,
    'SellingPlatform': SellingPlatform,
    'DeliveryOption': DeliveryOption
}


###################################################################
# Queries Functions
###################################################################

def filter_nodes(node_type, search_text, size, smell, lprice = 0, lrating = 0, hprice = 10000000000, hrating = 5):
    '''
    node_type: Perfume/Brand/..
    search_text: key word to serch --> Perfume.nodes.filter(name__contains=search_text)
    '''

    node_set = node_type.nodes

    # On DeliveryOption nodes we want to check the search_text against the description property
    # For any other we check against the name property
    if node_type.__name__ == 'DeliveryOption':
        node_set.filter(description__icontains=search_text)
    else:
        node_set.filter(name__icontains=search_text)

    # Only Perfume store size, smell, price, rating info
    # if node_type.__name__ == 'Perfume':
    #     node_set.filter(size__icontains=size)
    #     node_set.filter(smell__icontains=smell)
    #     node_set.filter(price__gte=lprice)
    #     node_set.filter(rating__gte=lrating)
    #     node_set.filter(price__lte=hprice)
    #     node_set.filter(rating__lte=lrating)

    return node_set


'''
count_info:
{
    'node_type': '',
    'name': '',
    'size': '',
    'smell': '',
    'lprice': ,
    'hprice': ,
    'lrating': ,
    'hrating':
}
'''

def count_nodes(count_info):
    count = {}
    node_type               = count_info['node_type']
    search_word             = count_info['name']
    size                 = count_info['size']
    smell            = count_info['smell']
    lprice             = count_info['lprice']
    hprice             = count_info['hprice']
    lrating             = count_info['lrating']
    hrating             = count_info['hrating']
    node_set                = filter_nodes(MODEL_ENTITIES[node_type], search_word, size, smell, lprice, lrating, hprice, hrating)
    count['count']          = len(node_set)

    return count


'''
fetch_info:
{
    'node_type': '',
    'name': '',
    'size': '',
    'smell': '',
    'lprice': ,
    'hprice': ,
    'lrating': ,
    'hrating':
    'limit': 10,
    'page': 1
}
'''
def fetch_nodes(fetch_info):
    node_type       = fetch_info['node_type']
    search_word     = fetch_info['name']
    size                 = fetch_info['size']
    smell            = fetch_info['smell']
    lprice             = fetch_info['lprice']
    hprice             = fetch_info['hprice']
    lrating             = fetch_info['lrating']
    hrating             = fetch_info['hrating']
    limit           = fetch_info['limit']
    start           = ((fetch_info['page'] - 1) * limit)
    end             = start + limit
    node_set           = filter_nodes(MODEL_ENTITIES[node_type], search_word, size, smell, lprice, lrating, hprice, hrating)
    fetched_nodes   = node_set[start:end]

    return [node.serialize for node in fetched_nodes]
    # return fetched_nodes


'''
node_info:
{
    'node_type': '',
    'node_id': ''
}
'''
def fetch_node_details(node_info):
    node_type       = node_info['node_type']
    id         = node_info['node_id']
    node            = MODEL_ENTITIES[node_type].nodes.get(node_id=id)
    node_details    = node.serialize
    # node_details    = node

    # Make sure to return an empty array if not connections
    node_details['node_connections'] = []
    if (hasattr(node, 'serialize_connections')):
        node_details['node_connections'] = node.serialize_connections

    return node_details


def fetch_perfume_names():
    return PERFUME_NAMES


# def fetch_jurisdictions():
#     return JURISDICTIONS


# def fetch_data_source():
#     return DATASOURCE
