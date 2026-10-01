import torch
import torch.quantization
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType


class ToxicityClassifier:
    """
    A class to handle text classification for toxic content using a
    DistilBERT model fine-tuned with LoRA (Low-Rank Adaptation).
    """

    def __init__(self, model_name: str = "martin-ha/toxic-comment-model"):
        self.device = "cpu"
        print(f"Loading Text Classification model on {self.device}...")

        try:
            # 1. Load the base DistilBERT model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.base_model = AutoModelForSequenceClassification.from_pretrained(model_name)

            # 2. Configure LoRA for DistilBERT
            lora_config = LoraConfig(
                task_type=TaskType.SEQ_CLS,
                r=8,
                lora_alpha=16,
                lora_dropout=0.1,
                target_modules=["q_lin", "v_lin"]
            )

            # 3. Apply LoRA to the base model
            self.peft_model = get_peft_model(self.base_model, lora_config)

            # 4. Merge LoRA weights into the base model
            self.peft_model = self.peft_model.merge_and_unload()
            self.peft_model.to(self.device)
            self.peft_model.eval()

            # 5. Apply Quantization
            print("Applying dynamic quantization to Text Classifier...")
            self.peft_model = torch.quantization.quantize_dynamic(
                self.peft_model, {torch.nn.Linear}, dtype=torch.qint8
            )

            # 6. Create the pipeline using the quantized model
            self.classifier = pipeline(
                "text-classification",
                model=self.peft_model,
                tokenizer=self.tokenizer,
                device=-1
            )
            print("Text Classifier with LoRA and Quantization loaded successfully.")

        except Exception as e:
            print(f"Error loading Text Classifier: {e}")
            raise

    def classify(self, text: str) -> dict:
        """
        Classifies the input text as toxic or non-toxic.
        Returns a dictionary with 'label' and 'score'.
        """
        if not text or not text.strip():
            return {"label": "non-toxic", "score": 1.0}

        try:
            result = self.classifier(text)[0]
            label = result['label']
            score = round(result['score'], 4)
            return {"label": label, "score": score}
        except Exception as e:
            print(f"Error classifying text: {e}")
            return {"label": "error", "score": 0.0}