FROM python:3.11

WORKDIR /py

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app.py . 

CMD ["python","app.py"]