import os
from datetime import datetime
from dotenv import load_dotenv
from summarise import summarise, OLLAMA_URL, GEMINI_URL
from email_tool import fetch_unread_newsletters
from tts import text_to_mp3, VOICE

load_dotenv()

def main():
    
    api_token = os.getenv("GEMINI_API_KEY")
    url = GEMINI_URL if api_token else OLLAMA_URL
    model = os.getenv("MODEL")

    newsletters = fetch_unread_newsletters(2)
    if isinstance(newsletters, str):
        print (f"Email fetch failed: {newsletters}")
        return
    
    newsletters_len = len(newsletters)
    
    tts_folder = 'tts_output'
    os.makedirs(tts_folder, exist_ok=True)


    for i, newsletter in enumerate(newsletters):
        print(f"Summarising: {newsletter[:100]}")
        reply_dict = summarise(newsletter, url, model, api_token)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"tts_{timestamp}.mp3"
        filepath = os.path.join(tts_folder, filename)
        text_to_mp3(reply_dict["tts_script"], filepath, VOICE)
        print(f"Processed email {i+1}/{newsletters_len}")
    

if __name__ == "__main__":
    main()
