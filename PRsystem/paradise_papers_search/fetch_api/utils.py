# from .constants import COUNTRIES, JURISDICTIONS, DATASOURCE
from .constants import PERFUME_NAMES
from neomodel import db

from .models import (
    Perfume,
    Brand,
    SellingPlatform
)

# For easily access each of the model classes programmatically, create a key-value map.
MODEL_ENTITIES = {
    'Perfume': Perfume,
    'Brand': Brand,
    'SellingPlatform': SellingPlatform
}


###################################################################
# Queries Functions
###################################################################

def filter_nodes(node_type, search_text, size, smell, lprice = 0, lrating = 0, hprice = 10000000000, hrating = 5):
    '''
    node_type: Perfume/Brand/..
    search_text: key word to serch --> Perfume.nodes.filter(name__contains=search_text)
    '''
    print('invoked by displayNodeSearch()')
    print('node_type:', node_type)
    print('search_text:', search_text)
    pre_node_set = node_type.nodes

    # On DeliveryOption nodes we want to check the search_text against the description property
    # For any other we check against the name property
    
    pre_node_set.filter(name__iexact=search_text)

    seednode = pre_node_set[0]

    seedid = seednode.node_id
    node_set =  db.cypher_query("MATCH (:Perfume {node_id: $seedid})\
         -[:sameAs]-> (n)\
        RETURN DISTINCT n",\
            {'seedid': seedid}
        )[0]
    
    SANODE = [node_type.inflate(n[0]) for n in node_set]
    SANODE.insert(0, seednode)
    
    # print('\n\n in filter_ssnodes, noe_set:', SSNODE)

    return SANODE

    # # Only Perfume store size, smell, price, rating info
    # # if node_type.__name__ == 'Perfume':
    # #     node_set.filter(size__icontains=size)
    # #     node_set.filter(smell__icontains=smell)
    # #     node_set.filter(price__gte=lprice)
    # #     node_set.filter(rating__gte=lrating)
    # #     node_set.filter(price__lte=hprice)
    # #     node_set.filter(rating__lte=lrating)

    # # # print(node_set[0])
    # # print(node_set[1])

    # return node_set

def filter_ssnodes(node_type, search_text, size, smell, lprice = 0, lrating = 0, hprice = 10000000000, hrating = 5):
    '''
    node_type: Perfume/Brand/..
    search_text: key word to serch --> Perfume.nodes.filter(name__contains=search_text)
    '''
    pre_node_set = node_type.nodes
    if search_text != '':
        pre_node_set.filter(name__iexact=search_text)
    if size != '':
        pre_node_set.filter(size__icontains=size)

    
    
    seednode = pre_node_set[0]
    '''
        seednode:
        {'node_properties': {'node_id': '1', 'name': 'Escape', 'size': '1.7 oz', 
        'smell': '', 'price': 31.99, 'rating': 4.5, 
        'comments': 'I love Calvin Klein escape. Problem is I ordered it February 22 and its still not here. 
        I had a second order and it already came. Love the prices, discounts, and convenience.', 
        'url': 'https://www.fragrancenet.com/cologne/calvin-klein/escape/edt#122757'}}
    '''
    seedid = seednode.node_id
    node_set =  db.cypher_query("MATCH (:Perfume {node_id: $seedid})\
         -[:haveSimilarScents]-> (n)\
        RETURN DISTINCT n",\
            {'seedid': seedid}
        )[0]
    
    SSNODE = [node_type.inflate(n[0]) for n in node_set]
    SSNODE.insert(0, seednode)
    
    # print('\n\n in filter_ssnodes, noe_set:', SSNODE)

    return SSNODE

def filter_spnodes(node_type, search_text, size, smell, lprice = 0, lrating = 0, hprice = 10000000000, hrating = 5):
    '''
    node_type: Perfume/Brand/..
    search_text: key word to serch --> Perfume.nodes.filter(name__contains=search_text)
    '''
    pre_node_set = node_type.nodes
    if search_text != '':
        pre_node_set.filter(name__iexact=search_text)
    if size != '':
        pre_node_set.filter(size__icontains=size)

    seednode = pre_node_set[0]
    seedid = seednode.node_id
    node_set =  db.cypher_query("MATCH (:Perfume {node_id: $seedid})\
         -[:haveSimilarPrices]-> (n)\
        RETURN DISTINCT n",\
            {'seedid': seedid}
        )[0]
    
    SPNODE = [node_type.inflate(n[0]) for n in node_set]
    SPNODE.insert(0, seednode)
    
    # print('\n\n in filter_spnodes, noe_set:', SPNODE)

    return SPNODE

