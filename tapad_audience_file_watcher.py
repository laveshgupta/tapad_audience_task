import time
from logger import Logger
from redis_connection_pool import RedisConnectionPool
from config import Config
from constants import Constants
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler
import threading
from tapad_audience_file_helper import TapadAudienceFileHelper as tafh

class AudienceFileWatcher:
    def __init__(self, directory=".", handler=FileSystemEventHandler()) -> None:
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(
            self.handler, self.directory, recursive = True
        )
        self.observer.start()
        logger.info(f"Watcher started monitoring directory: {self.directory}")
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        logger.info(f"Watcher stopped monitoring directory: {self.directory}")


class AudienceFileEventHandler(PatternMatchingEventHandler):
    def __init__(self):
            super().__init__(patterns=['*.txt'], ignore_directories=True)

    def on_created(self, event):
        audience_file_path = event.src_path
        tafh.process_audience_file(audience_file_path)


def main():
    audience_watch_dir = config.get('audience_data_dir', Constants.AUDIENCE_DATA_DIR)
    file_watcher = AudienceFileWatcher(audience_watch_dir, AudienceFileEventHandler())
    file_watcher.run()


if __name__ == '__main__':
    config = Config()
    __builtins__.config = config
    logger = Logger()
    __builtins__.logger = logger
    redis_pool = RedisConnectionPool()
    __builtins__.redis_pool = redis_pool
    main()