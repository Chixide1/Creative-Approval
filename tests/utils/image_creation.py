from PIL import Image
import io
import numpy as np


def create_test_image(width: int = 100, height: int = 100, color: tuple[int] = (128, 128, 128)) -> io.BytesIO:
    """Create a simple test image as BytesIO object."""
    img = Image.new('RGB', (width, height), color)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def create_high_contrast_image() -> io.BytesIO:
    """Create a high contrast image with standard deviation of approximately 80."""
    
    width, height = 100, 100
    
    # Create a checkerboard-like pattern with varying intensities
    img_array = np.zeros((height, width), dtype=np.uint8)
    
    # Fill with a pattern that should give us std dev around 80
    for i in range(height):
        for j in range(width):
            # Create a pattern with high contrast
            if (i // 10 + j // 10) % 2 == 0:
                img_array[i, j] = 255  # White
            else:
                img_array[i, j] = 0    # Black
    
    # Add some intermediate values to fine-tune the standard deviation
    # Adjust some pixels to intermediate gray values
    for i in range(0, height, 20):
        for j in range(0, width, 20):
            if i < height-5 and j < width-5:
                img_array[i:i+5, j:j+5] = 128  # Gray patches
    
    # Convert to PIL Image (grayscale)
    img = Image.fromarray(img_array, mode='L')
    
    # Calculate actual standard deviation for verification
    std_dev = np.std(img_array)
    print(f"Actual standard deviation: {std_dev:.2f}")
    
    # Convert to RGB for consistency with your original function
    img_rgb = img.convert('RGB')
    
    # Save to BytesIO buffer
    buffer = io.BytesIO()
    img_rgb.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer