import polars as pl
import openai
import sys
from openai.embeddings_utils import get_embedding, cosine_similarity
from get_file_data import check
from read_sources import dump
from create_dataset import parse

try:
    from constants import token
except ImportError as e:
    print("Couldn't get the credentials:", e)
    sys.exit(1)
openai.api_key = token

def make(include):
    dump(include)
    parse(include)

def embed(file, model="ada"):
    # make([file])
    try:
        df = pl.read_csv(f"ai_generated/data/{file}.csv")
        df = df.lazy().with_column(
                pl.col("text").apply(lambda text: get_embedding(text, engine=f'text-embedding-{model}-002')).alias("embed")
            ).collect()
        df.write_json(f"ai_generated/embeds/{file}.json")
    except:
        print(f"Invalid API token")
        sys.exit(1)
    
    return check()

def query(df, q, model="ada", n=3):
    search_query_emb = get_embedding(q, engine=f"text-embedding-{model}-002")
    df = df.lazy().with_column(
        pl.col("embed").apply(lambda emb: cosine_similarity(emb, search_query_emb)).alias("similarities")
    ).sort("similarities", reverse=True).collect()
    df = df.head(3)

    return [
        list(df["text"]),
        list(df["similarities"]),
        list(df["file_name"])
    ]

if __name__ == '__main__':
    embed("mind.pdf")

# def query(df, query, n=3):
#     search_query_embedding = get_embedding(
#         query,
#         engine="text-embedding-ada-002"
#     )
#     df['similarities'] = df["vector"].apply(lambda x: cosine_similarity(x, search_query_embedding))
#     res = df.sort_values('similarities', ascending=False)["text"].head(n)
#     return list(res)

# if __name__ == '__main__':
#     df = embed()
#     print(query(df, "good meditation"))
#     print(query(df, "lobha"))