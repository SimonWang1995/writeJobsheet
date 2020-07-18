import time,datetime,os
import logging

log_dir = os.getcwd()
logger =logging.getLogger()
logger.setLevel(logging.DEBUG)
Date = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
DATEFMT = '%Y-%m-%d %H:%M:%S'
log = '{0}/{1}-log'.format(log_dir, Date)
handler = logging.FileHandler(log)
FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
# FORMAT = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
handler.setFormatter(logging.Formatter(FORMAT,DATEFMT))
handler.setLevel(logging.DEBUG)
consoleLog = logging.StreamHandler()
consoleLog.setLevel(logging.DEBUG)
consoleLog.setFormatter(logging.Formatter(FORMAT, DATEFMT))
logger.addHandler(handler)
logger.addHandler(consoleLog)