import torch
import torch.quantization
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

class ToxicityClassifier:
    def __init__(self, model_name: str = "gravitee-io/distilbert-multilingual-toxicity-classifier"):
        self.device = "cpu"
        print(f"Loading Text Classification model on {self.device}...")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=2,
                id2label={0: "not-toxic", 1: "toxic"},
                label2id={"not-toxic": 0, "toxic": 1}
            )
            self.model.to(self.device)
            self.model.eval()

            print("Applying quantization")
            self.model = torch.quantization.quantize_dynamic(
                self.model, {torch.nn.Linear}, dtype=torch.qint8
            )

            self.classifier = pipeline(
                "text-classification",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1
            )
            print("Text Classifier loaded successfully.")

        except Exception as e:
            print(f"Error loading Text Classifier: {e}")
            raise

    def classify(self, text: str) -> dict:
        if not text or not text.strip():
            return {"label": "not-toxic", "score": 1.0}
        try:
            result = self.classifier(text)[0]
            label = "non-toxic" if result['label'] == "not-toxic" else "toxic"
            return {
                "label": label,
                "score": round(result['score'], 4)
            }
        except Exception as e:
            print(f"Error classifying text: {e}")
            return {"label": "error", "score": 0.0}