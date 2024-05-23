from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("pszemraj/pegasus-x-large-book-summary")
model = AutoModelForSeq2SeqLM.from_pretrained("pszemraj/pegasus-x-large-book-summary")

def read_in_chunks(filepath, chunk_size=800):
    with open(filepath, 'r', encoding='utf-8') as file:
            current_chunk = []
            for line in file:
                cleaned_line = line.strip()
                current_chunk.append(cleaned_line)
                if len(current_chunk) == chunk_size:
                    yield current_chunk
                    current_chunk = []  

            if current_chunk:
                yield current_chunk

def make_summary(chunk):
    inputs = tokenizer.encode(chunk, return_tensors="pt", truncation=True)

    summary_ids = model.generate(inputs)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary



def save_summary(source, target, chunk_size):
    with open(target,'w') as target:  
        for chunk in read_in_chunks(source, chunk_size=chunk_size):
            target.write(make_summary(' '.join(chunk)))

def print_summary(source, chunk_size):
    for chunk in read_in_chunks(source, chunk_size=chunk_size):
        print(make_summary(' '.join(chunk)))

