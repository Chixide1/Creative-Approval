from PIL import Image
import numpy as np
import io
from fastapi import UploadFile

def convert_file_to_image(upload: UploadFile) -> Image.Image:
    data = upload.file.read()
    return Image.open(io.BytesIO(data)).convert("RGB")

def calculate_skin_tone_ratio(img: Image.Image) -> float:
    # Convert to HSV then Numpy format
    hsv = img.convert("HSV")
    arr = np.asarray(hsv).astype(np.uint16)
    H = arr[...,0] * 360 // 255
    S = arr[...,1] * 100 // 255
    V = arr[...,2] * 100 // 255

    # Catches pixels between these values as skin-like
    mask = (
        ((H<=50)|(H>=330)) &
        (S>=30) &
        (S<=200) &
        (V>=50)
    )
    
    return float(mask.mean())

def calculate_red_pixel_ratio(img: Image.Image) -> float:
    # Convert to HSV then Numpy format
    hsv = img.convert("HSV")
    arr = np.asarray(hsv).astype(np.uint16)

    H = arr[...,0] * 360 // 255
    S = arr[...,1] * 100 // 255
    V = arr[...,2] * 100 // 255
    
    # Catches pixels between these values as blood-like (strong red)
    mask = (
        ((H<=12)|(H>=348)) &
        (S>=70) &
        (V>=50)
    )
    
    return float(mask.mean())


def calculate_contrast_std(img: Image.Image) -> float:
    grayscale_img = img.convert("L")
    pixels = np.array(grayscale_img)
    std = np.std(pixels)

    return std.item()