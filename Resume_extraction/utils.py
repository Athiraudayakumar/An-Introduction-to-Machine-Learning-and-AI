import re
import docx
import PyPDF2


# ============================================================
# PDF EXTRACTION
# ============================================================

def extract_text_from_pdf(
    pdf_path
):

    text = ""

    with open(pdf_path, "rb") as pdf_file:

        reader = PyPDF2.PdfReader(
            pdf_file
        )

        for page in reader.pages:

            page_text = (
                page.extract_text()
            )

            if page_text:

                text += (
                    page_text + "\n"
                )

    return text


# ============================================================
# DOCX EXTRACTION
# ============================================================

def extract_text_from_docx(
    docx_path
):

    doc = docx.Document(
        docx_path
    )

    return "\n".join([

        para.text

        for para in doc.paragraphs
    ])


# ============================================================
# RESUME EXTRACTION
# ============================================================

def extract_resume_text(
    file_path
):

    if file_path.endswith(".pdf"):

        return extract_text_from_pdf(
            file_path
        )

    elif file_path.endswith(".docx"):

        return extract_text_from_docx(
            file_path
        )

    else:

        raise ValueError(
            "Unsupported format"
        )


# ============================================================
# SECTION SPLITTER
# ============================================================

def split_resume_sections(
    text
):

    sections = {

        "experience": "",

        "skills": "",

        "projects": "",

        "education": "",

        "certifications": ""
    }

    patterns = {

        "experience":
        r"(experience|employment|work history)",

        "skills":
        r"(skills|technical skills)",

        "projects":
        r"(projects)",

        "education":
        r"(education)",

        "certifications":
        r"(certifications|certificates)"
    }

    current_section = None

    for line in text.split("\n"):

        clean = (
            line.strip().lower()
        )

        matched = False

        for section, pattern in patterns.items():

            if re.search(
                pattern,
                clean
            ):

                current_section = section

                matched = True

                break

        if (

            not matched

            and current_section
        ):

            sections[current_section] += (

                line + "\n"
            )

    return sections