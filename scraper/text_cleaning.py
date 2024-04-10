def clean_chapter(chapter: dict) -> dict:
    if "title" in chapter:
        chapter["title"] = clean_title(chapter["title"])
    
    if "content" in chapter:
        chapter["content"] = clean_paragraph(chapter["content"])
    
    return chapter


def clean_title(title: str) -> str:
    return title.replace("\n", "").strip()


def clean_paragraph(paragraph: str) -> str:
    lines = paragraph.strip().split("\n")
    nested_striped = "\n".join(line.strip() for line in lines)
    while "\n\n" in nested_striped:
        nested_striped = nested_striped.replace("\n\n", "\n")
    
    return nested_striped
