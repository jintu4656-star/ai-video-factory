import subprocess
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def assemble_video(script_data, output_file="final_short.mp4"):
    clips = []
    for scene in script_data["scenes"]:
        audio_clip = AudioFileClip(scene["audio_path"])
        duration = audio_clip.duration
        
        # Create clip matching audio length and apply a gentle zoom effect
        img_clip = (
            ImageClip(scene["image_path"])
            .set_duration(duration)
            .resize(lambda t: 1 + 0.04 * t)  # Smooth zoom-in over time
            .set_position(("center", "center"))
            .set_audio(audio_clip)
        )
        clips.append(img_clip)

    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(
        output_file,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )
    return output_file
