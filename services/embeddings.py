import json
import os

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATALOG_PATH = os.path.join(BASE_DIR, "data", "shl_catalog.json")
INDEX_PATH = os.path.join(BASE_DIR, "data", "faiss.index")

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index(INDEX_PATH)


def search(query, top_k=10):

    embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    faiss.normalize_L2(embedding)

    scores, indices = index.search(embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        item = catalog[idx].copy()
        item["score"] = float(score)

        results.append(item)

    return results