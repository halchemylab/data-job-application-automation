import os
import datetime
from docx import Document

def replace_placeholders(text, replacements):
    """Replaces placeholders in a given text with provided replacements."""
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)
    return text

def process_word_document(template_path, output_path, replacements):
    """Reads a Word document, replaces placeholders, and saves a new version."""
    doc = Document(template_path)
    for para in doc.paragraphs:
        para.text = replace_placeholders(para.text, replacements)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                cell.text = replace_placeholders(cell.text, replacements)
    doc.save(output_path)

def main():
    # Inputs
    job_position = "Data Scientist"
    company_name = "Flip"
    specific_job_project = "Leveraging data to drive innovation in the e-commerce industry"
    required_it_skills = "SQL, Python, R, ML, statistics, etc."
    
    # Paths
    static_folder = "static"
    output_folder = "output"
    resume_template = os.path.join(static_folder, "resume_template.docx")
    cover_letter_template = os.path.join(static_folder, "cover_letter_template.docx")
    
    # Date formatting
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    folder_date = datetime.datetime.now().strftime("%m%d%y")
    output_subfolder = os.path.join(output_folder, f"{company_name}_{folder_date}")
    os.makedirs(output_subfolder, exist_ok=True)
    
    # Output file paths
    resume_output = os.path.join(output_subfolder, "customized_resume.docx")
    cover_letter_output = os.path.join(output_subfolder, "customized_cover_letter.docx")
    
    # Replacements dictionary
    replacements = {
        "{{JOB_POSITION}}": job_position,
        "{{COMPANY_NAME}}": company_name,
        "{{SPECIFIC_JOB_PROJECT}}": specific_job_project,
        "{{IT_SKILLS}}": required_it_skills,
        "{{CURRENT_DATE}}": current_date,
    }
    
    # Process documents
    process_word_document(resume_template, resume_output, replacements)
    process_word_document(cover_letter_template, cover_letter_output, replacements)
    
    print(f"Customized resume saved at: {resume_output}")
    print(f"Customized cover letter saved at: {cover_letter_output}")

if __name__ == "__main__":
    main()
