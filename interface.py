import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import os
from job_scraper import extract_job_details  # Import your scraping function
from generate_resume_cover import process_word_document  # Import your generation function

class JobApplicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Automation Tool")
        self.root.geometry("600x700")

        # URL Entry
        tk.Label(root, text="Job URL:").pack(pady=5)
        self.url_entry = tk.Entry(root, width=70)
        self.url_entry.pack(pady=5)

        # Scrape Button
        self.scrape_button = tk.Button(root, text="Scrape Job Details", command=self.scrape_job_details)
        self.scrape_button.pack(pady=10)

        # Job Details Fields
        self.fields = {
            "Job Position": tk.StringVar(),
            "Company Name": tk.StringVar(),
            "Specific Job Project": tk.StringVar(),
            "Required IT Skills": tk.StringVar()
        }

        for field_name, var in self.fields.items():
            tk.Label(root, text=f"{field_name}:").pack(pady=5)
            tk.Entry(root, textvariable=var, width=70).pack(pady=5)

        # Generate Button
        self.generate_button = tk.Button(root, text="Generate Resume & Cover Letter", command=self.generate_documents)
        self.generate_button.pack(pady=20)

    def scrape_job_details(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a job URL.")
            return

        try:
            job_details = extract_job_details(url)
            if job_details:
                self.fields["Job Position"].set(job_details.get("Job Position", ""))
                self.fields["Company Name"].set(job_details.get("Company Name", ""))
                self.fields["Specific Job Project"].set(job_details.get("Specific Job Project", ""))
                self.fields["Required IT Skills"].set(job_details.get("Required IT Skills", ""))
                messagebox.showinfo("Success", "Job details scraped successfully! Please review and edit if needed.")
            else:
                messagebox.showerror("Error", "Failed to extract job details.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while scraping: {e}")

    def generate_documents(self):
        job_position = self.fields["Job Position"].get()
        company_name = self.fields["Company Name"].get()
        specific_job_project = self.fields["Specific Job Project"].get()
        required_it_skills = self.fields["Required IT Skills"].get()

        if not all([job_position, company_name]):
            messagebox.showwarning("Input Error", "Job Position and Company Name are required.")
            return

        # Prepare output folder
        current_date = datetime.now().strftime("%m%d%y")
        output_subfolder = os.path.join("output", f"{company_name}_{current_date}")
        os.makedirs(output_subfolder, exist_ok=True)

        # Paths to templates
        resume_template = "static/resume_template.docx"
        cover_letter_template = "static/cover_letter_template.docx"

        # Output file paths
        resume_output = os.path.join(output_subfolder, "henry_pai_resume.docx")
        cover_letter_output = os.path.join(output_subfolder, "henry_pai_cover_letter.docx")

        # Replacements dictionary
        replacements = {
            "{{JOB_POSITION}}": job_position,
            "{{COMPANY_NAME}}": company_name,
            "{{SPECIFIC_JOB_PROJECT}}": specific_job_project,
            "{{IT_SKILLS}}": required_it_skills,
            "{{CURRENT_DATE}}": datetime.now().strftime("%B %d, %Y")
        }

        try:
            process_word_document(resume_template, resume_output, replacements)
            process_word_document(cover_letter_template, cover_letter_output, replacements)
            messagebox.showinfo("Success", f"Documents generated and saved in {output_subfolder}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating documents: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JobApplicationApp(root)
    root.mainloop()
