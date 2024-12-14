FROM python:3.11-slim

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip install psycopg2-binary

RUN pip install SQLAlchemy

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

