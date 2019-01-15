# ProxyPool/Proxy/ProxyCrawler.py
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
        print('这是来自西刺的代理~')
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
        print('这是来自data5u的代理~')
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
