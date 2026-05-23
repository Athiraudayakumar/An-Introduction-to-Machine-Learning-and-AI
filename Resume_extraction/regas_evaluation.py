from datasets import Dataset

from ragas import evaluate

from ragas.metrics import (
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy
)

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings


# ============================================================
# GROQ LLM
# ============================================================

llm = ChatOpenAI(

    model="openai/gpt-oss-120b",

    temperature=0,
    n=1,

    openai_api_key="s",

    openai_api_base="https://api.groq.com/openai/v1"
)

ragas_llm = LangchainLLMWrapper(llm)


# ============================================================
# SENTENCE TRANSFORMER EMBEDDINGS
# ============================================================

embedding_model = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

ragas_embeddings = LangchainEmbeddingsWrapper(
    embedding_model
)


# ============================================================
# SAMPLE DATA
# ============================================================

data = {

    "question": [

        """
        Find Machine Learning Engineer in UAE
        with PySpark and GCP experience
        """
    ],

    "contexts": [[

        """
        Developed GCP AutoML model achieving ROC-AUC of 0.92.
        Deployed final model on Vertex AI.
        """,

        """
        Tech Stack:
        PySpark, BigQuery, Airflow,
        GCP, Hadoop, Docker, Kubernetes.
        """,

        """
        Migrated and refactored 500+ PySpark jobs
        using Spark on Dataproc.
        """
    ]],

    "answer": [

        """
        ATHIRA KRISHNA is a Senior Machine Learning Engineer
        based in UAE with expertise in PySpark,
        GCP, BigQuery, Airflow, and ETL pipelines.
        """
    ],

    "ground_truth": [

        """
        Candidate is a Machine Learning Engineer
        in UAE with strong PySpark and GCP experience.
        """
    ]

}


# ============================================================
# CREATE DATASET
# ============================================================

dataset = Dataset.from_dict(data)


# ============================================================
# RUN RAGAS
# ============================================================

result = evaluate(

    dataset=dataset,

    metrics=[

        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy
    ],

    llm=ragas_llm,

    embeddings=ragas_embeddings,

    raise_exceptions=True
)


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n========== RAGAS RESULTS ==========\n")

print(result)