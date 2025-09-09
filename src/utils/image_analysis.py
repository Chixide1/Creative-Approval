from PIL import Image
import numpy as np
import io
from fastapi import UploadFile

def convert_file_to_image(upload: UploadFile) -> Image.Image:
    """Convert an UploadFile to a PIL Image."""

    data = upload.file.read()
    return Image.open(io.BytesIO(data)).convert("RGB")

def calculate_skin_tone_ratio(img: Image.Image) -> float:
    """Calculate the ratio of skin-tone-like pixels in the image."""

    # Convert to HSV then Numpy format
    hsv = img.convert("HSV")
    arr = np.asarray(hsv).astype(np.uint16)
    H = arr[...,0] * 360 // 255
    S = arr[...,1] * 100 // 255
    V = arr[...,2] * 100 // 255

    mask = (
        # Primary skin hue range (yellow-orange-red)
        (((H >= 0) & (H <= 50)) | ((H >= 340) & (H <= 360))) &
        # Saturation: not too gray, not too vivid
        (S >= 15) & (S <= 80) &
        # Value: avoid very dark shadows and overexposed areas
        (V >= 35) & (V <= 95)
    ) | (
        # Secondary range for some skin tones (more yellow/beige)
        ((H >= 15) & (H <= 35)) &
        (S >= 10) & (S <= 60) &
        (V >= 40) & (V <= 90)
    )
    
    return float(mask.mean())

def calculate_blood_pixel_ratio(img: Image.Image) -> float:
    """Calculate the ratio of blood-like red pixels in the image."""

    # Convert to HSV then Numpy format
    hsv = img.convert("HSV")
    arr = np.asarray(hsv).astype(np.uint16)

    H = arr[...,0] * 360 // 255
    S = arr[...,1] * 100 // 255
    V = arr[...,2] * 100 // 255
    
    mask = (
        # Pure red range (wrapping around 0/360)
        (((H >= 0) & (H <= 15)) | ((H >= 345) & (H <= 360))) &
        # High saturation for vivid red color
        (S >= 60) & (S <= 100) &
        # Medium to dark values (blood isn't bright red)
        (V >= 20) & (V <= 80)
    ) | (
        # Dark red/maroon range for dried blood
        (((H >= 350) & (H <= 360)) | ((H >= 0) & (H <= 10))) &
        (S >= 40) & (S <= 90) &
        (V >= 15) & (V <= 50)
    )
    
    return float(mask.mean())

def calculate_contrast_std(img: Image.Image) -> float:
    """Calculate the standard deviation of pixels in the image."""

    grayscale_img = img.convert("L")
    pixels = np.array(grayscale_img)
    std = np.std(pixels)

    return std.item()

def format_file_size(size: int) -> str:
    """Convert file size in bytes to human-readable string format"""
    sizes = ["B", "KB", "MB", "GB"]
    order = 0
    length = float(size)
    
    while length >= 1024 and order < len(sizes) - 1:
        order += 1
        length /= 1024
    
    return f"{length:.2g} {sizes[order]}"