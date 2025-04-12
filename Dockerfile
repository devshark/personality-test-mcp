FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./server/
COPY client/ ./client/

EXPOSE 8000

CMD ["python", "server/app.py"]
