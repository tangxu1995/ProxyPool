from flask import Flask, g, jsonify
from Db.RedisClient import RedisClient
from werkzeug.wrappers import Response


app = Flask(__name__)

__author__ = 'tangxu'

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResponse, cls).force_type(response, environ)

app.response_class = JsonResponse

api_list = {
    'get': u'Get a random proxy',
    'count': u'Get the numbers of proxies'
}

@app.route('/')
def index():
    return api_list

@app.route('/random')
def get_proxy():
    """
    获取随机可用代理
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    """
    获取代理池总量
    :return:
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()