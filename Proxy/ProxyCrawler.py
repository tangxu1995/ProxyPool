# ProxyPool/Proxy/ProxyCrawler.py
import re
import requests
from lxml import etree

__author__ = 'tangxu'


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'Proxy_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class ProxyCrawler(object, metaclass=ProxyMetaclass):

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def Proxy_Xici(self):
        for page in range(1, 3):
            url = 'https://www.xicidaili.com/nn/{}'.format(page)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                tree = etree.HTML(response.text)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        print(e)

    def Proxy_Data5u(self):
        url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tree = etree.HTML(response.text)
            items = tree.xpath("//ul[@class='l2']")
            for ul in items:
                try:
                    yield ':'.join(ul.xpath(".//li/text()")[0:2])
                except Exception as e:
                    print(e)

    def Proxy_Xila(self):
        for page in range(1, 4):
            url = 'http://www.xiladaili.com/gaoni/{}'.format(page)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                items = re.findall('(\d+.\d+.\d+.\d+:\d+)', response.text)
                for item in items:
                    try:
                        yield item
                    except Exception as e:
                        print(e)

    def Proxy_31daili(self):
        url_list = ['https://31f.cn/http-proxy/', 'https://31f.cn/https-proxy/']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        for url in url_list:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                tree = etree.HTML(response.text)
                items = tree.xpath("//table//tr")[1:51]
                for item in items:
                    try:
                        ip = item.xpath(".//td[2]/text()")[0]
                        port = item.xpath(".//td[3]/text()")[0]
                        yield ip + ":" + port
                    except Exception as e:
                        print(e)
