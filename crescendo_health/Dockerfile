FROM python:3.9-slim

# /the/workdir/path
WORKDIR /crescendo_health

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "home.py"]