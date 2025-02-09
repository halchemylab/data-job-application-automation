import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
from job_scraper import extract_job_details  # Import your scraping function
from generate_resume_cover import generate_resume_and_cover  # Updated import for refactored function

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

        try:
            output_folder = generate_resume_and_cover(
                job_position=job_position,
                company_name=company_name,
                specific_job_project=specific_job_project,
                required_it_skills=required_it_skills
            )
            messagebox.showinfo("Success", f"Documents generated and saved in {output_folder}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating documents: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JobApplicationApp(root)
    root.mainloop()
