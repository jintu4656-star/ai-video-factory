import gc, json, torch
import soundfile as sf
from kokoro import KPipeline
from faster_whisper import WhisperModel

def generate_audio_and_subs(script_data, out_dir="temp"):
    os.makedirs(out_dir, exist_ok=True)
    # 1. Generate Voiceover with Kokoro-82M
    tts = KPipeline(lang_code='a') # American English
    
    for scene in script_data["scenes"]:
        sid = scene["scene_id"]
        audio_chunks = [audio for _, _, audio in tts(scene["narration"], voice='af_heart', speed=1.05)]
        full_audio = torch.cat(audio_chunks, dim=0).numpy()
        wav_path = f"{out_dir}/scene_{sid}.wav"
        sf.write(wav_path, full_audio, 24000)
        scene["audio_path"] = wav_path

    # 2. Extract Word-Level Timestamps for Captions
    whisper = WhisperModel("base", device="cuda", compute_type="float16")
    for scene in script_data["scenes"]:
        segments, _ = whisper.transcribe(scene["audio_path"], word_timestamps=True)
        words = [{"word": w.word.strip(), "start": w.start, "end": w.end} 
                 for seg in segments for w in seg.words]
        scene["words"] = words

    # 3. CRITICAL: Free GPU VRAM before loading heavy visual models
    del tts, whisper
    gc.collect()
    torch.cuda.empty_cache()
    return script_data
