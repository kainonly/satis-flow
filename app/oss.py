from oss2 import Auth, Bucket, ObjectIterator
from .config import Config


class Oss:
    def __init__(self, config: Config):
        self._auth = Auth(
            config.access_key_id,
            config.access_key_secret
        )
        self.bucket = Bucket(
            self._auth,
            config.endpoint,
            config.bucket_name
        )

    def find(self, prefix: str) -> ObjectIterator:
        return ObjectIterator(self.bucket, prefix)

    def add(self, object_name: str, local_file: str):
        return self.bucket.put_object_from_file(object_name, local_file)

    def delete(self, lists):
        return self.bucket.batch_delete_objects(lists)
