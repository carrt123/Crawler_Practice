# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time

from scrapy import signals
from selenium.webdriver.chrome.options import Options
import scrapy

# useful for handling different item types with a single interface
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class LightsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class LightsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        with open('user_agents.txt', 'r') as f:
            self.user_agents = f.read().splitlines()
        self.options = Options()
        # self.options.add_argument('--headless')
        self.options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver = webdriver.Chrome(options=self.options)
        with open('stealth.min.js') as f:
            js = f.read()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
              "source": js
        })
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(1)
        request.headers.setdefault('User-Agent', random.choice(self.user_agents))
        return scrapy.http.HtmlResponse(url=request.url, body=self.driver.page_source.encode('utf-8'), encoding='utf-8',
                                        request=request,
                                        status=200)
