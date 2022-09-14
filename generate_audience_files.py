import time
import random
import threading
from pathlib import Path
from datetime import date, timedelta

USERNAME_FILENAME = "usernames.txt"
NUM_AUDIENCE_IDS = 100
AUDIENCE_START_ID = 100
AUDIENCE_END_ID = 10000
PARENT_DIRECTORY = "../tapad_audience_data"
NUM_DATES = 10
NUM_FILES = 1000
NUM_THREADS = 1
NUM_FILES_PER_THREAD = int(NUM_FILES / NUM_THREADS)

usernames = []
audience_ids = []
dates = []
dates_str = []
len_usernames = 0



def load_usernames():
    global usernames, len_usernames
    username_filepath = Path(USERNAME_FILENAME)
    if username_filepath.exists():
        with open(USERNAME_FILENAME) as f:
            usernames = f.read().splitlines()
    len_usernames = len(usernames)


def generate_audience_ids():
    global audience_ids
    for i in range(NUM_AUDIENCE_IDS):
        audience_id = random.randint(AUDIENCE_START_ID, AUDIENCE_END_ID)
        audience_ids.append(str(audience_id))
        audience_ids.append(f"{audience_id}-")


def generate_dates():
    global dates, dates_str
    today_date = date.today()
    for i in range(NUM_DATES):
        current_date = today_date - timedelta(days=i)
        current_date_str = current_date.strftime('/%Y/%m/%d/')
        dates.append(current_date)
        dates_str.append(current_date_str)


class GenerateAudienceFiles(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = f"Thread-{self.thread_id}"


    def run(self):
        print(f"Thread: {self.thread_name} Start generating files")
        self.generate_files()
        print(f"Thread: {self.thread_name} Done generating files")


    def generate_files(self):
        for i in range(NUM_FILES_PER_THREAD):
            date_str = random.choice(dates_str)
            audience_id = random.choice(audience_ids)
            audience_dir_path = f"{PARENT_DIRECTORY}{date_str}{audience_id}"
            Path(audience_dir_path).mkdir(parents=True, exist_ok=True)
            random_usernames = random.sample(usernames, random.randint(100, len_usernames))
            audience_file_name = f"part-{random.randint(1000, 1999)}.txt"
            audience_file_full_name = f"{audience_dir_path}/{audience_file_name}"
            audience_file_path = Path(audience_file_full_name)
            if not audience_file_path.exists():
                with open(audience_file_full_name, 'w') as f:
                    for i in range(len(random_usernames) - 1):
                        f.write(f"{random_usernames[i]}\n")
                    f.write(random_usernames[len(random_usernames)-1])


def main():
    load_usernames()
    generate_audience_ids()
    generate_dates()

    generator_threads = []
    for i in range(1, NUM_THREADS+1):
        generator_thread = GenerateAudienceFiles(i)
        generator_thread.start()
        generator_threads.append(generator_thread)

    for generator_thread in generator_threads:
        generator_thread.join()


if __name__ == '__main__':
    main()
