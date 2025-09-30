
import pytest
import os
from unittest import mock
from src.core.generator import generate_resume_and_cover
from src.config import PROJECT_ROOT
import datetime

@mock.patch('src.core.generator.process_word_document')
@mock.patch('os.makedirs')
def test_generate_resume_and_cover(mock_makedirs, mock_process_word_document):
    # Input data
    job_position = "Test Position"
    company_name = "Test Company"
    specific_job_project = "Test Project"
    required_it_skills = "Python, Pytest"

    # Expected values
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    folder_date = datetime.datetime.now().strftime("%m%d%y")
    expected_output_folder = os.path.join(PROJECT_ROOT, "output", f"{company_name}_{folder_date}")
    
    expected_replacements = {
        "{{JOB_POSITION}}": job_position,
        "{{COMPANY_NAME}}": company_name,
        "{{SPECIFIC_JOB_PROJECT}}": specific_job_project,
        "{{IT_SKILLS}}": required_it_skills,
        "{{CURRENT_DATE}}": current_date,
    }
    
    resume_template = os.path.join(PROJECT_ROOT, "static", "resume_template.docx")
    cover_letter_template = os.path.join(PROJECT_ROOT, "static", "cover_letter_template.docx")
    resume_output = os.path.join(expected_output_folder, "henry_pai_resume.docx")
    cover_letter_output = os.path.join(expected_output_folder, "henry_pai_cover_letter.docx")

    # Call the function
    output_folder = generate_resume_and_cover(job_position, company_name, specific_job_project, required_it_skills)

    # Assertions
    mock_makedirs.assert_called_once_with(expected_output_folder, exist_ok=True)
    
    assert output_folder == expected_output_folder

    # Check that process_word_document was called correctly for both resume and cover letter
    mock_process_word_document.assert_any_call(resume_template, resume_output, expected_replacements)
    mock_process_word_document.assert_any_call(cover_letter_template, cover_letter_output, expected_replacements)
    assert mock_process_word_document.call_count == 2
