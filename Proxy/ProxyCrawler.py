# ProxyPool/Proxy/ProxyCrawler.py
import re
from lxml import etree
from Util.WebRequest import web_request

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
            html = web_request(url)
            tree = etree.HTML(html)
            proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
            for proxy in proxy_list:
                try:
                    yield ':'.join(proxy.xpath('./td/text()')[0:2])
                except Exception as e:
                    print(e)

    def Proxy_Data5u(self):
        url = 'http://www.data5u.com/free/gngn/index.shtml'
        html = web_request(url)
        tree = etree.HTML(html)
        items = tree.xpath("//ul[@class='l2']")
        for ul in items:
            try:
                yield ':'.join(ul.xpath(".//li/text()")[0:2])
            except Exception as e:
                print(e)

    def Proxy_Xila(self):
        for page in range(1, 4):
            url = 'http://www.xiladaili.com/gaoni/{}'.format(page)
            html = web_request(url)
            items = re.findall('(\d+.\d+.\d+.\d+:\d+)', html)
            for item in items:
                try:
                    yield item
                except Exception as e:
                    print(e)

    def Proxy_31daili(self):
        url_list = ['https://31f.cn/http-proxy/', 'https://31f.cn/https-proxy/']
        for url in url_list:
            html = web_request(url)
            tree = etree.HTML(html)
            items = tree.xpath("//table//tr")[1:51]
            for item in items:
                try:
                    ip = item.xpath(".//td[2]/text()")[0]
                    port = item.xpath(".//td[3]/text()")[0]
                    yield ip + ":" + port
                except Exception as e:
                    print(e)

    def Proxy_Goubj(self):
        for page in range(1, 3):
            url = 'http://ip.jiangxianli.com/?page={}'.format(page)
            html = web_request(url)
            tree = etree.HTML(html)
            tr_list = tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            for tr in tr_list:
                yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]

    def Proxy_Iphai(self):
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        for url in urls:
            html = web_request(url)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 html)
            for proxy in proxies:
                yield ":".join(proxy)


if __name__ == '__main__':
    spider = ProxyCrawler()
    items = spider.Proxy_Data5u()
    for item in items:
        print(item)
