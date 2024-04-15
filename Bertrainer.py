# 将Bert-Large-Chinese解压到当前目录下
# 既可使用本训练程序

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
from transformers import BertTokenizer, BertModel, AdamW, get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
import pandas as pd
import os
from tqdm import tqdm

# 定义一个多任务学习模型
class BertForMultiTaskLearning(nn.Module):
    def __init__(self, model_name, num_labels_emotion, num_labels_rational):
        super(BertForMultiTaskLearning, self).__init__()
        self.bert = BertModel.from_pretrained(model_name)
        self.classifiers = nn.ModuleDict({
            'emotion': nn.Linear(self.bert.config.hidden_size, num_labels_emotion),
            'rational': nn.Linear(self.bert.config.hidden_size, num_labels_rational)
        })
    
    def forward(self, input_ids, attention_mask, task_name):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        pooled_output = outputs[1]
        return self.classifiers[task_name](pooled_output)

# 加载数据
def load_data(filename):
    df = pd.read_csv(filename)
    return df['content'], df['emotion'], df['rational']

# 准备数据集
def prepare_dataset(contents, labels, tokenizer, max_len=256):
    input_ids = []
    attention_masks = []
    for content in contents:
        encoded_dict = tokenizer.encode_plus(
            content,
            add_special_tokens=True,
            max_length=max_len,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)
    labels = torch.tensor(labels.tolist())
    return TensorDataset(input_ids, attention_masks, labels)

def train_and_validate_multitask(model, device, train_datasets, validation_datasets, epochs=4, batch_size=16, save_path='model_checkpoints'):
    optimizers = {task: AdamW(model.parameters(), lr=2e-5, eps=1e-8) for task in train_datasets.keys()}
    schedulers = {task: get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=len(train_datasets[task]) * epochs / batch_size)
                  for task, optimizer in optimizers.items()}

    for epoch in range(epochs):
        for task, data_loader in train_datasets.items():
            model.train()
            total_loss = 0
            data_loader = DataLoader(data_loader, sampler=RandomSampler(data_loader), batch_size=batch_size)
            progress_bar = tqdm(enumerate(data_loader), total=len(data_loader), desc=f"Epoch {epoch+1}, Task {task}")

            for step, batch in progress_bar:
                b_input_ids, b_input_mask, b_labels = tuple(t.to(device) for t in batch)
                model.zero_grad()
                logits = model(b_input_ids, b_input_mask, task)
                loss = nn.CrossEntropyLoss()(logits, b_labels)
                total_loss += loss.item()
                loss.backward()
                optimizers[task].step()
                schedulers[task].step()

                progress_bar.set_postfix({'loss': loss.item()})

            print(f"Task {task}, Epoch {epoch+1}, Average Loss: {total_loss / len(data_loader)}")

        # Save checkpoint every 20 epochs
        if (epoch + 1) % 20 == 0:
            checkpoint_path = os.path.join(save_path, f'checkpoint_epoch_{epoch+1}.pth')
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': {task: optimizer.state_dict() for task, optimizer in optimizers.items()},
                'loss': total_loss,
            }, checkpoint_path)
            print(f"Saved checkpoint for epoch {epoch+1} at '{checkpoint_path}'")

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print('Using device:', device)
    contents, emotions, rationals = load_data('BV1bc411f7fK_updated.csv')
    tokenizer = BertTokenizer.from_pretrained('Bert-Large-Chinese')
    # 准备数据集
    datasets = {
        'emotion': prepare_dataset(contents, emotions, tokenizer),
        'rational': prepare_dataset(contents, rationals, tokenizer)
    }
    # 创建模型
    model = BertForMultiTaskLearning('Bert-Large-Chinese', num_labels_emotion=5, num_labels_rational=5).to(device)
    # 训练和验证
    train_and_validate_multitask(model, device, datasets, datasets)  # 示例中使用相同数据集作为训练和验证
    
if __name__ == "__main__":
    main()
