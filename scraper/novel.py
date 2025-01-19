from __future__ import annotations
from typing import TextIO
import json


class DictClass:
    def __getitem__(self, name: str) -> any:
        if not hasattr(self, name):
            raise AttributeError(f"{name} is not an attribute of the class {type(self).__name__}")
        
        return getattr(self, name)

    def __setitem__(self, name: str, value: any) -> None:
        if not hasattr(self, name):
            raise AttributeError(f"{name} is not an attribute of the class {type(self).__name__}")
    
        setattr(self, name, value)
    
    def __iter__(self):
        return iter(self.__dict__)


class Chapter(DictClass):
    def __init__(self, chapter_rep: dict[str, any]) -> None:
        self.title = chapter_rep["title"]
        self.content = chapter_rep["content"]
        self.scenes = chapter_rep["scenes"]


class Novel(DictClass):
    def __init__(self, title: str, first_chapter_url: str, last_scraped_url: str, chapters: dict[str, any]) -> None:
        self.title = title
        self.first_chapter_url = first_chapter_url
        self.last_scraped_url = last_scraped_url
        self.chapters = chapters

    def serialize(self, file: TextIO) -> None:
        novel_rep = self.__dict__
        novel_rep["chapters"] = [chapter.__dict__ for chapter in self["chapters"]]
        json.dump(novel_rep, file, indent=4)

    @classmethod
    def deserialize(cls, file: TextIO) -> Novel:
        novel_rep = json.load(file)
        novel_rep["chapters"] = [Chapter(chapter_rep) for chapter_rep in novel_rep["chapters"]]
        novel = Novel(None, None, None, None)
        novel.__dict__ = novel_rep
        return novel
