from pathlib import Path

import chromadb

from app.core.llm import embed_text


def retrieve(
    course_id: str,
    question: str,
    embedding_model: str,
    top_k: int = 5,
    allowed_content_types: list[str] | None = None,
) -> list[dict]:
    db_dir = Path("courses") / course_id / "chroma_db"
    client = chromadb.PersistentClient(path=str(db_dir))
    collection = client.get_or_create_collection(name="course_materials")

    question_embedding = embed_text(question, embedding_model)

    where = None
    if allowed_content_types:
        if len(allowed_content_types) == 1:
            where = {"content_type": allowed_content_types[0]}
        else:
            where = {"$or": [{"content_type": ct} for ct in allowed_content_types]}

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        where=where,
    )

    ids = results.get("ids", [[]])[0]
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    hits = []
    for doc_id, text, meta, distance in zip(ids, docs, metas, distances):
        hits.append(
            {
                "id": doc_id,
                "text": text,
                "meta": meta or {},
                "distance": distance,
            }
        )

    return hits