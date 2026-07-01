import json
import os
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATALOG_PATH = os.path.join(BASE_DIR, "data", "shl_catalog.json")

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

documents = [assessment_to_text(item) for item in catalog]

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    show_progress_bar=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

faiss.normalize_L2(embeddings)

index.add(embeddings)


def search(query, top_k=10):
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        assessment = catalog[idx].copy()
        assessment["score"] = float(score)
        results.append(assessment)

    return results