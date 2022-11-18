from typing import List, Dict, Any
import re
from typing import List, Dict, Any
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

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
brand = {}
EMPTY_STRING = ''
EMPTY_FLOAT = 'null'


def sephora_process(record):
    record["name"] = record["name"].split("Eau")[0].strip()
    record["brand"] = record["brand"].strip().lower()
    size = re.search("[0-9]+.*[0-9]*.*(oz|ml)", record["size"],re.I)
    record["size"] = size.group() if size else EMPTY_STRING
    rating = re.search("[0-9]+\.*[0-9]*" ,record['rating'])
    record["ratings"] = rating.group() if rating else EMPTY_FLOAT
    price = re.search("[0-9]+\.*[0-9]*", record["price"])
    record["price"] = price.group() if price else EMPTY_FLOAT
    for key in record.keys():
        if re.match("scent", key, re.I):
            record["scent"] = record[key].strip()
            break
    if ("scent" not in record):
        record["scent"] = None
    return record


def commit_ent_rel(tx, data: List[Dict[str, Any]], plt_info:dict) ->None:
    global perfume_id, brand_id, brand;

    # Query String
    add_perfume = ""
    add_brand = ""
    add_platform = ""
    add_relation = ""

    nonstr = ['price', 'ratings', 'comments']
    string = ['name', 'size', 'scent', 'brand', 'url']

    # Add Platform Entity
    plt_id = plt_info['id']
    plt_name = plt_info['name']
    plt_store = plt_info['store']
    add_platform = 'CREATE ( t'+plt_id+':Platform {name: "'+ \
            plt_name+'", has_offine_store: '+plt_store+'}) '

    for record in data:
        # processing data
        record = plt_info["func"](record)

        # Add Brand Entity
        if (record["brand"] not in brand):
            brand[record["brand"]] = f"b{brand_id}"
            brand_id += 1
            add_brand += "CREATE ( b{0}:Brand {1}) ".format(
                brand_id, '{name: "'+ record["brand"] +'"}'
            )

        # Add Perfume Entity
        line = "CREATE ( n{0}:Perfume {1}) "
        line2 = ", ".join(map(lambda x: f'{x}:"{record[x]}"', string))
        line3 = ", ".join(map(lambda x: f'{x}: {record[x]}', nonstr))
        r = line.format(perfume_id, "{"+line2+", "+line3+"}")
        add_perfume += r

        # Add relation
        add_relation += f"CREATE (n{perfume_id})-[:listed_on]->(t{plt_id}) "
        add_relation += "CREATE (n{0})-[:product_of]->(t{1}) ".format(
            perfume_id, brand[record["brand"]]
        )
        perfume_id += 1


    # run query:
    tx.run(add_perfume) #Entity
    tx.run(add_brand)   #Entity
    tx.run(add_platform)#Entity
    tx.run(add_relation)#Relation
    return None


if __name__ == "__main__":
    import os, sys
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("../")
    sys.path.append(os.getcwd())
    import crawler.modules.jsonl as jsonl

    # sephora_data = jsonl.load_to_list("./data/sephora.jsonl")

    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "perfumeKG"

    platform_infos = [
        {"name":"Amazon", "id": '0', "store": '0', "data": "./data/amazon.jsonl", "func": None},
        {"name":"Sephora", "id": "1", "store": '1', "data": "./data/sephora.jsonl", "func": sephora_process},
        {"name": "FragranceNet", "id": '2', "store": '0', "data": "./data/fragranceNet.jsonl", "func": None},
    ]

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session(database="neo4j") as session:
        for info in platform_infos[1:2]:
            result = session.execute_write(
                commit_ent_rel,
                jsonl.load_to_list(info["data"]),
                info
            )
    # commit_ent_rel_sephora(data)


