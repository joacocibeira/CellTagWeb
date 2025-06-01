import os
import random
from app.redis_client import get_user_tagged_images

IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "/images")  # Must match Docker volume


def _list_all_images():
    valid_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}
    return [
        os.path.join(IMAGE_FOLDER, fname)
        for fname in os.listdir(IMAGE_FOLDER)
        if os.path.splitext(fname)[-1].lower() in valid_extensions
    ]


def get_random_untagged_image(user: str) -> str | None:
    all_images = _list_all_images()
    tagged = get_user_tagged_images(user)
    untagged = [img for img in all_images if os.path.basename(img) not in tagged]

    if not untagged:
        return None
    return random.choice(untagged)
