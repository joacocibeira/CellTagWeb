import redis
import json
import os

CLASS_LABELS = [
    "Interfase",
    "Profase",
    "Metafase",
    "Anafase",
    "Telofase",
    "Indeterminado",
    "No es célula",
]

# Redis config
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# Connect to Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Keys
TAG_PREFIX = "tagged_image"

# Classification storage directory (persisted to host)
CLASS_DIR = os.path.join(os.getenv("IMAGE_FOLDER", "/data/images"), "classifications")
os.makedirs(CLASS_DIR, exist_ok=True)


def store_classification(user: str, image_name: str, label: str):
    key = f"{TAG_PREFIX}:{user}:{image_name}"

    # Numeric label mapping
    try:
        label_numeric = CLASS_LABELS.index(label)
    except ValueError:
        label_numeric = None  # fallback if label is not in list

    payload = {
        "user": user,
        "image_name": image_name,
        "label": label,
        "label_numeric": label_numeric,
    }

    # Save to Redis
    r.set(key, json.dumps(payload))

    # Save to per-user file
    user_path = os.path.join(CLASS_DIR, f"{user}.json")

    if os.path.exists(user_path):
        with open(user_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    if not any(entry["image_name"] == image_name for entry in data):
        data.append(payload)
        with open(user_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def get_user_tagged_images(user: str) -> set:
    pattern = f"{TAG_PREFIX}:{user}:*"
    keys = r.keys(pattern)
    return {key.split(":")[-1] for key in keys}
