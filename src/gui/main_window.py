import tkinter as tk
from tkinter import messagebox
import random
from src.core.logic import scrape_job_details_logic, generate_documents_logic
import time

class JobApplicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Automation Tool")
        self.root.geometry("700x750")
        self.root.resizable(False, False)  # Make the window non-resizable
        self.root.configure(padx=20, pady=20, bg="white")  # Set background to white for light theme

        # Canvas for Balloon Animation
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
        job_details = scrape_job_details_logic(url)
        if job_details:
            self.fields["Job Position"].set(job_details.get("Job Position", ""))
            self.fields["Company Name"].set(job_details.get("Company Name", ""))
            self.fields["Specific Job Project"].set(job_details.get("Specific Job Project", ""))
            self.fields["Required IT Skills"].set(job_details.get("Required IT Skills", ""))

    def generate_documents(self):
        if generate_documents_logic(self.fields):
            self.run_balloon_animation()

    def run_balloon_animation(self):
        colors = ["#ff6666", "#66ff66", "#6666ff", "#ffff66", "#ff66ff", "#66ffff"]
        balloons = []
        
        # Create balloon objects with timestamp
        for _ in range(5):
            x = random.randint(50, 650)
            y = 800
            size = random.randint(30, 50)
            color = random.choice(colors)
            balloon = self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="black")
            string = self.canvas.create_line(x+size/2, y+size, x+size/2, y+size+30, fill="black")
            # Add creation time to each balloon
            balloons.append({
                'balloon': balloon,
                'string': string,
                'created_at': time.time()
            })
        
        def animate():
            current_time = time.time()
            # Create a new list for remaining balloons
            remaining_balloons = []
            
            for balloon_info in balloons:
                # Check if balloon should be removed (2 seconds passed)
                if current_time - balloon_info['created_at'] < 2:
                    # Move balloon up if less than 2 seconds old
                    self.canvas.move(balloon_info['balloon'], 0, -5)
                    self.canvas.move(balloon_info['string'], 0, -5)
                    remaining_balloons.append(balloon_info)
                else:
                    # Delete balloon if 2 seconds passed
                    self.canvas.delete(balloon_info['balloon'])
                    self.canvas.delete(balloon_info['string'])
            
            # Update balloons list
            balloons[:] = remaining_balloons
            
            # Continue animation if there are balloons left
            if remaining_balloons:
                self.root.after(50, animate)
        
        animate()
