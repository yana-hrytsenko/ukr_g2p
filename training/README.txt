# Training

`byT5.py` fine-tunes `google/byt5-small` as a neural G2P model, as an
alternative/complement to the rule-based engine in `src/ukr_g2p`.

```bash
pip install -r requirements.txt
```

Expects a `data/silver_dataset.json` (relative to wherever you run the
script from) containing a list of `{"input": ..., "target": ...}` pairs.
A CUDA GPU is picked up automatically if available; not required, but
strongly recommended for training speed.
