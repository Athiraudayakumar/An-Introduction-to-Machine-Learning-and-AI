from dataclasses import field
from textwrap import indent
from urllib import response
import openai
import os
#import docx
import PyPDF2
import json
#from dotenv import load_dotenv
from openai import AzureOpenAI
import re

#load_dotenv()

# client = AzureOpenAI(
#     azure_endpoint=os.getenv("AZURE_ENDPOINT_EUS"),
#     api_key=os.getenv("AZURE_OPENAI_API_KEY_EUS"),
#     api_version="2024-02-15-preview"
# )


# Function for extract content from pdf formatted resume
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        reader =  PyPDF2.PdfReader(pdf_file)
        print("the extracted data,     .....",reader)
        text = "\n".join([page.extract_text()  for page in reader.pages if page.extract_text()])

    return text

# Function for ectracting content form docx formatted Resume
# def extract_text_from_docx(docx_path):
#     doc = docx.Document(docx_path)
#     return "\n".join([para.text for para in doc.paragraphs])

def extract_resume_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    # elif file_path.endswith(".docx"):
    #     return extract_text_from_docx(file_path)
    else: 
        ValueError("Unsupported file format. Please uplaod file in .pdf or .docx format")


def extract_details_from_resume(resume_text):
    
    prompt= f"""
    You are an AI that extracts structured details from resumes.
    Extract the following details from the given resume text:
    - Full Name
    - Email
    - Phone Number
    - Location (City, State, Country)
    - Willing to Relocate? (Yes/No)
    - Total Experience (in Years)
    - Current Job Title
    - Company History (Employer names and duration)
    - Job Responsibilities
    - Industry Experience
    - Work Preferences
    - Highest Qualification
    - University/Institute
    - Certifications
    - Technical Skills
    - Soft Skills
    - Tools & Technologies
    - LinkedIn Profile
    - GitHub, Kaggle, Portfolio

    Return the response in a structured JSON format. Do not include explanations.

    Resume Text:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="BT-OpenAIGPT4",
        messages=[{"role": "system", "content": "You are an AI that extracts structured data from resumes."},
                  {"role": "user", "content": prompt}]
    )
    try:
        response_text = response.choices[0].message.content.strip()
        cleaned_text = response_text.strip("```json").strip()


        print("\nresponse", cleaned_text)
        print("...................................")
        extracted_data = json.loads(cleaned_text)
        print("\njson formatted data", extracted_data)
        print("...................................")

        return extracted_data


    except json.JSONDecodeError:
        return {"error": "failed to parse the response"}

def find_missing_details(extracted_data):
    required_files = {
        "Full Name",
        "Email",
        "Phone Number",
        "Location",
        "Willing to Relocate",
        "Total Experience",
        "Current Job Title",
        "Company History",
        "Job Responsibilities",
        "Industry Experience",
        "Work Preferences",
        "Highest Qualification",
        "University/Institute",
        "Certifications",
        "Skills Acquired During Education",
        "Technical Skills",
        "Soft Skills",
        "Tools & Technologies",
        "Skill Proficiency",
        "Current Salary",
        "Expected Salary",
        "Notice Period",
        "Employment Type",
        "Work Authorization",
        "Preferred Work Type",
        "Personality Traits",
        "Workplace Preferences",
        "Team vs. Individual Work Style",
        "LinkedIn Profile",
        "GitHub, Kaggle, Portfolio",
        "Published Papers, Blogs, Patents"
    }

    missing_details = [field for field in required_files if field not in extracted_data or not extracted_data[field]]

    return missing_details


def chat_completion(missing_details):
    user_data = {}

    print("\n🤖 Chatbot: Hi! Let's complete your profile. I will only ask for missing details.")
    
    for detail in missing_details:
        prompt = f"Ask the user in a conversational way for their {detail}. Keep it natural and avoid repeating phrases."

        response = client.chat.completions.create(
            model="BT-OpenAIGPT4",
            messages=[{"role": "system", "content": "You are a friendly chatbot collecting missing resume details."},
                      {"role": "user", "content": prompt}]
        )

        chatbot_questions = response.choices[0].message.content.strip()
        user_input = input(f"🤖 Chatbot: {chatbot_questions}\n👤 You: ")
        user_data[detail] = user_input

    return user_data


def store_data(user_data):
    """Function which saves the user details"""
    with open("user_data.json", "w") as file:
        json.dump(user_data, file, indent=4)
    print("\nDetails saved successfully!")


def main():

    file_path = input("Enter the path of your resume (PDF/DOCX):")

    resume_text = extract_resume_text(file_path)

    print("resume_text\n",resume_text)

    extracted_data = extract_details_from_resume(resume_text)
    print("extracted_data\n", extracted_data)



    print("\n The extracted data from resume\t")
    print(json.dumps(extracted_data, indent = 4))


    missing_details = find_missing_details(extracted_data)

    if missing_details:
        print("\nThere are some missing details: {missing_details}")
        additional_data = chat_completion(missing_details)
        extracted_data.update(additional_data)

    store_data(extracted_data)
    
    print("\n📄 Extracted Data:")
    print(json.dumps(extracted_data, indent=4))

if __name__ == "__main__":
    main()