def filter_sbnodes(node_type, search_text, size, smell, lprice = 0, lrating = 0, hprice = 10000000000, hrating = 5):
    '''
    node_type: Perfume/Brand/..
    search_text: key word to serch --> Perfume.nodes.filter(name__contains=search_text)
    '''
    pre_node_set = node_type.nodes
    if search_text != '':
        pre_node_set.filter(name__iexact=search_text)
    if size != '':
        pre_node_set.filter(size__icontains=size)

    
    
    seednode = pre_node_set[0]
    seedid = seednode.node_id
    seedbrand = db.cypher_query("MATCH (:Perfume {node_id: $seedid})\
                                -[:productOf]-> (n)\
                                return n.name", {'seedid': seedid})[0][0][0]

    print(seedbrand)

    node_set =  db.cypher_query("MATCH (:Perfume {node_id: $seedid})\
                          -[:productOf]-> (:Brand {name: $seedbrand}) <-[:productOf]-(n)\
                        return n",\
                         {'seedid': seedid, 'seedbrand': seedbrand}
        )[0]
    
    SSNODE = [node_type.inflate(n[0]) for n in node_set]
    SSNODE.insert(0, seednode)
    
    # print('\n\n in filter_ssnodes, noe_set:', SSNODE)
    print('len(sbnodes):', len(SSNODE))

    return SSNODE
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

def count_ssnodes(count_info):
    count = {}
    node_type               = count_info['node_type']
    search_word             = count_info['name']
    size                 = count_info['size']
    smell            = count_info['smell']
    lprice             = count_info['lprice']
    hprice             = count_info['hprice']
    lrating             = count_info['lrating']
    hrating             = count_info['hrating']
    node_set                = filter_ssnodes(MODEL_ENTITIES[node_type], search_word, size, smell, lprice, lrating, hprice, hrating)
    count['count']          = len(node_set)

    return count

def count_spnodes(count_info):
    count = {}
    node_type               = count_info['node_type']
    search_word             = count_info['name']
    size                 = count_info['size']
    smell            = count_info['smell']
    lprice             = count_info['lprice']
    hprice             = count_info['hprice']
    lrating             = count_info['lrating']
    hrating             = count_info['hrating']
    node_set                = filter_spnodes(MODEL_ENTITIES[node_type], search_word, size, smell, lprice, lrating, hprice, hrating)
    count['count']          = len(node_set)

    return count

def count_sbnodes(count_info):
    count = {}
    node_type               = count_info['node_type']
    search_word             = count_info['name']
    size                 = count_info['size']
    smell            = count_info['smell']
    lprice             = count_info['lprice']
    hprice             = count_info['hprice']
    lrating             = count_info['lrating']
    hrating             = count_info['hrating']
    node_set                = filter_sbnodes(MODEL_ENTITIES[node_type], search_word, size, smell, lprice, lrating, hprice, hrating)
    count['count']          = len(node_set)

    print('len(sbnodes):', count)
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
def assign_platform(node_id):
    platform = db.cypher_query(
        "MATCH (:Perfume {node_id: $node_id})\
        -[:listedOn]->(n:SellingPlatform) RETURN n.name ", {'node_id': node_id} )[0]

    # print('platform:',platform)
    if len(platform) != 0 :
        return platform[0][0]
    else:
        return '-'

def assign_brand(node_id):
    brand = db.cypher_query(
        "MATCH (:Perfume {node_id: $node_id})\
        -[:productOf]->(n:Brand) RETURN n.name ", {'node_id': node_id} )[0]

    # print('brand:',brand)
    if len(brand) != 0 and brand[0][0] != 'Na':
        return brand[0][0]
    else:
        return '-'

