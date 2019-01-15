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
        if not self.is_over_threshold():
            print('获取器开始执行')
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    if self.redis.add(proxy):
                        print('代理 %s 添加成功' % proxy)

    def count1(self):
        return self.redis.count()

if __name__ == '__main__':

    getter = ProxyGetter()
    getter.run()

    print(getter.count1())