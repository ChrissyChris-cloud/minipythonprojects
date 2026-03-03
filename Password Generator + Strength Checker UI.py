import tkinter as tk
from tkinter import scrolledtext, messagebox
import string

# --- Core logic (unchanged) ---

def check_common_password(password, common_file="common-password.txt"):
    try:
        with open(common_file, "r") as f:
            common = set(f.read().splitlines())
        return password in common
    except FileNotFoundError:
        return False

def password_strength(password):
    score = 0
    length = len(password)
    upper_case = any(c.isupper() for c in password)
    lower_case = any(c.islower() for c in password)
    special = any(c in string.punctuation for c in password)
    digits = any(c.isdigit() for c in password)

    if length > 8:
        score += 1
    if length > 12:
        score += 1
    if length > 17:
        score += 1
    if length > 20:
        score += 1

    score += sum([upper_case, lower_case, special, digits]) - 1

    if score < 4:
        strength = "Weak"
    elif score == 4:
        strength = "Okay"
    elif 4 < score < 6:
        strength = "Good"
    else:
        strength = "Strong"

    return strength, score

def feedback(password):
    if check_common_password(password):
        return "Password was found in a common list. Score: 0/7"

    strength, score = password_strength(password)
    messages = [f"Password strength: {strength} (Score: {score}/7)"]

    if score < 4:
        messages.append("Suggestions to improve your password:")
        if len(password) <= 8:
            messages.append("- Make your password longer (more than 8 characters).")
        if not any(c.isupper() for c in password):
            messages.append("- Include uppercase letters.")
        if not any(c.islower() for c in password):
            messages.append("- Include lowercase letters.")
        if not any(c in string.punctuation for c in password):
            messages.append("- Add special characters (e.g., @, #, $).")
        if not any(c.isdigit() for c in password):
            messages.append("- Add numbers.")

    return "\n".join(messages)

# --- GUI logic ---

def check_password_gui():
    pwd = password_entry.get()
    if not pwd:
        messagebox.showwarning("Input Required", "Please enter a password.")
        return
    result_text.config(state='normal')
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, feedback(pwd))
    result_text.config(state='disabled')

root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("500x400")
root.resizable(False, False)

tk.Label(root, text="Enter your password:", font=("Arial", 12)).pack(pady=10)
password_entry = tk.Entry(root, show="*", width=40, font=("Arial", 12))
password_entry.pack(pady=5)

tk.Button(root, text="Check Strength", command=check_password_gui, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

tk.Label(root, text="Feedback:", font=("Arial", 12)).pack(pady=5)
result_text = scrolledtext.ScrolledText(root, width=60, height=12, font=("Arial", 11), state='disabled')
result_text.pack(pady=5)

root.mainloop()
