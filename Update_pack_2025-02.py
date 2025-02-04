import os
import django


os.chdir(r"D:\Projects\Offline_translator-webapp")

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "translator.settings")  # Replace with your project name
django.setup()

# Now you can use Django ORM
from users.models import Language

# Define the language codes
language_codes = ["English", "Arabic", "Persian", "Hebrew"]

# Create and save the languages
for code in language_codes:
    Language.objects.get_or_create(code=code)

print("Languages added successfully!")