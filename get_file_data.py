import os
from datetime import datetime
import pandas as pd

def check():
    data = {
        "src": {},
        "emb": {}
    }
    regen = []
    for root, _, files in os.walk("sources"):
        for file in files:
            if file == ".gitkeep":
                continue
            absdate = os.path.getmtime(f"{root}/{file}")
            fmtdate = datetime.fromtimestamp(absdate).strftime('%a, %b %d %H:%M:%S %Y')
            data["src"][file] = {}
            data["src"][file]["absdate"] = absdate
            data["src"][file]["fmtdate"] = fmtdate
            try:
                df = pd.read_csv(f"ai_generated/data/{file}.csv")
                data["src"][file]["token_size"] = int(df["token_size"].sum())
                emb_absdate = os.path.getmtime(f"ai_generated/embeds/{file}.json")
                if emb_absdate < absdate:
                    print(f"ai_generated/embeds/{file}.json EMBED EXPIRED")
                    regen.append(file)
                emb_fmtdate = datetime.fromtimestamp(emb_absdate).strftime('%a, %b %d %H:%M:%S %Y')
                data["emb"][file] = {}
                data["emb"][file]["absdate"] = emb_absdate
                data["emb"][file]["fmtdate"] = emb_fmtdate
            except:
                print(f"ai_generated/embeds/{file}.json EMBED NOT FOUND")
                regen.append(file)
    data["regen"] = regen
    print()
    return data 


if __name__ == '__main__':
    print((check()))