import torch
from torch.utils.data import Dataset, DataLoader, random_split
from transformers import BertTokenizer, BertForSequenceClassification, get_scheduler
from tqdm import tqdm
import pandas as pd

class SentimentModelTrainer:
    def __init__(self, model_path, tokenizer, filepath, split_ratio=0.8):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")  # 打印正在使用的设备
        self.model = BertForSequenceClassification.from_pretrained(model_path, num_labels=3).to(self.device)
        self.tokenizer = tokenizer
        self.filepath = filepath
        self.split_ratio = split_ratio

        # 初始化数据集
        self.train_dataset, self.test_dataset = self.load_and_split_data()

    def load_and_split_data(self):
        # 读取数据并处理NaN值
        df = pd.read_csv(self.filepath)
        df.dropna(subset=['content', 'index_qingxu'], inplace=True)  # 删除任何含有NaN的行
        df['index_qingxu'] = df['index_qingxu'].apply(lambda x: int(x) - 1)  # 转换标签

        texts = df['content'].tolist()
        labels = df['index_qingxu'].tolist()

        full_dataset = SentimentDataset(self.tokenizer, texts, labels)
        train_size = int(len(full_dataset) * self.split_ratio)
        test_size = len(full_dataset) - train_size
        return random_split(full_dataset, [train_size, test_size])

    def train(self, batch_size=8, epochs=3):
        train_loader = DataLoader(self.train_dataset, batch_size=batch_size, shuffle=True)
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=2e-5)
        num_training_steps = len(train_loader) * epochs
        lr_scheduler = get_scheduler("linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps)

        for epoch in range(epochs):
            self.model.train()
            loop = tqdm(train_loader, leave=True)
            for batch in loop:
                optimizer.zero_grad()
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                lr_scheduler.step()

                loop.set_description(f'Epoch {epoch + 1}')
                loop.set_postfix(loss=loss.item())

    def save_model(self, save_path):
        self.model.save_pretrained(save_path)
        print(f"模型已保存到{save_path}。")

class SentimentDataset(Dataset):
    def __init__(self, tokenizer, texts, labels):
        self.tokenizer = tokenizer
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
        inputs = {key: value.squeeze() for key, value in inputs.items()}
        return {
            'input_ids': inputs['input_ids'],
            'attention_mask': inputs['attention_mask'],
            'labels': torch.tensor(label, dtype=torch.long)
        }

# 使用示例
model_path = 'Bert-Large-Chinese'
tokenizer = BertTokenizer.from_pretrained(model_path)
filepath = 'tag_data\\traindata.csv'
trainer = SentimentModelTrainer(model_path, tokenizer, filepath)
trainer.train()
trainer.save_model('Bert-updated-qingxu')
