from neomodel import db

perfume_names = db.cypher_query(
    '''
    MATCH (n:Perfume) 
    RETURN DISTINCT n.name AS perfume_names
    '''
)[0]

PERFUME_NAMES = sorted([perfume_name[0] for perfume_name in perfume_names])



# perfume_sizes = db.cypher_query(
#     '''
#     MATCH (n:Perfume) 
#     RETURN DISTINCT n.size AS perfume_sizes
#     '''
# )[0]

# PERFUME_SIZES = sorted([perfume_size[0] for perfume_size in perfume_sizes])

# jurisdictions = db.cypher_query(
#     '''
#     MATCH (n)
#     RETURN DISTINCT n.jurisdiction AS jurisdiction
#     '''
# )[0]

# data_sources = db.cypher_query(
# 	'''
# 	MATCH (n)
# 	RETURN DISTINCT n.sourceID AS dataSource
# 	'''
# )[0]

# COUNTRIES = sorted([country[0] for country in countries])
# JURISDICTIONS = sorted([jurisdiction[0] for jurisdiction in jurisdictions if isinstance(jurisdiction[0], str)])
# DATASOURCE = sorted([data_source[0] for data_source in data_sources if isinstance(data_source[0], str)])
