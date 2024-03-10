import tkinter as tk
from tkinter import ttk

def submit_info():
    selected_job = job_var.get()
    selected_level = level_var.get()
    num_candidates = int(num_candidates_entry.get())
    
    # Process the selected information (e.g., print or store it)
    print("Selected Job:", selected_job)
    print("Selected Level:", selected_level)
    print("Number of Candidates Required:", num_candidates)
    # You can perform further actions here, such as sending the data to a server or database.

# Create main window
root = tk.Tk()
root.title("Job Application")

# Create job selection dropdown
jobs = ["Software Engineer", "Data Scientist", "Product Manager"]  # Example job list
job_label = tk.Label(root, text="Select Job:")
job_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
job_var = tk.StringVar()
job_dropdown = ttk.Combobox(root, textvariable=job_var, values=jobs)
job_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")
job_dropdown.current(0)

# Create candidate level selection dropdown
levels = ["Entry Level", "Mid Level", "Senior Level"]  # Example level list
level_label = tk.Label(root, text="Select Level:")
level_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
level_var = tk.StringVar()
level_dropdown = ttk.Combobox(root, textvariable=level_var, values=levels)
level_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")
level_dropdown.current(0)

# Create entry field for number of candidates
num_candidates_label = tk.Label(root, text="Number of Candidates:")
num_candidates_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
num_candidates_entry = tk.Entry(root)
num_candidates_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Create submit button
submit_button = tk.Button(root, text="Submit", command=submit_info)
submit_button.grid(row=3, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()