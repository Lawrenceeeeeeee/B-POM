import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax

class ModelInferer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models = {}
        
        # 内置模型目录和tokenizer路径
        model_dirs = {
            "manyi": "models/Bert-updated-manyi",
            "qingxu": "models/Bert-updated-qingxu",
            "taolun": "models/Bert-updated-taolun",
            "tiwen": "models/Bert-updated-tiwen",
            "wangeng": "models/Bert-updated-wangeng"
        }
        tokenizer_path = "models/Bert-Large-Chinese"
        
        # 加载tokenizer
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)

        # 加载模型
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
