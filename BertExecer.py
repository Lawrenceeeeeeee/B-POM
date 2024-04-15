import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# 加载模型和分词器
def load_model(model_path):
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model.eval()  # 设置为评估模式
    return model, tokenizer

# 预测单条文本
def predict(text, model, tokenizer, device, is_rational=False):
    encoded_dict = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=256,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    input_ids = encoded_dict['input_ids'].to(device)
    attention_mask = encoded_dict['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=1)
        predicted_class = torch.argmax(probs, dim=1) + 1  # 转换为1-5的范围

    # 如果是理性分析，转换输出为0或1
    if is_rational:
        predicted_class = 0 if predicted_class <= 3 else 1  # 假定1-3为类别“0”，4-5为类别“1”

    return predicted_class.item()

# 处理CSV文件
def process_csv(input_csv, output_csv, model_path, device):
    model, tokenizer = load_model(model_path)
    df = pd.read_csv(input_csv)
    # 情感分析，输出范围1-5
    df['emotion'] = [predict(row['content'], model, tokenizer, device, is_rational=False) for index, row in df.iterrows()]
    # 理性分析，输出范围0或1
    df['rational'] = [predict(row['content'], model, tokenizer, device, is_rational=True) for index, row in df.iterrows()]

    df.to_csv(output_csv, index=False)

# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 路径和文件
input_csv_path = 'path_to_your_input_csv.csv'
output_csv_path = 'path_to_your_output_csv.csv'
model_path = 'path_to_your_trained_model'

# 执行预测并处理CSV
process_csv(input_csv_path, output_csv_path, model_path, device)
