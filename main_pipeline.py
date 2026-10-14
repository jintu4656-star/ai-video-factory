import os, importlib, requests

script_agent = importlib.import_module("agents.1_script_agent")
audio_agent = importlib.import_module("agents.2_audio_agent")
visual_agent = importlib.import_module("agents.3_visual_agent")
editor_agent = importlib.import_module("agents.4_editor_agent")

def send_to_telegram(video_path, caption):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print(f"Video saved at {video_path} (Telegram credentials not set)")
        return
    url = f"https://api.telegram.org/bot{token}/sendVideo"
    with open(video_path, "rb") as video:
        requests.post(url, data={"chat_id": chat_id, "caption": caption}, files={"video": video})

if __name__ == "__main__":
    topic = "What happens if a teaspoon of a Neutron Star hit Earth?"
    print("Step 1: Writing viral script...")
    script = script_agent.generate_script(topic)
    
    print("Step 2: Generating voiceover & word timestamps...")
    script = audio_agent.generate_audio_and_subs(script)
    
    print("Step 3: Generating 9:16 vertical visuals...")
    script = visual_agent.generate_visuals(script)
    
    print("Step 4: Rendering final MP4...")
    final_mp4 = editor_agent.assemble_video(script, output_file="final_short.mp4")
    
    print("Step 5: Delivering video...")
    send_to_telegram(final_mp4, caption=script["title"])
