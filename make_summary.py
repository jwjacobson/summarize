from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("pszemraj/pegasus-x-large-book-summary")
model = AutoModelForSeq2SeqLM.from_pretrained("pszemraj/pegasus-x-large-book-summary")

def make_summary(text):
    inputs = tokenizer.encode(text, return_tensors="pt", truncation=True)

    summary_ids = model.generate(inputs)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary
