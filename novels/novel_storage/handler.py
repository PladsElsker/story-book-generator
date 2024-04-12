import os
import json
from pathlib import Path


Novel = dict[str, any]
Chapters = list[dict[str, any]]

ROOT_DIRECTORY = Path(__file__).parent.parent


def make_novel_directory(novel_key: str) -> None:
    novel_directory = ROOT_DIRECTORY / novel_key
    if not novel_directory.exists():
        os.mkdir(novel_directory)
    
    assets = novel_directory / "assets"
    if not assets.exists():
        os.mkdir(assets)

    novel = novel_directory / "novel.json"
    if not novel.exists():
        set_novel(dict())


def merge_scraped(novel_key: str, scraped: dict) -> None:
    novel = get_novel(novel_key)
    
    if all((key in novel) for key in ["title", "first_chapter_url", "last_scraped_url", "chapters"]):
        novel["chapters"] = get_merged_chapters(novel["chapters"], scraped["chapters"])
        novel["title"] = scraped["title"]
        novel["last_scraped_url"] = scraped["last_scraped_url"]
    else:
        novel = scraped

    set_novel(novel)


def get_merged_chapters(initial: Chapters, new: Chapters) -> Chapters:
    last_title = new[0]["title"]
    try:
        last_index = next(iter(i for i, chapter in reversed(list(enumerate(initial))) if chapter["title"] == last_title))
        return initial[:last_index] + new
    except StopIteration:
        msg = "Unable to merge because the new chapters don't overlap with the existing ones"
        raise KeyError(msg)


def get_last_scraped_url(novel_key: str) -> str:
    novel = get_novel(novel_key)
    if "last_scraped_url" not in novel:
        return None

    return novel["last_scraped_url"]


def get_novel(novel_key: str) -> Novel:
    novel_file = ROOT_DIRECTORY / novel_key / "novel.json"
    if not novel_file.exists():
        return None
    
    with open(novel_file, "r") as file:
        return json.loads(file.read())


def set_novel(novel_key: str, novel: Novel) -> None:
    novel_file = ROOT_DIRECTORY / novel_key / "novel.json"
    with open(novel_file, "w") as file:
        file.write(json.dumps(novel, indent=4))


def set_chapters(novel_key: str, chapters: Chapters) -> None:
    novel = get_novel(novel_key)
    novel["chapters"] = chapters
    set_novel(novel_key, novel)
