import os
import json


class SingleFileCache:
    def __init__(self, location):
        self.location = location
        if not os.path.exists(location):
            with open(location, 'w') as file:
                json.dump({}, file)

    def add_to_cache(self, key, value):
        with open(self.location, 'r+') as file:
            cache = json.load(file)
            cache[key] = value
            file.seek(0)
            json.dump(cache, file)
            file.truncate()

    def retrieve_value(self, key):
        with open(self.location, 'r') as file:
            cache = json.load(file)
            result = cache.get(key)
            if result is not None:
                print(f"cache hit. key:{key}")
            return result

    def delete_cache(self):
        if os.path.exists(self.location):
            os.remove(self.location)