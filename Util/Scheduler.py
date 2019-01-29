# ProxyPool/Util/Scheduler.py
import time
from multiprocessing import Process
from Api.ProxyApi import app
from Proxy.ProxyGetter import ProxyGetter
from Proxy.CheckProxy import CheckProxy

TESTER_ENABLE = True
GETTER_ENABLE = True
API_ENABLE = True

__author__ = 'tangxu'


class Scheduler(object):
    def schedule_tester(self):
        """
        定时检测代理
        """
        tester = CheckProxy()
        while True:
            print('测试器开始运行~')
            tester.run()
            time.sleep(20)

    def schedule_getter(self):
        """
        定时获取代理
        """
        getter = ProxyGetter()
        while True:
            getter.run()
            time.sleep(20)

    def schedule_api(self):
        """
        开启 API
        :return:
        """
        app.run('0.0.0.0', '5000')

    def run(self):

        print('代理池开始运行')
        if TESTER_ENABLE:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLE:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLE:
            api_process = Process(target=self.schedule_api)
            api_process.start()
