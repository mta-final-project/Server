from datetime import time

from beanie import Document


class BaseDocument(Document):
    class Settings:
        bson_encoders = {time: str}
