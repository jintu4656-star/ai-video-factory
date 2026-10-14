import os, requests
from agents.script_agent import generate_script
from agents.audio_agent import generate_audio_and_subs
from agents.visual_agent import generate_visuals
from agents.editor_agent import assemble_video

def send_to_telegram(video_path, caption):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendVideo"
    with open(video_path, "rb") as video:
        requests.post(url, data={"chat_id": chat_id, "caption": caption}, files={"video": video})

if __name__ == "__main__":
    topic = "What happens if a teaspoon of a Neutron Star hit Earth?"
    script = generate_script(topic)
    script = generate_audio_and_subs(script)
    script = generate_visuals(script)
    final_mp4 = assemble_video(script, output_file="final_short.mp4")
    send_to_telegram(final_mp4, caption=script["title"])
