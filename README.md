# story-book-generator
Generate a story book narated and depicted by AI from written novels

## Roadmap

### Light novel scraper

- Chrome extension
- Python + headless browser
- Should easily be able to scrape different web sites, and click on the "next chapter" link automatically

`Input` A web url of a light novel.  
`Output` A uniquely named folder containing a chapters.json file of this format:  
```json
{
  "title": "Mushoko tenser",
  "first_chapter_url": "https://www.webnovel.com/fsdjfjsf/chapter-1",
  "last_scraped_url": "https://www.webnovel.com/fsdjfjsf/chapter-118",
  "chapters": [
    {
      "title": "title",
      "content": "content\ncontent"
    }
  ]
}
```

### Paragraph splitter

To make sure both the audio and the image are in sync, the chapters must be split into visually similar paragraphs and then those splits must be reused for both the audio and visual pipelines.  

`Input` A scraped light novel JSON file.  
`Output` A sequence of scenes containing a consistent context over a few lines (visual context).  
```json
{
  "title": "Mushoko tenser",
  "first_chapter_url": "https://www.webnovel.com/fsdjfjsf/chapter-1",
  "last_scraped_url": "https://www.webnovel.com/fsdjfjsf/chapter-118",
  "chapters": [
    {
      "title": "title",
      "content": "- Content!\n- No, you content!",
      "scenes": [
        "- Content!",
        "- No, you content!"
      ]
    }
  ],
}
```

### Light novel to audio
- https://huggingface.co/metavoiceio/metavoice-1B-v0.1
- https://huggingface.co/Pendrokar/xvapitch_nvidia
- https://huggingface.co/spaces/coqui/xtts
- https://github.com/yl4579/StyleTTS2
- https://huggingface.co/ShoukanLabs/Vokan
- [rvc](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)?
- Maybe something else?
- Selecting the right voice actor for the right dialog

`Input` A scene in text.  
`Output` `scene-<i>.wav` located in the folder `assets/chapter-<j>/`.  

### Light novel to sequence of images

- Stable diffusion transformer model?
- LLM to fetch previous images from database for consistency?
- Basic natural language analysis and embbeding database?
- Split characters and background?
- A repository of previously generated images and associated annotations. An annotation is a text associated to a generated image, could be the original light novel text or a reasoning about the image. Annotations are optimized to be searched when generating the next image.

`Input` A scene in text.  
`Output` `scene-<i>.png` located in the folder `assets/chapter-<j>/`.  

### Mobile consumption

- Consume the audio and video easily from a cellphone while traveling.  
- Offline generation and save generated story on a mobile app.  

`Input` A processed novel folder.  
`Output` Mobile app playback.  
