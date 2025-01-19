import sys
if "." not in sys.path:
    sys.path[0:0] = ["."]

import requests
import json
from typing import Optional
from io import BytesIO
from tqdm import tqdm

from storage_handler import get_novel, save_scene_speech


def tts_inference(
    text,
    *,
    reference_audio_path: str,
    guidance: float = 3.0,
    top_p: float = 0.95,
    top_k: Optional[float] = None,
    url: str = 'http://localhost:58004/tts',
) -> BytesIO:
    with open(reference_audio_path, 'rb') as f:
        reference_audio = f.read()
    
    data = json.dumps({
        'text': text,
        'guidance': guidance,
        'top_p': top_p,
        'top_k': top_k,
    })
    headers = {
        'X-Payload': data,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=reference_audio)
    response.raise_for_status()
    return BytesIO(response.content)


def generate_speech_from_scenes(novel_key: str) -> None:
    novel = get_novel(novel_key)

    for i, chapter in enumerate(tqdm(novel["chapters"][:1], desc="Chapters")):
        for j, scene in enumerate(tqdm(chapter["scenes"], desc="Scenes")):
            generated_audio = tts_inference(
                scene,
                reference_audio_path='audio/speakers/YannicKilcher.wav',
            )
            save_scene_speech(novel_key, generated_audio, i, j)


def cli() -> None:
    # novel_key = "https___www.webnovel.com_book_mushoku-tensei-full-version_27096259406624705_volume-1-prologue_72736022055680334"
    novel_key = "https___www.webnovel.com_book_reincarnated-with-the-mind-control-powers-in-another-world._25331737205609705_chapter-1_67999384498920800"
    generate_speech_from_scenes(novel_key)


if __name__ == "__main__":
    cli()
