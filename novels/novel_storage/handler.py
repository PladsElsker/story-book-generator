import os
import json
from pathlib import Path


ROOT_DIRECTORY = Path(__file__).parent.parent


def make_novel_directory(novel_key: str) -> None:
    novel_directory = ROOT_DIRECTORY / novel_key
    if not novel_directory.exists():
        os.mkdir(novel_directory)
    
    assets = novel_directory / "assets"
    if not assets.exists():
        os.mkdir(assets)

    chapters = novel_directory / "chapters.json"
    if not chapters.exists():
        with open(chapters, "w") as file:
            file.write("{}")


def merge_scraped(novel_key: str, scraped: dict) -> None:
    chapters_file = ROOT_DIRECTORY / novel_key / "chapters.json"
    with open(chapters_file, "r") as file:
        chapters = json.loads(file.read())
    
    if all((key in chapters) for key in ["title", "first_chapter_url", "last_scraped_url", "chapters"]):
        chapters["chapters"] = get_merged_chapters(chapters["chapters"], scraped["chapters"])
        chapters["title"] = scraped["title"]
        chapters["last_scraped_url"] = scraped["last_scraped_url"]
    else:
        chapters = scraped

    with open(chapters_file, "w") as file:
        file.write(json.dumps(chapters, indent=4))


def get_merged_chapters(initial, new):
    last_title = new[0]["title"]
    try:
        last_index = next(iter(i for i, chapter in reversed(list(enumerate(initial))) if chapter["title"] == last_title))
        return initial[:last_index] + new
    except StopIteration:
        msg = "Unable to merge because the new chapters don't overlap with the existing ones"
        raise KeyError(msg)


def get_last_scraped_url(novel_key: str) -> str:
    chapters = ROOT_DIRECTORY / novel_key / "chapters.json"
    if not chapters.exists():
        return

    with open(chapters, "r") as file:
        chapters_json = json.loads(file.read())
    
    if "last_scraped_url" not in chapters_json:
        return

    return chapters_json["last_scraped_url"]
