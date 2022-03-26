import logging;
import os;

LOG_DIR = '../logging/';
LOG_NAME = 'loaf-bot.log';
LOG_LEVEL = logging.INFO

def initializeLogger():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(filename=LOG_DIR + LOG_NAME, encoding='utf-8', level=LOG_LEVEL, format='[%(levelname)s][%(asctime)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p');

initializeLogger()
