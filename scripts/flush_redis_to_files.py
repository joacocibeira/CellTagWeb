import redis
import json
import os
from collections import defaultdict

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CLASS_DIR = os.getenv("CLASS_DIR", "data/images/classifications")

os.makedirs(CLASS_DIR, exist_ok=True)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def flush_all_user_tags_to_files():
    keys = r.keys("tagged_image:*:*")
    user_data = defaultdict(list)

    for key in keys:
        value = r.get(key)
        if value:
            try:
                entry = json.loads(value)
                user = entry["user"]
                user_data[user].append(entry)
            except Exception as e:
                print(f"Skipping invalid entry {key}: {e}")

    for user, entries in user_data.items():
        path = os.path.join(CLASS_DIR, f"{user}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        print(f"✅ Flushed {len(entries)} entries for user '{user}'")


if __name__ == "__main__":
    flush_all_user_tags_to_files()
