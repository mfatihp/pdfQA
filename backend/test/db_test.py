import requests


url = 'http://127.0.0.1:8000/upload'
file_path = '../data/pdfs/mathematics-10-01555-v2.pdf'

with open(file_path, "rb") as f:
    files = {"pdf_file": ("mathematics-10-01555-v2.pdf", f, "application/pdf")}
    response = requests.post(url, files=files)


print(response.json())