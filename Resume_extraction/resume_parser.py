import uuid

from openai import OpenAI

# from dotenv import load_dotenv

import os

from utils import (
    extract_resume_text,
    split_resume_sections
)

from embedding import (
    store_resume_embeddings
)

import json


# ============================================================
# ENV
# ============================================================

# load_dotenv()


# ============================================================
# AZURE CLIENT
# ============================================================

client = OpenAI(
        api_key="",
        base_url="https://api.groq.com/openai/v1",
    )

# ============================================================
# METADATA EXTRACTION
# ============================================================

def extract_candidate_metadata(
    resume_text
):

    prompt = f"""
    Extract structured resume information.

    Return ONLY valid JSON.

    Extract:

    - Full Name
    - Email
    - Phone Number
    - Location
    - Total Experience
    - Current Job Title
    - Technical Skills
    - Certifications
    - Highest Qualification

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[

            {
                "role": "system",
                "content":
                "You are a resume parser."
            },

            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0,

        response_format={
            "type": "json_object"
        }
    )

    return json.loads(
        response.choices[0]
        .message.content
    )


# ============================================================
# PROCESS RESUME
# ============================================================

def process_resume(file_path):

    resume_text = extract_resume_text(
        file_path
    )

    sections = split_resume_sections(
        resume_text
    )

    metadata = (
        extract_candidate_metadata(
            resume_text
        )
    )

    employee_id = str(uuid.uuid4())

    metadata["employee_id"] = (
        employee_id
    )

    store_resume_embeddings(
        employee_id,
        metadata,
        sections
    )

    return metadata