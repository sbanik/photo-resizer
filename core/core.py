from PIL import Image
import io
from typing import Any, Dict

def resize_image(image: Image.Image, width: int, height: int, quality: int = 95):
    resized_img = image.resize((width, height), Image.Resampling.LANCZOS)
    exif_data = image.info.get('exif')
    img_format = image.format if image.format in ['JPEG', 'PNG'] else 'PNG'
    buf = io.BytesIO()
    save_kwargs: Dict[str, Any] = {"format": img_format}
    if exif_data and img_format == "JPEG":
        save_kwargs["exif"] = exif_data
    if img_format == "JPEG":
        save_kwargs["quality"] = quality
        save_kwargs["optimize"] = True
    resized_img.save(buf, **save_kwargs)
    buf.seek(0)
    return resized_img, img_format, buf

def parse_size(size_str: str) -> int:
    size_str = size_str.strip().upper()
    if size_str.endswith("KB"):
        return int(float(size_str[:-2]) * 1024)
    elif size_str.endswith("MB"):
        return int(float(size_str[:-2]) * 1024 * 1024)
    else:
        return int(size_str)
