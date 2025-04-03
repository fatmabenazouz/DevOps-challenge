#!/usr/bin/env python3
"""
Generate a secure random Django secret key and output it.
This can be used to generate a secret key for the .env file.
"""
import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure random string for Django's SECRET_KEY setting."""
    chars = string.ascii_letters + string.digits + string.punctuation
    chars = chars.replace('"', '').replace("'", '').replace('\\', '').replace('`', '')
    
    return ''.join(secrets.choice(chars) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print(f"Generated SECRET_KEY: {secret_key}")
    print("\nAdd this to your .env file:")
    print(f"SECRET_KEY={secret_key}")