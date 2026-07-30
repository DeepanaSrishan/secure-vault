from zxcvbn import zxcvbn
import string

def check_password_strength(password: str):

    score = 0
    suggestions = []


    # Length check
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append(
            "Password should have at least 8 characters"
        )


    # Uppercase check
    if any(char.isupper() for char in password):
        score += 1
    else:
        suggestions.append(
            "Add uppercase letters"
        )


    # Lowercase check
    if any(char.islower() for char in password):
        score += 1
    else:
        suggestions.append(
            "Add lowercase letters"
        )


    # Number check
    if any(char.isdigit() for char in password):
        score += 1
    else:
        suggestions.append(
            "Add numbers"
        )


    # Special character check
    if any(char in string.punctuation for char in password):
        score += 1
    else:
        suggestions.append(
            "Add special characters"
        )


    # Strength calculation

    if score <= 2:
        strength = "Weak"

    elif score <= 4:
        strength = "Medium"

    else:
        strength = "Strong"


    return {
        "strength": strength,
        "score": score,
        "suggestions": suggestions
    }