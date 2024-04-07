# story-book-generator
Generate a story book narated and depicted by AI from written novels

## Roadmap

### Light novel scraper

- Chrome extension
- Python + headless browser
- Should easily be able to scrape different web sites, and click on the "next chapter" link automatically

Input: A web url of a light novel.

Output: A folder of one markdown file per chapter. The folder also contains a metadata file with the title & url of the main page and last scrapped page, to support incremental generation.

### Paragraph splitter

To make sure both the audio and the image are in sync, the chapters must be split into visually similar paragraphs and then those splits must be reused for both the audio and visual pipelines.

Input: A markdown chapter.

Output: A sequence markdown paragraph txt files.

### Light novel to audio
- https://huggingface.co/metavoiceio/metavoice-1B-v0.1
- https://huggingface.co/Pendrokar/xvapitch_nvidia
- https://huggingface.co/spaces/coqui/xtts
- https://huggingface.co/ShoukanLabs/Vokan
- Maybe something else?

Input: One markdown paragraph file.

Output: One mp3 file.

### Light novel to sequence of image

- Stable diffusion transformer model?
- LLM to fetch previous images from database for consistency?
- Basic natural language analysis and embbeding database?
- Split characters and background?

Input: A markdown file for a paragraph. A repository of previously generated images and associated annotations. An annotation is a text associated to a generated image, could be the original light novel text or a reasoning about the image. Annotations are optimized to be searched when generating the next image.

Output: One image representing the paragraph, along with the annotation of the image.

### Mobile consumption

- Consume the audio and video easily from a cellphone while traveling.
- Web server + mobile browser for real time generation?
- offline generation and save generated story on a mobile app? This is probably more realistic.

Input:
