import logging

class Constants:
    APP_CONFIG_FILE_PATH = 'tapad_audience_task.json'
    DEFAULT_REDIS_MAX_CONN = 20
    DEFAULT_REDIS_HOST = 'localhost'
    DEFAULT_REDIS_PORT = 6379
    DEFAULT_REDIS_DATABASE = 2
    DEFAULT_REDIS_PASSWORD = 'ORQXAYLE'
    LOG_LEVEL = 'DEBUG'
    LOGGING_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    LOG_FILE = 'tapad_audience_task.log'
    AUDIENCE_DATA_DIR = "../tapad_audience_data"
