from typing import Dict, List, Tuple
from time import sleep
import requests as rqs
from lxml import etree
import os

def Get_Root_dir():
    path = __file__
    for _ in range(3):
        path = os.path.split(path)[0]
    return path

class PatchResult:
    def __init__(self, domain: str, header: dict) -> None:
        self.node = None
        self.root_url = domain
        self.header = header

    def _get_text_list(self, xpath, if_null) ->List[str]:
        result = self.node.xpath(xpath)
        if (len(result)):
            return [i.strip() for i in result]
        else:
            return [if_null]

    def _get_joined_text(self, xpath:str, sep:str) ->str:
        texts = self._get_text_list(xpath, "")
        return sep.join(texts)

    def _get_details(self, remove_key: List[str]=[]):
        details_key = self._get_text_list("//*[@id='detailBullets_feature_div']//li/span/span[1]/text()", "")
        details_val = self._get_text_list("//*[@id='detailBullets_feature_div']//li/span/span[2]/text()", "")
        details_key = [i.split("\n")[0].strip('\u200e') for i in details_key]
        result = dict(map(lambda x,y: (x, y), details_key, details_val))
        for key in remove_key:
            if (key in result): result.pop(key)
        return result

    def _get_ave_ratings(self):
        ratings = {}
        # overall
        stars = self._get_text_list("//span[@data-hook='rating-out-of-text']/text()", "")
        ratings["Overall"] = stars
        nodes = self.node.xpath("//div[@data-hook='cr-summarization-attribute']/div/div")
        for node in nodes:
            key = node.xpath("./div[1]//span/text()")[0].strip()
            value = node.xpath("./div[2]/i/span/text()")[0].strip()
            ratings[key] = value
        return ratings

    def _get_comments(self, max_len: int=50) -> List[Tuple[str]]:
        reviews_link = self.node.xpath("//*[@data-hook='see-all-reviews-link-foot']/@href")
        if (not len(reviews_link)): return []
        href = reviews_link[0]
        href = ("https://www.amazon.com/"+href)
        response = rqs.get(href, headers=self.header)
        reviews_link = self.node.xpath("//*[@data-hook='see-all-reviews-link-foot']/@href")

        if (not len(reviews_link)): return []
        href = reviews_link[0]

        i=1
        comments = []
        review_objs = [None]
        print("    Crawling Comments:  Page 0...", end=' ')
        while (len(review_objs) and i<=max_len):
            param = "&pageNumber={0}"
            url = (self.root_url+href+param.format(i))
            response = rqs.get(url, headers=self.header)
            if (response.status_code != 200):
                print(response.status_code)
                break
            ct = etree.HTML(response.text)
            review_objs = ct.xpath("//*[@data-hook='review']")
            for obj in review_objs:
                reviews = obj.xpath(".//*[@data-hook='review-star-rating']//text()")
                reviews = " ".join(map(lambda x: x.strip(), reviews)).strip()
                comment = obj.xpath(".//*[@data-hook='review-body']//text()")
                comment = " ".join(map(lambda x: x.strip(), comment)).strip()
                comments.append((reviews, comment))
            print(f"\r    Crawling Comments: Page {i}...", end = ' ')
            sleep(0.6)
            i+=1
        print("done.")
        return comments


class Amazon_Detail_Patch(PatchResult):
    def __init__(self, header: dict) -> None:
        super().__init__("https://www.amazon.com/", header)

    def get_result(self, URL_pattern, **kwargs) -> Dict[str, str]:
        r = rqs.get(URL_pattern, headers=self.header)
        if (r.status_code!=200):
            print(f"Error: {r.status_code}")
            return {}
        self.node = etree.HTML(r.text)
        title = self._get_joined_text("//*[@id='productTitle']/text()", "")
        price = self._get_joined_text("//*[@id='corePrice_desktop']//*[@id='sns-base-price']/text()", "")
        style = self._get_joined_text("//*[@id='variation_style_name']/div/span/text()", "")
        details = self._get_details(remove_key=["UPC", "ASIN", "Batteries"])
        ratings = self._get_ave_ratings()
        comments = self._get_comments(**kwargs)
        attr_key = self._get_text_list("//table[@class='a-normal a-spacing-micro']//tr/td[1]/span/text()", "")
        attr_val = self._get_text_list("//table[@class='a-normal a-spacing-micro']//tr/td[2]/span/text()", "")
        attrs = dict(zip(attr_key, attr_val))
        result =  {
            "title": title,
            "price": price,
            "style": style,
            "ratings": ratings,
            "comments": comments,
        }
        result.update(attrs)
        result.update(details)
        # "attrs": attrs, "details": details,
        self.node = None
        return result

    def get_page_urls(self, page_pattern:str, max_page:int=30) -> List[str]:
        all_urls = []
        for page in range(max_page):
            print(f"\r---> Processing Search Page: {page+1}...", end='')
            r = rqs.get(page_pattern.format(page), headers=self.header)
            if (r.status_code != 200):
                print(f"Http Error: {r.status_code}")
                return all_urls
            self.node = etree.HTML(r.text)
            hrefs = self._get_text_list("//*[@data-component-type='s-search-result']//h2/a/@href", None)
            for url in hrefs:
                if (url != None):
                    all_urls.append(self.root_url + url)
        print(" done.")
        return all_urls
