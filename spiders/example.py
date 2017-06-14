# -*- coding: utf-8 -*-
from items import OpenwhiskrawlerItem
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import XMLFeedSpider
from twisted.internet import reactor
from scrapy.utils.log import configure_logging


class MySpider(XMLFeedSpider):
    name = 'tedcdn.com'
    allowed_domains = ['pa.tedcdn.com']
    start_urls = ['https://pa.tedcdn.com/feeds/talks.rss']
    iterator = 'xml'  # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))

        item = OpenwhiskrawlerItem()
        item['title'] = node.xpath('title').extract()
        print "title %s" % item['title']
        return item


if __name__ == '__main__':
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(MySpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
