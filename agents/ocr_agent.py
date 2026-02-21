from core.ocr import images_from_upload, ocr_images

def run_ocr(file_bytes: bytes, filename: str) -> str:
    images = images_from_upload(file_bytes, filename)
    return ocr_images(images)