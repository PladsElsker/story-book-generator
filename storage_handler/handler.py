import os
from pathlib import Path
from io import BytesIO

from scraper.novel import Chapter, Novel


ROOT_DIRECTORY = Path(__file__).parent.parent / "novels"


def ensure_novel_directory_created(novel_key: str, title: str, first_chapter_url: str) -> None:
    novel_directory = ROOT_DIRECTORY / novel_key
    if not novel_directory.exists():
        os.mkdir(novel_directory)
    
    assets = novel_directory / "assets"
    if not assets.exists():
        os.mkdir(assets)

    novel_file = novel_directory / "novel.json"
    if not novel_file.exists():
        novel = Novel(title, first_chapter_url, first_chapter_url, [])
        set_novel(novel_key, novel)

def get_novel(novel_key: str) -> Novel:
    novel_file = ROOT_DIRECTORY / novel_key / "novel.json"
    with open(novel_file) as file:
        return Novel.deserialize(file)


def set_novel(novel_key: str, novel: Novel) -> None:
    novel_file = ROOT_DIRECTORY / novel_key / "novel.json"
    with open(novel_file, "w") as file:
        return novel.serialize(file)


def merge_scraped(novel_key: str, scraped: Novel) -> None:
    novel_file = ROOT_DIRECTORY / novel_key / "novel.json"
    with open(novel_file, "r") as file:
        novel = Novel.deserialize(file)
    
    if all((key in novel) for key in ["title", "first_chapter_url", "last_scraped_url", "chapters"]):
        novel["chapters"] = _get_merged_chapters(novel["chapters"], scraped["chapters"])
        novel["title"] = scraped["title"]
        novel["last_scraped_url"] = scraped["last_scraped_url"]
    else:
        novel = scraped

    set_novel(novel_key, novel)


def _get_merged_chapters(initial: list[Chapter], new: list[Chapter]) -> list[Chapter]:
    if len(initial) == 0:
        return new

    last_title = new[0]["title"]
    try:
        last_index = next(iter(i for i, chapter in reversed(list(enumerate(initial))) if chapter["title"] == last_title))
        return initial[:last_index] + new
    except StopIteration:
        msg = "Unable to merge because the new chapters don't overlap with the existing ones"
        raise KeyError(msg)


def save_scene_speech(novel_key: str, generated_audio: BytesIO, chapter_index, scene_index) -> None:
    assets_chapter_path = ROOT_DIRECTORY / novel_key / "assets" / f"chapter-{chapter_index}"
    if not assets_chapter_path.exists():
        os.mkdir(assets_chapter_path)
    
    output_file = assets_chapter_path / f"scene-{scene_index}.wav"
    with open(output_file, "wb") as f:
        f.write(generated_audio.read())
