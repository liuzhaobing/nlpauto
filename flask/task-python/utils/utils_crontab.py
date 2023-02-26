import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
import logging

def run():
    logging.getLogger()
    print(datetime.datetime.now())


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(run, "cron", second="5")
    scheduler.start()
