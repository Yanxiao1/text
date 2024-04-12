import os
import cv2
from PIL import Image
import numpy as np
from natsort import natsorted

from diffusers.utils import load_image
from models.pipline import StableDiffusionControlNetPipeline
from diffusers import ControlNetModel
from diffusers import UniPCMultistepScheduler, EulerAncestralDiscreteScheduler
import torch
from models import attention_control, attention_utils
from controlnet_util.util import save_grid

def process_image(
        input_image_path: str,
        pretrained_model_path: str,
        control_net_path: str,
        output_dir: str,
        canny: dict,
        inference: dict,
        device: str,
        seed: int,
        ddim_inv: dict,
        extra: dict,
        mixed_precision: str = "fp16",
        use_uni_scheduler: bool = True,
        use_cpu_offload: bool = True,
        use_xformer: bool = True,
):
    os.environ['CUDA_VISIBLE_DEVICES'] = device

    # For mixed precision training we cast the text_encoder and vae weights to half-precision
    # as these models are only used for inference, keeping weights in full precision is not required.
    weight_dtype = torch.float32
    if mixed_precision == "fp16":
        weight_dtype = torch.float16
    elif mixed_precision == "bf16":
        weight_dtype = torch.bfloat16

    # load pretrained model
    controlnet = ControlNetModel.from_pretrained(control_net_path, torch_dtype=weight_dtype)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        pretrained_model_path, controlnet=controlnet, torch_dtype=weight_dtype
    )
    if seed is not None:
        generator = [torch.Generator(device=pipe.controlnet.device).manual_seed(seed) for _ in range(inference["num_image_per_prompt"])]
    else:
        generator = None

    img_list = natsorted(list(set([file.split('.')[0] for file in os.listdir(input_image_path)])))
    prompt_list = open(inference["prompts_path"], 'r').readlines()
    prompt_list = [text.strip() for text in prompt_list]

    for img_name in img_list:
        image = load_image(os.path.join(input_image_path, img_name + '.png'))
        image = image.resize((inference["width"], inference["height"]))  # image.shape h*w*c

        bbx_image, mask_img = attention_utils.get_draw_img_and_mask(os.path.join(input_image_path, img_name + '.txt'), image)

        image = np.array(image)
        bbx_image = np.array(bbx_image)

        # process with canny
        image = cv2.Canny(image, canny['low_threshold'], canny['high_threshold'])
        image = image[:, :, None]
        image = np.concatenate([image, image, image], axis=2)
        canny_image = Image.fromarray(image)
        bbx_image = cv2.Canny(bbx_image, canny['low_threshold'], canny['high_threshold'])
        bbx_image = bbx_image[:, :, None]
        bbx_image = np.concatenate([bbx_image, bbx_image, bbx_image], axis=2)
        canny_bbx_image = Image.fromarray(bbx_image)

        prompts = []
        prompts_choice = np.random.choice(prompt_list, 1, replace=False)
        for idx, prompt in enumerate(prompts_choice):
            prompts.append(prompt + inference["additional_prompt"])
        negative_prompt = [inference["negative_prompt"]] * len(prompts)

        if use_uni_scheduler:
            pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
        if use_cpu_offload:
            pipe.enable_model_cpu_offload()
        if use_xformer:
            pipe.enable_xformers_memory_efficient_attention()
        sign_words_list = attention_utils.find_words_in_string(extra["word_list"], prompts[0])
        equalizer, inds = attention_utils.get_equalizer_from_mask(pipe.tokenizer, prompts[0], (sign_words_list), mask_img, device=device, dtype=pipe.unet.dtype)
        controller = attention_control.AttentionReweight(prompts, pipe.tokenizer, inference["num_step"], cross_replace_steps=0.3,
                                                          self_replace_steps=0.5,
                                                          equalizer=equalizer[0][0], select_inds=inds,
                                                          self_equalizer=None, bbx=None)
        controlnet_controller = attention_control.AttentionReweight(prompts, pipe.tokenizer, inference["num_step"], cross_replace_steps=0.3,
                                                                     self_replace_steps=0.5,
                                                                     equalizer=equalizer[0][0], select_inds=inds,
                                                                     self_equalizer=None, bbx=None)

        output, _ = pipe(
            controller,
            prompts,
            canny_image,
            negative_prompt=negative_prompt,
            num_inference_steps=inference["num_step"],
            generator=generator,
            latents=None,
            num_images_per_prompt=inference["num_image_per_prompt"],
            controlnet_conditioning_scale=inference["controlnet_conditioning_scale"],
            guidance_scale=inference["classifer_free_guidance_scale"],
            image_guidance_scale=inference["image_guidance_scale"],
            init_image=None,
            strength=ddim_inv["SDEdit_strength"],
            control_controller=controlnet_controller,
            canny_bbx_image=canny_bbx_image,
            bbx_guidance_scale=inference["bbx_guidance_scale"],
        )

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for p in prompts:
            if len(p) > 150:
                p = p[:150]
        save_grid(output.images, len(prompts_choice), len(output.images) // len(prompts_choice), prompts, output_dir, img_name)

if __name__=="__main__":
    input_image_path = "C:/shuiyin/steg(1)/text_result/"
    pretrained_model_path = "C:/shuiyin/steg(1)/checkpoints/stable-diffusion-v1-5"
    control_net_path = "C:/shuiyin/steg(1)/checkpoints/sd-controlnet-canny"
    output_dir = "C:/shuiyin/steg(1)/output_images/"
    canny = {'low_threshold': 50, 'high_threshold': 150}
    inference = {'prompts_path': "C:/shuiyin/steg(1)/prompts.txt", 'width': 200, 'height': 200, 'additional_prompt': "additional prompt", 
             'negative_prompt': "negative prompt", 'num_step': 100, "num_image_per_prompt": 1, 'controlnet_conditioning_scale': 1.0,
             'classifer_free_guidance_scale': 1.0, 'image_guidance_scale': 1.0, 'bbx_guidance_scale': 1.0,}
    device = "cuda:0"
    seed =42
    ddim_inv = {'SDEdit_strength': 1.0}
    extra = {'word_list': [''], 'bbx_num': 0}#加载图片

# 调用函数
    process_image(
        input_image_path,
        pretrained_model_path,
        control_net_path,
        output_dir,
        canny,
        inference,
        device,
        seed,
        ddim_inv,
        extra,
    )



