import tkinter as tk
from tkinter import ttk
from logic.scheduler import allocate_study_time
from logic.database import init_db, insert_user, insert_session
import random

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# ------------------------- Setup Main Window ------------------------- #
window = tk.Tk()
window.title("Z-Study Buddy")
window.attributes("-fullscreen", True)
window.resizable(False, False)
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))
window.config(bg="#f0f8ff")
window.iconbitmap('./assets/r.ico')

# ------------------------- Custom Styles ------------------------- #
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",
    font=("Helvetica", 20, "bold"),
    padding=10
)

style.configure("Main.TButton",
    background="#28a745",
    foreground="white"
)
style.map("Main.TButton",
    background=[("active", "#218838")]
)

style.configure("Exit.TButton",
    background="#dc3545",
    foreground="white"
)
style.map("Exit.TButton",
    background=[("active", "#c82333")]
)

style.configure("Form.TLabel",
    font=("Helvetica", 14),
    background="#f0f8ff"
)

style.configure("Header.TLabel",
    font=("Helvetica", 22, "bold"),
    background="#f0f8ff"
)

# ------------------------- Data ------------------------- #
subjects_list = ["English", "Chemistry", "Math", "Biology", "Physics"]

quotes = [
    "Success doesn't come from what you do occasionally, it comes from what you do consistently.",
    "Push yourself, because no one else is going to do it for you.",
    "You are capable of amazing things!",
    "Small steps every day lead to big results.",
    "Don’t watch the clock; do what it does. Keep going."
]

# ------------------------- Log Session Window ------------------------- #
def open_log_session():
    log_window = tk.Toplevel(window)
    log_window.title("Log Session")
    log_window.geometry("500x650")
    log_window.config(bg="#f0f8ff")
    log_window.iconbitmap('./assets/r.ico')

    ttk.Label(log_window, text="📝 Fill your information below", style="Header.TLabel").pack(pady=30)

    fields = {}
    for label in ["Name", "Age", "Grade", "Enter available study hours"]:
        ttk.Label(log_window, text=label + ":", style="Form.TLabel").pack()
        entry = ttk.Entry(log_window, font=("Helvetica", 14))
        entry.pack(pady=5)
        fields[label.lower()] = entry

    ttk.Label(log_window, text="Rank your subjects (1-5):", style="Form.TLabel").pack(pady=20)

    interest_vars = []
    for i in range(5):
        ttk.Label(log_window, text=f"#{i+1} Subject:", style="Form.TLabel").pack()
        var = tk.StringVar(log_window)
        var.set(subjects_list[0])
        dropdown = ttk.OptionMenu(log_window, var, *subjects_list)
        dropdown.pack()
        interest_vars.append(var)

    def submit_info():
        try:
            name = fields["name"].get()
            age = int(fields["age"].get())
            grade = fields["grade"].get()
            available_hours = float(fields["enter available study hours"].get())

            user_id = insert_user(name, age, grade)

            ranked_subjects = []
            chosen = set()
            for i, var in enumerate(interest_vars):
                subject = var.get()
                if subject in chosen:
                    raise ValueError("Duplicate subjects selected.")
                chosen.add(subject)

                weight = 4 if i == 0 else 2 if i == 4 else 3
                ranked_subjects.append({"name": subject, "weight": weight})

            schedule = allocate_study_time(ranked_subjects, available_hours)
            show_schedule(schedule)

        except ValueError as ve:
            error = tk.Toplevel(log_window)
            error.title("Error")
            tk.Label(error, text=f"❌ {ve}", font=("Helvetica", 12)).pack(padx=20, pady=20)

    ttk.Button(log_window, text="Generate My Schedule", command=submit_info, style="Main.TButton").pack(pady=30)

# ------------------------- Show Schedule Window ------------------------- #
def show_schedule(schedule):
    schedule_window = tk.Toplevel(window)
    schedule_window.title("Your Study Schedule")
    schedule_window.geometry("500x500")
    schedule_window.config(bg="#ffffff")
    schedule_window.iconbitmap('./assets/r.ico')

    ttk.Label(schedule_window, text="📅 Personalized Study Plan", font=("Helvetica", 18, "bold")).pack(pady=10)

    for subject, time in schedule:
        ttk.Label(schedule_window, text=f"{subject}: {time:.2f} hours", font=("Helvetica", 14)).pack(anchor="w", padx=20)

    quote = random.choice(quotes)
    quote_frame = tk.Frame(schedule_window, bg="#d1ecf1", bd=2, relief="groove", padx=10, pady=10)
    quote_frame.pack(padx=20, pady=30, fill="both")

    tk.Label(quote_frame, text="💡 Motivation for You:", font=("Helvetica", 14, "bold"), bg="#d1ecf1", fg="#0c5460").pack(anchor="w")
    tk.Label(quote_frame, text=quote, font=("Helvetica", 12), bg="#d1ecf1", fg="#0c5460", wraplength=400, justify="left").pack(anchor="w", pady=5)

# ------------------------- Main Window Layout ------------------------- #
init_db()

tk.Label(
    window,
    text="🎓 Welcome to Z-Study Buddy",
    font=("Helvetica", 60, "bold"),
    bg="#f0f8ff",
    fg="#003366"
).pack(pady=100)

ttk.Button(
    window,
    text="Log Study Session",
    command=open_log_session,
    style="Main.TButton"
).pack(pady=10)

ttk.Button(
    window,
    text="❌ Exit App",
    command=window.destroy,
    style="Exit.TButton"
).pack(pady=20)

window.mainloop()
