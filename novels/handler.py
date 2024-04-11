import os
import click
import json
from pathlib import Path


ROOT_DIRECTORY = Path.cwd() / "novels"


@click.group()
@click.argument("novel-key", type=str)
def storage(novel_key: str) -> None:
    storage.key = novel_key
    make_novel_directory()


def make_novel_directory() -> None:
    novel_directory = ROOT_DIRECTORY / storage.key
    if not os.path.exists(novel_directory):
        os.mkdir(novel_directory)
    
    assets = novel_directory / "assets"
    if not os.path.exists(assets):
        os.mkdir(assets)

    chapters = novel_directory / "chapters.json"
    if not os.path.exists(chapters):
        with open(chapters, "w") as file:
            file.write("{}")


@storage.command()
@click.argument("scraped_file", type=click.Path(exists=True))
def merge_scraped(scraped_file: str) -> None:
    with open(scraped_file, "rb") as file:
        scraped = json.loads(file.read().decode("utf-8"))
    
    chapters_file = ROOT_DIRECTORY / storage.key / "chapters.json"
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
        last_index = next(iter(i for i, chapter in enumerate(initial) if chapter["title"] == last_title))
        return initial[:last_index] + new
    except StopIteration:
        msg = "Unable to merge because the new chapters don't overlap with the existing ones"
        raise KeyError(msg)


@storage.command()
def get_last_scraped_url() -> None:
    chapters = ROOT_DIRECTORY / storage.key / "chapters.json"
    
    if not os.path.exists(chapters):
        return

    with open(chapters, "r") as file:
        chapters_json = json.loads(file.read())
    
    if "last_scraped_url" not in chapters_json:
        return

    print(chapters_json["last_scraped_url"])


if __name__ == "__main__":
    storage()
