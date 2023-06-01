from typing import Union
import uvicorn
from fastapi import FastAPI
import tempfile
from pathlib import Path
import logging
import yaml
import os
from glob import glob
import random
from io import BytesIO
from fastapi.responses import StreamingResponse
from typing import Optional
from typing_extensions import Annotated
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
import animated_drawings.render

MOTION_DIR = './config/motion' 
RETARGET_CFG = './config/retarget/fair1_ppf.yaml' 
MASK_FILE = "mask.png"
TEXTURE_FILE = "texture.png"
CHARACTER_CONFIG = "char_cfg.yaml"
logger = logging.getLogger(__name__) 
app = FastAPI()


def select_random_motion_cfg(fixed_id: Optional[int]=None):
    file_paths = []
    for root, dirs, files in os.walk(MOTION_DIR):
        for file in files:
            file_paths.append(os.path.join(root, file))

    if fixed_id:
        assert fixed_id < len(file_paths) and fixed_id > 0
        return file_paths[fixed_id]
    else:
        return random.choice(file_paths)

def choose_retarget_cfg(motion_cfg):
    file_name = os.path.basename(motion_cfg) 
    if file_name == "jesse_dance.yaml": 
        return './config/retarget/mixamo_fff.yaml'
    elif file_name == "jumping_jacks.yaml":
        return './config/retarget/cmu1_pfp.yaml'
    else: 
        return './config/retarget/fair1_ppf.yaml'


@app.get("/ping")
def read_ping():
    return {"Response": "Healthy"}

@app.post("/render")
async def render(mask: UploadFile=File(...),
                 texture: UploadFile=File(...),
                 char_cfg: UploadFile=File(...),
                 motion_id: int=Form(...)):
    try: 
        temp_dir = tempfile.TemporaryDirectory()
        print(f"Created tmp dir: {temp_dir.name}")
        chr_cfg_path = os.path.join(temp_dir.name, CHARACTER_CONFIG) 
        with open(os.path.join(temp_dir.name, MASK_FILE ), 'wb') as f:
            f.write(await mask.read())
        with open(os.path.join(temp_dir.name, TEXTURE_FILE ), 'wb') as f:
            f.write(await texture.read())
        with open(chr_cfg_path, 'wb') as f: 
            f.write(await char_cfg.read())
        print(motion_id)
        random_motion_cfg = select_random_motion_cfg(motion_id)
        animated_drawing_dict = {
        'character_cfg': chr_cfg_path,
        'motion_cfg': random_motion_cfg,
        'retarget_cfg': choose_retarget_cfg(random_motion_cfg)}
        print(animated_drawing_dict )

        # create mvc config
        output_gif = str(Path(temp_dir.name, 'video.gif').resolve())
        mvc_cfg = {
            'scene': {'ANIMATED_CHARACTERS': [animated_drawing_dict]},  
            'controller': {
                'MODE': 'video_render', 
                'OUTPUT_VIDEO_PATH': output_gif}  
        }

        # write the new mvc config file out
        output_mvc_cfn_fn = str(Path(temp_dir.name, 'mvc_cfg.yaml'))
        with open(output_mvc_cfn_fn, 'w') as f:
            yaml.dump(dict(mvc_cfg), f)

        # render the video
        animated_drawings.render.start(output_mvc_cfn_fn)
        with open(output_gif, 'rb') as f:
            img_raw = f.read()
        byte_io = BytesIO(img_raw)
        return StreamingResponse(byte_io, media_type='image/gif')

    finally: 
        print(f"Deleting tmp dir: {temp_dir.name}")
        temp_dir.cleanup()

    return  HTTPException(status_code=418, detail="Processing failed!")