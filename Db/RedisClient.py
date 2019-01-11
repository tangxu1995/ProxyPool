# ProxyPool/Db/RedisClient.py
import redis
import random

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD  = None
REDIS_KEY = 'proxies'
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

__author__ = 'tangxu'


class RedisClient():

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        数据库连接初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis 密码
        """
        # 连接 Redis 数据库
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理到数据库
        :param proxy:
        :return:
        """
        # zscore 获取值对应的分数
        # zadd 新增
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def decrease(self, proxy):
        """
        代理分数-1, 若分数小于最小值，则删除该代理
        :param proxy:
        :return:
        """
        # zincrby 自增
        # zrem 将指定值删除
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '已不可用', score, '删除')
            return self.db.zrem(REDIS_KEY, proxy)

    def max(self, proxy):
        """
        将代理设置为 MAX_SCORE
        :param proxy:
        :return:
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def all(self):
        """
        获取全部代理
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def random(self):
        """
        随机获取有效代理
        :return:
        """
        # zrevrangebyscore 按照分数从大到小排序
        # zrangebyscore 按照分数从小到大排序

        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            # return result
            return random.choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 100, 0)
            if len(result):
                return random.choice(result)
            else:
                print('代理池为空')


    def batch(self, start, stop):
        """
        批量获取
        :return:
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)

if __name__ == '__main__':
    redis = RedisClient()
    result = redis.random()
    print(result)