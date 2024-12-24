from typing import List

from CodeFile import CodeFile


class DataFilter:

    def __init__(self, languages: List[str], path_prefix: str, keyword: str):
        self.languages = languages
        self.path_prefix = path_prefix
        self.keyword = keyword

    def matches_file_extensions(self, path: str) -> bool:
        for ext in self.languages:
            if path.endswith(f".{ext.lower()}"):
                return True
        return False

    def matches_directory(self, path: str) -> bool:
        return path.startswith(self.path_prefix)

    def matches_meta(self, item: str) -> bool:
        return item["type"] == "blob" and self.keyword.lower() in item["path"].lower()

    def parse_data(self, payload):
        data_result = []
        tree = payload["tree"]
        for i in tree:
            if self.matches_meta(i) \
                    and self.matches_file_extensions(i["path"]) \
                    and self.matches_directory(i["path"]):
                data_result.append(i["path"])

        json_result = {
            "files": data_result
        }
        return json_result

    def get_file_counts_and_lengths(self, payload):
        data_result = []
        tree = payload["tree"]
        for i in tree:
            if self.matches_meta(i) \
                    and self.matches_file_extensions(i["path"]) \
                    and "grails" not in i["path"] \
                    and self.matches_directory(i["path"]):
                data_result.append(CodeFile(path=i["path"], size=i["size"]))

        json_result = {
            "files": data_result
        }
        return json_result
