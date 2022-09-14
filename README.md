# Tapad Audience
This repo is created to solve Task Assignment to get audience details

## File Structure
* config.py:- This is used to have config for the application
* constants.py:- This file contains all the constants value
* docker-compose.yml:- This file is used to start all the services: redis.
* generate_audience_files.py:- This file uses multithreading to generate audience files choosing random dates and audience ids.
* get_audience_details.py:- This file is responsible for getting audience details pertaining to audience id and number of days.
* logger.py:- This file defined logger for logging messages.
* redis_connection_pool.py:- This file is used to create Redis connection pool and to give Redis client from Redis connection pool.
* requirements.txt:- This file specifies all the packages to run above application. Run this as `pip3 install -r requirements.txt`
* tapad_audience_file_helper.py:- This file consists of helper functions to process audience files.
* tapad_audience_file_watcher.py:- This file creates a watcher service to monitor new files being created.
* tapad_audience_task.json:- This json file can be used to alter default values specified in constants.py file
* usernames.txt:- This file serves as an input to script generate_audience_files.py


# Run Application

 Need to install python 3.9.
 Install all the dependencies mentioned in requirements.txt. Create a virtualenv and then use pip3 to install dependencies

 ```
 virtualenv <path>
 source <path>/bin/activate
 pip3 instal -r requirements.txt
 ```

 # Run Application

 Start Redis first using,

 ```
 docker-compose up -d
 ```

 Activate above created virtualenv, Then run tapad_audience_file_watcher.py file. This will start the file watcher/monitor service on directory mentioned in tapad_audience_task.json

 ```
 source <path>/bin/activate
 python3 tapad_audience_file_watcher.py
 ```

 To stop all services:- redis, run

 ```
 docker-compose down
 ```

 To get audience details for days, run

 ```
 python3 get_audience_details.py --audience_id {audience_id} --num_days {num_days}
 ```