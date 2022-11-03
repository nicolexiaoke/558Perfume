from typing import Dict, List, Tuple
from time import sleep
import requests as rqs
from lxml import etree


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

if __name__ == "__main__":
    import sys, os
    path = __file__
    for _ in range(2):
        path = os.path.split(path)[0]
    sys.path.append(path)
    from modules.proj_os import Get_Root_dir
    header = {
        "authority": "www.amazon.com",
        "scheme":"https",
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.90",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,en-CN;q=0.7",
        "cookie": 'session-id=137-3328056-1763758; ubid-main=132-7960620-4393815; aws-ubid-main=744-3338385-3071068; session-id-eu=258-8382607-9461569; ubid-acbuk=260-8504814-0792203; x-main="MT30@1?PvLY0mSohFkFYBXnBXVcn9KLJ?p9K2KsKaDmRtRU61BuQnmm@jdeEAsSv"; at-main=Atza|IwEBIG4HmLRFnwFKYVcouxkJ-dvwOK6pKb9glsfFfXPyEffibKPpvhFdzlbdoCxeJBhQjCfqeoM8A_ZjvtFLNolhBS4XhuvSyDL2FDVucyKXdoKMtpKiJ6tSz2ZZG6iM55IQsVy4T8saTizg-AcmOPWSk_9SeZuZIE8l0-gupScTQEZHRRC_wG4Y_Y6EJbMLCZxBAydZ_1fs8CSGw0E5IHTFrnw-; sess-at-main="i33quMZwZ7wXMSkTPqgzpwZOL2h2/nb71aKj9MwsGqA="; sst-main=Sst1|PQGY5cbqIJUKRZkRR82Q1sKQCTnjzglU2LJqYztkzAM6Tw4H-pNkc6JUM-ruRRM9uAbz6aES8xAk8mvXT1Aig-wpXxykpntYDae6fB-Cv_6DUtfmdDee89vFTLSAthqEA_qJxnnXQFCuXw0AXTY8lcjPaRy2NaSxAodDsaCwPwOm2iKjaM3c6jOep7EXi41a4mwtZgWMUeIpVfnVsgvhdOySmeQJZXoglrmBlDIpnXF3zmI7-Kk76FlKH7s9-BBTja1T7w7X4bwHlvB4oOADYWiCbhLd6H5LMxGJW08p2gQKNPI; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6IjNhYWFiODU3LTRlZjItNGRjNi1iOTEwLTI4Y2IwYmZiNDM3ZSJ9.eyJzdWIiOiIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoiN0xTNVloUGxIbWZ5OGV1QTA5U2hWcnpVN1wvWFJZVG1PcXhsNGhXQzE3MkU9IiwiYXJuIjoiYXJuOmF3czppYW06Ojk1OTcyNjAzMjI5OTpyb290IiwidXNlcm5hbWUiOiJjenEwMSJ9.D90z7xEnFo7TbU6r58EODRgMSoIj-IU0NxPW54xh8upmioSWwZunJx5qwfqlsB8Ppy7rWScYdhIN69pmzL1W5lHdbJW5_274fZSyCm5kbMi4vf4cCcMgX3W3GdJ4Hmmj; aws-userInfo={"arn":"arn:aws:iam::959726032299:root","alias":"","username":"czq01","keybase":"7LS5YhPlHmfy8euA09ShVrzU7/XRYTmOqxl4hWC172E\u003d","issuer":"http://signin.aws.amazon.com/signin","signinType":"PUBLIC"}; _RCRTX03-samesite=f567ca77ffeb11ec9ae6cb6f21e2e6d68ee2d79592214149ac1f0dac6da708ea; i18n-prefs=USD; lc-main=en_US; skin=noskin; csd-key=eyJ3YXNtVGVzdGVkIjp0cnVlLCJ3YXNtQ29tcGF0aWJsZSI6dHJ1ZSwid2ViQ3J5cHRvVGVzdGVkIjpmYWxzZSwidiI6MSwia2lkIjoiODIxMzRjIiwia2V5IjoiaWtzT3pmaHdYZGRCd0lJWDB0bXlJMkpvY1VRcXhPV0RwUmZrSEtsRG83NU5pcWNGcGpqNWUvRTl4ekxOZWdRUzN6dXU5NUkvUi9pSVlGTlJWNDVWR3pmN0lZdkFPdDMwZTBVSDhRYkp6Yk5Qb0Z1RFF5TFAwSnkvdzdabUhEaTBGa3N3cmFDYUhHL3ZkbWh1ZzNONEExSWRXa3QxWXFJTXdkVDJzYnVscVBoR1EraVBOYVdwWkhpZ0xidjl2V3hVaXVhV0FqMWFKRzdhMk9BeTBNdzd3YWt1WERWZkNDMlNXQmVGZzFlcGlSNGh6a3Nka3ovdVJ3RUQ0NzRFVWN5U2ZxVmhVNlpLeFBQTE04NWRUdy9mN096SWlOWGszUEtGVkNYbGlLK2VHVmJGU2hHUFV6NFdreDVCb0lCSlNITWx2U0ZzbkpxS2dJTjN0SkdDSnlFZDRRPT0ifQ==; _rails-root_session=ZUhRdHl1Vi9sUmJjU0xoUTg1VndKdS9xaHM3NlVoTjNVbHdnRU9LUU5wL1FObVRVd0V3Q0x3V1p6YU9NRjN4cDQzd2dPQ3VCRFZUdTVoelJvSHF0WFZuTXdIU2lvUmtJT2gydTVlUVBGeVBqN3E4QzBHS3pOYUNkUzNaNGMwYStEMURHaHhId2p1dXhwbTc3ZUZTQzhBYzZyelo5WFdaVGZweHJtK2k1Y0h4TUJBT1BISklxWUhFeGVhY0VqZjRoLS0rNHFmamNjSUk5aTNveDh6bVE1MmZnPT0=--1722e538c0108096427bdde65389fce1d9311e33; s_fid=138AFD1A879D8EB6-04CBB4AA6978C4A4; s_cc=true; csm-hit=tb:9YZE5Z96FMH7BHK5M81N+s-9YZE5Z96FMH7BHK5M81N|1665027781318&t:1665027781318&adb:adblk_yes; session-id-time=2082787201l; session-token=tRdG2mAHAs14hOY1f03rTaQqcYJI4ZQ592QeVdIWUpqXtPamw+H0EnA9XNc7lsjeMfuNpFtTXBJ28kQ7K+nxOdNqL+37UznaSDazcgvlVmos4KLRExcgUKXsl3XeOo/zt3dl7pyTZfDrrSscApi5lMNEmDKzx8YVWAJ/HfDcd+jNtBs4Px1pm3tgt60XLBkatAxjgDzoEUzClPEj3FogufAfvDVTFG8kF4W/3pn6off3xelnw92h7PNcXrkQCRq8AqRtxyLmI4Oet2GWOoAVTw==',
        "device-memory": "8",
        "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        "sec-ch-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    }

    tool = Amazon_Detail_Patch(header)
    search_pattern = "https://www.amazon.com/s?k=perfume&page={0}&qid=1665350946&sprefix=perfu%2Caps%2C128&ref=sr_pg_{0}"
    hrefs = tool.get_page_urls(search_pattern, 5)

    with open(Get_Root_dir() + "/data/amazon.jsonl", 'w', encoding='utf-8') as f:
        count =1
        total = len(hrefs)
        for item_url in hrefs:
            print(f"---> Processing item: {count}/{total}...")
            result = tool.get_result(item_url,max_len=10)
            f.write(f"{result}\n")
            count += 1
