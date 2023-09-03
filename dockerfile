FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt

COPY structure.yaml structure.yaml

RUN pip install --no-cache-dir -r requirements.txt          

COPY . .

CMD ["python", "app.py"]
