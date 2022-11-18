### ---> data splitting:

### Original Table:
### table[record idx][col_name]
### ['name', 'price', 'size', 'scent', 'brand', 'url', 'ratings', 'comments', 'platform(id)']

### To
# Ent Table:
#
### Table 1: (Perfume)
### ['name', 'price', 'size', 'scent', 'url', 'ratings', 'comments'] + 'id'
### Table 2: (Platform)
### ['name', 'platform(id)']
### Table 3: (Brand)
### ['name'] + 'brand_id'

# To Rel Table:
#

### Table 4: (is product of)
### ['Perfume_id',"Brand_id"]
### Table 5: (is listed on)
### ["Perfume_id", "Platform_id"]


def commit_entities() ->None:
        pass

def commit_relationship(data: List[str], rel: str) -> None:
        assert len(data)==2;
        pass
