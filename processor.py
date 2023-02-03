import csv
import re
from collections import defaultdict


class Processor:
    def __init__(self):
        self.result = defaultdict(list)
        with open('stop_words.txt', 'r') as f:
            self.stop_words = [line.rstrip('\n') for line in f if line]

    def reset(self):
        self.__init__()

    def get_result(self) -> dict:
        return dict(self.result)

    def __reader(self, file_name: str) -> str:
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            headers = next(reader)  # CSV file must have headers
            uri_index = headers.index("uri")  # required field
            query_index = headers.index("query_string")  # required field

            for csv_row in reader:
                uri = csv_row[uri_index]

                if any(stop_word in uri for stop_word in self.stop_words):
                    continue

                query = csv_row[query_index]

                if query:
                    uri += f"?{query}"

                yield uri

    @staticmethod
    def __get_uri_mask(uri: str) -> str:
        uri_parts = [x for x in uri.split("?")[0].split("/") if x]

        for i in range(1, len(uri_parts)):
            if re.search(r'\d+', uri_parts[i]):
                uri_parts[i] = "{id}"

        return "/" + "/".join(uri_parts)

    def process(self, file_name: str):
        for url in self.__reader(file_name):
            mask = self.__get_uri_mask(url)
            self.result[mask].append(url)
