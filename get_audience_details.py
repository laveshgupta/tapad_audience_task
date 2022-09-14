import argparse
import redis
from datetime import date, timedelta

parser = argparse.ArgumentParser()
parser.add_argument('--audience_id', '-a', type=int, required=True, help="Enter the audience id")
parser.add_argument('--num_days', '-n', type=int, required=True, help="Enter number of days you want data for")
args = parser.parse_args()

def __get_redis_client():
    redis_client = redis.Redis(host='127.0.0.1', port=6379, db=2, password="ORQXAYLE", decode_responses=True,)
    return redis_client

def get_audience_details():
    redis_client = __get_redis_client()
    total_additions = total_removals = 0
    redis_keys = []
    dates_asked = []
    for i in range(args.num_days):
        process_date = date.today() - timedelta(days=i)
        process_date_str = process_date.strftime('%Y-%m-%d')
        redis_keys.append(f"{process_date_str}:{args.audience_id}")
        dates_asked.append(process_date_str)

    print(
        "Date    AudienceID    Additions    Removals    Total Additions    Total Removals"
    )

    for i in range(len(dates_asked)):
        value = redis_client.hgetall(redis_keys[i])
        date_str = dates_asked[i]
        removals = int(value.get('removals', 0))
        additions = int(value.get('additions', 0))
        total_additions += additions
        total_removals += removals
        print(
            f"{date_str}    {args.audience_id}    {additions}    {removals}    {total_additions}    {total_removals}"
        )

    print(
        f"Total additions and removals for {args.audience_id} over {args.num_days} days: "
        f"Total Additions: {total_additions}    Total Removals: {total_removals}"
    )


def main():
    get_audience_details()

if __name__ == '__main__':
    main()