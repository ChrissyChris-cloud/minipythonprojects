import string

# Check if password is in a list of common passwords
def check_common_password(password, common_file="common-password.txt"):
    try:
        with open(common_file, "r") as f:
            common = set(f.read().splitlines())
        return password in common
    except FileNotFoundError:
        print(f"Warning: {common_file} not found. Skipping common password check.")
        return False

# Evaluate password strength and return a score
def password_strength(password):
    score = 0
    length = len(password)

    # Character type checks
    upper_case = any(c.isupper() for c in password)
    lower_case = any(c.islower() for c in password)
    special = any(c in string.punctuation for c in password)
    digits = any(c.isdigit() for c in password)

    # Length-based scoring
    if length > 8:
        score += 1
    if length > 12:
        score += 1
    if length > 17:
        score += 1
    if length > 20:
        score += 1

    # Character diversity scoring
    score += sum([upper_case, lower_case, special, digits]) - 1  # avoid double-counting

    # Strength classification
    if score < 4:
        strength = "Weak"
    elif score == 4:
        strength = "Okay"
    elif 4 < score < 6:
        strength = "Good"
    else:
        strength = "Strong"

    return strength, score

# Generate feedback for the user
def feedback(password):
    if check_common_password(password):
        return "Password was found in a common list. Score: 0/7"

    strength, score = password_strength(password) # Get strength and score
    messages = [f"Password strength: {strength} (Score: {score}/7)"] # Initial feedback message

    # Suggestions for improvement
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

    return "\n".join(messages) # Join messages with newlines for better readability

# Main execution
def main():
    password = input("Enter the password: ")
    print(feedback(password))

if __name__ == "__main__":
    main()
