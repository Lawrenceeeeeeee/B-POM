# 将Bert-Large-Chinese解压到当前目录下
# 既可使用本训练程序

import torch
import os
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
from transformers import BertTokenizer, BertForSequenceClassification, get_linear_schedule_with_warmup
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

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
            add_special_tokens=True,      # 添加'[CLS]'和'[SEP]'
            max_length=max_len,           # 填充 & 截断长度
            padding='max_length',         # 填充至max_len
            return_attention_mask=True,   # 构造 attn. masks
            return_tensors='pt'           # 返回 pytorch tensors 格式的数据
        )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)
    labels = torch.tensor(labels.tolist())  # 将labels转换为列表

    return TensorDataset(input_ids, attention_masks, labels)

# 设置模型
def set_model(device, model_dir, num_labels=5):
    tokenizer = BertTokenizer.from_pretrained(model_dir)
    model = BertForSequenceClassification.from_pretrained(
        model_dir,  
        num_labels=num_labels,
        output_attentions=False,
        output_hidden_states=False,
    )
    model.to(device)
    return model, tokenizer

# 训练和验证模型
import os
import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from transformers import get_linear_schedule_with_warmup
from torch.optim import AdamW

def train_and_validate(model, device, train_dataset, validation_dataset, epochs=4, batch_size=16, save_path='model_checkpoints'):
    train_dataloader = DataLoader(train_dataset, sampler=RandomSampler(train_dataset), batch_size=batch_size)
    validation_dataloader = DataLoader(validation_dataset, sampler=SequentialSampler(validation_dataset), batch_size=batch_size)

    optimizer = AdamW(model.parameters(), lr=2e-5, eps=1e-8)
    total_steps = len(train_dataloader) * epochs
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

    for epoch in range(epochs):
        model.train()
        total_train_loss = 0

        for step, batch in enumerate(train_dataloader):
            b_input_ids, b_input_mask, b_labels = batch
            b_input_ids = b_input_ids.to(device)
            b_input_mask = b_input_mask.to(device)
            b_labels = b_labels.to(device)
            
            model.zero_grad()        
            outputs = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)
            
            loss = outputs.loss
            total_train_loss += loss.item()
            loss.backward()
            optimizer.step()
            scheduler.step()

            if step % 10 == 0:
                print(f"Epoch {epoch+1}, Step {step}, Loss: {loss.item()}")

        avg_train_loss = total_train_loss / len(train_dataloader)
        print(f"Epoch {epoch+1}, Average Training Loss: {avg_train_loss}")

        # 保存每20个epoch的checkpoint
        if (epoch + 1) % 20 == 0:
            checkpoint_path = os.path.join(save_path, f'checkpoint_epoch_{epoch+1}.pth')
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': avg_train_loss,
            }, checkpoint_path)
            print(f"Saved checkpoint for epoch {epoch+1} at '{checkpoint_path}'")

        model.eval()
        total_eval_loss = 0
        total_eval_accuracy = 0

        for batch in validation_dataloader:
            b_input_ids, b_input_mask, b_labels = batch
            b_input_ids = b_input_ids.to(device)
            b_input_mask = b_input_mask.to(device)
            b_labels = b_labels.to(device)

            with torch.no_grad():
                outputs = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)
            
            loss = outputs.loss
            total_eval_loss += loss.item()
            logits = outputs.logits
            logits = logits.detach().cpu().numpy()
            label_ids = b_labels.to('cpu').numpy()
            total_eval_accuracy += np.sum(np.argmax(logits, axis=1).flatten() == label_ids.flatten())

        avg_val_accuracy = total_eval_accuracy / len(validation_dataset)
        avg_val_loss = total_eval_loss / len(validation_dataloader)
        print(f"Epoch {epoch+1}, Validation Accuracy: {avg_val_accuracy:.2f}")
        print(f"Epoch {epoch+1}, Validation Loss: {avg_val_loss}")

# 主程序
def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print('Using device:', device)

    # 假设你已经将数据准备好在以下路径
    contents, emotions, rational = load_data('BV1bc411f7fK_updated.csv')

    # 指定模型文件夹路径
    model_dir = 'Bert-Large-Chinese'

    # 设置模型和分词器
    model, tokenizer = set_model(device, model_dir, num_labels=5)

    # 分割数据用于训练和验证
    content_train, content_val, emotion_train, emotion_val = train_test_split(contents, emotions, test_size=0.1, random_state=42)
    _, _, rational_train, rational_val = train_test_split(contents, rationals, test_size=0.1, random_state=42)
    
    # 准备训练和验证数据集
    emotion_train_dataset = prepare_dataset(content_train, emotion_train, tokenizer)
    emotion_val_dataset = prepare_dataset(content_val, emotion_val, tokenizer)
    rational_train_dataset = prepare_dataset(content_train, rational_train, tokenizer)
    rational_val_dataset = prepare_dataset(content_val, rational_val, tokenizer)
    
    # 训练和验证情感模型
    print("Training and validating emotion model...")
    train_and_validate(model, device, emotion_train_dataset, emotion_val_dataset)

    # 重新设置模型，避免权重干扰
    model, _ = set_model(device, model_dir, num_labels=5)

    # 训练和验证理性模型
    print("Training and validating rational model...")
    train_and_validate(model, device, rational_train_dataset, rational_val_dataset)

    print("Training complete!")

if __name__ == "__main__":
    main()


       
