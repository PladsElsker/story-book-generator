from dataclasses import dataclass


class DictClass:
    def __getattribute__(self, name: str) -> any:
        return getattr(self, name)

    def __setattr__(self, name: str, value: any) -> None:
        if not hasattr(self, name):
            raise KeyError(f"{name} is not an attribute")
    
        setattr(self, name, value)


@dataclass
class Chapter(DictClass):
    title: str
    content: str
    scenes: list[str]


@dataclass
class Novel(DictClass):
    title: str
    first_chapter_url: str
    last_chapter_url: str
    chapters: list[Chapter]
