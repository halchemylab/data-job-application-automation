import tkinter as tk
from tkinter import messagebox
import os
import sys
import subprocess
from src.core.logic import scrape_job_details_logic, generate_documents_logic
from src.logger import logger
from src.gui.ui_components import create_section_divider, create_description, create_labeled_entry
from src.gui.animations import run_balloon_animation
from src.config import UI_SETTINGS

class JobApplicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title(UI_SETTINGS["title"])
        self.root.geometry(UI_SETTINGS["geometry"])
        self.root.resizable(False, False)  # Make the window non-resizable
        self.root.configure(padx=20, pady=20, bg=UI_SETTINGS["bg_color"])  # Set background to white for light theme

        # Canvas for Balloon Animation
        self.canvas = tk.Canvas(root, width=700, height=800, bg=UI_SETTINGS["bg_color"], highlightthickness=0)
        self.canvas.place(x=0, y=0)

        # Section 1: Web Scraping
        create_section_divider(self.root, "Web Scraping")
        create_description(self.root, "Insert Job URL below. The GPT-4o-mini engine will extract and recommend keywords for the fields. This will also add the company record to 'data/tracker.csv'.")

        self.url_entry = create_labeled_entry(self.root, "Job URL:", "url_entry")

        self.scrape_button = tk.Button(root, text="SCRAPE JOB DETAILS", font=("Arial", 12, "bold"), height=2, width=30, command=self.scrape_job_details, bg="#e8e8e8", fg="black", relief="groove")
        self.scrape_button.pack(pady=15)

        # Section 2: Resume and Cover Letter Generation
        create_section_divider(self.root, "Resume and Cover Letter")
        create_description(self.root, "Review or edit the extracted details below. Once ready, generate your customized resume and cover letter.")

        self.fields = {
            "Job Position": tk.StringVar(),
            "Company Name": tk.StringVar(),
            "Specific Job Project": tk.StringVar(),
            "Required IT Skills": tk.StringVar()
        }

        for field_name, var in self.fields.items():
            create_labeled_entry(self.root, f"{field_name}:", var)

        self.generate_button = tk.Button(root, text="GENERATE RESUME & COVER LETTER", font=("Arial", 12, "bold"), height=2, width=40, command=self.generate_documents, bg="#e8e8e8", fg="black", relief="groove")
        self.generate_button.pack(pady=20)

    def scrape_job_details(self):
        try:
            url = self.url_entry.get()
            if not url:
                messagebox.showwarning("Input Error", "Please enter a job URL.")
                return

            job_details = scrape_job_details_logic(url)
            if job_details:
                self.fields["Job Position"].set(job_details.get("Job Position", ""))
                self.fields["Company Name"].set(job_details.get("Company Name", ""))
                self.fields["Specific Job Project"].set(job_details.get("Specific Job Project", ""))
                self.fields["Required IT Skills"].set(job_details.get("Required IT Skills", ""))
                messagebox.showinfo("Success", "Job details scraped successfully and saved to tracker.csv! Please review and edit if needed.")
            else:
                messagebox.showerror("Error", "Failed to extract job details. Please check the URL and your internet connection.")
        except Exception as e:
            logger.error(f"An unexpected error occurred during scraping: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def generate_documents(self):
        try:
            output_folder = generate_documents_logic(self.fields)
            if output_folder:
                messagebox.showinfo("Success", f"Documents generated and saved in {output_folder}")
                run_balloon_animation(self.canvas)
                if sys.platform == "win32":
                    os.startfile(output_folder)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.Popen([opener, output_folder])
            else:
                messagebox.showerror("Error", "Failed to generate documents. Please check the logs for more details.")
        except FileNotFoundError as e:
            logger.error(f"File not found during document generation: {e}")
            messagebox.showerror("Error", f"Error generating documents: {e}. Make sure the template files exist.")
        except Exception as e:
            logger.error(f"An unexpected error occurred during document generation: {e}")
            messagebox.showerror("Error", f"An error occurred while generating documents: {e}")
