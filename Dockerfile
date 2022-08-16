FROM python:3

WORKDIR /app
COPY ./bince.py app.py
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["/app/app.py"]
