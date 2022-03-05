from django.core.management.utils import get_random_secret_key  

secret_key = get_random_secret_key()

print(f"secret_key = '{secret_key}'", file=open("ournft_site//ournft_site//secret_settings.py","w"))