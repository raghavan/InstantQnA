from get_file_data import check
from read_sources import dump
from create_dataset import parse
from embed import embed, query
from tqdm import tqdm
import pandas as pd
import polars as pl
import sys
import os

if __name__ == '__main__':
    print(f"\n{'Instant Q&A Builder':^100}\n")
    need_emb = check()["regen"]

    if len(need_emb) > 0:
        parse(dump(need_emb))

        total = 0
        with tqdm(total=len(need_emb), desc="Calculating total token") as pbar:
            for file in need_emb:
                pbar.update(1)
                total += pd.read_csv(f'ai_generated/data/{file}.csv')["token_size"].sum()
        value = total/1000 * 0.0004 # cost of ada model
        print(f"\n{total:,} tokens in total, (approx. ${str(round(value,2))})")

        if input("Would you like to embed? (y/n)").lower() == 'y':
            with tqdm(total=len(need_emb), desc="Embedding files") as pbar:
                for file in need_emb:
                    pbar.update(1)
                    embed(file)
        else:
            sys.exit(1)
    dfs = []
    for root, _, files in os.walk("ai_generated/embeds"):
        for file in files:
            if file == ".gitkeep":
                continue
            dfs.append(pl.read_json(f"{root}/{file}"))
    if len(dfs) == 0:
        print('No PDFs to index');
        sys.exit(1)
    else:
        combined_df = pl.concat(dfs)
    
    while True:
        u_input = input("Enter your search query: ")
        print()
        if u_input.lower() == "done":
            break
        result = query(combined_df, u_input)
        for idx, text in enumerate(result[0]):
            print(f"Result {idx + 1} ({result[1][idx]})")
            print(f"{result[2][idx]}")
            print(text)
            print()

