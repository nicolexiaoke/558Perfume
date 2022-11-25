from functools import reduce
from typing import List, Dict, Any
import re
from typing import List, Dict, Any
from neo4j import GraphDatabase
import os, sys
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


perfume_id = brand_id = 1
all_brands = {}
EMPTY_STRING = 'NULL'
EMPTY_RATING_FLOAT = 0x0
EMPTY_PRICING_FLOAT = ~(-1 ^ (1<<0x1F))

def hexstring_to_normal(string: str):
    if ("+" in string): return string
    new_url = ""
    flag = 0
    num = ""
    for char in string:
        if (not flag and char != '%'):
            new_url+=char
        elif (char == '%'):
            flag = 2
        elif (flag == 2):
            num = char
            flag -= 1
        else:
            num += char
            new_url += chr(int(num, base=16))
            flag = 0
    return new_url

def sephora_process(record: Dict[str, str]):
    # print(record)
    record["name"] = record["name"].split("Eau")[0].strip()
    record["brand"] = record["brand"].strip().lower()
    # size = re.search("[0-9]+.*[0-9]*.*(oz|ml)", record["size"],re.I)
    # record["size"] = size.group().lower() if size else EMPTY_STRING
    rating = re.search("[0-9]+\.*[0-9]*" ,record['rating'])
    record["ratings"] = rating.group() if rating else EMPTY_RATING_FLOAT
    price = re.search("[0-9]+\.*[0-9]*", record["price"])
    record["price"] = price.group() if price else EMPTY_PRICING_FLOAT
    for key in list(record.keys()):
        if re.search("scent", key, re.I):
            if record[key]:
                record["scent"] = record[key].strip()
    if ("scent" not in record):
        record["scent"] = None
    return record

def amazon_process(record: Dict[str, str]):
    url = hexstring_to_normal(record['url'])
    name = record["name"].split("Eau")
    record["name"] = name[0].strip()
    brand = re.search("keywords\=perfume\+[a-z\-\_]+\&" ,url, re.I)
    if (brand):
        record["brand"] = brand.group().split("+")[-1][:-1].strip().lower()
    title_size = re.search("[0-9]+\.*[0-9]*[^a-zA-Z]*(oz|ml)", name[-1], re.I)
    if (not record["size"] and title_size):
        record["size"] = title_size.group().lower()

    ratings = re.search("[0-9]+\.*[0-9]*" ,record["ratings"]["Overall"][0])
    record["ratings"] = ratings.group() if ratings else EMPTY_RATING_FLOAT
    if record["price"]:
        price = re.search("[0-9]+\.*[0-9]*", record["price"])
        record["price"] = price.group() if price else EMPTY_PRICING_FLOAT
    else: record["price"] = EMPTY_PRICING_FLOAT
    comments =  [i[1].replace("\"","\'") for i in record["comments"]]
    record["comments"] = comments
    if (not record["scent"]): record["scent"] = EMPTY_STRING
    else: record["scent"] = record["scent"].replace("\"","'").replace("\xa0","")
    return record

def fragranceNet_process(record: Dict[str, str]):
    path_like = os.path.dirname(record["url"])
    path_like = os.path.split(path_like)
    record["name"] = path_like[1].replace("_", " ").replace("-", ' ')
    record["brand"] = os.path.split(path_like[0])[1]
    if record["size"]:
        size = re.search("[0-9]+\.*[0-9]* (oz|ml)",record["size"])
        record["size"] =  size.group() if size else EMPTY_STRING
    if not record["scent"]:
        record["scent"] = EMPTY_STRING
    if not record["ratings"]:
        record["ratings"] = EMPTY_RATING_FLOAT
    price = re.search("[0-9]+\.*[0-9]*", record["price"])
    record["price"] = price.group() if price else EMPTY_PRICING_FLOAT

    comments =  [i[1].replace("\"","\'") for i in record["comments"]]
    record["comments"] = comments
    # print(record)
    return record

def size_converter(size: str, is_numeric:bool = False, unit:str = "") -> float:
    change = {"Cubic": 0.554113, "(Milli|ml)": 0.0338140499119871,
                  "Centi":3.381404991198710195, "(Ounce|oz)": 1}

    if (is_numeric):
        if isinstance(size, str): return None
        num_size = size
    else:
        if (not size or size==EMPTY_STRING): return None
        numeric = re.search("[0-9]+\.*[0-9]*", size)
        if (not numeric):
            return None
        num_size = float(numeric.group())
        unit = size[numeric.end():].strip()

    for key, item in change.items():
        if re.search(key,unit, re.I):
            if key=="(Milli|ml)" and num_size<10:
                return num_size
            if key=="(Ounce|oz)" and num_size>100:
                return num_size*0.033814
            return num_size*item

    if (num_size<10):
        return num_size
    elif (num_size>=100 or not num_size%10):
        return num_size*0.033814
    else:
        return num_size*0.55413

