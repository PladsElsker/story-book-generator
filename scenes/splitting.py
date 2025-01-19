import sys
if "." not in sys.path:
    sys.path[0:0] = ["."]

from storage_handler import get_novel, set_novel


SENTENCE_SEPARATOR_REGEX = "\n"


def split_scenes(content: str) -> list[str]:
    return content.split(SENTENCE_SEPARATOR_REGEX)


def novel_split_scenes(novel_key: str) -> None:
    novel = get_novel(novel_key)
    for chapter in novel["chapters"]:
        chapter["scenes"] = [scene for scene in split_scenes(chapter["content"])]

    set_novel(novel_key, novel)


def cli() -> None:
    # novel_key = "https___www.webnovel.com_book_mushoku-tensei-full-version_27096259406624705_volume-1-prologue_72736022055680334"
    novel_key = "https___www.webnovel.com_book_reincarnated-with-the-mind-control-powers-in-another-world._25331737205609705_chapter-1_67999384498920800"
    novel_split_scenes(novel_key)


if __name__ == "__main__":
    cli()
