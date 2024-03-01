import base64
import math
from PIL import Image
import io


def compress_image(base64_image, max_size=300.0, quality=60):
    image_bytes = io.BytesIO(base64.b64decode(base64_image))
    pil_image = Image.open(image_bytes)
    x, y = pil_image.size
    largest = max(x, y)
    resize_factor = max_size / largest
    x, y = (x * resize_factor, y * resize_factor)
    pil_image = pil_image.resize((math.floor(x), math.floor(y)))
    output_buffer = io.BytesIO()

    try:
        pil_image.save(output_buffer, format='JPEG', quality=quality)
    except Exception:
        pil_image.save(output_buffer, format='PNG', quality=quality)

    compressed_image = output_buffer.getvalue()
    return base64.b64encode(compressed_image).decode('utf-8')
