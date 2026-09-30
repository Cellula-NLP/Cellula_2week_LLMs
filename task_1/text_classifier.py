import torch
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType


class ToxicityClassifier:
    """
    A class to handle text classification for toxic content using a
    DistilBERT model fine-tuned with LoRA (Low-Rank Adaptation).
    """

    def __init__(self, model_name: str = "martin-ha/toxic-comment-model"):
        # Dynamic device selection
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading Text Classification model on {self.device}...")

        try:
            # 1. Load the base DistilBERT model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.base_model = AutoModelForSequenceClassification.from_pretrained(model_name)

            # 2. Configure LoRA for DistilBERT
            # Target the query and value projection layers (q_lin, v_lin)
            # You can also include "k_lin" for keys if desired
            lora_config = LoraConfig(
                task_type=TaskType.SEQ_CLS,
                r=8,
                lora_alpha=16,
                lora_dropout=0.1,
                target_modules=["q_lin", "v_lin"]
            )

            # 3. Apply LoRA to the base model
            self.peft_model = get_peft_model(self.base_model, lora_config)
            self.peft_model.to(self.device)
            self.peft_model.eval()

            # 4. Create the pipeline using the LoRA-wrapped model
            pipeline_device = 0 if torch.cuda.is_available() else -1
            self.classifier = pipeline(
                "text-classification",
                model=self.peft_model,
                tokenizer=self.tokenizer,
                device=pipeline_device
            )
            print("Text Classifier with LoRA loaded successfully.")

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