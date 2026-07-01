import os
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATALOG_PATH = os.path.join(BASE_DIR, "data", "shl_catalog.json")
INDEX_PATH = os.path.join(BASE_DIR, "data", "faiss.index")

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")


def assessment_to_text(item):
    return f"""
Name: {item['name']}
Description: {item['description']}
Categories: {' '.join(item['keys'])}
Job Levels: {' '.join(item['job_levels'])}
Duration: {item['duration']}
"""


documents = [assessment_to_text(x) for x in catalog]

embeddings = model.encode(
    documents,
    convert_to_numpy=True
)

faiss.normalize_L2(embeddings)

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, INDEX_PATH)

print("Index saved to", INDEX_PATH)