import os
import json
import shutil


CACHE_LOCATION = "cache"


class MultiFileCache:
    def __init__(self, location):
        self.location = location
        if not os.path.exists(location):
            os.makedirs(location)

    def _generate_filename(self, key):
        return self.location + "/" + key + ".json"

    # Overwrites previous values
    def add_to_cache(self, key, value):
        with open(self._generate_filename(key), 'w') as file:
            json.dump(value, file)

    def retrieve_value(self, key):
        if os.path.exists(self._generate_filename(key)):
            print(f"cache hit. key:{key}")
            with open(self._generate_filename(key), 'r') as file:
                return json.load(file)
        else:
            return None

    def delete_cache(self):
        if os.path.exists(self.location):
            shutil.rmtree(self.location)
