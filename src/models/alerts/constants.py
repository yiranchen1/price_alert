import os

URL = os.environ.get('MAILGUN_URL')
API_KEY = os.environ.get('API_KEY')
FROM = os.environ.get('FROM')
Alert_time = 1
COLLECTION = "alerts"