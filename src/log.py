# encoding=utf-8
import jieba
import string
import os
import re
import time
import sys
import shutil
#import pandas as pd
#import numpy as np

from json import *
reload(sys)
sys.setdefaultencoding('utf-8')

import ConfigParser

#config = ConfigParser.ConfigParser()
#config.readfp(open('/var/www/html/python/ML/conf/conf.ini'))
#LOG_DIR = config.get("LOG","LOG_DIR")
DIR_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
LOG_DIR = os.path.join(DIR_ROOT,'log','run.log')

def write(log_message):
    global LOG_DIR
    isExists = os.path.exists(LOG_DIR)
    if not isExists:
        f = file(LOG_DIR, 'w')
        f.write("")
        f.close()
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    f = file(LOG_DIR, 'a')
    f.write(date+ '\t'+ log_message + '\n')
    f.close()
