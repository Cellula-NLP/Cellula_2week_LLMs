import socket
from io import BytesIO
from PIL import Image
from .config import ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE_MB

def is_online(host: str = "huggingface.co", port: int = 443, timeout: int = 3) -> bool:
    """Detect if the machine has internet (needed on first model download)."""
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except OSError:
        return False

def validate_image(uploaded_file) -> tuple[bool, str, Image.Image | None]:
    """Validate an uploaded image file."""
    if uploaded_file is None:
        return False, "No file uploaded.", None

    extension = uploaded_file.name.split(".")[-1].lower()
    if extension not in ALLOWED_IMAGE_TYPES:
        return False, f"Invalid file type '.{extension}'. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}.", None

    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        return False, f"File too large ({size_mb:.1f} MB). Max allowed: {MAX_IMAGE_SIZE_MB} MB.", None

    try:
        image = Image.open(BytesIO(uploaded_file.getvalue())).convert("RGB")
        return True, "OK", image
    except Exception as exc:
        return False, f"Corrupted or unreadable image: {exc}", None