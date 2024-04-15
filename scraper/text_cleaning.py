from scraper.novel import Chapter


def clean_chapter(chapter: Chapter) -> Chapter:
    chapter["title"] = clean_title(chapter["title"])
    chapter["content"] = clean_content(chapter["content"])
    
    return chapter


def clean_title(title: str) -> str:
    return title.replace("\n", "").strip()


def clean_content(content: str) -> str:
    lines = content.strip().split("\n")
    nested_striped = "\n".join(line.strip() for line in lines if len(line.strip()) > 0)
    return nested_striped


def url_to_novel_key(url: str) -> str:
    return url.replace("/", "_").replace(":", "_")
