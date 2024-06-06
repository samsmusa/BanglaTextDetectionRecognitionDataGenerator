import csv
import logging
import re

import wikipedia

from btdr.utils import get_path, create_file_not_exist

logger = logging.getLogger(__name__)

wikipedia.set_lang("bn")
class Topic:
    def __init__(self, file_name, limit, topics=None):
        if topics is None:
            topics = set()
        self.file_name = file_name
        self.limit = limit
        self.topics = topics

    def get_file_topics(self, file_name=None):
        _file_name = get_path(file_name if file_name is not None else self.file_name)
        with open(_file_name, "r") as file:
            self.topics += set(file.readlines())
        return self.topics

    def write_topics(self, topics=None, file_name=None):
        _topics = topics if topics else self.topics
        _file_name = get_path(file_name if file_name is not None else self.file_name)
        create_file_not_exist(_file_name)
        with open(_file_name, "w") as file:
            write = csv.writer(file, delimiter=' ', quoting=csv.QUOTE_NONE, escapechar='\\')
            write.writerows([[ent.strip()] for ent in _topics])

    def get_topic(self, topics=None, limit=None):
        _topics = topics if topics else self.topics
        _limit = limit if limit else self.limit
        while len(_topics) < _limit:
            new_topics = wikipedia.random(pages=500)
            _topics.update(new_topics)
            logger.info("topics: %s", len(_topics))
        self.topics = _topics
        return _topics


class Wikigenrator:
    def __init__(self, file_name, limit, topics=None, regx=None):
        if topics is None:
            self.topics = set()
        else:
            self.topics = topics
        self.file_name = file_name
        self.limit = limit
        self.regx = regx if regx else r'^[\u0980-\u09FF\s\d!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]+$'

    def read_topics(self, file_name):
        with open(get_path(file_name), 'r') as file:
            self.topics = set(file.readlines())
        return self.topics
    def get_content(self, topic):
        try:
            return wikipedia.page(topic).content
        except Exception as e:
            logger.error("not found for %s", topic)
            return None

    def is_bengali(self, text):
        bengali_or_special_pattern = re.compile(
            self.regx)
        return bool(bengali_or_special_pattern.match(text))

    def write_write(self, topics=None, file_name=None, mode="w", split_delimiter=" "):
        _topics = topics if topics else self.topics
        _file_name = get_path(file_name if file_name else self.file_name)
        with (open(_file_name, mode) as file):
            writer = csv.writer(file, delimiter=' ', quoting=csv.QUOTE_NONE, escapechar=' ')
            for _topic in _topics:
                logger.info("writing topic %s", _topic)
                cnt = self.get_content(_topic)
                if cnt is None:
                    continue
                cnt = cnt.strip().replace("\n", " ")
                words = cnt.split(split_delimiter)
                rows = [[word.strip()] for word in words if self.is_bengali(word.strip())]
                writer.writerows(rows)


if __name__ == "__main__":
    t = Topic("topics.txt", 2000)
    topics = t.get_topic()

    w = Wikigenrator("n_word.txt", 2000, topics)
    w.write_write()
    # t.write_topics()
