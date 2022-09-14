import redis


class TapadAudienceFileHelper:

    @staticmethod
    def process_audience_file(audience_file_path):
        audience_file_name_index = audience_file_path.rfind('/')
        audience_file_name = audience_file_path[audience_file_name_index+1:]
        audience_id_index = audience_file_path.rfind('/', 0, audience_file_name_index)
        audience_id = audience_file_path[audience_id_index+1:audience_file_name_index]
        day_index = audience_file_path.rfind('/', 0, audience_id_index)
        day_str = audience_file_path[day_index+1:audience_id_index]
        month_index = audience_file_path.rfind('/', 0, day_index)
        month_str = audience_file_path[month_index+1:day_index]
        year_index = audience_file_path.rfind('/', 0, month_index)
        year_str = audience_file_path[year_index+1:month_index]

        num_audience_members = TapadAudienceFileHelper.get_num_audience_members(audience_file_path)

        removal_flag = False
        aud_id = audience_id
        if '-' in audience_id:
            removal_flag = True
            dash_index = audience_id.find('-')
            if dash_index == 0:
                aud_id = audience_id[1:]
            else:
                aud_id = audience_id[:-1]

        redis_key = f"{year_str}-{month_str}-{day_str}:{aud_id}"

        redis_client = redis_pool.get_redis_client()
        with redis_client.pipeline() as process_audience_file_pipeline:
            retry_count = 0
            while True:
                try:
                    process_audience_file_pipeline.watch(redis_key)
                    redis_key_exists = process_audience_file_pipeline.exists(redis_key)
                    if redis_key_exists:
                        process_audience_file_pipeline.multi()
                        if removal_flag:
                            process_audience_file_pipeline.hincrby(redis_key, 'removals', -1*num_audience_members)
                        else:
                            process_audience_file_pipeline.hincrby(redis_key, 'additions', num_audience_members)
                        process_audience_file_pipeline.execute()
                    else:
                        redis_key_value = {
                            'additions': num_audience_members if not removal_flag else 0,
                            'removals': (-1*num_audience_members) if removal_flag else 0,
                        }
                        process_audience_file_pipeline.multi()
                        process_audience_file_pipeline.hmset(redis_key, redis_key_value)
                        process_audience_file_pipeline.execute()
                    break
                except redis.WatchError:
                    retry_count += 1
                    logger.warning(f"Watcherror on processing audience file {audience_file_name}. Tried {retry_count} times")


    @staticmethod
    def get_num_audience_members(audience_file_path):
        num_audience_members = 0
        with open(audience_file_path) as f:
            audience_members = f.read().splitlines()
        num_audience_members = len(audience_members)
        return num_audience_members