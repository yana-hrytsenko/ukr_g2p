from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

CHECKPOINT = "models/byt5/checkpoint-XXXXX"
OUTPUT = "models/byt5/final"

model = AutoModelForSeq2SeqLM.from_pretrained(CHECKPOINT)
tokenizer = AutoTokenizer.from_pretrained(CHECKPOINT)

model.save_pretrained(OUTPUT)
tokenizer.save_pretrained(OUTPUT)

print("saved")