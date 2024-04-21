import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax

class ModelInferer:
    def __init__(self, model_dirs, tokenizer_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models = {}
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)

        for key, model_dir in model_dirs.items():
            print(f"Loading model from {model_dir}...")
            model = BertForSequenceClassification.from_pretrained(model_dir)
            
            model.to(self.device)
            model.eval()
            
            self.models[key] = model

    def predict(self, text, model_key):
        model = self.models[model_key]
        inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
        input_ids = inputs['input_ids'].to(self.device)
        attention_mask = inputs['attention_mask'].to(self.device)

        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)
            probs = softmax(outputs.logits, dim=1)

        predicted_label = torch.argmax(probs, dim=1).item()
        return predicted_label + 1 if model_key in ['manyi', 'qingxu'] else predicted_label

# Paths to the trained models
model_dirs = {
    "manyi": "models/Bert-updated-manyi",
    "qingxu": "models/Bert-updated-qingxu",
    "taolun": "models/Bert-updated-taolun",
    "tiwen": "models/Bert-updated-tiwen",
    "wangeng": "models/Bert-updated-wangeng"
}

tokenizer_path = "models\Bert-Large-Chinese"  # Replace with the path where the common tokenizer is stored
inferer = ModelInferer(model_dirs, tokenizer_path)

# Example text to predict
text = "这个产品真不错！"

# Making predictions with each model
for key in model_dirs.keys():
    prediction = inferer.predict(text, key)
    print(f"Prediction using {key} model: {prediction}")