def commit_ent_rel(tx, data: List[Dict[str, Any]], plt_info:dict) ->List[str]:
    global perfume_id, brand_id, all_brands;
    _brand_name = {}
    # Query String
    add_perfume = ""
    add_brand = ""
    add_platform = ""
    add_relation = ""

    nonstr = ['price', 'rating', 'comments']
    string = ['name', 'size', 'scent', 'brand', 'url']

    # Add Platform Entity
    plt_id = plt_info['id']
    plt_name = plt_info['name']
    plt_store = plt_info['store']
    add_platform = 'CREATE (t'+plt_id+':SellingPlatform {name: "'+ \
            plt_name+f'", has_offline_store: "{plt_store}", node_id: "t{plt_id}" '+'}) '
    lines = []
    for record in data:
        # processing data
        if not len(record): continue

        record: Dict[str, str] = plt_info["func"](record)
        record["rating"] = record["ratings"]
        record["name"] = re.sub("[\x01-\x19\x7b-\x7f\'\",]",'', record["name"]).strip("(-_<>)^$. \t").capitalize()
        if record["brand"]:
            record["brand"] = re.sub("[-_]", " ",record["brand"]).capitalize()
            _brand_name[record['name']] = record["brand"]
        else:
            record["brand"] = _brand_name[record['name']] if record['name'] in _brand_name else EMPTY_STRING

        size = size_converter(record["size"])
        record["size"] = f"{size:.1f} oz" if size else EMPTY_STRING

        if reduce(lambda x,y: x or y, map(lambda x: re.search(x, record["name"], re.I),
                                        ["Mascara", "Lip", "Conceal", "Lash", 'primer']), False):
            continue

        # Add Brand Entity
        if (record["brand"] not in all_brands):
            all_brands[record["brand"]] = f"b{brand_id}"
            add_brand += "CREATE ( b{0}:Brand {1}) ".format(brand_id,
                '{name: "'+ record["brand"] +'", node_id: "' + f"b{brand_id}" +'"}'
            )
            brand_id += 1


        # Add relation
        add_relation += f"CREATE (n{perfume_id})-[:listedOn]->(t{plt_id}) "
        add_relation += "CREATE (n{0})-[:productOf]->({1}) ".format(
            perfume_id, all_brands[record["brand"]]
        )
        # print(add_relation)

        lines.append(f"n{perfume_id},{record['brand']},{all_brands[record['brand']]},{plt_name},t{plt_id},"+
                     ",".join(map(lambda x: f'"{record[x]}"', string)) + "," +
                     ",".join(map(lambda x: f'{record[x]}' , nonstr)))
        perfume_id += 1
        # break

    # run query:
    # return [add_perfume, add_brand, add_platform, add_relation]
    return lines

platform_infos = [
    {"name":"Amazon", "id": '0', "store": 'no', "data": "../data/amazon.jsonl", "func": amazon_process},
    {"name":"Sephora", "id": "1", "store": 'yes', "data": "../data/sephora.jsonl", "func": sephora_process},
    {"name": "FragranceNet", "id": '2', "store": 'no', "data": "../data/fragranceNet.jsonl", "func": fragranceNet_process},
]

if __name__ == "__main__":
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)
    sys.path.append(os.path.split(file_path)[0])
    import crawler.modules.jsonl as jsonl

    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "perfumeKG"

    platform_infos = [
        {"name":"Amazon", "id": '0', "store": 'no', "data": "../data/amazon.jsonl", "func": amazon_process},
        {"name":"Sephora", "id": "1", "store": 'yes', "data": "../data/sephora.jsonl", "func": sephora_process},
        {"name": "FragranceNet", "id": '2', "store": 'no', "data": "../data/fragranceNet.jsonl", "func": fragranceNet_process},
    ]

    add_perfume  = ""
    add_brand    = ""
    add_platform = ""
    add_relation = ""

    driver = GraphDatabase.driver(uri, auth=(user, password))
    lines = []
    with driver.session(database="neo4j") as session:
        for info in platform_infos:

            # perfume, brand, platform, relation = session.execute_write(
            lines.extend(session.execute_write(
                commit_ent_rel,
                jsonl.load_to_list(info["data"]),
                info
            ))

    with open("../data/all_data.csv", 'w', encoding='utf-8') as f:
        f.write(",".join(['id','brand_id',"brand_name",'plt_name', 'plt_id',
            'name', 'size', 'scent', 'brand', 'url','price', 'rating', 'comments'])+"\n")
        for lin in lines:
            f.write(lin + "\n")


