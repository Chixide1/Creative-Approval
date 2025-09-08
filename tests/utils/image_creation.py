from PIL import Image
import io
import numpy as np


def get_png_image(img: Image.Image):
    """Convert a PIL Image to PNG bytes."""

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.getvalue()

def create_test_image(width: int = 100, height: int = 100, color: tuple[int, int, int] = (0,0,0)) -> bytes:
    """Create a simple test image as BytesIO object."""

    img = Image.new('RGB', (width, height), color)
    return get_png_image(img)

def create_high_contrast_image() -> bytes:
    """Create a high contrast checkerboard image with standard deviation of 127.5"""

    width, height, block = 100, 100, 10

    # Use broadcasting to build checkerboard pattern
    pattern = (np.add.outer(np.arange(height) // block, np.arange(width) // block) % 2) * 255
    img = Image.fromarray(pattern.astype(np.uint8)).convert("RGB")

    return get_png_image(img)

def create_text_image() -> bytes:
    """Create a simple text file as BytesIO object."""

    text_bytes = io.BytesIO()
    text_bytes.write(b"This is a test text file.")
    text_bytes.seek(0)
    return text_bytes.getvalue()