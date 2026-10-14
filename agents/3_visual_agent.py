import os, gc, torch
from diffusers import StableDiffusionXLPipeline, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

def generate_visuals(script_data, out_dir="temp"):
    os.makedirs(out_dir, exist_ok=True)
    base = "stabilityai/stable-diffusion-xl-base-1.0"
    repo = "ByteDance/SDXL-Lightning"
    ckpt = "sdxl_lightning_4step_unet.safetensors"

    # Load fast 4-step pipeline in 16-bit to fit easily inside a free 15GB T4 GPU
    pipe = StableDiffusionXLPipeline.from_pretrained(
        base, torch_dtype=torch.float16, variant="fp16"
    ).to("cuda")
    pipe.scheduler = EulerDiscreteScheduler.from_config(
        pipe.scheduler.config, timestep_spacing="trailing"
    )
    pipe.unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device="cuda"))

    for scene in script_data["scenes"]:
        sid = scene["scene_id"]
        prompt = f"{scene['visual_prompt']}, ultra detailed, cinematic lighting, vertical 9:16"
        image = pipe(
            prompt,
            height=1024,
            width=576,
            num_inference_steps=4,
            guidance_scale=0
        ).images[0]
        
        img_path = f"{out_dir}/scene_{sid}.png"
        image.save(img_path)
        scene["image_path"] = img_path

    # Clear GPU VRAM completely
    del pipe
    gc.collect()
    torch.cuda.empty_cache()
    return script_data
