import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Digitalhealthcare.settings')
os.environ.setdefault('EMAIL_HOST', 'localhost')
os.environ.setdefault('EMAIL_PORT', '587')
os.environ.setdefault('EMAIL_HOST_USER', 'test@example.com')
os.environ.setdefault('EMAIL_HOST_PASSWORD', 'pass')
os.environ.setdefault('EMAIL_USE_TLS', 'True')
os.environ.setdefault('DEFAULT_FROM_EMAIL', 'test@example.com')
