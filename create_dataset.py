import os
import polars as pl
from transformers import GPT2TokenizerFast
from tqdm import tqdm

def parse(include: "list[str]" = None) -> None:
    texts: "list[str]" = []
    parsed_text: "list[str]" = []
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    for root, _, files in os.walk("ai_generated/dumps"):
        file_count = sum(len(files) for _, _, files in os.walk("sources")) 
        with tqdm(total=file_count, desc="Creating dataset") as pbar:
            for file in files:
                pbar.update(1)
                if include and file not in include or '.gitkeep' in file:
                    continue
                with open(os.path.join(root, file), "r", encoding="utf-8") as rf:
                    for line in rf:
                        for word in line.split(". "):
                            if len(tokenizer.encode(" ".join([*texts, *word.split()]))) <= 256:
                                texts = [*texts, *word.split()]
                            else:
                                parsed_text.append(" ".join(texts))
                                texts = []
                                texts = [*texts, *word.split()]
                parsed_text.append(" ".join(texts))
                texts = []
                pl.DataFrame({
                    "file_name": [file.replace("_dump.txt", "")] * len(parsed_text),
                    "text": parsed_text,
                    "token_size": [len(tokenizer.encode(x)) for x in parsed_text],
                    "embed": [None] * len(parsed_text)
                }).write_csv(f"ai_generated/data/{file}.csv")
                parsed_text = []
    print()    

if __name__ == '__main__':
    parse()