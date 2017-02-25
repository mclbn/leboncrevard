import os


SMTP_USER = os.environ.get('LBC_SMTP_USER', "user")
SMTP_PASS = os.environ.get('LBC_SMTP_PASS', "pass")
SMTP_SERVER = os.environ.get('LBC_SMTP_SERVER', "smtp.gmail.com:587")
JOB_FILE = os.environ.get('LBC_JOB_FILE', "jobs.csv")
DELETE_FILE = os.environ.get('LBC_DELETE_FILE', "delete.csv")
