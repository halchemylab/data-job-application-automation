from src.core.scraper import extract_job_details, save_job_to_csv
from src.core.generator import generate_resume_and_cover

def scrape_job_details_logic(url):
    if not url:
        raise ValueError("Please enter a job URL.")

    job_details = extract_job_details(url)
    if job_details:
        save_job_to_csv(job_details, url)
        return job_details
    else:
        return None

def generate_documents_logic(fields):
    job_position = fields["Job Position"].get()
    company_name = fields["Company Name"].get()
    specific_job_project = fields["Specific Job Project"].get()
    required_it_skills = fields["Required IT Skills"].get()

    if not all([job_position, company_name]):
        raise ValueError("Job Position and Company Name are required.")

    output_folder = generate_resume_and_cover(
        job_position=job_position,
        company_name=company_name,
        specific_job_project=specific_job_project,
        required_it_skills=required_it_skills
    )
    return output_folder
