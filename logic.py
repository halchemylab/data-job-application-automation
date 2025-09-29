import tkinter as tk
from tkinter import messagebox
from job_scraper import extract_job_details, save_job_to_csv
from generate_resume_cover import generate_resume_and_cover

def scrape_job_details_logic(url):
    if not url:
        messagebox.showwarning("Input Error", "Please enter a job URL.")
        return None

    job_details = extract_job_details(url)
    if job_details:
        save_job_to_csv(job_details, url)
        messagebox.showinfo("Success", "Job details scraped successfully and saved to tracker.csv! Please review and edit if needed.")
        return job_details
    else:
        messagebox.showerror("Error", "Failed to extract job details.")
        return None

def generate_documents_logic(fields):
    job_position = fields["Job Position"].get()
    company_name = fields["Company Name"].get()
    specific_job_project = fields["Specific Job Project"].get()
    required_it_skills = fields["Required IT Skills"].get()

    if not all([job_position, company_name]):
        messagebox.showwarning("Input Error", "Job Position and Company Name are required.")
        return

    try:
        output_folder = generate_resume_and_cover(
            job_position=job_position,
            company_name=company_name,
            specific_job_project=specific_job_project,
            required_it_skills=required_it_skills
        )
        messagebox.showinfo("Success", f"Documents generated and saved in {output_folder}")
        return True
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"Error generating documents: {e}. Make sure the template files exist.")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while generating documents: {e}")
        return False
