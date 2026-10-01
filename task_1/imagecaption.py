import torch
import torch.quantization
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


class ImageCaptioner:
    """
    A class to handle image captioning using the BLIP model.
    """

    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):

        self.device = "cpu"

        print(f"Loading Image Captioning model on {self.device}...")
        try:
            self.processor = BlipProcessor.from_pretrained(model_name)
            self.model = BlipForConditionalGeneration.from_pretrained(model_name)

            # Apply Quantization
            print("Applying dynamic quantization to BLIP model")
            self.model = torch.quantization.quantize_dynamic(
                self.model, {torch.nn.Linear}, dtype=torch.qint8
            )
            self.model.to(self.device)
        except Exception as e:
            print(f"Error loading BLIP model: {e}")
            raise

    def generate_caption(self, image: Image.Image) -> str:
        """
        Generates a caption for the given PIL Image.
        """
        if image is None:
            return "No image provided."

        try:
            # Prepare image for the model
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)

            # Generate caption
            with torch.no_grad():
                out = self.model.generate(**inputs, max_new_tokens=50)

            # Decode the output
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            return caption.strip()

        except Exception as e:
            print(f"Error generating caption: {e}")
            return "Error generating caption."