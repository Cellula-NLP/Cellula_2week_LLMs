import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


class ImageCaptioner:
    """
    A class to handle image captioning using the BLIP model.
    """

    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):
        # Check if GPU is available, otherwise use CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading Image Captioning model on {self.device}...")
        try:
            self.processor = BlipProcessor.from_pretrained(model_name)
            self.model = BlipForConditionalGeneration.from_pretrained(model_name).to(self.device)
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