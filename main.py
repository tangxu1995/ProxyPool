from Util.Scheduler import Scheduler

__author__ = 'tangxu'


def main():
    try:
        scheduler = Scheduler()
        scheduler.run()
    except:
        main()


if __name__ == '__main__':
    main()
