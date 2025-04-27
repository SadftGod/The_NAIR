import os
from PIL import Image

class ImageOperator:
    @staticmethod
    def save_avatar(image: Image.Image, user_id: int) -> str:
        directory = "app/static/user_avatars/"
        os.makedirs(directory, exist_ok=True)

        path = os.path.join(directory, f"{user_id}_avatar.png")
        image.save(path, format='PNG', optimize=True)
        return path