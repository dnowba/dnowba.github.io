import scrapy
from abc import ABCMeta, abstractmethod


class TosneetSpider(scrapy.Spider, metaclass=ABCMeta):
    name = "TBD"
    start_urls = [
        'TBD',
    ]

    # Override
    def __init__(self, pfull_html=None, ppage_limit=None, *args, **kwargs):
        super(TosneetSpider, self).__init__(*args, **kwargs)
        self.pfull_html = pfull_html
        self.ppage_limit = int(ppage_limit)
        self.page_count = 0

    # Override
    def parse(self, response):
        yield from self._scrape_page(response)

        next_page = response.css('.pagination').xpath(
            ".//a[text()='›']/@href").extract_first()
        if self.ppage_limit is not None and self.page_count >= self.ppage_limit:
            next_page = None

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def _scrape_page(self, res):
        headers = self._get_tableheader(res)
        for row in res.css('.results-table tbody tr'):
            yield self._parse_row_and_trace(row, headers, res)
        self.page_count += 1

    def _get_tableheader(self, res):
        thead = res.css('.results-table > thead > tr')[0]
        headers = [tr.xpath('text()').extract_first() for tr in thead.css('th')]
        # Hardcode null header name as 'img'
        headers = [h if h else 'img' for h in headers]
        return headers

    def _parse_row_and_trace(self, row, headers, res):
        data = self._parse_row(row, headers)
        if self.pfull_html:
            href = row.css('td a::attr(href)').extract_first()
            # Reference: How can i use multiple requests and pass items in between them in scrapy python
            # https://stackoverflow.com/questions/13910357/how-can-i-use-multiple-requests-and-pass-items-in-between-them-in-scrapy-python/25571270
            return res.follow(href, callback=self._parse_html,
                              meta={'data': data})
        return data

    # Could be overriden
    def _parse_row(self, row, headers):
        data = {}
        for i, head in enumerate(headers):
            data[head] = row.css('td:nth-child({})::text'.format(i + 1))
        data = {key: value.extract_first() for key, value in data.items()}
        # Set ClassID as speical attribute
        data['ClassID'] = row.css('td a::text').extract_first()
        return data

    def _parse_html(self, response):
        data = response.meta['data']
        data['html'] = response.body
        return data