def beautify_frontend_display(serialized_nodes):
    for i, node in enumerate(serialized_nodes):
        nid = node['node_properties']['node_id']
        serialized_nodes[i]['node_properties']['platform'] = assign_platform(nid)
        serialized_nodes[i]['node_properties']['brand'] = assign_brand(nid)
        if serialized_nodes[i]['node_properties']['smell'] == 'NULL'\
                or serialized_nodes[i]['node_properties']['smell'] == 'None':
            serialized_nodes[i]['node_properties']['smell'] = '-'
        if serialized_nodes[i]['node_properties']['rating'] == 0:
            serialized_nodes[i]['node_properties']['rating'] = '-'
        if serialized_nodes[i]['node_properties']['price'] == 2147483648:
            serialized_nodes[i]['node_properties']['price'] = '-'
        if serialized_nodes[i]['node_properties']['size'] == 'NULL':
            serialized_nodes[i]['node_properties']['size'] = '-'


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
    fetched_nodes   = node_set
    serialized_nodes = [node.serialize for node in fetched_nodes]
    # print('in fetch_nodes:', type(serialized_nodes[0]), serialized_nodes[0])


    print('in fetch_nodes:', type(serialized_nodes[0]), serialized_nodes[0])
    def myFunc_rating(e):
        return e['node_properties']['rating']
    serialized_nodes.sort(key=myFunc_rating, reverse=True)
 
    #add platform and brand here, alter the output of some missing data
    beautify_frontend_display(serialized_nodes)


    return serialized_nodes
    # return fetched_nodes

def fetch_lpnodes(fetch_info):
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
    fetched_nodes   = node_set
    serialized_nodes = [node.serialize for node in fetched_nodes]

    def myFunc_price(e):
        return e['node_properties']['price']
    
    serialized_nodes.sort(key=myFunc_price, reverse=False)

    print(len(serialized_nodes))

    #add platform and brand here, alter the output of some missing data
    beautify_frontend_display(serialized_nodes)

    return serialized_nodes

def fetch_ssnodes(fetch_info):
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
    node_set           = filter_ssnodes(MODEL_ENTITIES[node_type], search_word, size, smell, lprice, lrating, hprice, hrating)
    fetched_nodes   = node_set
    serialized_nodes = [node.serialize for node in fetched_nodes]


    seed_node = serialized_nodes[0]
    serialized_nodes = serialized_nodes[1:]

    def myFunc_rating(e):
        return e['node_properties']['rating']
    serialized_nodes.sort(key=myFunc_rating, reverse=True)

    serialized_nodes.insert(0, seed_node)
 
    #add platform and brand here, alter the output of some missing data
    beautify_frontend_display(serialized_nodes)

    return serialized_nodes


def fetch_sbnodes(fetch_info):
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
    node_set           = filter_sbnodes(MODEL_ENTITIES[node_type], search_word, size, smell, lprice, lrating, hprice, hrating)
    fetched_nodes   = node_set
    serialized_nodes = [node.serialize for node in fetched_nodes]

    seed_node = serialized_nodes[0]
    serialized_nodes = serialized_nodes[1:]

    def myFunc_rating(e):
        return e['node_properties']['rating']
    serialized_nodes.sort(key=myFunc_rating, reverse=True)

    
    serialized_nodes.insert(0, seed_node)

    #add platform and brand here, alter the output of some missing data
    beautify_frontend_display(serialized_nodes)

    return serialized_nodes

def fetch_spnodes(fetch_info):
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
    node_set           = filter_spnodes(MODEL_ENTITIES[node_type], search_word, size, smell, lprice, lrating, hprice, hrating)
    fetched_nodes   = node_set
    serialized_nodes = [node.serialize for node in fetched_nodes]


    seed_node = serialized_nodes[0]
    serialized_nodes = serialized_nodes[1:]

    def myFunc_rating(e):
        return e['node_properties']['rating']
    serialized_nodes.sort(key=myFunc_rating, reverse=True)
    
    serialized_nodes.insert(0, seed_node)

    #add platform and brand here, alter the output of some missing data
    beautify_frontend_display(serialized_nodes)

    return serialized_nodes

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

def fetch_perfume_sizes(name_info):
    print('in utils, fetch_perfume_sizes, name_info:', name_info)
    name_info = name_info
    
    if name_info != '':
        perfume_sizes = db.cypher_query(
        "MATCH (n:Perfume {name: $name_info})\
        RETURN DISTINCT n.size AS perfume_sizes", {'name_info': name_info} )[0]
    else:
        perfume_sizes = db.cypher_query(
        '''
        MATCH (n:Perfume) 
        RETURN DISTINCT n.size AS perfume_sizes
        '''
        )[0]

    PERFUME_SIZES = sorted([perfume_size[0] for perfume_size in perfume_sizes])
    
    return PERFUME_SIZES




# def fetch_jurisdictions():
#     return JURISDICTIONS


# def fetch_data_source():
#     return DATASOURCE
