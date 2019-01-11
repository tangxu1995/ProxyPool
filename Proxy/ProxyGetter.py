from Db.RedisClient import RedisClient
from Proxy.ProxyCrawler import ProxyCrawler

POOL_UPPER_THRESHOLD = 2500

__author__ = 'tangxu'


class ProxyGetter(object):

    def __init__(self):
        self.redis = RedisClient()
        self.crawler = ProxyCrawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('开始抓取代理~')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxis(callback)
                for proxy in proxies:
                    if self.redis.add(proxy):
                        print('代理添加成功: %s' % proxy)

    def count1(self):
        return self.redis.count()

if __name__ == '__main__':

    getter = ProxyGetter()
    getter.run()

    print(getter.count1())