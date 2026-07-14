from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from ukr_g2p.pipeline import transcribe


MODEL_PATH = "models/byt5/final"


tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)

model.eval()


words = [
    #add list the words
]


for word in words:

    inputs = tokenizer(
        word,
        return_tensors="pt",

        max_length=32,
        truncation=True

    )

    with torch.no_grad():
        output = model.generate(
            **inputs,
            #max_length=32

            max_length=64,
            num_beams=4,
            early_stopping=True
            
        )

    prediction = tokenizer.decode(
        output[0],
        skip_special_tokens=True
    )

    rule_output = transcribe(
        word,
        mode="ipa_broad"
    )

    print(word)
    print("RULE:", rule_output)
    print("BYT5:", prediction)
    print()