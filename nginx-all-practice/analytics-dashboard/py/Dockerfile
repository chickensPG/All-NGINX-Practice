FROM python:3.11

WORKDIR /py

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app.py . 
COPY templates/ ./templates/
COPY .env .

CMD ["python","app.py"]