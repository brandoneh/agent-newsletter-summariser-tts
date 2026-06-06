import asyncio
import sys
from datetime import datetime
import edge_tts
from pathlib import Path


# edge-tts uses ProactorEventLoop on Windows which closes prematurely during cleanup
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

VOICE = "en-US-JennyNeural"


async def _generate(text: str, output_path: str, voice: str) -> None:
    # Initialise the edge_tts.Communicate object with text and voice
    # then await the save to output_path
    communicate = edge_tts.Communicate(text, voice)

    await communicate.save(output_path)


def text_to_mp3(text: str, output_path: str, voice: str = VOICE) -> None:
    # Bridge from synchronous code into the async _generate coroutine
    asyncio.run(_generate(text, output_path, voice))


if __name__ == "__main__":
    test_script = "Good morning! Big news in AI this week: Meta just dropped Llama 3.1, \
a powerful new open-source model that's reportedly outperforming GPT-4o, \
with weights available for you to download and run locally."

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"tts_{timestamp}.mp3"
    filepath = f'tts_output/{filename}'

    Path("tts_output").mkdir(exist_ok=True)
    text_to_mp3(test_script, filepath, VOICE)
    print(f"Audio saved to: {filepath}")
