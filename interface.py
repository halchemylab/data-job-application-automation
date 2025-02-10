import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from job_scraper import extract_job_details  # Import your scraping function
from generate_resume_cover import generate_resume_and_cover  # Updated import for refactored function

class JobApplicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Automation Tool")
        self.root.geometry("700x800")
        self.root.configure(padx=20, pady=20, bg="white")  # Set background to white for light theme

        # Section 1: Web Scraping
        self.create_section_divider("Web Scraping")
        self.create_description("Insert Job URL below. The GPT-4o-mini engine will extract and recommend keywords for the fields.")

        tk.Label(root, text="Job URL:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
        self.url_entry = tk.Entry(root, width=80, font=("Arial", 12), bg="white", fg="black", insertbackground="black")
        self.url_entry.pack(pady=5)

        self.scrape_button = tk.Button(root, text="SCRAPE JOB DETAILS", font=("Arial", 12, "bold"), height=2, width=30, command=self.scrape_job_details, bg="#f0f0f0", fg="black")
        self.scrape_button.pack(pady=15)

        # Section 2: Resume and Cover Letter Generation
        self.create_section_divider("Resume and Cover Letter")
        self.create_description("Review or edit the extracted details below. Once ready, generate your customized resume and cover letter.")

        self.fields = {
            "Job Position": tk.StringVar(),
            "Company Name": tk.StringVar(),
            "Specific Job Project": tk.StringVar(),
            "Required IT Skills": tk.StringVar()
        }

        for field_name, var in self.fields.items():
            tk.Label(root, text=f"{field_name}:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
            tk.Entry(root, textvariable=var, width=80, font=("Arial", 12), bg="white", fg="black", insertbackground="black").pack(pady=5)

        self.generate_button = tk.Button(root, text="GENERATE RESUME & COVER LETTER", font=("Arial", 12, "bold"), height=2, width=40, command=self.generate_documents, bg="#f0f0f0", fg="black")
        self.generate_button.pack(pady=20)

    def create_section_divider(self, text):
        divider = tk.Label(self.root, text=text, font=("Arial", 16, "bold"), bg="#e0e0e0", fg="black", width=60)
        divider.pack(pady=15, fill='x')

    def create_description(self, text):
        description = tk.Label(self.root, text=text, font=("Arial", 11), fg="gray40", bg="white", wraplength=650, justify="left")
        description.pack(pady=5)

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
