import scrapy


class FragrancenetSpider(scrapy.Spider):
    name = "Fragrancenet"

    def start_requests(self):
        urls = [
            'https://www.fragrancenet.com/cologne/calvin-klein/escape/edt#122757',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'fragrancenet-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')