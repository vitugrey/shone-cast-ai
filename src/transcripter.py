# ============ Importação ============= #
import os
import json
import tempfile
import subprocess

from pathlib import Path
from dotenv import load_dotenv, find_dotenv

import assemblyai as aai

# ============ Constantes ============= #
_ = load_dotenv(find_dotenv(".env"))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

aai.settings.api_key = ASSEMBLYAI_API_KEY


# ============== Código =============== #
def extract_audio(video_path, audio_path):
    cmd = ["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le",
           "-ar", "16000", "-ac", "1", audio_path, '-y']

    subprocess.run(cmd, check=True, capture_output=True)


def transcribe_audio(audio_path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    return transcript.text


def process_video():
    video_dir = Path("videos")
    transcriptions = {}

    for creator_dir in video_dir.iterdir():
        if creator_dir.is_dir():
            creator_name = creator_dir.name
            transcriptions[creator_name] = []

            for video_file in creator_dir.glob("*.mp4"):
                print(f"Processing {video_file.name}...")
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                    audio_path = temp_audio_file.name

                try:
                    extract_audio(video_file, audio_path)
                    transcription = transcribe_audio(audio_path)
                    transcriptions[creator_name].append({
                        "video": video_file.name,
                        "transcription": transcription
                    })
                except Exception as e:
                    print(f"Error processing {video_file.name}: {e}")
                finally:
                    os.unlink(audio_path)
    with open("transcriptions.json", "w", encoding="utf-8") as f:
        json.dump(transcriptions, f, indent=2, ensure_ascii=False)


# ============= Execução ============== #
if __name__ == "__main__":
    pass
