import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import random
from job_scraper import extract_job_details  # Import your scraping function
from generate_resume_cover import generate_resume_and_cover  # Updated import for refactored function

class JobApplicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Automation Tool")
        self.root.geometry("700x750")
        self.root.resizable(False, False)  # Make the window non-resizable
        self.root.configure(padx=20, pady=20, bg="white")  # Set background to white for light theme

        # Canvas for Confetti Animation
        self.canvas = tk.Canvas(root, width=700, height=800, bg="white", highlightthickness=0)
        self.canvas.place(x=0, y=0)

        # Section 1: Web Scraping
        self.create_section_divider("Web Scraping")
        self.create_description("Insert Job URL below. The GPT-4o-mini engine will extract and recommend keywords for the fields. This will also add the company record to 'data/tracker.csv'.")

        self.create_labeled_entry("Job URL:", "url_entry")

        self.scrape_button = tk.Button(root, text="SCRAPE JOB DETAILS", font=("Arial", 12, "bold"), height=2, width=30, command=self.scrape_job_details, bg="#e8e8e8", fg="black", relief="groove")
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
            self.create_labeled_entry(f"{field_name}:", var)

        self.generate_button = tk.Button(root, text="GENERATE RESUME & COVER LETTER", font=("Arial", 12, "bold"), height=2, width=40, command=self.generate_documents, bg="#e8e8e8", fg="black", relief="groove")
        self.generate_button.pack(pady=20)

    def create_section_divider(self, text):
        divider = tk.Label(self.root, text=text, font=("Arial", 16, "bold"), bg="#e0e0e0", fg="black", width=60)
        divider.pack(pady=15, fill='x')

    def create_description(self, text):
        description = tk.Label(self.root, text=text, font=("Arial", 11), fg="gray40", bg="white", wraplength=650, justify="left")
        description.pack(pady=5)

    def create_labeled_entry(self, label_text, variable):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill='x', pady=5)

        label = tk.Label(frame, text=label_text, font=("Arial", 12), bg="white", fg="black", anchor="w")
        label.pack(side="top", anchor="w")

        if isinstance(variable, str):
            entry = tk.Entry(frame, width=80, font=("Arial", 12), bg="#f9f9f9", fg="black", insertbackground="black")
            setattr(self, variable, entry)
        else:
            entry = tk.Entry(frame, textvariable=variable, width=80, font=("Arial", 12), bg="#f9f9f9", fg="black", insertbackground="black")
        entry.pack(side="top", anchor="w")

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
            self.run_confetti_animation()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating documents: {e}")

    def run_confetti_animation(self):
        colors = ["#ff6666", "#66ff66", "#6666ff", "#ffff66", "#ff66ff", "#66ffff"]
        confetti = []

        for _ in range(100):
            x = random.randint(0, 700)
            y = random.randint(-800, 0)
            size = random.randint(5, 15)
            color = random.choice(colors)
            confetti.append(self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline=""))

        def animate():
            for piece in confetti:
                self.canvas.move(piece, 0, 5)
                if self.canvas.coords(piece)[1] > 800:
                    self.canvas.coords(piece, random.randint(0, 700), random.randint(-800, 0), random.randint(0, 700) + size, random.randint(-800, 0) + size)
            self.root.after(50, animate)

        animate()

if __name__ == "__main__":
    root = tk.Tk()
    app = JobApplicationApp(root)
    root.mainloop()