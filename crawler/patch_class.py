from typing import Dict, List, Tuple
from time import sleep
import requests as rqs
from lxml import etree

class PatchResult:
    def __init__(self, response, domain: str, header: dict) -> None:
        self.node = etree.HTML(response.text)
        self.root_url = domain
        self.header = header

    def get_text_list(self, xpath, if_null) ->List[str]:
        result = self.node.xpath(xpath)
        if (len(result)):
            return [i.strip() for i in result]
        else:
            return [if_null]

    def get_joined_text(self, xpath:str, sep:str) ->str:
        texts = self.get_text_list(xpath, "")
        return sep.join(texts)

    def get_details(self, remove_key: List[str]=[]):
        details_key = self.get_text_list("//*[@id='detailBullets_feature_div']//li/span/span[1]/text()", "")
        details_val = self.get_text_list("//*[@id='detailBullets_feature_div']//li/span/span[2]/text()", "")
        details_key = [i.split("\n")[0].strip('\u200e') for i in details_key]
        result = dict(map(lambda x,y: (x, y), details_key, details_val))
        for key in remove_key:
            if (key in result): result.pop(key)
        return result

    def get_ave_ratings(self):
        ratings = {}
        # overall
        stars = self.get_text_list("//span[@data-hook='rating-out-of-text']/text()", "")
        ratings["Overall"] = stars
        nodes = self.node.xpath("//div[@data-hook='cr-summarization-attribute']/div/div")
        for node in nodes:
            key = node.xpath("./div[1]//span/text()")[0].strip()
            value = node.xpath("./div[2]/i/span/text()")[0].strip()
            ratings[key] = value
        return ratings

    def get_comments(self) -> List[Tuple[str]]:
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
        print("Crawling Comments:  Page 0...", end=' ')
        while (len(review_objs)):
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
            print(f"\rCrawling Comments: Page {i}...", end = ' ')
            sleep(0.6)
            i+=1
        print("done.")
        return comments


class Amazon_Detail_Patch(PatchResult):
    def __init__(self, response, header: dict) -> None:
        super().__init__(response, "https://www.amazon.com/", header)

    def get_result(self):
        title = self.get_joined_text("//*[@id='productTitle']/text()", "")
        price = self.get_joined_text("//*[@id='corePrice_desktop']//*[@id='sns-base-price']/text()", "")
        style = self.get_joined_text("//*[@id='variation_style_name']/div/span/text()", "")
        details = self.get_details(remove_key=["UPC", "ASIN", "Batteries"])
        ratings = self.get_ave_ratings()
        comments = self.get_comments()
        # todo return result
        return

