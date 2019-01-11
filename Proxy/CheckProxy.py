import time
import asyncio
import aiohttp
from aiohttp import ClientError, ClientConnectorError
from Db.RedisClient import RedisClient

VALID_STATUS_CODES = [200]
TEST_URL = 'https://www.baidu.com/'
BATCH_TEST_SIZE = 10

__author__ = 'tangxu'


class CheckProxy(object):

    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy: 单个代理
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('状态码不合法', proxy)
            except (ClientError, ClientConnectorError, TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    def run(self):
        """
        测试主函数
        :return:
        """
        print('开始测试~')
        try:
            count = self.redis.count()
            print('当前剩余', count, '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第', start +1, '-', stop, '个代理')
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
            # proxies = self.redis.all()
            # loop = asyncio.get_event_loop()
            # for i in range(0, len(proxies), BATCH_TEST_SIZE):
            #     test_proxies = proxies[i:i + BATCH_TEST_SIZE]
            #     tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
            #     loop.run_until_complete(asyncio.wait(tasks))
            #     time.sleep(5)
        except Exception as e:
            print('测试发生错误', e.args)


if __name__ == '__main__':
    test = CheckProxy()
    test.run()