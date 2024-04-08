# story-book-generator
Generate a story book narated and depicted by AI from written novels

## Roadmap

### Light novel scraper

- Chrome extension
- Python + headless browser
- Should easily be able to scrape different web sites, and click on the "next chapter" link automatically

### Light novel to audio

- https://huggingface.co/spaces/coqui/xtts
- https://huggingface.co/suno/bark
- https://huggingface.co/suno/bark-small
- https://huggingface.co/metavoiceio/metavoice-1B-v0.1
- https://huggingface.co/microsoft/speecht5_tts
- https://huggingface.co/ShoukanLabs/Vokan
- https://huggingface.co/facebook/mms-tts-eng
- https://huggingface.co/myshell-ai/MeloTTS-English
- Maybe something else?

### Light novel to sequence of image

- Stable diffusion transformer model?
- LLM to fetch previous images from database for consistency?
- Basic natural language analysis and embbeding database?
- Split characters and background?

### Web server

- Consume the audio and video easily from a cellphone while traveling.
