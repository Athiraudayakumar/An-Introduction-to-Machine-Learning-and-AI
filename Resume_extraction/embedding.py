import os
import pickle
import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)


# ============================================================
# MODELS
# ============================================================

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

cross_encoder = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


# ============================================================
# VECTOR DB
# ============================================================

VECTOR_DIMENSION = 384

INDEX_PATH = "resume_index.faiss"

METADATA_PATH = "metadata.pkl"


# ============================================================
# LOAD / CREATE INDEX
# ============================================================

if os.path.exists(INDEX_PATH):

    index = faiss.read_index(
        INDEX_PATH
    )

    with open(
        METADATA_PATH,
        "rb"
    ) as f:

        metadata_store = pickle.load(f)

else:

    index = faiss.IndexFlatL2(
        VECTOR_DIMENSION
    )

    metadata_store = []


# ============================================================
# TEXT CHUNKING
# ============================================================

def split_text(
    text,
    chunk_size=120,
    overlap = 30
):

    words = text.split()

    chunks = []
    start = 0

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunks.append(chunk)
        start += (
        chunk_size - overlap
    )

    return chunks


# ============================================================
# SEMANTIC CHUNKING
# ============================================================

def create_semantic_chunks(
    employee_id,
    sections
):

    chunks = []

    searchable_sections = [

        "experience",

        "skills",

        "projects",

        "certifications"
    ]

    for section_name in searchable_sections:

        content = sections.get(
            section_name,
            ""
        )

        if not content.strip():

            continue

        split_chunks = split_text(
            content
        )

        for chunk_text in split_chunks:

            chunks.append({

                "employee_id":
                employee_id,

                "section":
                section_name,

                "text":
                chunk_text
            })

    return chunks


# ============================================================
# STORE EMBEDDINGS
# ============================================================

def store_resume_embeddings(
    employee_id,
    metadata,
    sections
):

    chunks = create_semantic_chunks(
        employee_id,
        sections
    )

    for chunk in chunks:

        embedding = embedding_model.encode(
            chunk["text"]
        )

        embedding = np.array(
            [embedding]
        ).astype("float32")

        index.add(embedding)

        metadata_store.append({

            "employee_id":
            employee_id,

            "name":
            metadata.get(
                "Full Name"
            ),

            "email":
            metadata.get(
                "Email"
            ),

            "phone":
            metadata.get(
                "Phone Number"
            ),

            "location":
            metadata.get(
                "Location"
            ),

            "section":
            chunk["section"],

            "text":
            chunk["text"]
        })

    faiss.write_index(
        index,
        INDEX_PATH
    )

    with open(
        METADATA_PATH,
        "wb"
    ) as f:

        pickle.dump(
            metadata_store,
            f
        )


# ============================================================
# SEMANTIC SEARCH
# ============================================================

def semantic_search(
    query,
    top_k=20
):

    query_embedding = (
        embedding_model.encode(query)
    )

    query_embedding = np.array(
        [query_embedding]
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    retrieved = []

    for idx in indices[0]:

        if idx < len(metadata_store):

            retrieved.append(
                metadata_store[idx]
            )

    return retrieved


# ============================================================
# RERANKING
# ============================================================

def rerank_candidates(
    query,
    candidates
):

    pairs = []

    for candidate in candidates:

        pairs.append([
            query,
            candidate["text"]
        ])

    scores = cross_encoder.predict(
        pairs
    )

    ranked = []

    for candidate, score in zip(
        candidates,
        scores
    ):

        candidate["score"] = (
            float(score)
        )

        ranked.append(candidate)

    ranked = sorted(

        ranked,

        key=lambda x: x["score"],

        reverse=True
    )

    return ranked


# ============================================================
# FINAL SEARCH
# ============================================================

def intelligent_search(
    query
):

    retrieved = semantic_search(
        query=query,
        top_k=20
    )

    ranked = rerank_candidates(
        query,
        retrieved
    )

    return ranked[:5]