from src.core.scraper import extract_job_details, save_job_to_csv
from src.core.generator import generate_resume_and_cover
from src.logger import logger

def scrape_job_details_logic(url):
    logger.info(f"Scraping job details from URL: {url}")
    if not url:
        logger.error("No URL provided for scraping.")
        raise ValueError("Please enter a job URL.")

    job_details = extract_job_details(url)
    if job_details:
        logger.info("Successfully extracted job details.")
        save_job_to_csv(job_details, url)
        logger.info("Job details saved to CSV.")
        return job_details
    else:
        logger.error("Failed to extract job details.")
        return None

def generate_documents_logic(fields):
    job_position = fields["Job Position"].get()
    company_name = fields["Company Name"].get()
    specific_job_project = fields["Specific Job Project"].get()
    required_it_skills = fields["Required IT Skills"].get()

    logger.info(f"Generating documents for {job_position} at {company_name}")

    if not all([job_position, company_name]):
        logger.error("Missing job position or company name for document generation.")
        raise ValueError("Job Position and Company Name are required.")

    output_folder = generate_resume_and_cover(
        job_position=job_position,
        company_name=company_name,
        specific_job_project=specific_job_project,
        required_it_skills=required_it_skills
    )
    logger.info(f"Documents generated in: {output_folder}")
    return output_folder
