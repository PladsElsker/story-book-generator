import click
from novel_storage import get_novel, set_chapters


SENTENCE_SEPARATOR_REGEX = "\n"


def split_scenes(content: str) -> list[str]:
    return content.split(SENTENCE_SEPARATOR_REGEX)


@click.command()
@click.option("--novel-key", "-k", required=True, type=str)
def cli(novel_key: str) -> None:
    novel = get_novel(novel_key)
    for chapter in novel["chapters"]:
        chapter["scenes"] = [scene for scene in split_scenes(chapter["content"])]
    
    set_chapters(novel_key, novel["chapters"])


if __name__ == "__main__":
    cli()
