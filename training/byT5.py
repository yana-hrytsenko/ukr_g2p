import json
import random

import torch
from torch.utils.data import Dataset

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments
)

print(torch.cuda.is_available())

MODEL_NAME = "google/byt5-small"

DATASET_PATH = "data/silver_dataset.json"

OUTPUT_DIR = "models/byt5"

BATCH_SIZE = 16
EPOCHS = 5
LEARNING_RATE = 5e-5
MAX_LENGTH = 32

VALIDATION_SPLIT = 0.1

SEED = 42

random.seed(SEED)
torch.manual_seed(SEED)


class G2PDataset(Dataset):

    def __init__(self, examples, tokenizer):

        self.examples = examples
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):

        word = self.examples[idx]["input"]
        ipa = self.examples[idx]["target"]

        inputs = self.tokenizer(
            word,
            truncation=True,
            max_length=MAX_LENGTH,
            padding="max_length",
            return_tensors="pt",
        )

        labels = self.tokenizer(
            ipa,
            truncation=True,
            max_length=MAX_LENGTH,
            padding="max_length",
            return_tensors="pt",
        )

        labels = labels.input_ids.squeeze()

        labels[labels == self.tokenizer.pad_token_id] = -100

        return {
            "input_ids": inputs.input_ids.squeeze(),
            "attention_mask": inputs.attention_mask.squeeze(),
            "labels": labels,
        }
    

with open(DATASET_PATH, encoding="utf8") as f:
    dataset = json.load(f)

random.shuffle(dataset)

split = int(len(dataset) * VALIDATION_SPLIT)

val_examples = dataset[:split]
train_examples = dataset[split:]

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

train_dataset = G2PDataset(train_examples, tokenizer)
val_dataset = G2PDataset(val_examples, tokenizer)



training_args = Seq2SeqTrainingArguments(
    output_dir=OUTPUT_DIR,

    do_train=True,
    do_eval=True,

    num_train_epochs=EPOCHS,

    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,

    learning_rate=LEARNING_RATE,

    eval_strategy="epoch",

    save_strategy="epoch",

    load_best_model_at_end=True,

    metric_for_best_model="eval_loss",

    logging_steps=100,

    predict_with_generate=True,

    fp16=False,

    max_grad_norm=1.0
)


trainer = Seq2SeqTrainer(
    model=model,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=val_dataset,

    processing_class=tokenizer,
)


trainer.train()