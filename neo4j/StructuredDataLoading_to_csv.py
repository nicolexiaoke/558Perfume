from functools import reduce
from typing import List, Dict, Any, Union
import re
from typing import List, Dict, Any
from neo4j import GraphDatabase
import os, sys
from CrawlingDataLoading import *
import CrawlingDataLoading

EMPTY_STRING = 'NULL'
EMPTY_RATING_FLOAT = 0
EMPTY_PRICING_FLOAT = ~(-1 ^ (1<<31))

##     nonstr = ['price', 'rating', 'comments']
##     string = ['name', 'size', 'scent', 'brand', 'url']
## Ent: Brand
## Ent: SellingPlatform (Not applicable)

all_brands: Dict[str, str]
brand_id: int
structured_id = 1

def find_brand(name, brand):
    global all_brands, brand_id;
    # 原 brand
    if (not brand or re.match("na", brand.strip(), re.I) or brand==''): said_brand = None
    else: said_brand = brand.strip()
    # 预测brand
    pred_brand = None
    for brand in all_brands.keys():
        if said_brand and re.search(brand, said_brand, re.I) or re.search(brand, name, re.I):
            pred_brand = brand; break;

    if (pred_brand):
        return False,pred_brand
    elif said_brand:
        all_brands[said_brand] = f"b{brand_id}";
        brand_id+=1;
        return True,said_brand;
    else:
        all_brands["Unknown"] = f"b{brand_id}"
        brand_id+=1
        return True, "Unknown"

def preprocessing(record: List[Union[str,float]]) -> Dict[str, Union[str, float]]:
    mapping = {}
    mapping["name"] = record[0].strip().capitalize()
    mapping['brand'] = record[2].strip().replace("-"," ").capitalize() \
                    if isinstance(record[2], str) else ''
    oz_size = CrawlingDataLoading.size_converter(record[3], 1, "ml")
    mapping["size"] = f"{oz_size:.1f} oz" \
                        if oz_size else EMPTY_STRING
    mapping["scent"] = EMPTY_STRING
    mapping["url"] = EMPTY_STRING
    mapping["price"] = round((float(record[7].replace(",","")) \
                if isinstance(record[7], str) else record[7])/3.75, 2)
    mapping["rating"] = EMPTY_RATING_FLOAT
    mapping["comments"] = []
    return mapping

def commit_ent_rel(tx, data: List[List[Union[str, float]]]):
    global all_brands, structured_id;
    nonstr = ['price', 'rating', 'comments']
    string = ['name', 'size', 'scent', 'brand', 'url']
    lines = []
    for raw_rec in data:
        record = preprocessing(raw_rec)
        flag, brand = find_brand(record["name"], record["brand"])
        record["brand"] = brand if brand else "Unknown"

        lines.append(f's{structured_id}, {all_brands[brand]},"{brand}",,,'+
                     ",".join(map(lambda x: f'"{record[x]}"', string)) + "," +
                     ",".join(map(lambda x: f'{record[x]}' , nonstr)))
        structured_id += 1
    return lines

if __name__ == "__main__":
    import pandas as pd
    work_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(work_path)
    sys.path.append(os.path.split(work_path)[0])
    import crawler.modules.jsonl as jsonl

    # 处理新 structured data
    df = pd.read_csv("../data/structured_data/abeer_alshathri_parfum_souq.csv")
    data = df.values.tolist()

    # 获取原数据
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "perfumeKG"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session(database="neo4j") as session:
        for info in CrawlingDataLoading.platform_infos:
            session.execute_write(
                CrawlingDataLoading.commit_ent_rel,
                jsonl.load_to_list(info["data"]),
                info
            )
        lines = session.execute_write(
            commit_ent_rel,
            data,
        )
        with open("../data/all_data.csv", 'a+', encoding='utf-8') as f:
            # f.write(",".join(['id','brand_id',"brand_name",'plt_name', 'plt_id',
            #      'name', 'size', 'scent', 'brand', 'url','price', 'rating', 'comments'])+"\n")
            for lin in lines:
                f.write(lin + "\n")


