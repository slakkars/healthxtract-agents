from __future__ import annotations
from typing import List, Union
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import io

def images_from_upload(file_bytes: bytes, filename: str) -> List[Image.Image]:
    name = (filename or "").lower()
    if name.endswith(".pdf"):
        # convert pdf pages -> PIL images
        return convert_from_bytes(file_bytes, dpi=200)
    # assume image
    return [Image.open(io.BytesIO(file_bytes)).convert("RGB")]

def ocr_images(images: List[Image.Image]) -> str:
    chunks = []
    for i, img in enumerate(images, start=1):
        text = pytesseract.image_to_string(img)
        chunks.append(f"\n--- page {i} ---\n{text}")
    return "\n".join(chunks)