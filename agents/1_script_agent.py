import os, json
from google import genai
from google.genai import types

def generate_script(niche_topic: str, output_path="script.json"):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    prompt = f"""
    Create a viral 45-second vertical video script about: {niche_topic}.
    Rules for monetization & virality:
    1. First sentence MUST be a high-curiosity 3-second hook.
    2. Last sentence MUST grammatically loop right back into the first sentence.
    3. Break into 6 scenes. Provide a highly detailed cinematic 9:16 image/video prompt for each scene.
    Return ONLY valid JSON:
    {{
      "title": " Catchy SEO Title",
      "scenes": [
        {{"scene_id": 1, "narration": "...", "visual_prompt": "cinematic 9:16 vertical, ..."}}
      ]
    }}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    with open(output_path, "w") as f:
        f.write(response.text)
    return json.loads(response.text)
